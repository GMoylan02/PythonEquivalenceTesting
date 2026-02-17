from src.UniversalStrategy import make_function_equivalence_test


def stateful_args_ineq_lhs():
    x = [0]

    def program(f):
        def arg():
            x[0] = x[0] + 1

        f(arg)

        if x[0] == 2:
            return True
        else:
            return False

    return program

def stateful_args_ineq_rhs():
    x = [0]

    def program(f):
        def arg():
            x[0] = x[0] - 1

        f(arg)

        if x[0] == 2:
            return True
        else:
            return False

    return program

test_stateful_args_ineq = make_function_equivalence_test(stateful_args_ineq_lhs, stateful_args_ineq_rhs, log_failure=True)