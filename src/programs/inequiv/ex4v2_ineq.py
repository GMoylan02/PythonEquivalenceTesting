from ..Ref import Ref

x = Ref(0)
c = Ref(0)


def ex4v2_lhs(f):
    x.v = 0
    c.v = c.v + 1
    f()

    if c.v < 2:
        x.v = 1

    c.v = 0
    f()
    return x.v


def ex4v2_rhs(f):
    f()
    f()
    return 1