from src.UniversalStrategy import make_function_equivalence_test


def make_lhs():
    y = [0]
    def set(z): y[0] = z
    def get(): return y[0]
    return (set, get)


def make_rhs():
    y1 = [0]
    y2 = [0]
    p = [0]
    def set1(z):
        p[0] = p[0] + 1
        if p[0] % 2 == 0:
            y1[0] = z
        else:
            y2[0] = z
    def get1():
        return y1[0] if p[0] % 2 == 0 else y2[0]
    return (set1, get1)

test_cell_4 = make_function_equivalence_test(make_lhs, make_rhs, log_failure=True)