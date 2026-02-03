def hector_scope_extrusion_1_3(f):
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


def hector_scope_extrusion_1_3(f):

    def inner(y):
        return y

    return f(inner)
