from ..Ref import Ref

def make_bsearch_ineq_3_1():
    array = Ref((1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    length = 10

    def get(n):
        a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = array.v
        if n == 0: return a0
        elif n == 1: return a1
        elif n == 2: return a2
        elif n == 3: return a3
        elif n == 4: return a4
        elif n == 5: return a5
        elif n == 6: return a6
        elif n == 7: return a7
        elif n == 8: return a8
        elif n == 9: return a9
        else: return -1

    lo = Ref(0)
    hi = Ref(length - 1)
    found = Ref(False)

    def bsearch(key):
        if lo.v <= hi.v and not found.v:
            mid = (lo.v + hi.v) // 2
            if get(mid) < key:
                lo.v = mid + 1
            elif get(mid) > key:
                hi.v = mid - 1
            else:
                found.v = True
            return bsearch(key)
        else:
            return found.v   # NO reset (intentional)

    return bsearch

def make_bsearch_ineq_3_2():
    array = Ref((1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    length = 10

    def get(n):
        a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = array.v
        if n == 0: return a0
        elif n == 1: return a1
        elif n == 2: return a2
        elif n == 3: return a3
        elif n == 4: return a4
        elif n == 5: return a5
        elif n == 6: return a6
        elif n == 7: return a7
        elif n == 8: return a8
        elif n == 9: return a9
        else: return -1

    lo = Ref(0)
    hi = Ref(length)
    found = Ref(False)

    def bsearch(key):
        if lo.v + 1 < hi.v:
            mid = (lo.v + hi.v) // 2
            if get(mid) <= key:
                lo.v = mid          # intentional choice, as in HOBBIT
            else:
                hi.v = mid
            return bsearch(key)
        else:
            result = (get(lo.v) == key)
            lo.v = 0
            hi.v = length
            found.v = False
            return result

    return bsearch
