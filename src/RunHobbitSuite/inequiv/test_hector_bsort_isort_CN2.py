from src.RunHobbitSuite import initialise_test

name, fn = initialise_test("hector_bsort_isort_CN2.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
