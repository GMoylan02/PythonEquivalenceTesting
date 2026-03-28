import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib_venn import venn2


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
    """Returns (class_name, suffix) from a meta key."""
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
    """Proportional Venn diagram of kill sets."""
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

    # colour the regions
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


def main(meta_dir, killed_file, output_dir="."):
    records = load_comparison(meta_dir, killed_file)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5),
                             gridspec_kw={"width_ratios": [1, 1.2]})
    fig.suptitle("Equivalence Tester vs Test Suite", fontsize=14, fontweight="bold")

    plot_venn(records, axes[0])
    plot_per_class_breakdown(records, axes[1])

    fig.tight_layout()
    path = f"{output_dir}/comparison_plots.png"
    fig.savefig(path, dpi=150)
    print(f"\nSaved {path}")


if __name__ == "__main__":
    meta_dir = sys.argv[1] if len(sys.argv) > 1 else "fixed_mutants/src"
    killed_file = sys.argv[2] if len(sys.argv) > 2 else "killed_mutants.txt"
    out_dir = sys.argv[3] if len(sys.argv) > 3 else "."
    main(meta_dir, killed_file, out_dir)