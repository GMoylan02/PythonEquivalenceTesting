"""
Check whether the 'both' set (mutants killed by both the equivalence tester
and the test suite) is sufficient to guide test writing.

For each test in the suite, check whether it kills at least one mutant in
the 'both' set. If every test kills at least one 'both' mutant, a developer
working only with the 'both' set would notice the absence of any test.
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

    mutant_to_tests = load_mutant_tests(mutant_tests_path)
    killed_by_tool = load_killed_by_tool(killed_by_tool_path)

    killed_by_suite = set(mutant_to_tests.keys())
    both = killed_by_suite & killed_by_tool
    suite_only = killed_by_suite - killed_by_tool

    test_sets = {m: set(tests) for m, tests in mutant_to_tests.items()}

    print(f"Killed by suite: {len(killed_by_suite)}")
    print(f"Killed by tool: {len(killed_by_tool)}")
    print(f"Killed by both: {len(both)}")
    print(f"Suite only (A\\B): {len(suite_only)}\n")

    # build reverse mapping: test -> mutants it kills
    test_to_mutants_all = defaultdict(set)
    test_to_mutants_both = defaultdict(set)

    for m, tests in test_sets.items():
        for t in tests:
            test_to_mutants_all[t].add(m)
            if m in both:
                test_to_mutants_both[t].add(m)

    all_tests = set(test_to_mutants_all.keys())
    tests_with_both_kills = set(test_to_mutants_both.keys())
    tests_without_both_kills = all_tests - tests_with_both_kills

    print(f"Total unique tests: {len(all_tests)}")
    print(f"Tests that kill a 'both' mutant: {len(tests_with_both_kills)}")
    print(f"Tests that kill NO 'both' mutant: {len(tests_without_both_kills)}\n")

    if tests_without_both_kills:
        print(" Tests not represented in 'both' set:")
        for t in sorted(tests_without_both_kills):
            kills = test_to_mutants_all[t]
            print(f"{t}")
            print(f"kills {len(kills)} mutant(s), all suite-only:")
            for m in sorted(kills):
                print(f"-{m}")
        print(f"\nResult: {len(tests_without_both_kills)} tests would NOT be flagged")
        print(" as missing by the 'both' set alone.")
    else:
        print("Result: Every test in the suite kills at least one 'both' mutant")
        print("Given only the mutants that the equiv. tester killed, a developer would notice the absence of any test in the suite")

    # save results
    output = {
        "killed_by_suite": len(killed_by_suite),
        "killed_by_tool": len(killed_by_tool),
        "both": len(both),
        "suite_only": len(suite_only),
        "total_tests": len(all_tests),
        "tests_covering_both": len(tests_with_both_kills),
        "tests_not_covering_both": len(tests_without_both_kills),
        "uncovered_tests": sorted(tests_without_both_kills),
    }
    output_path = "both_set_analysis.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\nDetailed results: {output_path}")


if __name__ == "__main__":
    main()