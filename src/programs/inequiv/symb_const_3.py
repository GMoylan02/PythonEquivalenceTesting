from src.UniversalStrategy import make_function_equivalence_test


def symb_const_3_lhs(ab):
    a, b = ab
    return a == b


def symb_const_3_rhs(ab):
    return True

test_symb_const_3 = make_function_equivalence_test(symb_const_3_lhs, symb_const_3_rhs, log_failure=True)