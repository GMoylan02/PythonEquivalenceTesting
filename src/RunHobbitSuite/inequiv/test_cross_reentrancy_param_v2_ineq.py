from . import initialise_test

name, fn = initialise_test("cross_reentrancy_param_v2_ineq.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
