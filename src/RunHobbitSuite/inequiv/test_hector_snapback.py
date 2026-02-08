from . import initialise_test

name, fn = initialise_test("hector_snapback.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
