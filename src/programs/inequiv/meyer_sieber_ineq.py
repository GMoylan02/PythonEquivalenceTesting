from typing import Callable

from src.UniversalStrategy import make_function_equivalence_test

#def meyer_sieber_ineq_lhs(g: Callable):
def meyer_sieber_ineq_lhs(g):
    x = 0
    def f():
        nonlocal x
        x = x + 2
    g(f)
    if x <= 10:
        return None
    else:
        raise RuntimeError()


#def meyer_sieber_ineq_rhs(g: Callable):
def meyer_sieber_ineq_rhs(g):
    g(lambda x: None)
    return None

test_meyer_sieber_ineq = make_function_equivalence_test(meyer_sieber_ineq_lhs, meyer_sieber_ineq_rhs, log_failure=True)
