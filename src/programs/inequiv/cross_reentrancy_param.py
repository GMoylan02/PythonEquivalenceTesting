from src.UniversalStrategy import make_function_equivalence_test


def cross_reentrancy_param_lhs():
    x = [0]

    even = lambda n: (n - (n // 2) * 2) == 0

    def call_even():
        if even(x[0]):
            x[0] = x[0] + 1

    def call_odd():
        if even(x[0]):
            pass
        else:
            x[0] = x[0] + 1

    assert_fn = lambda: x[0] < 100

    return (call_even, call_odd, assert_fn)


def cross_reentrancy_param_rhs():
    x = [0]

    even = lambda n: (n - (n // 2) * 2) == 0

    def call_even():
        if even(x[0]):
            x[0] = x[0] + 1

    def call_odd():
        if even(x[0]):
            pass
        else:
            x[0] = x[0] + 1

    assert_fn = lambda: True

    return (call_even, call_odd, assert_fn)

test_cross_reentrancy_param = make_function_equivalence_test(cross_reentrancy_param_lhs, cross_reentrancy_param_rhs, log_failure=True)