from src.UniversalStrategy import make_function_equivalence_test


def hector_snapback_lhs(p):
    x = 0

    def inner(y):
        nonlocal x
        x = 1

    p(inner)

    if x == 1:
        raise RuntimeError("_bot_")
    else:
        return None


def hector_snapback_rhs(p):
    def inner(y):
        raise RuntimeError("_bot_")
    p(inner)

test_hector_snapback = make_function_equivalence_test(hector_snapback_lhs, hector_snapback_rhs, log_failure=True)
