from ..Ref import Ref

def hector_snapback_lhs(p):
    x = Ref(0)

    def inner(y):
        x.v = 1

    p(inner)

    if x.v == 1:
        raise RuntimeError("_bot_")
    else:
        return None


def hector_snapback_rhs(p):
    def inner(y):
        raise RuntimeError("_bot_")
    p(inner)
