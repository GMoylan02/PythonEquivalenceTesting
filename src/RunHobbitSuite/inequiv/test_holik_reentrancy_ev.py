from src.RunHobbitSuite import initialise_test

name, fn = initialise_test("holik_reentrancy_ev.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
