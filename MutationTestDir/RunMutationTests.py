import signal
import sys
import os
import subprocess
import importlib
import pkgutil
import time

from src.ProgramEquivalence import get_module_functions

TIMEOUT_SECONDS = 10
TEMP_FILENAME = "../src/temp_fuzz_node.py"
UTILS_IMPORT_PATH = "src.UniversalStrategy"
TARGET_PACKAGE = "mutmut_test"
PROJECT_ROOT = os.path.abspath(os.getcwd())

with open("hypofuzz_failures.log", 'w') as f:
    f.write("")


def run_fuzzing_session():
    sys.path.insert(0, PROJECT_ROOT)

    print(f"Loading modules from {TARGET_PACKAGE}...")
    try:
        base_pkg = importlib.import_module(TARGET_PACKAGE)
    except ImportError:
        print(f"Error: Could not import {TARGET_PACKAGE}. Check your path.")
        return

    modules = [
        importlib.import_module(f"{base_pkg.__name__}.{name}")
        for _, name, _ in pkgutil.iter_modules(base_pkg.__path__)
    ]
    no_mutants = 0
    for module in modules:
        print(f"\n--- Scanning Module: {module.__name__} ---")
        funcs = get_module_functions(module)

        # Identify originals
        originals = {
            name: func
            for name, func in funcs.items()
            if "__mutmut_orig" in name
        }
        # Associate mutants with originals
        for orig_name, orig_func in originals.items():
            for func_name, func_obj in funcs.items():
                if orig_name.replace("__mutmut_orig", "") in func_name and "__mutmut_orig" not in func_name:
                    # orig_func vs func_obj (mutant)
                    run_single_fuzz_case(module, orig_func, func_obj)
                    no_mutants += 1

    # Count number of lines in hypofuzz_failures
    with open("hypofuzz_failures.log", 'r') as f:
        mutants_identified = len(f.readlines())
    print(f"Mutants identified: {mutants_identified}/{no_mutants}")
    KEEP_FILES = {
        "hypofuzz_failures.log",
        "RunMutationTests.py"
    }
    dir_path = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)

        if filename in KEEP_FILES or not os.path.isfile(file_path):
            continue

        os.remove(file_path)

def run_single_fuzz_case(module, orig_func, mutant_func):
    """Generates a script for a single pair and runs hypofuzz."""

    orig_name = orig_func.__name__
    mut_name = mutant_func.__name__
    test_name = f"test_{orig_name}_vs_{mut_name}"

    print(f"Running {test_name}...", end=" ", flush=True)
    file_content = f"""
import sys
import {module.__name__} as target_module
from {UTILS_IMPORT_PATH} import make_function_equivalence_test

orig_func = getattr(target_module, "{orig_name}__mutmut_orig")
mutant_func = getattr(target_module, "{mut_name}")

{test_name} = make_function_equivalence_test(orig_func, mutant_func, log_failure=True)

"""

    with open(TEMP_FILENAME, "w") as f:
        f.write(file_content)

    start_time = time.time()
    result_status = "UNKNOWN"

    cmd = ["hypothesis", "fuzz", TEMP_FILENAME, "--no-dashboard"]
    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_ROOT + os.pathsep + env.get("PYTHONPATH", "")

    process = None

    try:

        process = subprocess.Popen(
            cmd,
            env=env,
            #stdout=subprocess.DEVNULL,
            #stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid if os.name != 'nt' else None
        )

        process.wait(timeout=TIMEOUT_SECONDS)
        print("FINISHED_EARLY (Odd)")

    except Exception as e:
        kill_process_tree(process)

    # hack fix to prevent weird race condition
    time.sleep(0.5)

def kill_process_tree(process):
    """Reliably kill the process and its children."""
    if process is None:
        return

    # Check if it's already dead
    if process.poll() is not None:
        return

    try:
        if os.name != 'nt':
            # linux/mac
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        else:
            # windows
            subprocess.call(
                ['taskkill', '/F', '/T', '/PID', str(process.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    except Exception:
        pass

if __name__ == "__main__":
    run_fuzzing_session()