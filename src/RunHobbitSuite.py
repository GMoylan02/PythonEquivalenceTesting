import os
import subprocess
import sys
import time
import types
from pathlib import Path

from MutationTestDir.RunMutationTests import kill_process_tree

BASE_DIR = Path(__file__).resolve().parent
INEQUIV_DIR = BASE_DIR / "programs" / "inequiv"
HOBBIT_DIR = BASE_DIR / "RunHobbitSuite" / "inequiv"
EQUIV_DIR = BASE_DIR  / "programs" / "equiv"
paths = list(INEQUIV_DIR.glob("*.txt"))
PROJECT_ROOT = os.path.abspath(os.getcwd())
TIMEOUT_SECONDS = 15

def run_existing_suite():
    with open("hypofuzz_failures.log", 'w', encoding="utf-8") as f:
        f.write("")

    paths = list(INEQUIV_DIR.glob("*.py"))
    before = time.time()
    for path in paths:
        run_script(path)
    after = time.time()
    print(f"Completed in: {(after - before)/60} minutes")

def run_script(filepath):
    print(f"Running test on {str(filepath).split("\\")[-1]}")
    log_file = "hypofuzz_failures.log"
    cmd = ["hypothesis", "fuzz", filepath, "--no-dashboard"]
    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_ROOT + os.pathsep + env.get("PYTHONPATH", "")
    env["MUTANT_UNDER_TEST"] = ""
    initial_failure_count = 0
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding="utf-8") as f:
            initial_failure_count = len(f.readlines())
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
            if time.time() - start_time > TIMEOUT_SECONDS:
                print("Timeout (Done)")
                break

            current_failure_count = 0
            if os.path.exists(log_file):
                with open(log_file, 'rb') as f:
                    current_failure_count = sum(1 for _ in f)

            new_failures = current_failure_count - initial_failure_count

            if new_failures >= 1:
                print(f"⚡ Early Exit! ({new_failures} failures found)")
                break
            time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")

    kill_process_tree(process)
    time.sleep(0.1)

run_existing_suite()