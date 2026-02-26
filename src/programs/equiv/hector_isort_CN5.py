from src.UniversalStrategy import make_function_equivalence_test


def hector_isort_CN5_lhs(read_x):
    a = [(0, 0, 0, 0, 0)]

    def a_get(n):
        a0, a1, a2, a3, a4 = a[0]
        if n == 0: return a0
        if n == 1: return a1
        if n == 2: return a2
        if n == 3: return a3
        if n == 4: return a4
        return -1

    def a_set(n):
        def inner(m):
            a0, a1, a2, a3, a4 = a[0]
            if n == 0: a[0] = (m, a1, a2, a3, a4)
            elif n == 1: a[0] = (a0, m, a2, a3, a4)
            elif n == 2: a[0] = (a0, a1, m, a3, a4)
            elif n == 3: a[0] = (a0, a1, a2, m, a4)
            elif n == 4: a[0] = (a0, a1, a2, a3, m)
        return inner

    i = [0]

    def while1():
        if i[0] < 5:
            a_set(i[0])(read_x())
            i[0] += 1
            while1()

    while1()

    i[0] = 1

    def while2():
        if i[0] < 5:
            val = [0]
            j = [0]
            val[0] = a_get(i[0])
            j[0] = i[0]
            def while3():
                if j[0] > 0 and a_get(j[0] - 1) > val[0]:
                    a_set(j[0])(a_get(j[0] - 1))
                    j[0] -= 1
                    while3()
            while3()
            a_set(j[0])(val[0])
            i[0] += 1
            while2()

    while2()

    i[0] = 0
    res = [True]

    def while4():
        if i[0] < 4:
            res[0] = res[0] and (a_get(i[0]) <= a_get(i[0] + 1))
            i[0] += 1
            while4()

    while4()
    return res[0]


def hector_isort_CN5_rhs(read_x):
    i = [0]

    def while1():
        if i[0] < 5:
            m = read_x()
            i[0] += 1
            while1()

    while1()
    return True

test_hector_isort_CN5 = make_function_equivalence_test(hector_isort_CN5_lhs, hector_isort_CN5_rhs, log_failure=True)
