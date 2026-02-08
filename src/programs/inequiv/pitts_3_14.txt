def empty(x):
    return -99

def cons(hd):
    def inner(tl):
        def lst(x):
            if x == 0:
                return hd
            else:
                return tl(x - 1)
        return lst
    return inner

def head(ls):
    return ls(0)

def tail(ls):
    def t(x):
        return ls(x - 1)
    return t

def map_(f):
    def mapper(l):
        if head(l) == head(empty):
            return empty
        else:
            return cons(f(head(l)))(map_(f)(tail(l)))
    return mapper

def filter_(u):
    def filt(l):
        if head(l) == head(empty):
            return empty
        elif u(head(l)):
            return cons(head(l))(filter_(u)(tail(l)))
        else:
            return filter_(u)(tail(l))
    return filt

def ml_function(u):
    def inner_v(v):
        def inner_l(l):
            return filter_(u)(map_(v)(l))
        return inner_l
    return inner_v

|||

def empty(x):
    return -99

def cons(hd):
    def inner(tl):
        def lst(x):
            if x == 0:
                return hd
            else:
                return tl(x - 1)
        return lst
    return inner

def head(ls):
    return ls(0)

def tail(ls):
    def t(x):
        return ls(x - 1)
    return t

def map_(f):
    def mapper(l):
        if head(l) == head(empty):
            return empty
        else:
            return cons(f(head(l)))(map_(f)(tail(l)))
    return mapper

def filter_(u):
    def filt(l):
        if head(l) == head(empty):
            return empty
        elif u(head(l)):
            return cons(head(l))(filter_(u)(tail(l)))
        else:
            return filter_(u)(tail(l))
    return filt

def ml_function(u):
    def compose(u):
        def inner(v):
            def inner_x(x):
                return u(v(x))
            return inner_x
        return inner
    def inner_v(v):
        def inner_l(l):
            return map_(v)(filter_(compose(u)(v))(l))
        return inner_l
    return inner_v
