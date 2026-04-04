import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib_venn import venn2

def load_report(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_meta_files(meta_dir):
    results = {}
    for path in Path(meta_dir).glob("*.meta"):
        source_file = path.stem
        if source_file.endswith(".py"):
            source_file = source_file[:-3]
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        results[source_file] = data.get("exit_code_by_key", {})
    return results


def parse_meta_key(key):
    """Returns (class_name, suffix) from a meta key"""
    m = re.search(r"x\u01c1(\w+)\u01c1(\w+__mutmut_\d+)$", key)
    if m:
        return m.group(1), m.group(2)
    m = re.search(r"x_(\w+__mutmut_\d+)$", key)
    if m:
        return "(module)", m.group(1)
    return "(unknown)", key


def parse_killed_line(line):
    m = re.match(r"x\u01c1(\w+)\u01c1(\w+__mutmut_\d+)$", line)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r"x_(\w+__mutmut_\d+)$", line)
    if m:
        return "(module)", m.group(1)
    return "(unknown)", line


def load_comparison(meta_dir, killed_file):
    meta_by_file = load_meta_files(meta_dir)

    suite_results = {}  # name: bool
    mutant_classes = {}  # name: class_name
    for source_file, exit_codes in meta_by_file.items():
        for key, code in exit_codes.items():
            class_name, suffix = parse_meta_key(key)
            name = f"{class_name}.{suffix}"
            suite_results[name] = (code != 0)
            mutant_classes[name] = class_name

    # Build equiv tester results
    equiv_kills = set()
    with open(killed_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            class_name, suffix = parse_killed_line(line)
            equiv_kills.add(f"{class_name}.{suffix}")

    records = []
    for name in sorted(suite_results):
        records.append({
            "name": name,
            "class": mutant_classes[name],
            "suite_killed": suite_results[name],
            "equiv_killed": name in equiv_kills,
        })
    return records


def plot_venn(records, ax):
    """Proportional Venn diagram of kill sets"""
    both = sum(1 for r in records if r["suite_killed"] and r["equiv_killed"])
    suite_only = sum(1 for r in records if r["suite_killed"] and not r["equiv_killed"])
    equiv_only = sum(1 for r in records if r["equiv_killed"] and not r["suite_killed"])
    neither = sum(1 for r in records if not r["suite_killed"] and not r["equiv_killed"])
    total = len(records)

    v = venn2(
        subsets=(suite_only, equiv_only, both),
        set_labels=("Test suite", "Equiv tester"),
        ax=ax,
    )

    if v.get_patch_by_id("10"):
        v.get_patch_by_id("10").set_color("#ef5350")
        v.get_patch_by_id("10").set_alpha(0.5)
    if v.get_patch_by_id("01"):
        v.get_patch_by_id("01").set_color("#42a5f5")
        v.get_patch_by_id("01").set_alpha(0.5)
    if v.get_patch_by_id("11"):
        v.get_patch_by_id("11").set_color("#66bb6a")
        v.get_patch_by_id("11").set_alpha(0.5)

    ax.set_title("Mutant kills: test suite vs equivalence tester")
    # annotate "neither" count below the diagram
    ax.text(0.5, -0.08, f"Killed by neither: {neither}/{total} ({neither/total*100:.1f}%)",
            ha="center", transform=ax.transAxes, fontsize=10, color="gray")


def plot_per_class_breakdown(records, ax):
    """Stacked horizontal bar chart: per-class kill breakdown"""
    by_class = defaultdict(lambda: {"both": 0, "suite_only": 0, "equiv_only": 0, "neither": 0, "total": 0})
    for r in records:
        cls = r["class"]
        by_class[cls]["total"] += 1
        if r["suite_killed"] and r["equiv_killed"]:
            by_class[cls]["both"] += 1
        elif r["suite_killed"]:
            by_class[cls]["suite_only"] += 1
        elif r["equiv_killed"]:
            by_class[cls]["equiv_only"] += 1
        else:
            by_class[cls]["neither"] += 1

    # sort by total mutants descending
    items = sorted(by_class.items(), key=lambda x: x[1]["total"], reverse=True)
    labels = [cls for cls, _ in items]
    both_vals = [v["both"] for _, v in items]
    suite_vals = [v["suite_only"] for _, v in items]
    equiv_vals = [v["equiv_only"] for _, v in items]
    neither_vals = [v["neither"] for _, v in items]
    totals = [v["total"] for _, v in items]

    y = range(len(labels))

    bars_both = ax.barh(y, both_vals, color="#66bb6a", label="Both killed", edgecolor="white", linewidth=0.5)
    left = both_vals
    bars_suite = ax.barh(y, suite_vals, left=left, color="#ef5350", label="Suite only", edgecolor="white", linewidth=0.5)
    left = [a + b for a, b in zip(left, suite_vals)]
    bars_equiv = ax.barh(y, equiv_vals, left=left, color="#42a5f5", label="Equiv only", edgecolor="white", linewidth=0.5)
    left = [a + b for a, b in zip(left, equiv_vals)]
    bars_neither = ax.barh(y, neither_vals, left=left, color="#bdbdbd", label="Neither", edgecolor="white", linewidth=0.5)

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Number of mutants")
    ax.set_title("Kill breakdown by class")
    ax.legend(loc="upper right", fontsize=8)

    # annotate totals at the end of each bar
    for i, t in enumerate(totals):
        ax.text(t + 0.5, i, str(t), va="center", fontsize=8, color="gray")

def _parse_class_and_method(mutant_name):
    """
    Extract (ClassName, method_name) from mutant names like:
      'x\\u01c1Stack\\u01c1peek__mutmut_3' -> ('Stack', 'peek')
      'BST.x_insert__mutmut_2' -> ('BST', 'insert')
      'x_my_func__mutmut_1' -> ('(module)', 'my_func')
    """
    # mutmut class-level: xǁClassǁmethod__mutmut_N
    m = re.match(r"x\u01c1(\w+)\u01c1(\w+)__mutmut_\d+", mutant_name)
    if m:
        return m.group(1), m.group(2)
    # qualname style: Class.x_method__mutmut_N
    m = re.match(r"(\w+)\.x_(\w+)__mutmut_\d+", mutant_name)
    if m:
        return m.group(1), m.group(2)
    # top-level function: x_func__mutmut_N
    m = re.match(r"x_(\w+)__mutmut_\d+", mutant_name)
    if m:
        return "(module)", m.group(1)
    return "(unknown)", mutant_name


def _q1(data):
    s = sorted(data)
    n = len(s)
    i = n // 4
    return s[i] if n % 4 else (s[i - 1] + s[i]) / 2


def _q3(data):
    s = sorted(data)
    n = len(s)
    i = (3 * n) // 4
    return s[i] if n % 4 else (s[i - 1] + s[i]) / 2


def plot_coverage_vs_killed(report, ax):
    """Box plot comparing coverage distributions of killed vs survived mutants"""
    killed_pcts = [r["pct"] for r in report if r["killed"] and r["total"] > 0]
    survived_pcts = [r["pct"] for r in report if not r["killed"] and r["total"] > 0]

    data = [killed_pcts, survived_pcts]
    bp = ax.boxplot(data, tick_labels=["Killed", "Survived"], patch_artist=True, widths=0.5, showfliers=False)

    bp["boxes"][0].set_facecolor("#66bb6a")
    bp["boxes"][1].set_facecolor("#ef5350")
    for i, median_line in enumerate(bp["medians"]):
        median_val = median_line.get_ydata()[0]
        ax.text(i + 1 + 0.28, median_val, f"{median_val:.1f}%",
                va="center", fontsize=9, fontweight="bold")

    ax.text(0.98, 0.02, "Orange lines: medians",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8, color="gray", fontstyle="italic")

    for i, group in enumerate(data, start=1):
        jitter = [i + (hash(str(v)) % 100 - 50) * 0.003 for v in group]
        ax.scatter(jitter, group, alpha=0.4, s=20, color="black", zorder=3)

    ax.set_ylabel("Coverage %")
    ax.set_title("Coverage distribution: killed vs survived")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.set_ylim(-5, 105)


def plot_coverage_vs_iterations(report, ax):
    """Scatter plot of coverage % vs iterations to kill (unused)"""
    killed = [r for r in report if r["killed"] and r["total"] > 0]
    pcts = [r["pct"] for r in killed]
    iters = [r["iterations"] for r in killed]

    ax.scatter(pcts, iters, alpha=0.6, edgecolors="black", linewidths=0.5, s=40, color="#42a5f5")
    ax.set_xlabel("Coverage %")
    ax.set_ylabel("Iterations to kill")
    ax.set_title("Coverage vs iterations to kill")
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    ax.set_xlim(-5, 105)


def plot_coverage_vs_method_calls(report, ax):
    """Scatter plot of coverage % vs total method calls to kill (unused)"""
    killed = [r for r in report if r["killed"] and r["total"] > 0]
    pcts = [r["pct"] for r in killed]
    calls = [r["total_method_calls"] for r in killed]

    ax.scatter(pcts, calls, alpha=0.6, edgecolors="black", linewidths=0.5, s=40, color="#ffa726")
    ax.set_xlabel("Coverage %")
    ax.set_ylabel("Total method calls to kill")
    ax.set_title("Coverage vs method calls to kill")
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    ax.set_xlim(-5, 105)


def plot_cumulative_kill_curve(report, ax):
    """
    Cumulative percentage of mutants killed as a function of iteration budget
    """
    killed = [r for r in report if r["killed"]]
    total = len(report)
    if not killed:
        ax.text(0.5, 0.5, "No killed mutants", ha="center", va="center", transform=ax.transAxes)
        return

    iters_sorted = sorted(r["iterations"] for r in killed)
    fractions = [(i + 1) / total for i in range(len(iters_sorted))]

    ax.step(iters_sorted, fractions, where="post", color="#5c6bc0", linewidth=2)
    ax.fill_between(iters_sorted, fractions, step="post", alpha=0.15, color="#5c6bc0")

    ax.set_xlabel("Iteration budget per mutant")
    ax.set_ylabel("Percentage of mutants killed")
    ax.set_title("Cumulative kill curve")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.set_ylim(0, 1.05)

    max_frac = len(killed) / total
    ax.axhline(y=max_frac, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)


def plot_kill_rate_by_method(report, ax):
    """
    Horizontal bar chart of kill rate grouped by class.method
    Filtered to only include methods with kill rate < 66, but may still need to be reworked to be less crowded
    """
    by_method = defaultdict(lambda: {"killed": 0, "total": 0})
    for r in report:
        cls, method = _parse_class_and_method(r["mutant"])
        key = f"{cls}.{method}"
        by_method[key]["total"] += 1
        if r["killed"]:
            by_method[key]["killed"] += 1

    # sort by kill rate ascending so the worst methods sit at the top
    items = sorted(by_method.items(), key=lambda x: x[1]["killed"] / max(x[1]["total"], 1))
    labels = [k for k, _ in items]
    rates = [v["killed"] / max(v["total"], 1) * 100 for _, v in items]
    counts = [f'{v["killed"]}/{v["total"]}' for _, v in items]
    MIN_RATE = 66
    # filter otherwise the plot is too crowded
    filtered = [(l, r, c) for l, r, c in zip(labels, rates, counts) if r < MIN_RATE]
    if not filtered:
        ax.text(0.5, 0.5, f"All methods ≥ {MIN_RATE}% kill rate",
                ha="center", va="center", transform=ax.transAxes)
        return
    labels, rates, counts = zip(*filtered)

    colors = ["#66bb6a" if r == 100 else "#ef5350" if r == 0 else "#ffa726" for r in rates]
    bars = ax.barh(labels, rates, color=colors, edgecolor="white", linewidth=0.5)

    for bar, count_str in zip(bars, counts):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                count_str, va="center", fontsize=8, color="gray")

    ax.set_xlabel("Kill rate %")
    ax.set_title(f"Kill rate by method (showing < {MIN_RATE}%)")
    ax.set_xlim(0, 115)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())


def plot_iterations_vs_method_calls(report, ax):
    """Scatter plot showing correlation between the two cost metrics"""
    killed = [r for r in report if r["killed"] and r["total"] > 0]
    iters = [r["iterations"] for r in killed]
    calls = [r["total_method_calls"] for r in killed]

    ax.scatter(iters, calls, alpha=0.6, edgecolors="black", linewidths=0.5, s=40, color="#ab47bc")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Iterations to kill")
    ax.set_ylabel("Method calls to kill")
    ax.set_title("Iterations vs method calls")

def plot_unkilled_by_coverage(records, report, ax):
    """
    Strip chart of all mutants the equivalence tester failed to kill,
    plotted by coverage %.
    Mutants confirmed inequivalent by the test suite are highlighted in red
    """
    record_by_name = {rec["name"]: rec for rec in records}

    survived = []
    for r in report:
        if r["killed"] or r["total"] == 0:
            continue
        cls, suffix = parse_killed_line(r["mutant"])
        key = f"{cls}.{suffix}"
        rec = record_by_name.get(key)
        suite_killed = rec["suite_killed"] if rec else False
        survived.append({
            "pct": r["pct"],
            "suite_killed": suite_killed,
            "mutant": r["mutant"],
        })

    if not survived:
        ax.text(0.5, 0.5, "No survived mutants", ha="center", va="center", transform=ax.transAxes)
        return

    confirmed   = [p for p in survived if p["suite_killed"]]
    unconfirmed = [p for p in survived if not p["suite_killed"]]

    # hash-based jitter on y axis
    def jitter(points):
        return [(hash(p["mutant"]) % 200 - 100) * 0.003 for p in points]

    if unconfirmed:
        ax.scatter(
            [p["pct"] for p in unconfirmed],
            jitter(unconfirmed),
            color="#bdbdbd", alpha=0.6, s=40,
            edgecolors="black", linewidths=0.4, zorder=2,
            label=f"Unknown equivalence ({len(unconfirmed)})",
        )
    if confirmed:
        ax.scatter(
            [p["pct"] for p in confirmed],
            jitter(confirmed),
            color="#ef5350", alpha=0.85, s=55,
            edgecolors="black", linewidths=0.4, zorder=3,
            label=f"Confirmed inequivalent — suite killed ({len(confirmed)})",
        )
        median_pct = sorted([p["pct"] for p in confirmed])[len(confirmed) // 2]
        ax.axvline(x=median_pct, color="#ef5350", linestyle="-", linewidth=1.5, alpha=0.7)
        ax.text(median_pct-0.5, 0.34, f"median of RED mutants: {median_pct:.1f}%",
                fontsize=9, color="#ef5350", fontweight="bold")

    ax.set_xlabel("Coverage %")
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    ax.set_xlim(-5, 105)
    ax.set_yticks([])
    ax.set_title("Survived mutants by coverage\n(red = confirmed inequivalent by test suite)")
    ax.legend(loc="upper left", fontsize=9)


def main(meta_dir, killed_file, coverage_report, output_dir="."):
    records = load_comparison(meta_dir, killed_file)
    report = load_report(coverage_report)

   # fig1, axes1 = plt.subplots(1, 3, figsize=(18, 5))
    fig1, axes1 = plt.subplots(1, 1, figsize=(10, 6))
    #fig1.suptitle("Mutation Testing: Coverage Metrics", fontsize=14, fontweight="bold")
    #fig1.suptitle("Mutation Testing: Coverage Metrics", fontsize=14, fontweight="bold")

    plot_coverage_vs_killed(report, axes1)

    # these don't really show anything interesting so just comment them for now
    #plot_coverage_vs_iterations(report, axes1[1])
    #plot_coverage_vs_method_calls(report, axes1[2])

    fig1.tight_layout()
    path1 = f"{output_dir}/coverage_plots.png"
    fig1.savefig(path1, dpi=150)
    print(f"Saved {path1}")

    fig2 = plt.figure(figsize=(18, 5))
    fig2.suptitle("Mutation Testing: Cost & Kill Rate", fontsize=14, fontweight="bold")

    # the kill-rate-by-method chart needs more horizontal room
    gs = fig2.add_gridspec(1, 2, width_ratios=[1, 1])
    ax_cum = fig2.add_subplot(gs[0])
    ax_bar = fig2.add_subplot(gs[1])

    plot_cumulative_kill_curve(report, ax_cum)
    plot_kill_rate_by_method(report, ax_bar)

    fig2.tight_layout()
    path2 = f"{output_dir}/extra_plots.png"
    fig2.savefig(path2, dpi=150)
    print(f"Saved {path2}")

    fig3, axes3 = plt.subplots(1, 2, figsize=(14, 5),
                             gridspec_kw={"width_ratios": [1, 1.2]})
    fig3.suptitle("Equivalence Tester vs Test Suite", fontsize=14, fontweight="bold")

    plot_venn(records, axes3[0])
    plot_per_class_breakdown(records, axes3[1])

    fig3.tight_layout()
    path = f"{output_dir}/comparison_plots.png"
    fig3.savefig(path, dpi=150)
    print(f"\nSaved {path}")

    fig4, ax4 = plt.subplots(figsize=(10, 4))
    plot_unkilled_by_coverage(records, report, ax4)
    fig4.tight_layout()
    path4 = f"{output_dir}/unkilled_coverage.png"
    fig4.savefig(path4, dpi=150)
    print(f"Saved {path4}")


if __name__ == "__main__":
    meta_dir = sys.argv[1] if len(sys.argv) > 1 else "fixed_mutants/src"
    killed_file = sys.argv[2] if len(sys.argv) > 2 else "killed_mutants.txt"
    coverage_file = sys.argv[3] if len(sys.argv) > 3 else "coverage_report.json"
    out_dir = sys.argv[4] if len(sys.argv) > 4 else "."
    main(meta_dir, killed_file, coverage_file, out_dir)