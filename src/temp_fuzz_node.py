
import sys
import os
os.environ["MUTANT_UNDER_TEST"] = ""
sys.path.insert(0, r'C:\Users\eyeba\Documents\PythonEquivalenceTesting\MutationTestDir')
import fixed_mutants_annotated.linked_list as mod_451
orig_methods_451 = {"__init__": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁ__init____mutmut_orig"), "display": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁdisplay__mutmut_orig"), "pop": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁpop__mutmut_orig"), "push": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁpush__mutmut_orig"), "remove": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁremove__mutmut_orig"), "search": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁsearch__mutmut_orig")}
mutant_methods_451 = {"__init__": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁ__init____mutmut_orig"), "display": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁdisplay__mutmut_3"), "pop": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁpop__mutmut_orig"), "push": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁpush__mutmut_orig"), "remove": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁremove__mutmut_orig"), "search": getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁsearch__mutmut_orig")}
OrigClass_451 = type("Orig_LinkedList_451", (), orig_methods_451)
MutantClass_451 = type("Mutant_LinkedList_451", (), mutant_methods_451)

import os as _os, json as _json, inspect as _inspect

# ── coverage setup ────────────────────────────────────────────────────────────
_mutant_func_for_cov = getattr(getattr(mod_451, "LinkedList"), "xǁLinkedListǁdisplay__mutmut_3")
_coverage_target_func = _mutant_func_for_cov

try:
    # getsourcelines can fail on bound methods in some Python versions; unwrap first.
    _fn_for_src = getattr(_mutant_func_for_cov, '__func__', _mutant_func_for_cov)
    _mutant_source_lines, _mutant_start = _inspect.getsourcelines(_fn_for_src)
    _coverage_total_lines = list(range(_mutant_start, _mutant_start + len(_mutant_source_lines)))
except Exception as _e:
    _coverage_total_lines = []

_covered_lines = set()

def _merge_coverage(new_lines):
    # Write incrementally on every update so the file always reflects the latest
    # state. atexit/SIGTERM are unreliable when the parent kills us with a hard
    # kill (taskkill /F on Windows, SIGKILL on Unix), so we can't rely on them.
    if not new_lines:
        return
    _covered_lines.update(new_lines)
    try:
        payload = {
            "lines_covered": sorted(_covered_lines),
            "lines_total":   _coverage_total_lines,
        }
        with open(r'C:\Users\eyeba\Documents\PythonEquivalenceTesting\MutationTestDir\.mutant_coverage\coverage_451.json', 'w', encoding='utf-8') as _f:
            _json.dump(payload, _f)
    except Exception:
        pass
# ── end coverage setup ────────────────────────────────────────────────────────


from src.ClassEquivalence import create_class_equivalence_test as _make_cls_test
from src.EquivalenceChecker import EquivalenceChecker as _EqChecker, run_and_test_equivalence as _rte
from hypothesis import given, settings as _settings
from hypothesis.strategies import data as _st_data
from src.ClassEquivalence import generate_sequence_strategy
from src.StateUtils import snapshot_object_state, restore_object_state
from src.Profiler import record_failure

_obj_a_451 = OrigClass_451()
_obj_b_451 = MutantClass_451()
_seq_strat_451 = generate_sequence_strategy(_obj_a_451, _obj_b_451)

@given(_seq_strat_451, _st_data())
@_settings(max_examples=1000)
def test_451(ops, data):
    snap_a = snapshot_object_state(_obj_a_451)
    snap_b = snapshot_object_state(_obj_b_451)
    unique_id = f"{type(_obj_a_451).__name__}_{type(_obj_b_451).__name__}"
    try:
        for op in ops:
            func_name = op[0]
            func_a = getattr(_obj_a_451, func_name)
            func_b = getattr(_obj_b_451, func_name)
            raw_args, raw_kwargs = op[1]
            # Instantiate checker directly so covered_lines can be captured in a
            # finally block. If we used _rte() the return value is never reached
            # when AssertionError is raised (mutant killed), losing all coverage.
            _c = _EqChecker(func_a, func_b, data, coverage_target=_coverage_target_func)
            try:
                _c.check(raw_args, raw_kwargs)
            finally:
                _merge_coverage(_c.covered_lines)
    except AssertionError as e:
        record_failure(type(_obj_a_451).__name__, e, unique_id)
        raise
    finally:
        restore_object_state(_obj_a_451, snap_a)
        restore_object_state(_obj_b_451, snap_b)

