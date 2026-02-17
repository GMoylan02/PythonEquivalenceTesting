from src.UniversalStrategy import make_function_equivalence_test


def vk_Aug10_1755_lhs(a):
    l = [0]

    def inner(b):
        if b():
            a()
            l[0] = l[0] - 1
        else:
            a()
            l[0] = l[0] + 1
        return l[0] == 0

    return inner


def vk_Aug10_1755_rhs(a):
    l = [0]

    def inner(b):
        if b():
            l[0] = l[0] - 1
            a()
        else:
            l[0] = l[0] + 1
            a()
        return l[0] == 0

    return inner

test_vk_Aug10_1755 = make_function_equivalence_test(vk_Aug10_1755_lhs, vk_Aug10_1755_rhs, log_failure=True)