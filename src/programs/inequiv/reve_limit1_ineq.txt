def f(n):
    r = 0
    if n <= 1:
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
        r = f(n - 3)
        r = n + (n - 1) + r
    return r
