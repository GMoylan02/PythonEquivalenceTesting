from src.UniversalStrategy import make_function_equivalence_test


def reve_limit1_ineq_lhs(n):
    r = 0
    if n <= 1:
        r = n
    else:
        r = reve_limit1_ineq_lhs(n - 1)
        r = n + r
    return r


def reve_limit1_ineq_rhs(n):
    r = 0
    if n <= 1:
        r = n
    else:
        r = reve_limit1_ineq_rhs(n - 3)
        r = n + (n - 1) + r
    return r

test_reve_limit1_ineq = make_function_equivalence_test(reve_limit1_ineq_lhs, reve_limit1_ineq_rhs, log_failure=True)
