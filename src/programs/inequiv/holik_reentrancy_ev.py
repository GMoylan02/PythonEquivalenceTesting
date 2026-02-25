from typing import Callable

from src.UniversalStrategy import make_function_equivalence_test


def holik_reentrancy_ev_lhs():
    funds = [100]

    #def withdraw(send1amount: tuple[Callable, int]):
    def withdraw(send1amount):
        send, amount = send1amount
        if not (funds[0] < amount):
            send()
            funds[0] = funds[0] - amount
        return funds[0]

    return withdraw


def holik_reentrancy_ev_rhs():
    funds = [100]

    #def withdraw(send1amount: tuple[Callable, int]):
    def withdraw(send1amount):
        send, amount = send1amount
        if not (funds[0] < amount):
            funds[0] = funds[0] - amount
            send()
        return funds[0]

    return withdraw

test_holik_reentrancy_ev \
    = make_function_equivalence_test(holik_reentrancy_ev_lhs,
                                     holik_reentrancy_ev_rhs,
                                     log_failure=True)