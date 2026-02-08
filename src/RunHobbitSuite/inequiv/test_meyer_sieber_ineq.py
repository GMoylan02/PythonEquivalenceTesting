from . import initialise_test

name, fn = initialise_test("meyer_sieber_ineq.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
