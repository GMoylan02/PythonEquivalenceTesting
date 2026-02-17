from src.UniversalStrategy import make_function_equivalence_test


def reve_nested_while_ineq_lhs(xg):
    x_val, g_val = xg
    x = [x_val]
    g = [g_val]
    i = [0]

    def outer_while(_=None):
        if i[0] < x[0]:
            i[0] = i[0] + 1
            g[0] = g[0] - 2
            g[0] = g[0] + 1

            def inner_while(_=None):
                if x[0] < i[0]:
                    x[0] = x[0] + 2
                    x[0] = x[0] - 1
                    g[0] = g[0] + 1
                    inner_while()

            inner_while()
            outer_while()

    outer_while()
    return g[0]


def reve_nested_while_ineq_rhs(xg):
    x_val, g_val = xg
    x = [x_val]
    g = [g_val]
    i = [0]

    def outer_while(_=None):
        if i[0] < x[0]:
            i[0] = i[0] + 1
            g[0] = g[0] - 2

            def inner_while(_=None):
                if x[0] < i[0]:
                    x[0] = x[0] + 1
                    g[0] = g[0] + 2
                    inner_while()

            inner_while()
            outer_while()

    outer_while()
    return g[0]

test_reve_nested_while_ineq = make_function_equivalence_test(reve_nested_while_ineq_lhs, reve_nested_while_ineq_rhs, log_failure=True)

