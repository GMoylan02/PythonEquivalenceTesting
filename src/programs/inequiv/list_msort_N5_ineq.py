from src.UniversalStrategy import make_function_equivalence_test


def list_msort_N5_ineq_lhs():
    list_len = 5
    nil = ((0, 0, 0, 0, 0), 0)

    def is_nil(ls):
        a, b = ls
        return b == 0

    def hd(ls):
        if is_nil(ls):
            raise Exception("_bot_")
        xs, l = ls
        return xs[0]

    def tl(ls):
        if is_nil(ls):
            raise Exception("_bot_")
        xs, l = ls
        a0, a1, a2, a3, a4 = xs
        return ((a1, a2, a3, a4, 0), l - 1)

    def cons(x):
        def cons_inner(xs):
            ls, l = xs
            if l >= list_len:
                raise Exception("_bot_")
            a0, a1, a2, a3, a4 = ls
            return ((x, a0, a1, a2, a3), l + 1)

        return cons_inner

    def is_sorted(ls):
        if is_nil(ls):
            return True

        def aux(ls, last):
            if is_nil(ls):
                return True
            x = hd(ls)
            xs = tl(ls)
            if last > x:
                return False
            return aux(xs, x)

        return aux(ls, hd(ls))

    def func(args):
        length, read = args

        def read_list(len_):
            if len_ <= 0:
                return nil
            return cons(read())(read_list(len_ - 1))

        list_ = read_list(length)

        def merge(ls1):
            return lambda ls2: (
                ls2 if is_nil(ls1) else
                ls1 if is_nil(ls2) else
                (lambda x, xs, y, ys:
                 cons(x)(merge(xs)(ls2)) if x <= y else cons(y)(merge(ls1)(ys))
                 )(hd(ls1), tl(ls1), hd(ls2), tl(ls2))
            )

        def split(ls):
            if is_nil(ls):
                return (nil, nil)
            x = hd(ls)
            zs = tl(ls)
            if is_nil(zs):
                return (cons(x)(nil), nil)
            y = hd(zs)
            zs = tl(zs)
            xs, ys = split(zs)
            return (cons(x)(xs), cons(y)(ys))

        def msort(ls):
            if is_nil(ls):
                return ls
            x = hd(ls)
            xs = tl(ls)
            if is_nil(xs):
                return ls
            cs, bs = split(ls)
            return merge(msort(cs))(msort(bs))

        return is_sorted(msort(list_))

    return func


def list_msort_N5_ineq_rhs():
    list_len = 5

    def func(args):
        length, read = args

        def read_list(len_):
            if len_ <= 0:
                return
            x = read()
            read_list(len_ - 1)

        read_list(length)
        return True

    return func

test_list_msort_N5_ineq = make_function_equivalence_test(list_msort_N5_ineq_lhs, list_msort_N5_ineq_rhs, log_failure=True)