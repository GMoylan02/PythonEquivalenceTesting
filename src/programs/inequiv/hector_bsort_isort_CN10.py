from ..Ref import Ref


def hector_bsort_isort_CN10_lhs(args):
    compare = args[0]
    read_x = args[1][0]
    write_x = args[1][1]

    length = 10

    a = Ref((0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    def a_get(n):
        (a0,a1,a2,a3,a4,a5,a6,a7,a8,a9) = a.v
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
        def setter(m):
            (a0,a1,a2,a3,a4,a5,a6,a7,a8,a9) = a.v
            if n == 0: a.v = (m,a1,a2,a3,a4,a5,a6,a7,a8,a9)
            elif n == 1: a.v = (a0,m,a2,a3,a4,a5,a6,a7,a8,a9)
            elif n == 2: a.v = (a0,a1,m,a3,a4,a5,a6,a7,a8,a9)
            elif n == 3: a.v = (a0,a1,a2,m,a4,a5,a6,a7,a8,a9)
            elif n == 4: a.v = (a0,a1,a2,a3,m,a5,a6,a7,a8,a9)
            elif n == 5: a.v = (a0,a1,a2,a3,a4,m,a6,a7,a8,a9)
            elif n == 6: a.v = (a0,a1,a2,a3,a4,a5,m,a7,a8,a9)
            elif n == 7: a.v = (a0,a1,a2,a3,a4,a5,a6,m,a8,a9)
            elif n == 8: a.v = (a0,a1,a2,a3,a4,a5,a6,a7,m,a9)
            elif n == 9: a.v = (a0,a1,a2,a3,a4,a5,a6,a7,a8,m)
        return setter

    i = Ref(0)

    def while1():
        if i.v < length:
            a_set(i.v)(read_x())
            i.v = i.v + 1
            while1()

    while1()

    flag = Ref(1)

    def while2():
        if flag.v == 1:
            i.v = 0
            flag.v = 0

            def while3():
                if i.v < length - 1:
                    if compare(a_get(i.v), a_get(i.v + 1)):
                        temp = Ref(0)
                        flag.v = 1
                        temp.v = a_get(i.v)
                        a_set(i.v)(a_get(i.v + 1))
                        a_set(i.v + 1)(temp.v)
                    i.v = i.v + 1
                    while3()

            while3()
            while2()

    while2()

    i.v = 0

    def while4():
        if i.v < length:
            write_x(a_get(i.v))
            i.v = i.v + 1
            while4()

    while4()


def hector_bsort_isort_CN10_rhs(args):
    compare = args[0]
    read_x = args[1][0]
    write_x = args[1][1]

    length = 10

    a = Ref((0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    def a_get(n):
        (a0,a1,a2,a3,a4,a5,a6,a7,a8,a9) = a.v
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
        def setter(m):
            (a0,a1,a2,a3,a4,a5,a6,a7,a8,a9) = a.v
            if n == 0: a.v = (m,a1,a2,a3,a4,a5,a6,a7,a8,a9)
            elif n == 1: a.v = (a0,m,a2,a3,a4,a5,a6,a7,a8,a9)
            elif n == 2: a.v = (a0,a1,m,a3,a4,a5,a6,a7,a8,a9)
            elif n == 3: a.v = (a0,a1,a2,m,a4,a5,a6,a7,a8,a9)
            elif n == 4: a.v = (a0,a1,a2,a3,m,a5,a6,a7,a8,a9)
            elif n == 5: a.v = (a0,a1,a2,a3,a4,m,a6,a7,a8,a9)
            elif n == 6: a.v = (a0,a1,a2,a3,a4,a5,m,a7,a8,a9)
            elif n == 7: a.v = (a0,a1,a2,a3,a4,a5,a6,m,a8,a9)
            elif n == 8: a.v = (a0,a1,a2,a3,a4,a5,a6,a7,m,a9)
            elif n == 9: a.v = (a0,a1,a2,a3,a4,a5,a6,a7,a8,m)
        return setter

    i = Ref(0)

    def while1():
        if i.v < length:
            a_set(i.v)(read_x())
            i.v = i.v + 1
            while1()

    while1()

    i.v = 1

    def while2():
        if i.v < length:
            val = Ref(0)
            j = Ref(0)
            val.v = a_get(i.v)
            j.v = i.v

            def while3():
                if j.v > 0 and compare(a_get(j.v - 1), val.v):
                    a_set(j.v)(a_get(j.v - 1))
                    j.v = j.v - 1
                    while3()

            while3()
            a_set(j.v)(val.v)
            i.v = i.v + 1
            while2()

    while2()

    i.v = 0

    def while4():
        if i.v < length:
            write_x(a_get(i.v))
            i.v = i.v + 1
            while4()

    while4()

