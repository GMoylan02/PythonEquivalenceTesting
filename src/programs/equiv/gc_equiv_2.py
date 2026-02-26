from src.UniversalStrategy import make_function_equivalence_test


def gc_equiv_2_lhs():
    f = [lambda: None]
    def outer():
        l = [None]
        f[0] = lambda: l[0]
        return f[0]()
    return outer


def gc_equiv_2_rhs():
    return lambda: None

test_gc_equiv_2 = make_function_equivalence_test(gc_equiv_2_lhs, gc_equiv_2_rhs, log_failure=True)
