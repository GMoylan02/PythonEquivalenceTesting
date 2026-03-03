from src.FunctionEquivalence import make_function_equivalence_test


def invariants_4_lhs():
    x = [0]

    def func(g):
        x[0] = x[0] + 1
        if x[0] > 10:
            x[0] = 0
        g()
        if x[0] <= 20:
            x[0] = x[0] + 1
        else:
            raise Exception("_bot_")

    return func


def invariants_4_rhs():
    def func(g):
        g()

    return func

test_invariants_4 = make_function_equivalence_test(invariants_4_lhs, invariants_4_rhs, log_failure=True)