from src.FunctionEquivalence import make_function_equivalence_test


def ex3_5_e_ineq_lhs():
    v2 = lambda: True
    return v2

def ex3_5_e_ineq_rhs():
    flag = [True]

    def v2():
        if flag[0]:
            flag[0] = False
            return True
        else:
            return False

    return v2

test_ex3_5_e_ineq = make_function_equivalence_test(ex3_5_e_ineq_lhs, ex3_5_e_ineq_rhs, log_failure=True)
#test_ex3_5_e_ineq()