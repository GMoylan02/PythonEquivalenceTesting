
import sys
import os
os.environ["MUTANT_UNDER_TEST"] = ""
sys.path.insert(0, r'C:\Users\eyeba\Documents\PythonEquivalenceTesting\MutationTestDir')
import fixed_mutants_annotated.a_queue as mod_2
orig_methods_2 = {"__init__": getattr(getattr(mod_2, "Queue"), "xǁQueueǁ__init____mutmut_orig"), "dequeue": getattr(getattr(mod_2, "Queue"), "xǁQueueǁdequeue__mutmut_orig"), "enqueue": getattr(getattr(mod_2, "Queue"), "xǁQueueǁenqueue__mutmut_orig"), "isEmpty": getattr(getattr(mod_2, "Queue"), "xǁQueueǁisEmpty__mutmut_orig"), "peek": getattr(getattr(mod_2, "Queue"), "xǁQueueǁpeek__mutmut_orig")}
mutant_methods_2 = {"__init__": getattr(getattr(mod_2, "Queue"), "xǁQueueǁ__init____mutmut_orig"), "dequeue": getattr(getattr(mod_2, "Queue"), "xǁQueueǁdequeue__mutmut_1"), "enqueue": getattr(getattr(mod_2, "Queue"), "xǁQueueǁenqueue__mutmut_orig"), "isEmpty": getattr(getattr(mod_2, "Queue"), "xǁQueueǁisEmpty__mutmut_orig"), "peek": getattr(getattr(mod_2, "Queue"), "xǁQueueǁpeek__mutmut_orig")}
OrigClass_2 = type("Orig_Queue_2", (), orig_methods_2)
MutantClass_2 = type("Mutant_Queue_2", (), mutant_methods_2)

import json as _json, inspect as _inspect

_mutant_func_for_cov = getattr(getattr(mod_2, "Queue"), "xǁQueueǁdequeue__mutmut_1")
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
        payload = {
            "lines_covered": sorted(_covered_lines),
            "lines_total":   _coverage_total_lines,
        }
        with open(r'C:\Users\eyeba\Documents\PythonEquivalenceTesting\MutationTestDir\.mutant_coverage\coverage_2.json', 'w', encoding='utf-8') as _f:
            _json.dump(payload, _f)
    except Exception:
        pass


from src.ClassEquivalence import create_class_equivalence_test as _make_cls_test
test_2 = _make_cls_test(
    OrigClass_2, MutantClass_2,
    coverage_target_func=_coverage_target_func,
    on_coverage=_merge_coverage,
)

