from typing import Callable

from src.UniversalStrategy import make_function_equivalence_test

#def hector_kierstead_lhs(f: Callable):
def hector_kierstead_lhs(f):
    return f(
        lambda x: f(
            lambda y: x()
        )
    )

#def hector_kierstead_rhs(f: Callable):
def hector_kierstead_rhs(f):
    return f(
        lambda x: f(
            lambda y: y()
        )
    )

test_hector_kierstead = make_function_equivalence_test(hector_kierstead_lhs, hector_kierstead_rhs, log_failure=True)
