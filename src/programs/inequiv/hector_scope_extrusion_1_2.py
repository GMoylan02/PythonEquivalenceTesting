#from typing import Callable
def hector_scope_extrusion_1_2(f):
    x = 0

    def inner(y):
        nonlocal x
        if x == 0:
            x = y
        else:
            x = y - 1
        return x

    return f(inner)


|||

#from typing import Callable
def hector_scope_extrusion_1_2(f):
    def inner(y):
        x = 0
        if x == 0:
            x = y
        else:
            x = y - 1
        return x

    return f(inner)