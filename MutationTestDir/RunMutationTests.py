import inspect
import json
import re
import signal
import sys
import os
import subprocess
import importlib
import pkgutil
import time
from pathlib import Path
from typing import Dict, Callable

from src.ClassEquivalence import get_module_methods
from src.TestingUtils import kill_process_tree, clean_directory, clear_log

TIMEOUT_SECONDS = 60
TEMP_FILENAME = "../src/temp_fuzz_node.py"
UTILS_IMPORT_PATH = "src.UniversalStrategy"
TARGET_PACKAGE = "fixed_mutants_annotated"
PROJECT_ROOT = os.path.abspath(os.getcwd())

# Directory where per-mutant coverage JSON files are written by the subprocesses.
COVERAGE_DIR = os.path.join(PROJECT_ROOT, ".mutant_coverage")

times_taken = []
mutants_killed = []


def _coverage_file_path(idx: int) -> str:
    os.makedirs(COVERAGE_DIR, exist_ok=True)
    return os.path.join(COVERAGE_DIR, f"coverage_{idx}.json")


def _read_coverage_result(idx: int) -> dict:
    """
    Read the JSON file written by the subprocess and return a dict:
        {
            "covered":  <int>,   # lines actually executed
            "total":    <int>,   # total lines in the mutant method
            "pct":      <float>, # 0-100
            "lines_covered": [...],
            "lines_total":   [...],
        }
    Returns zeroed-out values if the file doesn't exist or is malformed.
    """
    path = _coverage_file_path(idx)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        covered = len(data.get("lines_covered", []))
        total   = len(data.get("lines_total",   []))
        pct     = (covered / total * 100) if total > 0 else 0.0
        return {
            "covered":       covered,
            "total":         total,
            "pct":           pct,
            "lines_covered": data.get("lines_covered", []),
            "lines_total":   data.get("lines_total",   []),
        }
    except Exception:
        return {"covered": 0, "total": 0, "pct": 0.0,
                "lines_covered": [], "lines_total": []}


def _coverage_boilerplate(mutant_func_accessor: str, coverage_file: str) -> str:
    """
    Generates setup code injected into every temp file.
    """
    return f"""
import json as _json, inspect as _inspect

_mutant_func_for_cov = {mutant_func_accessor}
_coverage_target_func = _mutant_func_for_cov

try:
    _fn_for_src = getattr(_mutant_func_for_cov, '__func__', _mutant_func_for_cov)
    _mutant_source_lines, _mutant_start = _inspect.getsourcelines(_fn_for_src)
    _coverage_total_lines = list(range(_mutant_start, _mutant_start + len(_mutant_source_lines)))
except Exception:
    _coverage_total_lines = []

_covered_lines = set()

def _merge_coverage(new_lines):
    if not new_lines:
        return
    _covered_lines.update(new_lines)
    try:
        payload = {{
            "lines_covered": sorted(_covered_lines),
            "lines_total":   _coverage_total_lines,
        }}
        with open(r'{coverage_file}', 'w', encoding='utf-8') as _f:
            _json.dump(payload, _f)
    except Exception:
        pass
"""


def _class_test_assignment(idx: int) -> str:
    return f"""
from src.ClassEquivalence import create_class_equivalence_test as _make_cls_test
test_{idx} = _make_cls_test(
    OrigClass_{idx}, MutantClass_{idx},
    coverage_target_func=_coverage_target_func,
    on_coverage=_merge_coverage,
)
"""


def _func_test_assignment(idx: int) -> str:
    return f"""
from src.FunctionEquivalence import make_function_equivalence_test as _make_func_test
test_{idx} = _make_func_test(
    orig_func_{idx}, mutant_func_{idx},
    log_failure=True,
    coverage_target_func=_coverage_target_func,
    on_coverage=_merge_coverage,
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

        # ── class mutants ──────────────────────────────────────────────────
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
                killed, cov = run_class_fuzz_case(module, class_name, orig_methods, mutant_entry, idx)
                if killed:
                    mutants_identified += 1
                    module_mutants_identified += 1
                    mutants_killed.append(mutant_entry['attr_name'])
                coverage_report.append({
                    "mutant":  mutant_entry['attr_name'],
                    "killed":  killed,
                    "covered": cov["covered"],
                    "total":   cov["total"],
                    "pct":     round(cov["pct"], 1),
                })
                _print_coverage_line(mutant_entry['attr_name'], killed, cov)
                idx += 1

        # ── function mutants ───────────────────────────────────────────────
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
                killed, cov = run_func_fuzz_case(module, orig_func, func_obj, idx)
                if killed:
                    mutants_identified += 1
                    module_mutants_identified += 1
                    mutants_killed.append(func_obj)
                coverage_report.append({
                    "mutant":  func_obj.__qualname__,
                    "killed":  killed,
                    "covered": cov["covered"],
                    "total":   cov["total"],
                    "pct":     round(cov["pct"], 1),
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


def _print_coverage_line(mutant_name: str, killed: bool, cov: dict) -> None:
    status = "KILLED" if killed else "SURVIVED"
    if cov["total"] == 0:
        cov_str = "coverage: n/a"
    else:
        cov_str = f"coverage: {cov['covered']}/{cov['total']} lines ({cov['pct']:.1f}%)"
    print(f"    [{status}] {mutant_name}  —  {cov_str}")


def _print_coverage_summary(report: list[dict]) -> None:
    survived_low_cov = [
        r for r in report
        if not r["killed"] and r["total"] > 0 and r["pct"] < 50
    ]
    survived_high_cov = [
        r for r in report
        if not r["killed"] and r["total"] > 0 and r["pct"] >= 50
    ]
    print("\n── Coverage summary ──────────────────────────────────────────────────")
    print(f"  Survived with <50% coverage  (under-exercised): {len(survived_low_cov)}")
    print(f"  Survived with ≥50% coverage  (genuine equivalents or weak assertions): {len(survived_high_cov)}")
    if survived_low_cov:
        print("\n  Under-exercised survivors — consider improving input generation:")
        for r in survived_low_cov:
            print(f"    {r['mutant']}  {r['covered']}/{r['total']} lines ({r['pct']:.1f}%)")
    print("──────────────────────────────────────────────────────────────────────\n")


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
                times_taken.append(time.time() - start_time)
                killed = True
                break

            time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")

    kill_process_tree(process)
    # Brief pause to let the SIGTERM handler finish writing the coverage file
    # before we try to read it.
    time.sleep(0.3)
    return killed


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
    killed = run_fuzz_file(log_file, label)
    cov = _read_coverage_result(idx)
    return killed, cov


def run_class_fuzz_case(module, class_name, orig_methods, mutant_entry, idx):
    log_file = "hypofuzz_failures.log"
    coverage_file = _coverage_file_path(idx)
    mod_alias = f"mod_{idx}"
    mutant_method = mutant_entry["method_name"]
    mutant_attr   = mutant_entry["attr_name"]

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

    # The accessor for the mutant method specifically — this is what we want
    # coverage for, not the whole class.
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
    killed = run_fuzz_file(log_file, label)
    cov = _read_coverage_result(idx)
    return killed, cov


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