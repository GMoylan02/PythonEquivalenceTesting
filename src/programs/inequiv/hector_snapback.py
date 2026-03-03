from typing import Callable

from src.GenerateFunctions import h2
from src.FunctionEquivalence import make_function_equivalence_test


def hector_snapback_lhs(p):
    x = 0

    def inner(y):
        nonlocal x
        x = 1

    p(inner)

    if x == 1:
        raise RuntimeError("_bot_")
    else:
        return None


def hector_snapback_rhs(p):
    def inner(y):
        raise RuntimeError("_bot_")
    p(inner)

test_hector_snapback = make_function_equivalence_test(hector_snapback_lhs, hector_snapback_rhs, log_failure=True)
#test_hector_snapback()
#print(hector_snapback_lhs(h2))
#print(hector_snapback_rhs(h2))
