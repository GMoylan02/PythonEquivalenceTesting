x = 0
def g():
    global x
    if x % 2 != 0:
        x = 0
    x = x + 2
    g()
    if x % 2 == 0:
        x = x + 1
        return True
    else:
        return False

|||

def g():
    g()
    return True