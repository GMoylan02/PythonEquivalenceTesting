from src.UniversalStrategy import make_function_equivalence_test


def mccarthy_ineq_lhs(n):
    if n < 0:
        raise RuntimeError()
    elif n > 100:
        return n - 10
    else:
        return mccarthy_ineq_lhs(mccarthy_ineq_lhs(n + 12))


def mccarthy_ineq_rhs(n):
    if n < 0:
        raise RuntimeError()
    elif n > 100:
        return n - 10
    else:
        return 91

test_mccarthy_ineq = make_function_equivalence_test(mccarthy_ineq_lhs, mccarthy_ineq_rhs, log_failure=True)
