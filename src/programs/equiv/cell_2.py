from src.UniversalStrategy import make_function_equivalence_test


def cell_2_lhs():
    y = [0]
    def set(z): y[0] = z
    def get(): return y[0]
    return (set, get)


def cell_2_rhs():
    y1 = [0]
    y2 = [0]
    p = [True]
    def set(z):
        p[0] = not p[0]
        if p[0]:
            y1[0] = z
        else:
            y2[0] = z
    def get():
        return y1[0] if p[0] else y2[0]
    return (set, get)

test_cell_2 = make_function_equivalence_test(cell_2_lhs, cell_2_rhs, log_failure=True)