from src.UniversalStrategy import make_function_equivalence_test


def symb_const_3_1_lhs(a):
    def inner(b):
        return a == b
    return inner

def symb_const_3_1_rhs(a):
    def inner(b):
        return True
    return inner

test_symb_const_3_1 = make_function_equivalence_test(symb_const_3_1_lhs, symb_const_3_1_rhs, log_failure=True)