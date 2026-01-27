from ..Ref import Ref


def hector_bsort_isort_CN2_lhs(args):
    compare = args[0]
    read_x = args[1][0]
    write_x = args[1][1]

    a = Ref((0, 0))

    def a_get(n):
        (a0, a1) = a.v
        if n == 0:
            return a0
        if n == 1:
            return a1
        return -1

    def a_set(n):
        def setter(m):
            (a0, a1) = a.v
            if n == 0:
                a.v = (m, a1)
            elif n == 1:
                a.v = (a0, m)
        return setter

    i = Ref(0)

    def while1():
        if i.v < 2:
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
                if i.v < 1:
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
        if i.v < 2:
            write_x(a_get(i.v))
            i.v = i.v + 1
            while4()

    while4()


def hector_bsort_isort_CN2_rhs(args):
    compare = args[0]
    read_x = args[1][0]
    write_x = args[1][1]

    a = Ref((0, 0))

    def a_get(n):
        (a0, a1) = a.v
        if n == 0:
            return a0
        if n == 1:
            return a1
        return -1

    def a_set(n):
        def setter(m):
            (a0, a1) = a.v
            if n == 0:
                a.v = (m, a1)
            elif n == 1:
                a.v = (a0, m)
        return setter

    i = Ref(0)

    def while1():
        if i.v < 2:
            a_set(i.v)(read_x())
            i.v = i.v + 1
            while1()

    while1()

    i.v = 1

    def while2():
        if i.v < 2:
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
        if i.v < 2:
            write_x(a_get(i.v))
            i.v = i.v + 1
            while4()

    while4()
