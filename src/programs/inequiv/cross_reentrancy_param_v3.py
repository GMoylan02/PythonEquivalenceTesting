from src.FunctionEquivalence import make_function_equivalence_test


def cross_reentrancy_param_v3_lhs():
    is_even = [True]
    x = [0]

    def call_even():
        if is_even[0]:
            x[0] = x[0] + 1
        is_even[0] = False
        return x[0] < 5

    def call_odd():
        if is_even[0]:
            pass
        else:
            x[0] = x[0] + 1
        is_even[0] = True
        return x[0] < 5

    return lambda f: f(call_even, call_odd)


def cross_reentrancy_param_v3_rhs():
    is_even = [True]
    x = [0]

    def call_even():
        if is_even[0]:
            x[0] = x[0] + 1
        is_even[0] = False
        return True

    def call_odd():
        if is_even[0]:
            pass
        else:
            x[0] = x[0] + 1
        is_even[0] = True
        return True

    return lambda f: f(call_even, call_odd)

test_cross_reentrancy_param_v3 = make_function_equivalence_test(cross_reentrancy_param_v3_lhs, cross_reentrancy_param_v3_rhs, log_failure=True)
#test_cross_reentrancy_param_v3()