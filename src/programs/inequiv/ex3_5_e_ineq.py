from ..Ref import Ref


def v2_lhs():
    return True


flag = Ref(True)


def v2_rhs():
    if flag.v:
        flag.v = False
        return True
    else:
        return False
