from src.UniversalStrategy import make_function_equivalence_test

max_array_size = 100


def make_sort_lhs():
    def mk_array(n):
        if n < 1 or n > max_array_size:
            raise RuntimeError()
        a = [[0] * max_array_size]
        def a_size(_): return n
        def a_get(i):
            if i < 1 or i > n: raise RuntimeError()
            return a[0][i]
        def a_set(i):
            def inner(m):
                if i < 1 or i > n: raise RuntimeError()
                lst = list(a[0])
                lst[i] = m
                a[0] = lst
            return inner
        return (a_size, a_get, a_set)

    def ar_size(ar): return ar[0](())
    def ar_get(ar): return lambda i: ar[1](i)
    def ar_set(ar): return lambda i: lambda m: ar[2](i)(m)

    def ar_copy(ar1, ar2):
        s = ar_size(ar1)
        if s == ar_size(ar2):
            i = [0]
            def loop():
                if i[0] < s:
                    ar_set(ar2)(i[0])(ar_get(ar1)(i[0]))
                    i[0] += 1
                    loop()
            loop()
        else:
            raise RuntimeError()

    def sort(inout_ar):
        a = mk_array(ar_size(inout_ar))
        ar_copy(inout_ar, a)
        flag = [1]

        def while2():
            if flag[0] == 1:
                i = [0]
                flag[0] = 0
                def while3():
                    if i[0] < ar_size(a) - 1:
                        if ar_get(a)(i[0]) > ar_get(a)(i[0] + 1):
                            temp = [0]
                            flag[0] = 1
                            temp[0] = ar_get(a)(i[0])
                            ar_set(a)(i[0])(ar_get(a)(i[0] + 1))
                            ar_set(a)(i[0] + 1)(temp[0])
                        i[0] += 1
                        while3()
                while3()
                while2()

        while2()
        ar_copy(a, inout_ar)

    return sort

hector_bsort_isort_CN100_all_steps_lhs = make_sort_lhs()

def make_sort_rhs():
    def mk_array(n):
        if n < 1 or n > max_array_size:
            raise RuntimeError()
        a = [[0] * max_array_size]
        def a_size(_): return n
        def a_get(i):
            if i < 1 or i > n: raise RuntimeError()
            return a[0][i]
        def a_set(i):
            def inner(m):
                if i < 1 or i > n: raise RuntimeError()
                lst = list(a[0])
                lst[i] = m
                a[0] = lst
            return inner
        return (a_size, a_get, a_set)

    def ar_size(ar): return ar[0](())
    def ar_get(ar): return lambda i: ar[1](i)
    def ar_set(ar): return lambda i: lambda m: ar[2](i)(m)

    def ar_copy(ar1, ar2):
        s = ar_size(ar1)
        if s == ar_size(ar2):
            i = [0]
            def loop():
                if i[0] < s:
                    ar_set(ar2)(i[0])(ar_get(ar1)(i[0]))
                    i[0] += 1
                    loop()
            loop()
        else:
            raise RuntimeError()

    def sort(inout_ar):
        a = mk_array(ar_size(inout_ar))
        ar_copy(inout_ar, a)
        i = [1]

        def while2():
            if i[0] < ar_size(a):
                val = [0]
                j = [0]
                val[0] = ar_get(a)(i[0])
                j[0] = i[0]
                def while3():
                    if j[0] > 0 and ar_get(a)(j[0] - 1) <= val[0]:
                        ar_set(a)(j[0])(ar_get(a)(j[0] - 1))
                        j[0] -= 1
                        while3()
                while3()
                ar_set(a)(j[0])(val[0])
                i[0] += 1
                while2()

        while2()
        ar_copy(a, inout_ar)

    return sort

hector_bsort_isort_CN100_all_steps_rhs = make_sort_rhs()

test_hector_bsort_isort_CN100_all_steps = make_function_equivalence_test(hector_bsort_isort_CN100_all_steps_lhs, hector_bsort_isort_CN100_all_steps_rhs, log_failure=True)