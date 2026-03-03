from src.FunctionEquivalence import make_function_equivalence_test


def yy_1_apr_23_1_lhs(l1):
    def eq(l1):
        if l1 == []:
            def inner(l2):
                if l2 == []:
                    return True
                else:
                    return False

            return inner
        else:
            x, *xs = l1

            def inner(l2):
                if l2 == []:
                    return False
                else:
                    y, *ys = l2
                    return (x == y) and eq(xs)(ys)

            return inner
    def inner(l2):
        if eq(l1)(l2):
            return 42
        else:
            return 0
    return inner


def yy_1_apr_23_1_rhs(l1):
    def inner(l2):
        return 0
    return inner

test_yy_1_apr_23_1 = make_function_equivalence_test(yy_1_apr_23_1_lhs, yy_1_apr_23_1_rhs, log_failure=True)