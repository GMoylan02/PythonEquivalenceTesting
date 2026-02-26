from src.UniversalStrategy import make_function_equivalence_test


def ho_sum_v3_lhs():
    x = [0]
    def outer(fr):
        f, r = fr
        if r > 0:
            x[0] = x[0] + r
        f()
        return x[0]
    return outer

def ho_sum_v3_rhs():
    x = [0]
    def outer(fr):
        f, r = fr
        if r > 0:
            x[0] = x[0] - r
        f()
        return -x[0]
    return outer

test_ho_sum_v3 = make_function_equivalence_test(ho_sum_v3_lhs, ho_sum_v3_rhs, log_failure=True)
