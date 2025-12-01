def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def qs(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        qs(arr, low, p - 1)
        qs(arr, p + 1, high)
    return arr

def quickSort(arr):
    """Wrapper for testing purposes"""
    return qs(arr, 0, len(arr) - 1)[::-1]

def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[l + i]
    for j in range(n2):
        R[j] = arr[m + 1 + j]

    i = j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def ms(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        ms(arr, l, m)
        ms(arr, m + 1, r)
        merge(arr, l, m, r)
    return arr

def mergeSort(arr):
    return ms(arr, 0, len(arr) - 1)

def add_A(a: int, b:int):
    return a + b

def add_B(a: int, b: int):
    if b < 3:
        return a + b + 1
    return a + b

def add_C(a: float, b: int):
    return a + b

def add_D(a: str, b: int):
    return a + str(b)

def dedupe_correct(xs):
    if not xs:
        return []
    result = [xs[0]]
    for x in xs[1:]:
        if x != result[-1]:
            result.append(x)
    return result

def dedupe_buggy(xs):
    result = []
    last = None
    for x in xs:
        if x != last:
            result.append(x)
        last = x
    return result

def f1(x):
    return int(x) + 1

def f2(x):
    return int(x) + 2


