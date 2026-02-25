from src.UniversalStrategy import make_function_equivalence_test

#def reve_ackermann_ineq_lhs(mn: tuple[int, int]):
def reve_ackermann_ineq_lhs(mn):
    m, n = mn
    r = 0
    x = 0
    if m == 0:
        r = n + 1
    elif m > 0 and n == 0:
        r = reve_ackermann_ineq_lhs((m - 1, 1))
    else:
        x = reve_ackermann_ineq_lhs((m, n - 1))
        r = reve_ackermann_ineq_lhs((m - 1, x))
    return r


#def reve_ackermann_ineq_rhs(mn: tuple[int, int]):
def reve_ackermann_ineq_rhs(mn):
    m, n = mn
    r = 0
    x = 0
    if m > 0 and n == 0:
        r = reve_ackermann_ineq_rhs((m - 1, 1))
    elif m == 1:
        r = n + 1
    else:
        x = reve_ackermann_ineq_rhs((m, n - 1))
        r = reve_ackermann_ineq_rhs((m - 1, x))
    return r

test_reve_ackermann_ineq = make_function_equivalence_test(reve_ackermann_ineq_lhs, reve_ackermann_ineq_rhs, log_failure=True)
