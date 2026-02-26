from src.UniversalStrategy import make_function_equivalence_test


def hector_bsort_isort_CN10_one_steps_lhs(args):
    compare = args[0]
    read_x = args[1][0]
    write_x = args[1][1]
    length = 10
    a = [[0,0,0,0,0,0,0,0,0,0]]

    def a_get(n):
        a0,a1,a2,a3,a4,a5,a6,a7,a8,a9 = a[0]
        if n == 0: return a0
        if n == 1: return a1
        if n == 2: return a2
        if n == 3: return a3
        if n == 4: return a4
        if n == 5: return a5
        if n == 6: return a6
        if n == 7: return a7
        if n == 8: return a8
        if n == 9: return a9
        return -1

    def a_set(n):
        def inner(m):
            a0,a1,a2,a3,a4,a5,a6,a7,a8,a9 = a[0]
            if n == 0: a[0] = (m,a1,a2,a3,a4,a5,a6,a7,a8,a9)
            elif n == 1: a[0] = (a0,m,a2,a3,a4,a5,a6,a7,a8,a9)
            elif n == 2: a[0] = (a0,a1,m,a3,a4,a5,a6,a7,a8,a9)
            elif n == 3: a[0] = (a0,a1,a2,m,a4,a5,a6,a7,a8,a9)
            elif n == 4: a[0] = (a0,a1,a2,a3,m,a5,a6,a7,a8,a9)
            elif n == 5: a[0] = (a0,a1,a2,a3,a4,m,a6,a7,a8,a9)
            elif n == 6: a[0] = (a0,a1,a2,a3,a4,a5,m,a7,a8,a9)
            elif n == 7: a[0] = (a0,a1,a2,a3,a4,a5,a6,m,a8,a9)
            elif n == 8: a[0] = (a0,a1,a2,a3,a4,a5,a6,a7,m,a9)
            elif n == 9: a[0] = (a0,a1,a2,a3,a4,a5,a6,a7,a8,m)
        return inner

    i = [0]

    def while1():
        if i[0] < length:
            a_set(i[0])(read_x())
            i[0] += 1
            while1()

    while1()

    flag = [1]

    def while2():
        if flag[0] == 1:
            i[0] = 0
            flag[0] = 0
            def while3():
                if i[0] < length - 1:
                    if compare(a_get(i[0]))(a_get(i[0] + 1)):
                        temp = [0]
                        flag[0] = 1
                        temp[0] = a_get(i[0])
                        a_set(i[0])(a_get(i[0] + 1))
                        a_set(i[0] + 1)(temp[0])
                    i[0] += 1
                    while3()
            while3()
            while2()

    while2()

    i[0] = 0

    def while4():
        if i[0] < length:
            write_x(a_get(i[0]))
            i[0] += 1
            while4()

    while4()


def hector_bsort_isort_CN10_one_steps_rhs(args):
    compare = args[0]
    read_x = args[1][0]
    write_x = args[1][1]
    length = 10
    a = [[0,0,0,0,0,0,0,0,0,0]]

    def a_get(n):
        a0,a1,a2,a3,a4,a5,a6,a7,a8,a9 = a[0]
        if n == 0: return a0
        if n == 1: return a1
        if n == 2: return a2
        if n == 3: return a3
        if n == 4: return a4
        if n == 5: return a5
        if n == 6: return a6
        if n == 7: return a7
        if n == 8: return a8
        if n == 9: return a9
        return -1

    def a_set(n):
        def inner(m):
            a0,a1,a2,a3,a4,a5,a6,a7,a8,a9 = a[0]
            if n == 0: a[0] = (m,a1,a2,a3,a4,a5,a6,a7,a8,a9)
            elif n == 1: a[0] = (a0,m,a2,a3,a4,a5,a6,a7,a8,a9)
            elif n == 2: a[0] = (a0,a1,m,a3,a4,a5,a6,a7,a8,a9)
            elif n == 3: a[0] = (a0,a1,a2,m,a4,a5,a6,a7,a8,a9)
            elif n == 4: a[0] = (a0,a1,a2,a3,m,a5,a6,a7,a8,a9)
            elif n == 5: a[0] = (a0,a1,a2,a3,a4,m,a6,a7,a8,a9)
            elif n == 6: a[0] = (a0,a1,a2,a3,a4,a5,m,a7,a8,a9)
            elif n == 7: a[0] = (a0,a1,a2,a3,a4,a5,a6,m,a8,a9)
            elif n == 8: a[0] = (a0,a1,a2,a3,a4,a5,a6,a7,m,a9)
            elif n == 9: a[0] = (a0,a1,a2,a3,a4,a5,a6,a7,a8,m)
        return inner

    i = [0]

    def while1():
        if i[0] < length:
            a_set(i[0])(read_x())
            i[0] += 1
            while1()

    while1()

    i[0] = 1

    def while2():
        if i[0] < length:
            val = [0]
            j = [0]
            val[0] = a_get(i[0])
            j[0] = i[0]
            def while3():
                if j[0] > 0 and compare(a_get(j[0] - 1))(val[0]):
                    a_set(j[0])(a_get(j[0] - 1))
                    j[0] -= 1
                    while3()
            while3()
            a_set(j[0])(val[0])
            i[0] += 1
            while2()

    while2()

    i[0] = 0

    def while4():
        if i[0] < length:
            write_x(a_get(i[0]))
            i[0] += 1
            while4()

    while4()

test_hector_bsort_isort_CN10_one_steps = make_function_equivalence_test(hector_bsort_isort_CN10_one_steps_lhs, hector_bsort_isort_CN10_one_steps_rhs, log_failure=True)