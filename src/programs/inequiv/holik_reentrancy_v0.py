from typing import Callable

from src.FunctionEquivalence import make_function_equivalence_test


#def lhs(oppfuns: tuple[Callable, Callable]):
def holik_reentrancy_v0_lhs(oppfuns):
    send = oppfuns[0]
    assert_fn = oppfuns[1]
    funds = [100]

    def withdraw(m: int):
        if m < funds[0]:
            send(m)
            funds[0] = funds[0] - m
        assert_fn(m >= 0)

    return withdraw


#def rhs(oppfuns: tuple[Callable, Callable]):
def holik_reentrancy_v0_rhs(oppfuns):
    send = oppfuns[0]
    assert_fn = oppfuns[1]
    funds = [100]

    def withdraw(m: int):
        if m < funds[0]:
            send(m)
            funds[0] = funds[0] - m
        assert_fn(True)

    return withdraw


test_holik_reentrancy_v0 \
    = make_function_equivalence_test(holik_reentrancy_v0_lhs,
                                     holik_reentrancy_v0_rhs,
                                     log_failure=True)
#test_holik_reentrancy_v0()