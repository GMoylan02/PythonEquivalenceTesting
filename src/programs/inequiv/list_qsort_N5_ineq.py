list_len = 5

nil = ((0, 0, 0, 0, 0), 0)

def is_nil(ls):
    a, b = ls
    return b == 0

def hd(ls):
    if is_nil(ls):
        raise RuntimeError()
    xs, l = ls
    return xs[0]

def tl(ls):
    if is_nil(ls):
        raise RuntimeError()
    xs, l = ls
    a0, a1, a2, a3, a4 = xs
    return ((a1, a2, a3, a4, 0), l - 1)

def cons(x):
    def inner(xs):
        ls, l = xs
        if l >= list_len:
            raise RuntimeError()
        a0, a1, a2, a3, a4 = ls
        return ((x, a0, a1, a2, a3), l + 1)
    return inner

def append(ls1, ls2):
    if is_nil(ls1):
        return ls2
    x = hd(ls1)
    xs = tl(ls1)
    return cons(x)(append(xs, ls2))

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
        else:
            return aux(xs, x)
    return aux(ls, hd(ls))

def program(args):
    length, read = args

    def read_list(len_):
        if len_ <= 0:
            return nil
        else:
            return cons(read())(read_list(len_ - 1))

    list_ = read_list(length)

    def partition(pred, ls):
        if is_nil(ls):
            return (nil, nil)
        x = hd(ls)
        zs = tl(ls)
        if pred(x):
            xs, ys = partition(pred, zs)
            return (cons(x)(xs), ys)
        else:
            xs, ys = partition(pred, zs)
            return (xs, cons(x)(ys))

    def qsort(ls):
        if is_nil(ls):
            return ls
        x = hd(ls)
        xs = tl(ls)
        ys, zs = partition(lambda y: y < x, xs)
        return append(qsort(ys), cons(x)(qsort(zs)))

    return is_sorted(qsort(list_))

|||

list_len = 5

def program(args):
    length, read = args

    def read_list(len_):
        if len_ <= 0:
            return None
        else:
            x = read()
            return read_list(len_ - 1)

    read_list(length)
    return True
