def f(ij):
    i, j = ij
    r = 0
    if i == 0:
        r = j
    else:
        r = f((i - 1, j + 1))
    return r

|||

def f(ij):
    i, j = ij
    r = 0
    if i == 0:
        r = j
    elif i == 1:
        r = j + 1
    elif i == 2:
        r = j
    else:
        r = f((i - 1, j + 1))
    return r
