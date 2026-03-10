
import sys
import os
os.environ["MUTANT_UNDER_TEST"] = ""
sys.path.insert(0, r'C:\Users\eyeba\Documents\PythonEquivalenceTesting\MutationTestDir')
from src.ClassEquivalence import create_class_equivalence_test
import fixed_mutants_annotated.binheap as mod_19
orig_methods_19 = {"__init__": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁ__init____mutmut_orig"), "_balance": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁ_balance__mutmut_orig"), "_sift_down": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁ_sift_down__mutmut_orig"), "display": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁdisplay__mutmut_orig"), "pop": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁpop__mutmut_orig"), "push": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁpush__mutmut_orig")}
mutant_methods_19 = {"__init__": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁ__init____mutmut_orig"), "_balance": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁ_balance__mutmut_14"), "_sift_down": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁ_sift_down__mutmut_orig"), "display": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁdisplay__mutmut_orig"), "pop": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁpop__mutmut_orig"), "push": getattr(getattr(mod_19, "Binheap"), "xǁBinheapǁpush__mutmut_orig")}
OrigClass_19 = type("Orig_Binheap_19", (), orig_methods_19)
MutantClass_19 = type("Mutant_Binheap_19", (), mutant_methods_19)
test_19 = create_class_equivalence_test(OrigClass_19, MutantClass_19)
