from . import initialise_test

name, fn = initialise_test("holik_file_lock_param_e_large.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
