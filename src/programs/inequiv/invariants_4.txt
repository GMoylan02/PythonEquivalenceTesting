x = 0

def g():
    global x
    x = x + 1
    if x > 10:
        x = 0
    g()
    if x <= 20:
        x = x + 1
        return None
    else:
        raise RuntimeError()

|||

def g():
    g()
    return None
