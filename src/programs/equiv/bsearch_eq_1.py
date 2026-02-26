from src.UniversalStrategy import make_function_equivalence_test


def make_bsearch_eq_1_lhs():
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

    lo = [0]
    hi = [length - 1]
    found = [False]

    def bsearch(key):
        if lo[0] <= hi[0] and not found[0]:
            mid = (lo[0] + hi[0]) // 2
            if get(mid) < key:
                lo[0] = mid + 1
            elif get(mid) > key:
                hi[0] = mid - 1
            else:
                found[0] = True
            return bsearch(key)
        else:
            ret = found[0]
            lo[0] = 0
            hi[0] = length - 1
            found[0] = False
            return ret

    return bsearch

bsearch_eq_1_lhs = make_bsearch_eq_1_lhs()


def make_bsearch_eq_1_rhs():
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

    lo = [0]
    hi = [length]  # note: hi starts at length, not length-1
    found = [False]

    def bsearch(key):
        if lo[0] + 1 < hi[0]:
            mid = (lo[0] + hi[0]) // 2
            if get(mid) <= key:
                lo[0] = mid  # note: mid not mid+1 (potential mistake per comment)
            else:
                hi[0] = mid
            return bsearch(key)
        else:
            ret = get(lo[0]) == key
            lo[0] = 0
            hi[0] = length
            found[0] = False
            return ret

    return bsearch

bsearch_eq_1_rhs = make_bsearch_eq_1_rhs()

test_bsearch_eq_1 = make_function_equivalence_test(bsearch_eq_1_lhs, bsearch_eq_1_rhs, log_failure=True)