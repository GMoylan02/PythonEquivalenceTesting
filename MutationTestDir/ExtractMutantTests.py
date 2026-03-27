import json
import subprocess
import sys
from pathlib import Path

"""
Helper file to create a 1-N mapping from mutants to the tests that killed them
saves the results to mutation_tests.json
NB: This file only works on linux
"""

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


def get_tests_for_mutant(mutant_name):
    """Run mutmut tests-for-mutant and parse the output"""
    full_name = f"{mutant_name}"
    try:
        result = subprocess.run(
            ["mutmut", "tests-for-mutant", full_name],
            capture_output=True, text=True, timeout=30,
        )

        tests = [
            line.strip() for line in result.stdout.strip().splitlines()
            if line.strip() and "::" in line
        ]
        return tests
    except subprocess.TimeoutExpired:
        print(f"  Timeout: {full_name}")
        return []
    except Exception as e:
        print(f"  Error for {full_name}: {e}")
        return []


def main():
    meta_dir = sys.argv[1] if len(sys.argv) > 1 else "mutants/src"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "mutant_tests.json"

    meta_dict = load_meta_files(meta_dir)

    mutant_to_tests = {}
    total = 0
    killed = 0
    skipped = 0

    for filename, exit_codes in meta_dict.items():
        print(f"Processing {filename}...")
        for mutant_name, exit_code in exit_codes.items():
            total += 1
            if exit_code == 0:
                skipped += 1
                continue

            killed += 1
            tests = get_tests_for_mutant(mutant_name)
            if not tests:
                skipped += 1
                continue
            mutant_to_tests[mutant_name] = tests

            count = len(tests)
            print(f"  {mutant_name}: {count} test{'s' if count != 1 else ''}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(mutant_to_tests, f, indent=2)

    print(f"\nDone: {killed}/{total} killed mutants processed, {skipped} survived")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()