from src.RunHobbitSuite import initialise_test

name, fn = initialise_test("bsearch_eq_1.txt", True)
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
