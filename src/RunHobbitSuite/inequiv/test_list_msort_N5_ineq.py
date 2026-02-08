from src.RunHobbitSuite import initialise_test

name, fn = initialise_test("list_msort_N5_ineq.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
