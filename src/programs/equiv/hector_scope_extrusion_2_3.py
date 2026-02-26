from src.UniversalStrategy import make_function_equivalence_test


def hector_scope_extrusion_2_3_lhs(f):
    return f(lambda y: y)


def hector_scope_extrusion_2_3_rhs(f):
    def inner(y):
        x = [0]
        if x[0] == 0:
            x[0] = y
        else:
            x[0] = y - 1
        return x[0]
    return f(inner)

test_hector_scope_extrusion_2_3 = make_function_equivalence_test(hector_scope_extrusion_2_3_lhs, hector_scope_extrusion_2_3_rhs, log_failure=True)
