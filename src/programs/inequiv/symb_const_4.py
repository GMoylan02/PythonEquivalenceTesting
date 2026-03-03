from src.FunctionEquivalence import make_function_equivalence_test


def symb_const_4_lhs(ab):
    a, b = ab
    p = [a == b]

    def inner(c):
        if c:
            return p[0]
        else:
            return p[0]

    return inner


def symb_const_4_rhs(ab):
    def inner(c):
        return True

    return inner

test_symb_const_4 = make_function_equivalence_test(symb_const_4_lhs, symb_const_4_rhs, log_failure=True)