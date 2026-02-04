def program(g):
    x = 0
    def f():
        nonlocal x
        x = x + 2
    g(f)
    if x <= 10:
        return None
    else:
        raise RuntimeError()

|||

def program(g):
    g(lambda x: None)
    return None
