from src.UniversalStrategy import make_function_equivalence_test


arrays_1_lhs = lambda ar: lambda i: ar(i) if 0 <= i < 10 else 0

def make_rhs():
    rev = lambda ar: lambda i: ar(9 - i) if 0 <= i < 10 else 0
    return lambda ar: rev(rev(ar))

arrays_1_rhs = make_rhs()

test_arrays_1 = make_function_equivalence_test(arrays_1_lhs, arrays_1_rhs, log_failure=True)