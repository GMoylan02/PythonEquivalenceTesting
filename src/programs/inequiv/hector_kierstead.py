def hector_kierstead_lhs(f):
    return f(
        lambda x: f(
            lambda y: x()
        )
    )


def hector_kierstead_rhs(f):
    return f(
        lambda x: f(
            lambda y: y()
        )
    )
