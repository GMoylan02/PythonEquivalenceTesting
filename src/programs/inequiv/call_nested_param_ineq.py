def make_call():
    x = [0]

    def call(f):
        x[0] = x[0] + 1
        f()
        x[0] = x[0] - 1
        return x[0] < 100

    return call

|||

def make_call():
    x = [0]

    def call(f):
        x[0] = x[0] + 1
        f()
        x[0] = x[0] - 1
        return True

    return call
