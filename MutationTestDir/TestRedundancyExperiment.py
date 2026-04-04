"""
Check whether the 'both' set (mutants killed by both the equivalence tester
and the test suite) is sufficient to guide test writing.

Primary experiment: For each test that uniquely kills a mutant in the full
set, check whether it also uniquely kills a mutant in the 'both' set. If
yes, the 'both' set would detect the test's absence.

"""

import json
import sys
from collections import defaultdict


def normalize_mutant_name(name):
    """Strip module prefix: 'a_queue.xǁQueueǁpeek__mutmut_1' -> 'xǁQueueǁpeek__mutmut_1'"""
    for prefix in ["xǁ", "x_"]:
        idx = name.find(prefix)
        if idx != -1:
            return name[idx:]
    return name


def load_mutant_tests(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {normalize_mutant_name(k): v for k, v in raw.items()}


def load_killed_by_tool(path):
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def main():
    mutant_tests_path = sys.argv[1] if len(sys.argv) > 1 else "mutant_tests.json"
    killed_by_tool_path = sys.argv[2] if len(sys.argv) > 2 else "killed_mutants.txt"

    mutant_tests = load_mutant_tests(mutant_tests_path)
    killed_by_tool = load_killed_by_tool(killed_by_tool_path)

    killed_by_suite = set(mutant_tests.keys())
    both = killed_by_suite & killed_by_tool
    suite_only = killed_by_suite - killed_by_tool

    # mutant to tests
    mutant_to_tests = {m: set(tests) for m, tests in mutant_tests.items()}

    # test to mutants
    test_to_mutants_all = defaultdict(set)
    test_to_mutants_both = defaultdict(set)

    for m, tests in mutant_to_tests.items():
        for t in tests:
            test_to_mutants_all[t].add(m)
            if m in both:
                test_to_mutants_both[t].add(m)

    all_tests = set(test_to_mutants_all.keys())

    print(f"Killed by suite:   {len(killed_by_suite)}")
    print(f"Killed by tool:    {len(killed_by_tool)}")
    print(f"Killed by both:    {len(both)}")
    print(f"Suite only (A\\B):  {len(suite_only)}")
    print(f"Total tests:       {len(all_tests)}\n")

    # subset sufficiency experiment
    full_set_matters = []
    both_set_matters = []
    full_but_not_both = []

    for test in all_tests:
        full_unique = [m for m in test_to_mutants_all[test]
                       if not (mutant_to_tests[m] - {test})]
        both_unique = [m for m in test_to_mutants_both.get(test, set())
                       if not (mutant_to_tests[m] - {test})]

        if full_unique:
            full_set_matters.append((test, full_unique))
            if both_unique:
                both_set_matters.append((test, both_unique))
            else:
                full_but_not_both.append((test, full_unique))

    print("=" * 80)
    print("SUBSET SUFFICIENCY")
    print("  For each test that matters in the full set,")
    print("  does it also matter in the both-set?")
    print("=" * 80)
    print(f"  Tests that uniquely kill a full-set mutant:  {len(full_set_matters)}")
    print(f"  Of those, also uniquely kill a both-mutant:  {len(both_set_matters)}")
    print(f"  Flagged by full set but NOT by both-set:     {len(full_but_not_both)}")
    print()

    if full_but_not_both:
        print("  Tests the both-set would miss:")
        for test, kills in full_but_not_both:
            print(f"    {test}")
            for m in kills:
                print(f"      - {m}")
        print()
    else:
        print("  Every test that matters in the full set also matters in the")
        print("  both-set. The subset is sufficient to detect any missing test.")
        print()


    output = {
        "killed_by_suite": len(killed_by_suite),
        "killed_by_tool": len(killed_by_tool),
        "both": len(both),
        "suite_only": len(suite_only),
        "total_tests": len(all_tests),
        "full_set_matters": len(full_set_matters),
        "both_set_matters": len(both_set_matters),
        "full_but_not_both": len(full_but_not_both),
        "missed_tests": [t for t, _ in full_but_not_both],
    }
    with open("both_set_analysis.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"Saved: both_set_analysis.json")


if __name__ == "__main__":
    main()