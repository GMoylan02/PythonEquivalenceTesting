from src.FunctionEquivalence import make_function_equivalence_test


def make_bsearch_4_lhs():
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

    def bsearch_loop(key):
        return lambda lo: lambda hi: (
            (lambda mid:
                bsearch_loop(key)(mid + 1)(hi) if get(mid) <= key
                else bsearch_loop(key)(lo)(mid)
            )((lo + hi) // 2)
            if lo + 1 < hi
            else get(lo) == key
        )

    #def bsearch(key: int):
    def bsearch(key):
        return bsearch_loop(key)(0)(length)

    return bsearch


def make_bsearch_4_rhs():
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

    def bsearch_loop(key: int):
        return lambda lo: lambda hi: (
            (lambda mid:
                bsearch_loop(key)(mid)(hi) if get(mid) <= key
                else bsearch_loop(key)(lo)(mid)
            )((lo + hi) // 2)
            if lo + 1 < hi
            else get(lo) == key
        )

    #def bsearch(key: int):
    def bsearch(key):
        return bsearch_loop(key)(0)(length)

    return bsearch

test_bsearch_ineq_4 = make_function_equivalence_test(make_bsearch_4_lhs, make_bsearch_4_rhs, log_failure=True)
#test_bsearch_ineq_4()