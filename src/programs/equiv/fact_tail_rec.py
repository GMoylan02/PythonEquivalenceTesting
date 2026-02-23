from src.UniversalStrategy import make_function_equivalence_test


def make_lhs():
    def fact(n):
        if n <= 1:
            return 1
        else:
            return n * fact(n - 1)
    return fact

fact_lhs = make_lhs()


def make_rhs():
    def fact_acc(n):
        def inner(acc):
            if n <= 1:
                return acc
            else:
                return fact_acc(n - 1)(n * acc)
        return inner
    fact = lambda n: fact_acc(n)(1)
    return fact

fact_rhs = make_rhs()

test_fact_tail_rec = make_function_equivalence_test(make_lhs, make_rhs, log_failure=True)
