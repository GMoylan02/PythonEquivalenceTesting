from typing import Callable

from src.FunctionEquivalence import make_function_equivalence_test


def hector_bsort_isort_CNE_lhs():
    #def func(args: tuple[Callable, Callable, Callable, Callable, Callable]):
    def func(args):
        compare, write_x, length, a_get, a_set = args
        i = [0]
        flag = [1]

        def while2():
            if flag[0] == 1:
                i[0] = 0
                flag[0] = 0

                def while3():
                    if i[0] < length - 1:
                        if compare(a_get(i[0]), a_get(i[0] + 1)):
                            temp = [0]
                            flag[0] = 1
                            temp[0] = a_get(i[0])
                            a_set(i[0], a_get(i[0] + 1))
                            a_set(i[0] + 1, temp[0])
                        i[0] = i[0] + 1
                        while3()

                while3()
                while2()

        while2()
        i[0] = 0

        def while4():
            if i[0] < length:
                write_x(a_get(i[0]))
                i[0] = i[0] + 1
                while4()

        while4()

    return func


def hector_bsort_isort_CNE_rhs():
    #def func(args: tuple[Callable, Callable, Callable, Callable, Callable]):
    def func(args):
        compare, write_x, length, a_get, a_set = args
        i = [0]
        i[0] = 1

        def while2():
            if i[0] < length:
                val = [0]
                j = [0]
                val[0] = a_get(i[0])
                j[0] = i[0]

                def while3():
                    if j[0] > 0 and compare(a_get(j[0] - 1), val[0]):
                        a_set(j[0], a_get(j[0] - 1))
                        j[0] = j[0] - 1
                        while3()

                while3()
                a_set(j[0], val[0])
                i[0] = i[0] + 1
                while2()

        while2()
        i[0] = 0

        def while4():
            if i[0] < length:
                write_x(a_get(i[0]))
                i[0] = i[0] + 1
                while4()

        while4()

    return func

test_hector_bsort_isort_CNE = make_function_equivalence_test(hector_bsort_isort_CNE_lhs, hector_bsort_isort_CNE_rhs, log_failure=True)
#test_hector_bsort_isort_CNE()