from ..Ref import Ref

def make_v1_lhs():
    def v1(f):
        f()
        return True
    return v1

def make_v1_rhs():
    flag = Ref(True)

    def v1(f):
        if flag.v:
            flag.v = False
            f()
            flag.v = True
            return True
        else:
            f()
            return False

    return v1


