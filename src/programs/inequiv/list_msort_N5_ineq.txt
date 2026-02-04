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

    def merge(ls1, ls2):
        if is_nil(ls1):
            return ls2
        if is_nil(ls2):
            return ls1
        x = hd(ls1)
        xs = tl(ls1)
        y = hd(ls2)
        ys = tl(ls2)
        if x <= y:
            return cons(x)(merge(xs, ls2))
        else:
            return cons(y)(merge(ls1, ys))

    def split(ls):
        if is_nil(ls):
            return (nil, nil)
        x = hd(ls)
        zs = tl(ls)
        if is_nil(zs):
            return (cons(x)(nil), nil)
        y = hd(zs)
        zs2 = tl(zs)
        xs, ys = split(zs2)
        return (cons(x)(xs), cons(y)(ys))

    def msort(ls):
        if is_nil(ls):
            return ls
        x = hd(ls)
        xs = tl(ls)
        if is_nil(xs):
            return ls
        cs, bs = split(ls)
        return merge(msort(cs), msort(bs))

    return is_sorted(msort(list_))

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
