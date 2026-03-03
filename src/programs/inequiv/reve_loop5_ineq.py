from src.FunctionEquivalence import make_function_equivalence_test


def reve_loop5_ineq_lhs(n):
    i = [0]
    j = [0]

    def while_loop(_=None):
        if i[0] < n + n:
            j[0] = j[0] + 1
            i[0] = i[0] + 1
            while_loop()

    while_loop()
    return j[0]

def reve_loop5_ineq_rhs(n):
    i = [n + 1]
    j = [0]

    def while_loop(_=None):
        if i[0] > 0:
            j[0] = j[0] + 2
            i[0] = i[0] - 1
            while_loop()

    while_loop()
    return j[0]

test_reve_loop5_ineq = make_function_equivalence_test(reve_loop5_ineq_lhs, reve_loop5_ineq_rhs, log_failure=True)




