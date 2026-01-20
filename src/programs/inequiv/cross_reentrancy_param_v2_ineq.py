from ..Ref import Ref

def make_prog_lhs():
    x = Ref(0)

    def call_even():
        # parity test: x mod 2 == 0
        if (x.v - ((x.v // 2) * 2)) == 0:
            x.v = x.v + 1
        return x.v < 5

    def call_odd():
        if (x.v - ((x.v // 2) * 2)) != 0:
            x.v = x.v + 1
        return x.v < 5

    def program(f):
        # f : (unit -> bool) -> (unit -> bool) -> unit
        return f(call_even, call_odd)

    return program


def make_prog_rhs():
    x = Ref(0)

    def call_even():
        if (x.v - ((x.v // 2) * 2)) == 0:
            x.v = x.v + 1
        return True

    def call_odd():
        if (x.v - ((x.v // 2) * 2)) != 0:
            x.v = x.v + 1
        return True

    def program(f):
        return f(call_even, call_odd)

    return program