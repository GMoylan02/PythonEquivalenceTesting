from src.UniversalStrategy import make_function_equivalence_test


def make_bsearch_eq_2_lhs():
    array = [(1,2,3,4,5,6,7,8,9,10)]
    length = 10

    def get(n):
        a0,a1,a2,a3,a4,a5,a6,a7,a8,a9 = array[0]
        if n == 0: return a0
        if n == 1: return a1
        if n == 2: return a2
        if n == 3: return a3
        if n == 4: return a4
        if n == 5: return a5
        if n == 6: return a6
        if n == 7: return a7
        if n == 8: return a8
        if n == 9: return a9
        return -1

    def bsearch_loop(key):
        def inner(lo):
            def inner2(hi):
                if lo <= hi:
                    mid = (lo + hi) // 2
                    if get(mid) < key:
                        return bsearch_loop(key)(mid + 1)(hi)
                    elif get(mid) > key:
                        return bsearch_loop(key)(lo)(mid - 1)
                    else:
                        return True
                else:
                    return False
            return inner2
        return inner

    bsearch = lambda key: bsearch_loop(key)(0)(length - 1)
    return bsearch

bsearch_eq_2_lhs = make_bsearch_eq_2_lhs()


def make_bsearch_eq_2_rhs():
    array = [(1,2,3,4,5,6,7,8,9,10)]
    length = 10

    def get(n):
        a0,a1,a2,a3,a4,a5,a6,a7,a8,a9 = array[0]
        if n == 0: return a0
        if n == 1: return a1
        if n == 2: return a2
        if n == 3: return a3
        if n == 4: return a4
        if n == 5: return a5
        if n == 6: return a6
        if n == 7: return a7
        if n == 8: return a8
        if n == 9: return a9
        return -1

    def bsearch_loop(key):
        def inner(lo):
            def inner2(hi):
                if lo + 1 < hi:
                    mid = (lo + hi) // 2
                    if get(mid) <= key:
                        return bsearch_loop(key)(mid)(hi)  # note: mid not mid+1
                    else:
                        return bsearch_loop(key)(lo)(mid)
                else:
                    return get(lo) == key
            return inner2
        return inner

    bsearch = lambda key: bsearch_loop(key)(0)(length)  # note: length not length-1
    return bsearch

bsearch_eq_2_rhs = make_bsearch_eq_2_rhs()

test_bsearch_eq_2 = make_function_equivalence_test(bsearch_eq_2_lhs, bsearch_eq_2_rhs, log_failure=True)