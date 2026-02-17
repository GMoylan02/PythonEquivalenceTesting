def hector_stark_tricky(f):
    a = 0
    r = 0

    def inner(f):
        nonlocal r, a
        r = r + 1
        a = f(r)
        r = r - 1
        return a

    return inner(f)

|||

def hector_stark_tricky(f):
    return f(1)
