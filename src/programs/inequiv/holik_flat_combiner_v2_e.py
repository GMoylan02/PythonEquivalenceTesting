from typing import Callable

from src.UniversalStrategy import make_function_equivalence_test


def holik_flat_combiner_v2_e_lhs():
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

    def run(check):
        running[0] = 1
        if 0 < cnt[0]:
            list_ref[0](cnt[0])
            cnt[0] = cnt[0] - 1
            check(not (cnt[0] < 0))
            run(check)
        else:
            list_ref[0] = lambda x: None
            running[0] = 0

    #def func(g: Callable):
    def func(g):
        return g(enlist)(run)
    return func


def holik_flat_combiner_v2_e_rhs():
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

    def run(check):
        running[0] = 1
        if 0 < cnt[0]:
            list_ref[0](cnt[0])
            cnt[0] = cnt[0] - 1
            check(True)
            run(check)
        else:
            list_ref[0] = lambda x: None
            running[0] = 0

    #def func(g: Callable):
    def func(g):
        return g(enlist)(run)
    return func

test_holik_flat_combiner_v2_e \
    = make_function_equivalence_test(holik_flat_combiner_v2_e_lhs,
                                     holik_flat_combiner_v2_e_rhs,
                                     log_failure=True)
