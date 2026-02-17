from src.UniversalStrategy import make_function_equivalence_test


def yy_17_feb_23_2_lhs(f):
    def inner_ab(ab):
        def inner_c(c):
            a, b = ab
            if a == []:
                return f([c] + a)
            else:
                x, *xs = a
                return f([])
        return inner_c
    return inner_ab


def yy_17_feb_23_2_rhs(f):
    def inner_ab(ab):
        def inner_c(c):
            a, b = ab
            if b == []:
                return f([c] + b)
            else:
                x, *xs = b
                return f([])
        return inner_c
    return inner_ab

test_yy_17_feb_23_2 = make_function_equivalence_test(yy_17_feb_23_2_lhs, yy_17_feb_23_2_rhs, log_failure=True)