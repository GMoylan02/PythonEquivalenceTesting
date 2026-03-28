import json
import re
import statistics
import sys
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def load_report(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_class_and_method(mutant_name):
    """
    Extract (ClassName, method_name) from mutant names like:
      'x\\u01c1Stack\\u01c1peek__mutmut_3'  -> ('Stack', 'peek')
      'BST.x_insert__mutmut_2'              -> ('BST', 'insert')
      'x_my_func__mutmut_1'                 -> ('(module)', 'my_func')
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
    """Box plot comparing coverage distributions of killed vs survived mutants."""
    killed_pcts = [r["pct"] for r in report if r["killed"] and r["total"] > 0]
    survived_pcts = [r["pct"] for r in report if not r["killed"] and r["total"] > 0]

    data = [killed_pcts, survived_pcts]
    bp = ax.boxplot(data, tick_labels=["Killed", "Survived"], patch_artist=True, widths=0.5)

    bp["boxes"][0].set_facecolor("#66bb6a")
    bp["boxes"][1].set_facecolor("#ef5350")
    for i, median_line in enumerate(bp["medians"]):
        median_val = median_line.get_ydata()[0]
        ax.text(i + 1 + 0.28, median_val, f"{median_val:.1f}%",
                va="center", fontsize=9, fontweight="bold")

    ax.text(0.98, 0.02, "Values shown are medians",
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
    """Scatter plot of coverage % vs iterations to kill (killed mutants only)."""
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
    """Scatter plot of coverage % vs total method calls to kill (killed mutants only)"""
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
    Filtered to only include methods with kill rate < 80, but may still need to be reworked to be less crowded
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
    MIN_RATE = 80
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


def main(report_path, output_dir="."):
    report = load_report(report_path)

    fig1, axes1 = plt.subplots(1, 3, figsize=(18, 5))
    fig1.suptitle("Mutation Testing: Coverage Metrics", fontsize=14, fontweight="bold")

    plot_coverage_vs_killed(report, axes1[0])
    plot_coverage_vs_iterations(report, axes1[1])
    plot_coverage_vs_method_calls(report, axes1[2])

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


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "coverage_report.json"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    main(path, out_dir)