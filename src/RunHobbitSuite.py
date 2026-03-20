import argparse
import os
import re
import subprocess
import time
from collections import defaultdict
from pathlib import Path

from TestingUtils import clear_log, kill_process_tree

BASE_DIR = Path(__file__).resolve().parent
INEQUIV_DIR = BASE_DIR / "programs" / "inequiv"
HOBBIT_DIR = BASE_DIR / "RunHobbitSuite" / "inequiv"
EQUIV_DIR = BASE_DIR  / "programs" / "equiv"
paths = list(INEQUIV_DIR.glob("*.txt"))
PROJECT_ROOT = os.path.abspath(os.getcwd())

runtimes = {}

def parse_args():
    parser = argparse.ArgumentParser(
        prog="RunHobbitSuite",
        description="Run equivalence tester against the HOBBIT suites"
    )
    parser.add_argument(
        "--suite",
        type=str,
        default="inequiv",
        help="Run equivalence tester against the inequiv or equiv suite."
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Number of seconds to wait for a test failure"
    )

    return parser.parse_args()

def main():
    args = parse_args()
    suite = args.suite
    timeout_seconds = args.timeout
    run_existing_suite(suite, timeout_seconds)


def run_existing_suite(suite="inequiv", timeout_seconds=280):
    clear_log()

    if suite == "inequiv":
        paths = list(INEQUIV_DIR.glob("*.py"))
    else:
        paths = list(EQUIV_DIR.glob("*.py"))
    before = time.time()

    results = []
    for path in paths:
        if "__init__" in path.name: continue
        result = run_script(path, timeout_seconds)
        results.append(result)

    after = time.time()
    print(f"\nCompleted in: {(after - before)/60:.2f} minutes")
    print(f"5 longest runtimes: {sorted(runtimes.items(), key=lambda item: item[1], reverse=True)[:5]}")

    if suite == "inequiv":
        print_results_table(results)


def run_script(filepath, timeout_seconds=280):
    name = filepath.stem
    print(f"Running test on {name}...", end=" ", flush=True)
    log_file = "hypofuzz_failures.log"
    cmd = ["hypothesis", "fuzz", str(filepath), "--no-dashboard"]
    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_ROOT + os.pathsep + env.get("PYTHONPATH", "")
    env["MUTANT_UNDER_TEST"] = ""
    initial_failure_count = 0
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding="utf-8") as f:
            initial_failure_count = len(f.readlines())

    killed = False
    elapsed = None
    process = None
    try:
        process = subprocess.Popen(
            cmd, env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid if os.name != 'nt' else None
        )

        start_time = time.time()
        while True:
            if process.poll() is not None:
                print("Finished (Process Exited)")
                break
            if time.time() - start_time > timeout_seconds:
                print("Timeout (Done)")
                break

            current_failure_count = 0
            if os.path.exists(log_file):
                with open(log_file, 'rb') as f:
                    current_failure_count = sum(1 for _ in f)

            new_failures = current_failure_count - initial_failure_count

            if new_failures >= 1:
                elapsed = time.time() - start_time
                runtimes[filepath] = elapsed
                killed = True
                print(f"Early Exit! ({new_failures} failures found)")
                break
            time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")

    kill_process_tree(process)
    time.sleep(0.1)

    return {
        "name": name,
        "killed": killed,
        "time": elapsed,
    }


def print_results_table(results):
    total = len(results)
    total_killed = sum(1 for r in results if r["killed"])

    print()
    print("=" * 78)
    print(f"HOBBIT SUITE RESULTS: {total_killed}/{total} detected ({total_killed/total*100:.1f}%)")
    print("=" * 78)

    # detailed per-test results
    print(f"\n{'─' * 78}")
    print(f"  {'Test':50s}  {'Result':>8s}  {'Time':>8s}")
    print(f"  {'─' * 50}  {'─' * 8}  {'─' * 8}")

    for r in results:
        status = "PASS" if r["killed"] else "FAIL"
        time_str = f"{r['time']:.2f}s" if r["time"] is not None else "—"
        print(f"  {r['name']:50s}  {status:>8s}  {time_str:>8s}")

    # summary of failures
    failures = [r for r in results if not r["killed"]]
    if failures:
        print(f"\n{'─' * 78}")
        print(f"  UNDETECTED PATTERNS ({len(failures)}):")
    print("=" * 78)


if __name__ == "__main__":
    main()