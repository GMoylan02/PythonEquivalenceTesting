from ..Ref import Ref


x = Ref(0)
c = Ref(0)


def lhs(f):
    x.v = 0
    c.v = c.v + 1
    f()

    if c.v < 4:
        x.v = 1

    c.v = 0
    f()
    return x.v


def rhs(f):
    f()
    f()
    return 1
