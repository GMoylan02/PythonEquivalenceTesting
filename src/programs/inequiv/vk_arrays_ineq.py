from src.FunctionEquivalence import make_function_equivalence_test


def vk_arrays_ineq_lhs(ar):
    def inner(i):
        if 0 <= i:
            if i < 10:
                return ar(i)
            else:
                return 0
        else:
            return 0
    return inner

def vk_arrays_ineq_rhs(ar):
    def rev(ar):
        def inner(i):
            if 0 <= i:
                if i < 10:
                    return ar(10 - i)
                else:
                    return 0
            else:
                return 0

        return inner
    return rev(rev(ar))


test_vk_arrays_ineq = make_function_equivalence_test(vk_arrays_ineq_lhs, vk_arrays_ineq_rhs, log_failure=True)