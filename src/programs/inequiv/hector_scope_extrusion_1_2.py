from ..Ref import Ref


def hector_scope_extrusion_1_2_lhs(f):
    x = Ref(0)

    def inner(y):
        if x.v == 0:
            x.v = y
        else:
            x.v = y - 1
        return x.v

    return f(inner)


def hector_scope_extrusion_1_2_rhs(f):
    def inner(y):
        x = Ref(0)
        if x.v == 0:
            x.v = y
        else:
            x.v = y - 1
        return x.v

    return f(inner)