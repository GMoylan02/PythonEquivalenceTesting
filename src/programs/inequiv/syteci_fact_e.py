from src.FunctionEquivalence import make_function_equivalence_test


#def syteci_fact_e_lhs(n: int):
def syteci_fact_e_lhs(n):
    if n <= 1:
        return 1
    else:
        return n * syteci_fact_e_lhs(n - 1)


#def syteci_fact_e_rhs(n: int):
def syteci_fact_e_rhs(n):
    def aux(m):
        def inner(acc):
            if m < 0:
                return acc
            else:
                return aux(m - 1)(m * acc)
        return inner
    return aux(n)(1)



test_syteci_face_e = make_function_equivalence_test(syteci_fact_e_lhs, syteci_fact_e_rhs, log_failure=True)
