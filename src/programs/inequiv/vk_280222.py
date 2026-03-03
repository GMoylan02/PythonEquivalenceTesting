from src.FunctionEquivalence import make_function_equivalence_test


def vk_280222_lhs():
    x = [True]

    def program(f):
        y = x[0]
        f()
        if x[0] != y:
            raise Exception("_bot_")
        x[0] = not x[0]

    return program

def vk_280222_rhs():
    def program(f):
        f()
    return program

test_vk_280222 = make_function_equivalence_test(vk_280222_lhs, vk_280222_rhs, log_failure=True)