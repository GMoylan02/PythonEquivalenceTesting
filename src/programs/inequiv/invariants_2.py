from src.UniversalStrategy import make_function_equivalence_test


def invariants_2_lhs():
    x = [0]

    def func(g):
        if (x[0] % 2) != 0:
            x[0] = 0
        x[0] = x[0] + 2
        g()
        if (x[0] % 2) == 0:
            x[0] = x[0] + 1
        else:
            raise Exception("_bot_")

    return func

def invariants_2_rhs():
    def func(g):
        g()

    return func

test_invariants_2 = make_function_equivalence_test(invariants_2_lhs, invariants_2_rhs, log_failure=True)