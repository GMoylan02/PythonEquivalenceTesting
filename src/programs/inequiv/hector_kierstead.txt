def hector_kierstead(f):
    return f(
        lambda x: f(
            lambda y: x()
        )
    )


|||


def hector_kierstead(f):
    return f(
        lambda x: f(
            lambda y: y()
        )
    )
