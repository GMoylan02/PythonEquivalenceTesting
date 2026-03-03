from src.FunctionEquivalence import make_function_equivalence_test


def state_dependant_4_v2b_ineq_lhs():
    l1 = [False]
    l2 = [False]

    def program(f):
        def arg():
            if l1[0]:
                raise Exception("_bot_")
            else:
                l2[0] = True

        f(arg)

        if l2[0]:
            return True
        else:
            l1[0] = True
            return True

    return program

def state_dependant_4_v2b_ineq_rhs():
    def program(f):
        def arg():
            raise Exception("_bot_")

        f(arg)
        return True

    return program

test_state_dependant_4_v2b_ineq = make_function_equivalence_test(state_dependant_4_v2b_ineq_lhs, state_dependant_4_v2b_ineq_rhs, log_failure=True)