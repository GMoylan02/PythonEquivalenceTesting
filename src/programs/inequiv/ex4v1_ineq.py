def program():
    x = [0]
    c = [0]

    def func(f):
        x[0] = 0
        c[0] = c[0] + 1
        f()
        if c[0] < 1:
            x[0] = 1
        c[0] = 0
        f()
        return x[0]

    return func

|||


def program():
    def func(f):
        f()
        f()
        return 1

    return func
