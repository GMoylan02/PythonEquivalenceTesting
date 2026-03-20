
import sys
import os
os.environ["MUTANT_UNDER_TEST"] = ""
sys.path.insert(0, r'C:\Users\eyeba\Documents\PythonEquivalenceTesting\MutationTestDir')
import fixed_mutants.stack as mod_526
orig_methods_526 = {"__init__": getattr(getattr(mod_526, "Stack"), "xǁStackǁ__init____mutmut_orig"), "isEmpty": getattr(getattr(mod_526, "Stack"), "xǁStackǁisEmpty__mutmut_orig"), "peek": getattr(getattr(mod_526, "Stack"), "xǁStackǁpeek__mutmut_orig"), "pop": getattr(getattr(mod_526, "Stack"), "xǁStackǁpop__mutmut_orig"), "push": getattr(getattr(mod_526, "Stack"), "xǁStackǁpush__mutmut_orig")}
mutant_methods_526 = {"__init__": getattr(getattr(mod_526, "Stack"), "xǁStackǁ__init____mutmut_orig"), "isEmpty": getattr(getattr(mod_526, "Stack"), "xǁStackǁisEmpty__mutmut_orig"), "peek": getattr(getattr(mod_526, "Stack"), "xǁStackǁpeek__mutmut_orig"), "pop": getattr(getattr(mod_526, "Stack"), "xǁStackǁpop__mutmut_orig"), "push": getattr(getattr(mod_526, "Stack"), "xǁStackǁpush__mutmut_1")}
OrigClass_526 = type("Orig_Stack_526", (), orig_methods_526)
MutantClass_526 = type("Mutant_Stack_526", (), mutant_methods_526)

from src.Profiler import CoverageRecorder
coverage_target_func = getattr(getattr(mod_526, "Stack"), "xǁStackǁpush__mutmut_1")
recorder = CoverageRecorder(coverage_target_func, r'C:\Users\eyeba\Documents\PythonEquivalenceTesting\MutationTestDir\.mutant_coverage\coverage_526.json')


from src.ClassEquivalence import create_class_equivalence_test
test_526 = create_class_equivalence_test(
    OrigClass_526, MutantClass_526,
    coverage_target_func=coverage_target_func,
    coverage_recorder=recorder,
)

