
import sys
import os

# Prevent crash on import for libraries like requests
os.environ["MUTANT_UNDER_TEST"] = ""

sys.path.insert(0, r'C:\Users\eyeba\Documents\PythonEquivalenceTesting\MutationTestDir')
from src.UniversalStrategy import make_function_equivalence_test


import mutmut_test.utils as mod_0
orig_func_0 = getattr(mod_0, "x_urldefragauth__mutmut_orig")
mutant_func_0 = getattr(mod_0, "x_urldefragauth__mutmut_9")
# Ensure log_failure=True so it writes to the file we are watching!
test_x_urldefragauth_vs_x_urldefragauth__mutmut_9_0 = make_function_equivalence_test(orig_func_0, mutant_func_0, log_failure=True)
