from src.UniversalStrategy import make_function_equivalence_test


def holik_flat_combiner_v4_e_lhs():
    list_ref = [lambda x: None]
    cnt = [0]
    running = [0]

    def enlist(f):
        if not (running[0] == 0):
            pass
        else:
            cnt[0] = cnt[0] + 1
            c = cnt[0]
            l = list_ref[0]
            list_ref[0] = lambda z: f() if z == c else l(z)

    def run():
        running[0] = 1
        if 0 < cnt[0]:
            list_ref[0](cnt[0])
            cnt[0] = cnt[0] - 1
            if cnt[0] < 0:
                raise Exception("_bot_")
            run()
        else:
            list_ref[0] = lambda x: None
            running[0] = 0

    return lambda f: f(enlist)(run)


def holik_flat_combiner_v4_e_rhs():
    list_ref = [lambda x: None]
    cnt = [0]
    running = [0]

    def enlist(f):
        if not (running[0] == 0):
            pass
        else:
            cnt[0] = cnt[0] + 1
            c = cnt[0]
            l = list_ref[0]
            list_ref[0] = lambda z: f() if z == c else l(z)

    def run():
        running[0] = 1
        if 0 < cnt[0]:
            list_ref[0](cnt[0])
            cnt[0] = cnt[0] - 1
            run()
        else:
            list_ref[0] = lambda x: None
            running[0] = 0

    return lambda f: f(enlist)(run)

test_holik_flat_combiner_v4_e \
    = make_function_equivalence_test(holik_flat_combiner_v4_e_lhs,
                                     holik_flat_combiner_v4_e_rhs,
                                     log_failure=True)