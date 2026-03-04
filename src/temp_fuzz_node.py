
import sys
import os
os.environ["MUTANT_UNDER_TEST"] = ""
sys.path.insert(0, r'C:\Users\eyeba\Documents\PythonEquivalenceTesting\MutationTestDir')
from src.ClassEquivalence import create_class_equivalence_test
import mutmut_test.stack as mod_444
orig_methods_444 = {"__init__": getattr(getattr(mod_444, "Stack"), "xǁStackǁ__init____mutmut_orig"), "push": getattr(getattr(mod_444, "Stack"), "xǁStackǁpush__mutmut_orig")}
mutant_methods_444 = {"__init__": getattr(getattr(mod_444, "Stack"), "xǁStackǁ__init____mutmut_orig"), "push": getattr(getattr(mod_444, "Stack"), "xǁStackǁpush__mutmut_1")}
OrigClass_444 = type("Orig_Stack_444", (), orig_methods_444)
MutantClass_444 = type("Mutant_Stack_444", (), mutant_methods_444)
test_444 = create_class_equivalence_test(OrigClass_444, MutantClass_444)
