def f(x):
    r = x
    if x > 0:
        r = f(x - 1)
        r = r + 1
    if x < 0:
        r = 0
    return r

|||

def f(x):
    r = x
    if x > 1:
        r = f(x - 2)
        r = r + 2
    if x < 2:
        r = 0
    return r
