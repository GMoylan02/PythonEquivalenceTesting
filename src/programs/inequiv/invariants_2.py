x = 0
def g():
    global x
    if x % 2 != 0:
        x = 0
    x = x + 2
    g()
    if x % 2 == 0:
        x = x + 1
        return None
    else:
        raise Exception()

|||

def g():
    g()
    return None