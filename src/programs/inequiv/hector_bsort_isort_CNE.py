from ..Ref import Ref


def hector_bsort_isort_CNE_lhs(args):
    (compare, write_x, length, a_get, a_set) = args

    i = Ref(0)
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


def hector_bsort_isort_CNE_rhs(args):
    (compare, write_x, length, a_get, a_set) = args

    i = Ref(0)

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
