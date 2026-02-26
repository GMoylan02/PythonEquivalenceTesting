from src.UniversalStrategy import make_function_equivalence_test


def hector_pitts_stark_lhs():
    c = [0]
    def outer(f):
        c[0] = 1
        f()
        return c[0]
    return outer


def hector_pitts_stark_rhs():
    def outer(f):
        f()
        return 1
    return outer

test_hector_pitts_stark = make_function_equivalence_test(hector_pitts_stark_lhs, hector_pitts_stark_rhs, log_failure=True)