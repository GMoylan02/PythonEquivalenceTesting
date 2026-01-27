from ..Ref import Ref

x = Ref(0)

def call(f):
    x.v = x.v + 1
    f()
    x.v = x.v - 1
    return True
