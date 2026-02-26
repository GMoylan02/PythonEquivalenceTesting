from src.UniversalStrategy import make_function_equivalence_test


def ho_sum_v2_lhs():
    x = [0]
    r = [0]
    def outer(f):
        r[0] = f()
        def while_loop():
            if r[0] > 0:
                x[0] = x[0] + r[0]
                r[0] = f()
                while_loop()
        while_loop()
        return x[0]
    return outer

def ho_sum_v2_rhs():
    x = [0]
    r = [0]
    def outer(f):
        r[0] = f()
        def while_loop():
            if r[0] > 0:
                x[0] = x[0] - r[0]
                r[0] = f()
                while_loop()
        while_loop()
        return -x[0]
    return outer


test_ho_sum_v2 = make_function_equivalence_test(ho_sum_v2_lhs, ho_sum_v2_rhs, log_failure=True)