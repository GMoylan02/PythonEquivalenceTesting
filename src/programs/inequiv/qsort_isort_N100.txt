max_array_size = 100

def mk_array(n):
    if n < 1 or n > max_array_size:
        raise RuntimeError()
    a = [0] * 100
    a_size = n

    def a_get(i):
        if i < 0 or i > a_size:
            raise RuntimeError()
        return a[i]

    def a_set(i):
        def inner(m):
            if i < 0 or i > a_size:
                raise RuntimeError()
            a[i] = m
        return inner

    return (a_size, a_get, a_set)

def ar_size(ar):
    a_size, _, _ = ar
    return a_size

def ar_get(ar):
    _, a_get, _ = ar
    return a_get

def ar_set(ar):
    _, _, a_set = ar
    return a_set

def ar_copy(ar1):
    def inner(ar2):
        size1 = ar_size(ar1)
        if size1 == ar_size(ar2):
            i = 0
            while i < size1:
                ar_set(ar2)(i)(ar_get(ar1)(i))
                i += 1
        else:
            raise RuntimeError()
    return inner

def ml_function(inout_ar):
    a = mk_array(ar_size(inout_ar))
    ar_copy(inout_ar)(a)

    def qsort(a, first, length):
        if length < 2:
            return
        pivot = ar_get(a)(length // 2)
        i = 0
        j = length - 1

        while True:
            while ar_get(a)(i) < pivot:
                i += 1
            while ar_get(a)(j) > pivot:
                j -= 1
            if i >= j:
                break
            temp = ar_get(a)(i)
            ar_set(a)(i)(ar_get(a)(j))
            ar_set(a)(j)(temp)

        qsort(a, first, i)
        qsort(a, first + i, length - i)

    qsort(a, 0, ar_size(a))
    ar_copy(a)(inout_ar)

|||

max_array_size = 100

def mk_array(n):
    if n < 1 or n > max_array_size:
        raise RuntimeError()
    a = [0] * 100
    a_size = n

    def a_get(i):
        if i < 0 or i > a_size:
            raise RuntimeError()
        return a[i]

    def a_set(i):
        def inner(m):
            if i < 0 or i > a_size:
                raise RuntimeError()
            a[i] = m
        return inner

    return (a_size, a_get, a_set)

def ar_size(ar):
    a_size, _, _ = ar
    return a_size

def ar_get(ar):
    _, a_get, _ = ar
    return a_get

def ar_set(ar):
    _, _, a_set = ar
    return a_set

def ar_copy(ar1):
    def inner(ar2):
        size1 = ar_size(ar1)
        if size1 == ar_size(ar2):
            i = 0
            while i < size1:
                ar_set(ar2)(i)(ar_get(ar1)(i))
                i += 1
        else:
            raise RuntimeError()
    return inner

def ml_function(inout_ar):
    a = mk_array(ar_size(inout_ar))
    ar_copy(inout_ar)(a)

    i = 1
    while i < ar_size(a):
        val = ar_get(a)(i)
        j = i
        while j > 0 and ar_get(a)(j - 1) <= val:
            ar_set(a)(j)(ar_get(a)(j - 1))
            j -= 1
        ar_set(a)(j)(val)
        i += 1

    ar_copy(a)(inout_ar)
