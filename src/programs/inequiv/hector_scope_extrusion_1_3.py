from ..Ref import Ref

def lhs(f):
    x = Ref(0)

    def inner(y):
        if x.v == 0:
            x.v = y
        else:
            x.v = y - 1
        return x.v

    return f(inner)

def rhs(f):

    def inner(y):
        return y

    return f(inner)
