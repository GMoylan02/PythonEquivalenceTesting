from src.UniversalStrategy import make_function_equivalence_test


def mk_cell_lhs(x):
    y = [x]
    def set(z): y[0] = z
    def get(): return y[0]
    return (set, get)


def mk_cell_rhs(x):
    y1 = [x]
    y2 = [x]
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

test_cell_3 = make_function_equivalence_test(mk_cell_lhs, mk_cell_rhs, log_failure=True)
