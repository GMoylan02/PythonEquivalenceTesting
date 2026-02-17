from src.UniversalStrategy import make_function_equivalence_test


def holik_reentrancy_v0_lhs():
    def func(oppfuns):
        send = oppfuns[0]
        assert_fn = oppfuns[1]
        funds = [100]

        def withdraw(m):
            if m < funds[0]:
                send(m)
                funds[0] = funds[0] - m
            assert_fn(m >= 0)

        return withdraw

    return func


def holik_reentrancy_v0_rhs():
    def func(oppfuns):
        send = oppfuns[0]
        assert_fn = oppfuns[1]
        funds = [100]

        def withdraw(m):
            if m < funds[0]:
                send(m)
                funds[0] = funds[0] - m
            assert_fn(True)

        return withdraw

    return func

test_holik_reentrancy_v0 \
    = make_function_equivalence_test(holik_reentrancy_v0_lhs,
                                     holik_reentrancy_v0_rhs,
                                     log_failure=True)