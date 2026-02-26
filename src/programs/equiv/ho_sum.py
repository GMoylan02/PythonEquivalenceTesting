from src.UniversalStrategy import make_function_equivalence_test


def ho_sum_lhs():
    x = [0]
    def outer(f):
        r = f()
        if r > 0:
            x[0] = x[0] + r
        return x[0]
    return outer


def ho_sum_rhs():
    x = [0]
    def outer(f):
        r = f()
        if r > 0:
            x[0] = x[0] - r
        return -x[0]
    return outer

test_ho_sum = make_function_equivalence_test(ho_sum_lhs, ho_sum_rhs, log_failure=True)

