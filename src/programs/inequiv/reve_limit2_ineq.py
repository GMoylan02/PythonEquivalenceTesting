from src.UniversalStrategy import make_function_equivalence_test


def reve_limit2_ineq_lhs(n):
    r = 0
    if n <= 0:
        r = n
    else:
        r = reve_limit2_ineq_lhs(n - 1)
        r = n + r
    return r


def reve_limit2_ineq_rhs(n):
    r = 0
    if n <= 1:
        r = n
    else:
        r = reve_limit2_ineq_rhs(n - 1)
        r = n + r
        if n == 10:
            r = 10
    return r

test_reve_limit2_ineq = make_function_equivalence_test(reve_limit2_ineq_lhs, reve_limit2_ineq_rhs, log_failure=True)
