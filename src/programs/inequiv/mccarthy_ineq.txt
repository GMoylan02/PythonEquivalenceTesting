def mccarthy(n):
    if n < 0:
        raise RuntimeError()
    elif n > 100:
        return n - 10
    else:
        return mccarthy(mccarthy(n + 12))

|||

def mccarthy(n):
    if n < 0:
        raise RuntimeError()
    elif n > 100:
        return n - 10
    else:
        return 91
