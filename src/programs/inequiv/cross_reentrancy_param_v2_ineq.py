def program():
    x = [0]

    def call_even():
        if (x[0] - (x[0] // 2) * 2) == 0:
            x[0] = x[0] + 1
        return x[0] < 5

    def call_odd():
        if (x[0] - (x[0] // 2) * 2) == 0:
            pass
        else:
            x[0] = x[0] + 1
        return x[0] < 5

    return lambda f: f(call_even, call_odd)

|||

def program():
    x = [0]

    def call_even():
        if (x[0] - (x[0] // 2) * 2) == 0:
            x[0] = x[0] + 1
        return True

    def call_odd():
        if (x[0] - (x[0] // 2) * 2) == 0:
            pass
        else:
            x[0] = x[0] + 1
        return True

    return lambda f: f(call_even, call_odd)
