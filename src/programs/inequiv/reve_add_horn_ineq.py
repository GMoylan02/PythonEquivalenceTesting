from src.FunctionEquivalence import make_function_equivalence_test


def reve_add_horn_ineq_lhs(ij):
    i, j = ij
    r = 0
    if i == 0:
        r = j
    else:
        r = reve_add_horn_ineq_lhs((i - 1, j + 1))
    return r


def reve_add_horn_ineq_rhs(ij):
    i, j = ij
    r = 0
    if i == 0:
        r = j
    elif i == 1:
        r = j + 1
    elif i == 2:
        r = j
    else:
        r = reve_add_horn_ineq_rhs((i - 1, j + 1))
    return r

test_reve_add_horn_ineq = make_function_equivalence_test(reve_add_horn_ineq_lhs, reve_add_horn_ineq_rhs, log_failure=True)