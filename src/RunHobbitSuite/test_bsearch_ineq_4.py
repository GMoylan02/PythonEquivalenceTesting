from . import initialise_test

name, fn = initialise_test("bsearch_ineq_4.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
