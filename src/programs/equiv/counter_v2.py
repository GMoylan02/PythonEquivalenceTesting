from src.UniversalStrategy import make_function_equivalence_test


def counter_v2_lhs():
    c = [0]
    def count(): c[0] = c[0] + 1
    def get(): return c[0]
    return (count, get)


def counter_v2_rhs():
    c = [0]
    def count(): c[0] = c[0] - 2
    def get(): return -c[0] // 2
    return (count, get)

test_counter_v2 = make_function_equivalence_test(counter_v2_lhs, counter_v2_rhs, log_failure=True)
