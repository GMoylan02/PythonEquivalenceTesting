from typing import Callable

from src.UniversalStrategy import make_function_equivalence_test


def make_call_lhs():
    x = [0]

    #def call(f: Callable):
    def call(f):
        x[0] = x[0] + 1
        f()
        x[0] = x[0] - 1
        return x[0] < 100

    return call


def make_call_rhs():
    x = [0]

    #def call(f: Callable):
    def call(f):
        x[0] = x[0] + 1
        f()
        x[0] = x[0] - 1
        return True

    return call

test_call_nested_param_ineq = make_function_equivalence_test(make_call_lhs, make_call_rhs, log_failure=True)
#test_call_nested_param_ineq()