from src.RunHobbitSuite import initialise_test

name, fn = initialise_test("bsearch_ineq_1.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
