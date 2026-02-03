from . import initialise_test

name, fn = initialise_test(4)
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
