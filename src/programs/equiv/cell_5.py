from src.UniversalStrategy import make_function_equivalence_test


def cell_5_lhs():
    y = [0]
    def set(z): y[0] = z
    def get(): return y[0]
    return (set, get)


def cell_5_rhs():
    y1 = [0]
    y2 = [0]
    def set(z):
        if z % 2 == 0:
            y1[0] = z
        else:
            y1[0] = 1
            y2[0] = z
    def get():
        return y1[0] if y1[0] % 2 == 0 else y2[0]
    return (set, get)

test_cell_5 = make_function_equivalence_test(cell_5_lhs, cell_5_rhs, log_failure=True)