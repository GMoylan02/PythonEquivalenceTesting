from src.RunHobbitSuite import initialise_test

name, fn = initialise_test("meyer_sieber_v2_ineq.txt")
fn.__name__ = f"test_{name}"
globals()[fn.__name__] = fn
