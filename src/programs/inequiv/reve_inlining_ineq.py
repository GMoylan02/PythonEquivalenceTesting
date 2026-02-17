from src.UniversalStrategy import make_function_equivalence_test


def reve_inlining_ineq_lhs(x):
    r = x
    if x > 0:
        r = reve_inlining_ineq_lhs(x - 1)
        r = r + 1
    if x < 0:
        r = 0
    return r


def reve_inlining_ineq_rhs(x):
    r = x
    if x > 1:
        r = reve_inlining_ineq_rhs(x - 2)
        r = r + 2
    if x < 2:
        r = 0
    return r

test_reve_inlining_ineq = make_function_equivalence_test(reve_inlining_ineq_lhs, reve_inlining_ineq_rhs, log_failure=True)
