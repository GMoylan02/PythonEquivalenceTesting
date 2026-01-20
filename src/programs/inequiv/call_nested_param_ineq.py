from ..Ref import Ref
from typing import Callable

def make_call_lhs():
    x = Ref(0)

    def call(f: Callable):
        x.v = x.v + 1
        f()
        x.v = x.v - 1
        return x.v < 100

    return call

def make_call_rhs():
    x = Ref(0)

    def call(f: Callable):
        x.v = x.v + 1
        f()
        x.v = x.v - 1
        return True

    return call