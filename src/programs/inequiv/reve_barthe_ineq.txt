def f(nc):
    n, c = nc
    i = 0
    j = 0
    x = 0
    def while_():
        nonlocal i, j, x
        if i < n:
            j = 5 * i + c
            x = x + j
            i = i + 1
            while_()
        else:
            return None
    while_()
    return x

|||

def f(nc):
    n, c = nc
    i = 0
    j = c
    x = 0
    def while_():
        nonlocal i, j, x
        if i < n:
            x = x + j
            j = j + 5
            if i == 10:
                j = 10
            i = i + 1
            while_()
        else:
            return None
    while_()
    return x
