from ..Ref import Ref
from typing import Callable

def make_call_lhs():
    x = Ref(0)

    def call1(f: Callable):
        x.v = x.v + 1
        f()
        x.v = x.v - 1
        # this condition is problematic. you can obviously make it so f causes x to increase, but there is no observable
        # difference between when x==10 and x==20 etc. you could hardcode it to allow an f() that may cause x to be 100
        # but the upper limit we set in this case would be kind of arbitrary and if a test case then tests for x==101
        # then that's a problem.
        # similarly, it makes no sense to allow x to be infinitely large but without it being infinitely large we
        # always miss cases like this. at the heart of it, this pipeline can prove inequivalences by showing counter
        # examples, but it cannot prove equivalence
        return x.v < 100

    return call1

def make_call_rhs():
    x = Ref(0)

    def call2(f: Callable):
        x.v = x.v + 1
        f()
        x.v = x.v - 1
        return True

    return call2