from src.FunctionEquivalence import make_function_equivalence_test


def vk_280222_2_lhs():
    x = [True]

    def program(f):
        y = x[0]
        f()
        if x[0] != y:
            raise Exception("_bot_")
        x[0] = False
        f()
        x[0] = True

    return program

def vk_280222_2_rhs():
    def program(f):
        f()
        f()
    return program

test_vk_280222_2 = make_function_equivalence_test(vk_280222_2_lhs, vk_280222_2_rhs, log_failure=True)