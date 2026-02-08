from src.RunHobbitSuite import initialise_test

name, fn = initialise_test("holik_reentrancy_e3.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
