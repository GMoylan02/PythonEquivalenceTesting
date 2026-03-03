#from typing import Callable
from typing import Callable

from src.FunctionEquivalence import make_function_equivalence_test

#def hector_scope_extrusion_1_2_lhs(f: Callable):
def hector_scope_extrusion_1_2_lhs(f):
    x = 0

    def inner(y):
        nonlocal x
        if x == 0:
            x = y
        else:
            x = y - 1
        return x

    return f(inner)

#def hector_scope_extrusion_1_2_rhs(f: Callable):
def hector_scope_extrusion_1_2_rhs(f):
    def inner(y):
        x = 0
        if x == 0:
            x = y
        else:
            x = y - 1
        return x

    return f(inner)

test_hector_scope_extrusion_1_2 = make_function_equivalence_test(hector_scope_extrusion_1_2_lhs, hector_scope_extrusion_1_2_rhs, log_failure=True)