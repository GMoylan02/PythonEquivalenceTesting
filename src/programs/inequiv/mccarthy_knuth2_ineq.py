from src.FunctionEquivalence import make_function_equivalence_test


def mccarthy_knuth2_ineq_lhs(n):
    if n > 100:
        return n - 10
    else:
        return mccarthy_knuth2_ineq_lhs(mccarthy_knuth2_ineq_lhs(n + 11))


def mccarthy_knuth2_ineq_rhs(n):
    if n > 100:
        return n - 10
    else:
        return mccarthy_knuth2_ineq_rhs(n + 2)

test_mccarthy_knuth2_ineq = make_function_equivalence_test(mccarthy_knuth2_ineq_lhs, mccarthy_knuth2_ineq_rhs, log_failure=True)
