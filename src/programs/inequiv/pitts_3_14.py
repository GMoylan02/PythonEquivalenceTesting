from src.UniversalStrategy import make_function_equivalence_test


def pitts_3_14_lhs():
    empty = lambda x: -99

    def cons(hd):
        return lambda tl: lambda x: hd if x == 0 else tl(x - 1)

    head = lambda ls: ls(0)
    tail = lambda ls: lambda x: ls(x + 1)

    def map_f(f):
        def map_inner(l):
            if head(l) == head(empty):
                return empty
            else:
                return cons(f(head(l)))(map_f(f)(tail(l)))

        return map_inner

    def filter_f(u):
        def filter_inner(l):
            if head(l) == head(empty):
                return empty
            else:
                if u(head(l)):
                    return cons(head(l))(filter_f(u)(tail(l)))
                else:
                    return filter_f(u)(tail(l))

        return filter_inner

    def func(u):
        return lambda v: lambda l: filter_f(u)(map_f(v)(l))

    return func


def pitts_3_14_rhs():
    empty = lambda x: -99

    def cons(hd):
        return lambda tl: lambda x: hd if x == 0 else tl(x - 1)

    head = lambda ls: ls(0)
    tail = lambda ls: lambda x: ls(x + 1)

    def map_f(f):
        def map_inner(l):
            if head(l) == head(empty):
                return empty
            else:
                return cons(f(head(l)))(map_f(f)(tail(l)))

        return map_inner

    def filter_f(u):
        def filter_inner(l):
            if head(l) == head(empty):
                return empty
            else:
                if u(head(l)):
                    return cons(head(l))(filter_f(u)(tail(l)))
                else:
                    return filter_f(u)(tail(l))

        return filter_inner

    def compose(u):
        return lambda v: lambda x: u(v(x))

    def func(u):
        return lambda v: lambda l: map_f(v)(filter_f(compose(u)(v))(l))

    return func

test_pitts_3_14 = make_function_equivalence_test(pitts_3_14_lhs, pitts_3_14_rhs, log_failure=True)