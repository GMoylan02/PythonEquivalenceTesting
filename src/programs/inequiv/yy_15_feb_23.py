from src.FunctionEquivalence import make_function_equivalence_test


def yy_15_feb_23_lhs(f):
    def inner_a(a):
        def inner_b(b):
            return f((b, a))
        return inner_b
    return inner_a


def yy_15_feb_23_rhs(f):
    def inner_a(a):
        def inner_b(b):
            return f((a, a))
        return inner_b
    return inner_a

test_yy_15_feb_23 = make_function_equivalence_test(yy_15_feb_23_lhs, yy_15_feb_23_rhs, log_failure=True)