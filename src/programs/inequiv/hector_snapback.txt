def hector_snapback(p):
    x = 0

    def inner(y):
        nonlocal x
        x = 1

    p(inner)

    if x == 1:
        raise RuntimeError("_bot_")
    else:
        return None

|||

def hector_snapback(p):
    def inner(y):
        raise RuntimeError("_bot_")
    p(inner)
