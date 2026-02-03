list_fn = lambda x: None
cnt = 0
running = 0

def enlist(f):
    global cnt, list_fn, running
    if not (running == 0):
        return None
    else:
        cnt = cnt + 1
        c = cnt
        l = list_fn
        def new_list(z):
            if z == c:
                return f()
            else:
                return l(z)
        list_fn = new_list

def run(check):
    global cnt, list_fn, running
    running = 1
    if 0 < cnt:
        list_fn(cnt)
        cnt = cnt - 1
        check(not (cnt < 0))
        return run(check)
    else:
        list_fn = lambda x: None
        running = 0

def program(f):
    return f(enlist)(run)

|||

list_fn = lambda x: None
cnt = 0
running = 0

def enlist(f):
    global cnt, list_fn, running
    if not (running == 0):
        return None
    else:
        cnt = cnt + 1
        c = cnt
        l = list_fn
        def new_list(z):
            if z == c:
                return f()
            else:
                return l(z)
        list_fn = new_list

def run(check):
    global cnt, list_fn, running
    running = 1
    if 0 < cnt:
        list_fn(cnt)
        cnt = cnt - 1
        check(True)
        return run(check)
    else:
        list_fn = lambda x: None
        running = 0

def program(f):
    return f(enlist)(run)
