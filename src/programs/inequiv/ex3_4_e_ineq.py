from typing import Callable

from src.FunctionEquivalence import make_function_equivalence_test


def ex3_4_e_ineq_lhs():
    #def v1(f: Callable):
    def v1(f):
        f()
        return True
    #v1 = lambda f: (f(), True)[1]
    return v1


def ex3_4_e_ineq_rhs():
    flag = [True]

    #def v1(f: Callable):
    def v1(f):
        if flag[0]:
            flag[0] = False
            f()
            flag[0] = True
            return True
        else:
            f()
            return False

    return v1

test_ex3_4_e_ineq = make_function_equivalence_test(ex3_4_e_ineq_lhs, ex3_4_e_ineq_rhs, log_failure=True)
#test_ex3_4_e_ineq()