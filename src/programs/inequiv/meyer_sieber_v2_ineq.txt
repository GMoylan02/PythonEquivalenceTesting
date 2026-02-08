
def program(g):
    def even(x):
        return (x - ((x // 2) * 2)) == 0
    l = 0
    def f():
        nonlocal l
        l = l + 1
    g(f)
    if even(l):
        return lambda: None
    else:
        raise RuntimeError()

|||

def program(g):
    g(lambda: None)
    return lambda: None
