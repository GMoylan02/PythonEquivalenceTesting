from src.UniversalStrategy import make_function_equivalence_test


def vk_Oct9_1520_lhs(f, xy):
    x, y = xy
    if y <= 0:
        return 0
    else:
        return x + f((x, y - 1))

def f(xy):
    return vk_Oct9_1520_lhs(f, xy)



def vk_Oct9_1520_rhs(xy):
    x, y = xy
    if x <= 0:
        return 0
    else:
        return x * y

# this is a weird case. it is easy to instantly reject lhs and rhs for differing arities. if we define some f as
# i have done above, and curry lhs then there exist inputs for which these are equivalent, but it is still very easy
# to find an inequivalence
test_vk_Oct9_1520 = make_function_equivalence_test(f, vk_Oct9_1520_rhs, log_failure=True)