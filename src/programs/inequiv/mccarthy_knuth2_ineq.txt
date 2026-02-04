def mccarthy(n):
    if n > 100:
        return n - 10
    else:
        return mccarthy(mccarthy(n + 11))

|||

def mccarthy(n):
    if n > 100:
        return n - 10
    else:
        return mccarthy(n + 2)
