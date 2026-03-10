from src.FunctionEquivalence import make_function_equivalence_test

# possible only if we set MAX_TUPLE_CALLS to 100 in UniversalStrategy and
# get unreasonably lucky that the fuzzer draws even,odd in sequence 100 times
# this is not quite accurate, but if we assume a random fuzzer, the odds are
# 7.89 x 10^-31 or 1 in 1,267,650,600,228,229,401,496,703,205,376
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
#test_cross_reentrancy_param()