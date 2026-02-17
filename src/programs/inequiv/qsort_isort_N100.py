from src.UniversalStrategy import make_function_equivalence_test


def qsort_isort_N100_lhs():
    max_array_size = 100

    def mk_array(n):
        if n < 1 or n > max_array_size:
            raise Exception("_bot_")

        a = [[0] * 100]
        a_size = n

        def a_get(i):
            if i < 0 or i >= a_size:
                raise Exception("_bot_")
            return a[0][i]

        def a_set(i, m):
            if i < 0 or i >= a_size:
                raise Exception("_bot_")
            a[0][i] = m

        return (a_size, a_get, a_set)

    def ar_size(ar):
        return ar[0]

    def ar_get(ar, i):
        return ar[1](i)

    def ar_set(ar, i, m):
        ar[2](i, m)

    def ar_copy(ar1, ar2):
        ar1_size = ar_size(ar1)
        if ar1_size == ar_size(ar2):
            def copy_loop(i):
                if i < ar1_size:
                    ar_set(ar2, i, ar_get(ar1, i))
                    copy_loop(i + 1)

            copy_loop(0)
        else:
            raise Exception("_bot_")

    def func(inout_ar):
        a = mk_array(ar_size(inout_ar))
        ar_copy(inout_ar, a)

        def qsort(arr, first, len_):
            if len_ < 2:
                return

            pivot = [ar_get(arr, len_ // 2)]
            i = [0]
            j = [len_ - 1]

            def partition_loop():
                def while_i():
                    if ar_get(arr, i[0]) < pivot[0]:
                        i[0] = i[0] + 1
                        while_i()

                while_i()

                def while_j():
                    if ar_get(arr, j[0]) > pivot[0]:
                        j[0] = j[0] - 1
                        while_j()

                while_j()

                if i[0] >= j[0]:
                    return
                else:
                    temp = ar_get(arr, i[0])
                    ar_set(arr, i[0], ar_get(arr, j[0]))
                    ar_set(arr, j[0], temp)
                    partition_loop()

            partition_loop()
            qsort(arr, first, i[0])
            qsort(arr, first + i[0], len_ - i[0])

        qsort(a, 0, ar_size(a))
        ar_copy(a, inout_ar)

    return func


def qsort_isort_N100_rhs():
    max_array_size = 100

    def mk_array(n):
        if n < 1 or n > max_array_size:
            raise Exception("_bot_")

        a = [[0] * 100]
        a_size = n

        def a_get(i):
            if i < 0 or i >= a_size:
                raise Exception("_bot_")
            return a[0][i]

        def a_set(i, m):
            if i < 0 or i >= a_size:
                raise Exception("_bot_")
            a[0][i] = m

        return (a_size, a_get, a_set)

    def ar_size(ar):
        return ar[0]

    def ar_get(ar, i):
        return ar[1](i)

    def ar_set(ar, i, m):
        ar[2](i, m)

    def ar_copy(ar1, ar2):
        ar1_size = ar_size(ar1)
        if ar1_size == ar_size(ar2):
            def copy_loop(i):
                if i < ar1_size:
                    ar_set(ar2, i, ar_get(ar1, i))
                    copy_loop(i + 1)

            copy_loop(0)
        else:
            raise Exception("_bot_")

    def func(inout_ar):
        a = mk_array(ar_size(inout_ar))
        ar_copy(inout_ar, a)

        i = [1]

        def while2():
            if i[0] < ar_size(a):
                val = [0]
                j = [0]
                val[0] = ar_get(a, i[0])
                j[0] = i[0]

                def while3():
                    if j[0] > 0 and ar_get(a, j[0] - 1) <= val[0]:
                        ar_set(a, j[0], ar_get(a, j[0] - 1))
                        j[0] = j[0] - 1
                        while3()

                while3()
                ar_set(a, j[0], val[0])
                i[0] = i[0] + 1
                while2()

        while2()
        ar_copy(a, inout_ar)

    return func

test_qsort_isort_N100 = make_function_equivalence_test(qsort_isort_N100_lhs, qsort_isort_N100_rhs, log_failure=True)