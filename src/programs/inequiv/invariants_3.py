from src.FunctionEquivalence import make_function_equivalence_test


def invariants_3_lhs():
    x = [0]

    def func(g):
        if (x[0] % 2) != 0:
            x[0] = 0
        x[0] = x[0] + 2
        g()
        if (x[0] % 2) == 0:
            x[0] = x[0] + 1
            return True
        else:
            return False

    return func


def invariants_3_rhs():
    def func(g):
        g()
        return True

    return func

test_invariants_3 = make_function_equivalence_test(invariants_3_lhs, invariants_3_rhs, log_failure=True)