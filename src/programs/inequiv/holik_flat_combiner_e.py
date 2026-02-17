def program():
    # ref list' = (fun x -> ())
    list_ref = {'val': lambda x: None}

    # ref cnt = 0
    cnt = {'val': 0}

    # ref running = 0
    running = {'val': 0}

    # let enlist = ...
    def enlist(f):
        if not (running['val'] == 0):
            return None
        else:
            cnt['val'] = cnt['val'] + 1
            c = cnt['val']
            l = list_ref['val']
            list_ref['val'] = lambda z: f() if z == c else l(z)

    # let rec run () = ...
    def run():
        running['val'] = 1
        if 0 < cnt['val']:
            list_ref['val'](cnt['val'])
            cnt['val'] = cnt['val'] - 1
            if cnt['val'] < 0:
                raise Exception("_bot_")  # _bot_ represents bottom/error
            else:
                pass
            run()
        else:
            list_ref['val'] = lambda x: None
            running['val'] = 0

    # (fun f -> (f enlist) run)
    return lambda f: f(enlist)(run)

|||

def program():
    # ref list' = (fun x -> ())
    list_ref = {'val': lambda x: None}

    # ref cnt = 0
    cnt = {'val': 0}

    # ref running = 0
    running = {'val': 0}

    # let enlist = ...
    def enlist(f):
        if not (running['val'] == 0):
            return None
        else:
            cnt['val'] = cnt['val'] + 1
            c = cnt['val']
            l = list_ref['val']
            list_ref['val'] = lambda z: f() if z == c else l(z)

    # let rec run () = ...
    # The body is commented out in the original
    def run():
        running['val'] = 1
        # The rest of the function body is commented out

    # (fun f -> (f enlist) run)
    return lambda f: f(enlist)(run)
