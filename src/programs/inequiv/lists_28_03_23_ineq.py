from src.FunctionEquivalence import make_function_equivalence_test


def lists_28_03_23_ineq_lhs(l):
    def inner(f):
        if l == []:
            return f([])
        else:
            x = l[0]
            xs = l[1:]
            return f(xs)
    return inner


def lists_28_03_23_ineq_rhs(l):
    def inner(f):
        return f(l)
    return inner

test_lists_28_03_23_ineq = make_function_equivalence_test(lists_28_03_23_ineq_lhs, lists_28_03_23_ineq_rhs, log_failure=True)
#test_lists_28_03_23_ineq()