from src.UniversalStrategy import make_function_equivalence_test


def make_lhs():
    c = [(0, 0)]
    def count():
        x1, x2 = c[0]
        c[0] = (x1, x2 + 1)
    def get():
        x1, x2 = c[0]
        return x2
    return (count, get)


def make_rhs():
    c = [0]
    def count(): c[0] = c[0] - 1
    def get(): return -c[0]
    return (count, get)


test_counter = make_function_equivalence_test(make_lhs, make_rhs, log_failure=True)
