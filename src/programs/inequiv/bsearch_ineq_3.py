from src.UniversalStrategy import make_function_equivalence_test


def make_bsearch_3_lhs():
    array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    length = 10

    def get(n):
        a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = array
        if n == 0:
            return a0
        elif n == 1:
            return a1
        elif n == 2:
            return a2
        elif n == 3:
            return a3
        elif n == 4:
            return a4
        elif n == 5:
            return a5
        elif n == 6:
            return a6
        elif n == 7:
            return a7
        elif n == 8:
            return a8
        elif n == 9:
            return a9
        else:
            return -1

    lo = [0]
    hi = [length - 1]
    found = [False]

    #def bsearch(key: int):
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
            return found[0]

    return bsearch


def make_bsearch_3_rhs():
    array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    length = 10

    def get(n):
        a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = array
        if n == 0:
            return a0
        elif n == 1:
            return a1
        elif n == 2:
            return a2
        elif n == 3:
            return a3
        elif n == 4:
            return a4
        elif n == 5:
            return a5
        elif n == 6:
            return a6
        elif n == 7:
            return a7
        elif n == 8:
            return a8
        elif n == 9:
            return a9
        else:
            return -1

    lo = [0]
    hi = [length]
    found = [False]

    #def bsearch(key: int):
    def bsearch(key):
        if lo[0] + 1 < hi[0]:
            mid = (lo[0] + hi[0]) // 2
            if get(mid) <= key:
                lo[0] = mid
            else:
                hi[0] = mid
            return bsearch(key)
        else:
            return_val = get(lo[0]) == key
            lo[0] = 0
            hi[0] = length
            found[0] = False
            return return_val

    return bsearch

test_bsearch_ineq_3 = make_function_equivalence_test(make_bsearch_3_lhs, make_bsearch_3_rhs, log_failure=True)