from src.UniversalStrategy import make_function_equivalence_test


def fact_tail_rec_lhs(n):
    if n <= 1:
        return 1
    else:
        return n * fact_tail_rec_lhs(n - 1)


def fact_acc(n):
    def inner(acc):
        if n <= 1:
            return acc
        else:
            return fact_acc(n - 1)(n * acc)
    return inner

def fact_tail_rec_rhs(n):
    return fact_acc(n)(1)


test_fact_tail_rec = make_function_equivalence_test(fact_tail_rec_lhs, fact_tail_rec_rhs, log_failure=True)
