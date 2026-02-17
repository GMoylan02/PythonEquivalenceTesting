def make_bsearch():
    array = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    length = 10

    def get(n):
        # Destructuring the tuple exactly like the OCaml array ref
        a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = array
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

    # Python closure variables mimic OCaml refs
    lo = 0
    hi = length
    found = False

    def bsearch(key):
        nonlocal lo, hi, found

        if lo + 1 < hi:
            mid = (lo + hi) // 2  # Integer division mimics OCaml's /
            if get(mid) <= key:
                lo = mid + 1
            else:
                hi = mid
            return bsearch(key)
        else:
            found = (get(lo) == key)
            return found

    return bsearch

|||

def make_bsearch():
    array = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    length = 10

    def get(n):
        a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = array
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

    lo = 0
    hi = length
    found = False

    def bsearch(key):
        nonlocal lo, hi, found

        if lo + 1 < hi:
            mid = (lo + hi) // 2
            if get(mid) <= key:
                lo = mid  # potential mistake: lo := mid+1
            else:
                hi = mid
            return bsearch(key)
        else:
            found = (get(lo) == key)
            return found

    return bsearch
