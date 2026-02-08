from . import initialise_test

name, fn = initialise_test("holik_reentrancy_e.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
