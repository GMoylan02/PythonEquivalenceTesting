def f(n):
    r = 0
    if n <= 0:
        r = n
    else:
        r = f(n - 1)
        r = n + r
    return r

|||

def f(n):
    r = 0
    if n <= 1:
        r = n
    else:
        r = f(n - 1)
        r = n + r
        if n == 10:
            r = 10
    return r
