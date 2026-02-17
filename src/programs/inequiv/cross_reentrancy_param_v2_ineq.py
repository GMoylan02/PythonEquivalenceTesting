from src.UniversalStrategy import make_function_equivalence_test


def cross_reentrancy_param_v2_lhs():
    x = [0]

    def call_even():
        if (x[0] - (x[0] // 2) * 2) == 0:
            x[0] = x[0] + 1
        return x[0] < 5

    def call_odd():
        if (x[0] - (x[0] // 2) * 2) == 0:
            pass
        else:
            x[0] = x[0] + 1
        return x[0] < 5

    return lambda f: f(call_even, call_odd)


def cross_reentrancy_param_v2_rhs():
    x = [0]

    def call_even():
        if (x[0] - (x[0] // 2) * 2) == 0:
            x[0] = x[0] + 1
        return True

    def call_odd():
        if (x[0] - (x[0] // 2) * 2) == 0:
            pass
        else:
            x[0] = x[0] + 1
        return True

    return lambda f: f(call_even, call_odd)

test_cross_reentrancy_param_v2 = make_function_equivalence_test(cross_reentrancy_param_v2_lhs, cross_reentrancy_param_v2_rhs, log_failure=True)