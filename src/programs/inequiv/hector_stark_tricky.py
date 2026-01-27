from ..Ref import Ref


def hector_stark_tricky_lhs(f):
    a = Ref(0)
    r = Ref(0)

    def inner(f):
        r.v = r.v + 1
        a.v = f(r.v)
        r.v = r.v - 1
        return a.v

    return inner(f)


def hector_stark_tricky_rhs(f):
    return f(1)
