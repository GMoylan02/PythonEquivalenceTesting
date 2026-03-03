from typing import Callable

from src.FunctionEquivalence import make_function_equivalence_test


#def meyer_sieber_v2_ineq_lhs(g: Callable):
def meyer_sieber_v2_ineq_lhs(g):
    def even(x):
        return (x - ((x // 2) * 2)) == 0
    l = 0
    def f():
        nonlocal l
        l = l + 1
    g(f)
    if even(l):
        return lambda: None
    else:
        raise RuntimeError()


#def meyer_sieber_v2_ineq_rhs(g: Callable):
def meyer_sieber_v2_ineq_rhs(g):
    g(lambda: None)
    return lambda: None

test_meyer_sieber_v2_ineq = make_function_equivalence_test(meyer_sieber_v2_ineq_lhs, meyer_sieber_v2_ineq_rhs, log_failure=True)
