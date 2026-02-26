from src.UniversalStrategy import make_function_equivalence_test


def cell_ho_lhs():
    y = [lambda x: x + 1]
    def set(z): y[0] = z
    def get(): return y[0]
    return (set, get)


def cell_ho_rhs():
    y1 = [lambda x: x + 1]
    y2 = [lambda x: x + 1]
    p = [True]
    def set(z):
        p[0] = not p[0]
        y1[0] = z
        y2[0] = z
    def get():
        return y1[0] if p[0] else y2[0]
    return (set, get)

test_cell_ho = make_function_equivalence_test(cell_ho_lhs, cell_ho_rhs, log_failure=True)