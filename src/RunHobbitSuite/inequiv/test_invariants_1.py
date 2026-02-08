from src.RunHobbitSuite import initialise_test

name, fn = initialise_test("invariants_1.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
