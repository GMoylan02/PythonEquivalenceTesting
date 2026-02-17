from src.UniversalStrategy import make_function_equivalence_test


def rivcp_412_e_lhs():
    i = [0]

    def while_loop(cond):
        def run(command):
            if cond():
                command()
                while_loop(cond)(command)
        return run

    def program(sync):
        def cond():
            return i[0] <= 5

        def command():
            sync()
            i[0] = i[0] + 1

        while_loop(cond)(command)

    return program

def rivcp_412_e_rhs():
    i = [0]

    def while_loop(cond):
        def run(command):
            if cond():
                command()
                while_loop(cond)(command)
        return run

    def program(sync):
        def cond():
            return i[0] <= 6

        def command():
            sync()
            i[0] = i[0] + 1

        while_loop(cond)(command)

    return program

test_rivcp_412_e = make_function_equivalence_test(rivcp_412_e_lhs, rivcp_412_e_rhs, log_failure=True)