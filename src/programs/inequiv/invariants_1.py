from typing import Callable

from src.FunctionEquivalence import make_function_equivalence_test


def invariants_1_lhs():
    x = [0]

    #def func(g: Callable):
    def func(g):
        x[0] = x[0] + 1
        if x[0] > 10:
            x[0] = 0
        g()
        if x[0] <= 10:
            x[0] = x[0] + 1
        else:
            raise Exception("_bot_")

    return func

def invariants_1_rhs():
    #def func(g: Callable):
    def func(g):
        g()

    return func

test_invariants_1 = make_function_equivalence_test(invariants_1_lhs, invariants_1_rhs, log_failure=True)
#test_invariants_1()