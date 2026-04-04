import inspect
import json
import re
import sys
import os
import importlib
import pkgutil
import time
from typing import Dict, Callable

from src.TestingUtils import clear_log, run_hypothesis_fuzz

TIMEOUT_SECONDS = 300
TEMP_FILENAME = "../src/temp_fuzz_node.py"
UTILS_IMPORT_PATH = "src.UniversalStrategy"
TARGET_PACKAGE = "fixed_mutants.src"
PROJECT_ROOT = os.path.abspath(os.getcwd())

# Directory where per-mutant coverage JSON files are written by the subprocesses
COVERAGE_DIR = os.path.join(PROJECT_ROOT, ".mutant_coverage")

times_taken = []
mutants_killed = []

def _coverage_file_path(idx):
    os.makedirs(COVERAGE_DIR, exist_ok=True)
    return os.path.join(COVERAGE_DIR, f"coverage_{idx}.json")


def _read_coverage_result(idx):
    path = _coverage_file_path(idx)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "setup_error" in data:
            print(f"\n    [COVERAGE SETUP ERROR idx={idx}]:\n{data['setup_error'].strip()}")

        covered = len(data.get("lines_covered", []))
        total = len(data.get("lines_total", []))
        pct = (covered / total * 100) if total > 0 else 0.0
        return {
            "covered": covered,
            "total": total,
            "pct": pct,
            "iterations": data.get("iterations", 0),
            "total_method_calls": data.get("total_method_calls", 0),
            "failing_init_args": data.get("failing_init_args", []),
            "failing_init_kwargs": data.get("failing_init_kwargs", {}),
            "failing_method_calls": data.get("failing_method_calls", []),
            "failing_final_state": data.get("failing_final_state", {}),
            "lines_covered": data.get("lines_covered", []),
            "lines_total": data.get("lines_total", []),
        }
    except FileNotFoundError:
        # File was never written at all, the subprocess was killed before
        # even the initial write completed
        return {"covered": 0, "total": 0, "pct": 0.0, "iterations": 0, "total_method_calls": 0,
                "failing_init_args": [], "failing_init_kwargs": {}, "failing_method_calls": [], "failing_final_state": {},
                "lines_covered": [], "lines_total": []}
    except Exception:
        return {"covered": 0, "total": 0, "pct": 0.0, "iterations": 0, "total_method_calls": 0,
                "failing_init_args": [], "failing_init_kwargs": {}, "failing_method_calls": [], "failing_final_state": {},
                "lines_covered": [], "lines_total": []}

def _coverage_boilerplate(mutant_func_accessor, coverage_file):
    return f"""
from src.Profiler import CoverageRecorder
coverage_target_func = {mutant_func_accessor}
recorder = CoverageRecorder(coverage_target_func, r'{coverage_file}')
"""


def _class_test_assignment(idx):
    return f"""
from src.ClassEquivalence import make_class_equivalence_test
test_{idx} = make_class_equivalence_test(
    OrigClass_{idx}, MutantClass_{idx},
    coverage_target_func=coverage_target_func,
    coverage_recorder=recorder, higher_order=True
)
"""


def _func_test_assignment(idx):
    return f"""
from src.FunctionEquivalence import make_function_equivalence_test
test_{idx} = make_function_equivalence_test(
    orig_func_{idx}, mutant_func_{idx},
    log_failure=True,
    coverage_target_func=coverage_target_func,
    coverage_recorder=recorder, higher_order=True
)
"""

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
    # Per-mutant coverage summary: list of dicts
    coverage_report: list[dict] = []

    func_mutant_pattern = re.compile(r"^x_(.+)__mutmut_(\d+)$")
    idx = 0

    for module in modules:
        print(f"\n--- Scanning Module: {module.__name__} ---")

        # class mutants
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
                killed, cov, time_to_kill = run_class_fuzz_case(module, class_name, orig_methods, mutant_entry, idx)
                if killed:
                    mutants_identified += 1
                    module_mutants_identified += 1
                    mutants_killed.append(mutant_entry['attr_name'])
                coverage_report.append({
                    "mutant": mutant_entry['attr_name'],
                    "killed": killed,
                    "time_to_kill": round(time_to_kill, 2) if time_to_kill is not None else None,
                    "iterations": cov["iterations"],
                    "total_method_calls": cov["total_method_calls"],
                    "failing_init_args": cov["failing_init_args"],
                    "failing_init_kwargs": cov["failing_init_kwargs"],
                    "failing_method_calls": cov["failing_method_calls"],
                    "failing_final_state": cov["failing_final_state"],
                    "covered": cov["covered"],
                    "total": cov["total"],
                    "pct": round(cov["pct"], 1),
                })
                _print_coverage_line(mutant_entry['attr_name'], killed, cov)
                idx += 1

        # function mutants
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
                killed, cov, time_to_kill = run_func_fuzz_case(module, orig_func, func_obj, idx)
                if killed:
                    mutants_identified += 1
                    module_mutants_identified += 1
                    mutants_killed.append(func_obj)
                coverage_report.append({
                    "mutant":  func_obj.__qualname__,
                    "killed":  killed,
                    "time_to_kill": round(time_to_kill, 2) if time_to_kill is not None else None,
                    "iterations": cov["iterations"],
                    "total_method_calls": cov["total_method_calls"],
                    "covered": cov["covered"],
                    "total": cov["total"],
                    "pct": round(cov["pct"], 1),
                })
                _print_coverage_line(func_obj.__qualname__, killed, cov)
                idx += 1

        print(f"{module_mutants_identified}/{module_mutants_found} mutants identified in module {module}")

    print(f"\n5 Longest times taken: {sorted(times_taken)[-5:]}")
    print(f"\nMutants identified: {mutants_identified}/{total_mutants_found}")

    with open("killed_mutants.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(str(m) for m in mutants_killed))

    with open("coverage_report.json", "w", encoding="utf-8") as f:
        json.dump(coverage_report, f, indent=2)

    _print_coverage_summary(coverage_report)


def _print_coverage_line(mutant_name: str, killed: bool, cov: dict):
    status = "KILLED" if killed else "SURVIVED"
    iters = cov.get("iterations", 0)
    method_calls = cov.get("total_method_calls", 0)
    if cov["total"] == 0:
        cov_str = "coverage: n/a"
    else:
        cov_str = f"coverage: {cov['covered']}/{cov['total']} lines ({cov['pct']:.1f}%)"
    print(f"    [{status}] {mutant_name}  —  {cov_str}  —  {method_calls} method calls in {iters} iterations")


def _print_coverage_summary(report: list[dict]):
    survived_setup_failed = [r for r in report if not r["killed"] and r["total"] == 0]
    survived_never_reached = [
        r for r in report
        if not r["killed"] and r["total"] > 0 and r["covered"] == 0
    ]
    survived_low_cov = [
        r for r in report
        if not r["killed"] and r["total"] > 0 and 0 < r["pct"] < 50
    ]
    survived_high_cov = [
        r for r in report
        if not r["killed"] and r["total"] > 0 and r["pct"] >= 50
    ]

    print("\n Coverage summary: ")
    print(f"  Setup failed / constructor mutants (total=0):         {len(survived_setup_failed)}")
    print(f"  Method never reached by fuzzer (total>0, covered=0):  {len(survived_never_reached)}")
    print(f"  Survived with <50% coverage  (under-exercised):       {len(survived_low_cov)}")
    print(f"  Survived with >=50% coverage (possible equivalents):  {len(survived_high_cov)}")

    if survived_never_reached:
        print("\n  Never-reached survivors:")
        for r in survived_never_reached:
            print(f"    {r['mutant']}  (0/{r['total']} lines)")

    if survived_low_cov:
        print("\n  Under-exercised survivors — consider improving input generation:")
        for r in survived_low_cov:
            print(f"    {r['mutant']}  {r['covered']}/{r['total']} lines ({r['pct']:.1f}%)\n")

def run_fuzz_file(log_file, label):
    print(f"  {label}...", end=" ", flush=True)

    result = run_hypothesis_fuzz(
        TEMP_FILENAME,
        log_file=log_file,
        timeout_seconds=TIMEOUT_SECONDS,
        project_root=PROJECT_ROOT,
    )

    if result.killed:
        times_taken.append(result.elapsed)
        print("Killed!")
    else:
        print("Survived")

    return result.killed, result.elapsed


def run_func_fuzz_case(module, orig_func, mutant_func, idx):
    log_file = "hypofuzz_failures.log"
    coverage_file = _coverage_file_path(idx)
    mod_alias = f"mod_{idx}"

    orig_setup, orig_accessor = generate_getter(orig_func, mod_alias, f"orig_instance_{idx}")
    mutant_setup, mutant_accessor = generate_getter(mutant_func, mod_alias, f"mutant_instance_{idx}")

    setup_lines = ""
    if orig_setup:
        setup_lines += f"{orig_setup}\n"
    if mutant_setup:
        setup_lines += f"{mutant_setup}\n"

    cov_boilerplate = _coverage_boilerplate(mutant_accessor, coverage_file)
    test_body = _func_test_assignment(idx)

    content = f"""
import sys
import os
os.environ["MUTANT_UNDER_TEST"] = ""
sys.path.insert(0, r'{PROJECT_ROOT}')
import {module.__name__} as {mod_alias}
{setup_lines}
orig_func_{idx} = {orig_accessor}
mutant_func_{idx} = {mutant_accessor}
{cov_boilerplate}
{test_body}
"""

    with open(TEMP_FILENAME, "w", encoding="utf-8") as f:
        f.write(content)

    label = f"{orig_func.__qualname__} vs {mutant_func.__qualname__}"
    killed, time_to_kill = run_fuzz_file(log_file, label)
    cov = _read_coverage_result(idx)
    return killed, cov, time_to_kill


def run_class_fuzz_case(module, class_name, orig_methods, mutant_entry, idx):
    log_file = "hypofuzz_failures.log"
    coverage_file = _coverage_file_path(idx)
    mod_alias = f"mod_{idx}"
    mutant_method = mutant_entry["method_name"]
    mutant_attr = mutant_entry["attr_name"]

    init_entry = ""
    if "__init__" not in orig_methods:
        init_entry = (
            f'"__init__": getattr({mod_alias}, "{class_name}").__init__, '
        )

    orig_dict_entries = init_entry + ", ".join(
        f'"{method_name}": getattr(getattr({mod_alias}, "{class_name}"), "{attr_name}")'
        for method_name, attr_name in orig_methods.items()
    )
    mutant_dict_entries = init_entry + ", ".join(
        f'"{method_name}": getattr(getattr({mod_alias}, "{class_name}"), "{mutant_attr}")'
        if method_name == mutant_method
        else f'"{method_name}": getattr(getattr({mod_alias}, "{class_name}"), "{attr_name}")'
        for method_name, attr_name in orig_methods.items()
    )

    # The accessor for the mutant method specifically. this is what we want
    # coverage for, not the whole class
    mutant_method_accessor = f'getattr(getattr({mod_alias}, "{class_name}"), "{mutant_attr}")'
    cov_boilerplate = _coverage_boilerplate(mutant_method_accessor, coverage_file)
    test_body = _class_test_assignment(idx)

    content = f"""
import sys
import os
os.environ["MUTANT_UNDER_TEST"] = ""
sys.path.insert(0, r'{PROJECT_ROOT}')
import {module.__name__} as {mod_alias}
orig_methods_{idx} = {{{orig_dict_entries}}}
mutant_methods_{idx} = {{{mutant_dict_entries}}}
OrigClass_{idx} = type("Orig_{class_name}_{idx}", (), orig_methods_{idx})
MutantClass_{idx} = type("Mutant_{class_name}_{idx}", (), mutant_methods_{idx})
{cov_boilerplate}
{test_body}
"""

    with open(TEMP_FILENAME, "w", encoding="utf-8") as f:
        f.write(content)

    label = f"{class_name}.{mutant_method} mutant {mutant_entry['mutant_index']}"
    killed, time_to_kill = run_fuzz_file(log_file, label)
    cov = _read_coverage_result(idx)
    return killed, cov, time_to_kill


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
    return {
        name: fn
        for name, fn in inspect.getmembers(module, inspect.isfunction)
        if fn.__module__ == module.__name__
    }


if __name__ == "__main__":
    before = time.time()
    run_fuzzing_session()
    print(f"\nCompleted in {time.time() - before:.1f} seconds.")