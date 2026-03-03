from typing import Callable

from src.FunctionEquivalence import make_function_equivalence_test


def hector_bsort_isort_CN2_lhs():
    #def func(args: tuple[Callable, Callable, Callable]):
    def func(args):
        compare = args[0]
        read_x = args[1][0]
        write_x = args[1][1]
        a = [[0, 0]]

        def a_get(n):
            a0, a1 = a[0]
            if n == 0:
                return a0
            elif n == 1:
                return a1
            else:
                return -1

        def a_set(n, m):
            a0, a1 = a[0]
            if n == 0:
                a[0] = (m, a1)
            elif n == 1:
                a[0] = (a0, m)

        i = [0]

        def while1():
            if i[0] < 2:
                a_set(i[0], read_x())
                i[0] = i[0] + 1
                while1()

        while1()
        flag = [1]

        def while2():
            if flag[0] == 1:
                i[0] = 0
                flag[0] = 0

                def while3():
                    if i[0] < 1:
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
            if i[0] < 2:
                write_x(a_get(i[0]))
                i[0] = i[0] + 1
                while4()

        while4()

    return func


def hector_bsort_isort_CN2_rhs():
    #def func(args: tuple[Callable, Callable, Callable]):
    def func(args):
        compare = args[0]
        read_x = args[1][0]
        write_x = args[1][1]
        a = [[0, 0]]

        def a_get(n):
            a0, a1 = a[0]
            if n == 0:
                return a0
            elif n == 1:
                return a1
            else:
                return -1

        def a_set(n, m):
            a0, a1 = a[0]
            if n == 0:
                a[0] = (m, a1)
            elif n == 1:
                a[0] = (a0, m)

        i = [0]

        def while1():
            if i[0] < 2:
                a_set(i[0], read_x())
                i[0] = i[0] + 1
                while1()

        while1()
        i[0] = 1

        def while2():
            if i[0] < 2:
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
            if i[0] < 2:
                write_x(a_get(i[0]))
                i[0] = i[0] + 1
                while4()

        while4()

    return func

test_hector_bsort_isort_CN2 = make_function_equivalence_test(hector_bsort_isort_CN2_lhs, hector_bsort_isort_CN2_rhs, log_failure=True)