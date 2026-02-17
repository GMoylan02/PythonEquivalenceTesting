from src.UniversalStrategy import make_function_equivalence_test


def state_dependant_3_ineq_lhs():
    x = [0]

    def ho_inc(f):
        f()
        x[0] = x[0] + 1

    def get():
        return x[0]

    return ho_inc, get

def state_dependant_3_ineq_rhs():
    x = [0]

    def ho_inc(f):
        n = x[0]
        f()
        x[0] = n + 1

    def get():
        return x[0]

    return ho_inc, get

test_state_dependant_3_ineq = make_function_equivalence_test(state_dependant_3_ineq_lhs, state_dependant_3_ineq_rhs, log_failure=True)