from typing import Callable

from src.FunctionEquivalence import make_function_equivalence_test


def ex4v2_ineq_lhs():
    x = [0]
    c = [0]

    #def func(f: Callable):
    def func(f):
        x[0] = 0
        c[0] = c[0] + 1
        f()
        if c[0] < 2:
            x[0] = 1
        c[0] = 0
        f()
        return x[0]

    return func


def ex4v2_ineq_rhs():
    #def func(f: Callable):
    def func(f):
        f()
        f()
        return 1

    return func

test_ex4v2_ineq = make_function_equivalence_test(ex4v2_ineq_lhs, ex4v2_ineq_rhs, log_failure=True)