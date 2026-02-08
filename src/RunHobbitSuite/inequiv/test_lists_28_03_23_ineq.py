from src.RunHobbitSuite import initialise_test

name, fn = initialise_test("lists_28_03_23_ineq.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
