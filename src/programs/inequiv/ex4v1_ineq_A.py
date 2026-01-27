from ..Ref import Ref

x = Ref(0)  # ref x
c = Ref(0)  # ref c

def g(f):
    x.v = 0
    c.v += 1
    f()
    if c.v < 1:
        x.v = 1
    c.v = 0
    f()
    return x.v
