from src.GenerateFunctions import h5
from src.UniversalStrategy import make_function_equivalence_test


def hector_stark_tricky_lhs(f):
    a = 0
    r = 0

    def inner(f):
        nonlocal r, a
        r = r + 1
        a = f(r)
        r = r - 1
        return a

    return inner(f)


def hector_stark_tricky_rhs(f):
    return f(1)


test_hector_snapback = make_function_equivalence_test(hector_stark_tricky_lhs, hector_stark_tricky_rhs, log_failure=True)
