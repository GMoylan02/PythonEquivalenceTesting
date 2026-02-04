def program(l):
    def inner(f):
        if l == []:
            return f([])
        else:
            x = l[0]
            xs = l[1:]
            return f(xs)
    return inner

|||

def program(l):
    def inner(f):
        return f(l)
    return inner
