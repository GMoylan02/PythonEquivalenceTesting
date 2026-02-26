from src.UniversalStrategy import make_function_equivalence_test


def hector_thamsborg_lhs():
    c = [0]
    def outer(f):
        c[0] = 0
        f()
        c[0] = 1
        f()
        return c[0]
    return outer



def hector_thamsborg_rhs():
    def outer(f):
        f()
        f()
        return 1
    return outer

test_hector_thamsborg = make_function_equivalence_test(hector_thamsborg_lhs, hector_thamsborg_rhs, log_failure=True)