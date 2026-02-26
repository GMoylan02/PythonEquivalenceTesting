import inspect
import re
import signal
import sys
import os
import subprocess
import importlib
import pkgutil
import time
from typing import Dict, Callable

from src.ClassEquivalence import get_module_methods
from src.TestingUtils import kill_process_tree, clean_directory, clear_log

TIMEOUT_SECONDS = 10
TEMP_FILENAME = "../src/temp_fuzz_node.py"
UTILS_IMPORT_PATH = "src.UniversalStrategy"
TARGET_PACKAGE = "mutmut_test"
PROJECT_ROOT = os.path.abspath(os.getcwd())


def run_fuzzing_session():
    os.environ["MUTANT_UNDER_TEST"] = ""
    clear_log()

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

    total_mutants_found = 0
    mutants_identified = 0
    func_mutant_pattern = re.compile(r"^x_(.+)__mutmut_(\d+)$")
    idx = 0

    for module in modules:
        print(f"\n--- Scanning Module: {module.__name__} ---")

        # test class mutants
        try:
            class_mutant_info = get_class_mutants(module)
        except Exception as e:
            print(f"Skipping class scan of {module.__name__}: {e}")
            class_mutant_info = {}
        module_mutants_found = 0
        module_mutants_identified = 0
        for class_name, info in class_mutant_info.items():
            orig_methods = {
                method_name: f"xǁ{class_name}ǁ{method_name}__mutmut_orig"
                for method_name in info["orig_methods"]
            }
            for mutant_entry in info["mutants"]:
                total_mutants_found += 1
                module_mutants_found += 1
                killed = run_class_fuzz_case(module, class_name, orig_methods, mutant_entry, idx)
                if killed:
                    mutants_identified += 1
                    module_mutants_identified += 1
                idx += 1

        # test function mutants that don't belong to a class
        try:
            funcs = get_module_functions(module)
        except Exception as e:
            print(f"Skipping function scan of {module.__name__}: {e}")
            continue

        for func_key, func_obj in funcs.items():
            match = func_mutant_pattern.match(func_key)
            if not match:
                continue

            original_name = match.group(1)
            orig_func = funcs.get(f"x_{original_name}__mutmut_orig") or funcs.get(original_name)

            if orig_func:
                total_mutants_found += 1
                module_mutants_found += 1
                killed = run_func_fuzz_case(module, orig_func, func_obj, idx)
                if killed:
                    mutants_identified += 1
                    module_mutants_identified += 1
                idx += 1
        print(f"{module_mutants_identified}/{module_mutants_found} mutants identified in module {module}")
    print(f"\nMutants identified: {mutants_identified}/{total_mutants_found}")
    #clean_directory()


def run_fuzz_file(log_file, label):
    """Write the temp file, run hypofuzz, return True if a failure was detected."""
    initial_failure_count = 0
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding="utf-8") as f:
            initial_failure_count = len(f.readlines())

    print(f"  {label}...", end=" ", flush=True)

    cmd = ["hypothesis", "fuzz", TEMP_FILENAME, "--no-dashboard"]
    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_ROOT + os.pathsep + env.get("PYTHONPATH", "")
    env["MUTANT_UNDER_TEST"] = ""

    process = None
    killed = False
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
                print("Timeout")
                break

            current_failure_count = 0
            if os.path.exists(log_file):
                with open(log_file, 'rb') as f:
                    current_failure_count = sum(1 for _ in f)

            if current_failure_count > initial_failure_count:
                print("Killed!")
                killed = True
                break

            time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")

    kill_process_tree(process)
    time.sleep(0.1)
    return killed


def run_func_fuzz_case(module, orig_func, mutant_func, idx):
    log_file = "hypofuzz_failures.log"
    mod_alias = f"mod_{idx}"

    orig_setup, orig_accessor = generate_getter(orig_func, mod_alias, f"orig_instance_{idx}")
    mutant_setup, mutant_accessor = generate_getter(mutant_func, mod_alias, f"mutant_instance_{idx}")

    setup_lines = ""
    if orig_setup:
        setup_lines += f"{orig_setup}\n"
    if mutant_setup:
        setup_lines += f"{mutant_setup}\n"

    content = f"""
import sys
import os
os.environ["MUTANT_UNDER_TEST"] = ""
sys.path.insert(0, r'{PROJECT_ROOT}')
from {UTILS_IMPORT_PATH} import make_function_equivalence_test
import {module.__name__} as {mod_alias}
{setup_lines}
orig_func_{idx} = {orig_accessor}
mutant_func_{idx} = {mutant_accessor}
test_{idx} = make_function_equivalence_test(orig_func_{idx}, mutant_func_{idx}, log_failure=True)
"""

    with open(TEMP_FILENAME, "w", encoding="utf-8") as f:
        f.write(content)

    label = f"{orig_func.__qualname__} vs {mutant_func.__qualname__}"
    return run_fuzz_file(log_file, label)


def run_class_fuzz_case(module, class_name, orig_methods, mutant_entry, idx):
    log_file = "hypofuzz_failures.log"
    mod_alias = f"mod_{idx}"
    mutant_method = mutant_entry["method_name"]
    mutant_attr = mutant_entry["attr_name"]

    orig_dict_entries = ", ".join(
        f'"{method_name}": getattr(getattr({mod_alias}, "{class_name}"), "{attr_name}")'
        for method_name, attr_name in orig_methods.items()
    )

    mutant_dict_entries = ", ".join(
        f'"{method_name}": getattr(getattr({mod_alias}, "{class_name}"), "{mutant_attr}")'
        if method_name == mutant_method
        else f'"{method_name}": getattr(getattr({mod_alias}, "{class_name}"), "{attr_name}")'
        for method_name, attr_name in orig_methods.items()
    )

    content = f"""
import sys
import os
os.environ["MUTANT_UNDER_TEST"] = ""
sys.path.insert(0, r'{PROJECT_ROOT}')
from src.ClassEquivalence import create_class_equivalence_test
import {module.__name__} as {mod_alias}
orig_methods_{idx} = {{{orig_dict_entries}}}
mutant_methods_{idx} = {{{mutant_dict_entries}}}
OrigClass_{idx} = type("Orig_{class_name}_{idx}", (), orig_methods_{idx})
MutantClass_{idx} = type("Mutant_{class_name}_{idx}", (), mutant_methods_{idx})
test_{idx} = create_class_equivalence_test(OrigClass_{idx}, MutantClass_{idx})
"""

    with open(TEMP_FILENAME, "w", encoding="utf-8") as f:
        f.write(content)

    label = f"{class_name}.{mutant_method} mutant {mutant_entry['mutant_index']}"
    return run_fuzz_file(log_file, label)


def generate_getter(func_obj, mod_alias_str, instance_var=None):
    qname = func_obj.__qualname__
    if "." in qname:
        cls_name = qname.split(".")[-2]
        method_name = qname.split(".")[-1]
        setup = f'{instance_var} = getattr({mod_alias_str}, "{cls_name}")()'
        accessor = f'getattr({instance_var}, "{method_name}")'
        return setup, accessor
    else:
        return "", f'getattr({mod_alias_str}, "{qname}")'


def get_class_mutants(module):
    """
    Returns a dict structured as:
    {
        class_name: {
            "orig_methods": { method_name: func },   # __mutmut_orig versions
            "mutants": [
                { "method_name": str, "mutant_index": int, "func": func },
                ...
            ]
        }
    }
    Only includes classes that have at least one mutant method.
    1. This data is used to reconstruct an original class from a mutated module (none of its methods are mutants)
    2. For each mutant method:
            reconstruct a class identical to the un-mutated version, but with the mutant method in place of its original
    This way, we can run create_class_equivalence_test on the original class vs a class with 1 mutant at a time and
    iteratively test each mutant individually
    """
    cls_mutant_pattern = re.compile(r"^xǁ(.+)ǁ(.+)__mutmut_(\d+)$")
    orig_pattern = re.compile(r"^xǁ(.+)ǁ(.+)__mutmut_orig$")
    result = {}

    for cls_name, cls_obj in inspect.getmembers(module, inspect.isclass):
        if cls_obj.__module__ != module.__name__:
            continue

        orig_methods = {}
        mutants = []

        for attr_name, method_obj in inspect.getmembers(cls_obj):
            if not (inspect.isfunction(method_obj) or inspect.ismethod(method_obj)):
                continue

            orig_match = orig_pattern.match(attr_name)
            if orig_match:
                orig_methods[orig_match.group(2)] = method_obj
                continue

            mut_match = cls_mutant_pattern.match(attr_name)
            if mut_match:
                mutants.append({
                    "method_name": mut_match.group(2),
                    "mutant_index": int(mut_match.group(3)),
                    "attr_name": attr_name,
                    "func": method_obj
                })

        if mutants and orig_methods:
            result[cls_name] = {"orig_methods": orig_methods, "mutants": mutants}

    return result

def get_module_functions(module) -> Dict[str, Callable]:
    functions = {
        name: fn
        for name, fn in inspect.getmembers(module, inspect.isfunction)
        if fn.__module__ == module.__name__
    }

    return functions


if __name__ == "__main__":
    before = time.time()
    run_fuzzing_session()
    print(f"\nCompleted in {time.time() - before:.1f} seconds.")