from src.FunctionEquivalence import make_function_equivalence_test


def yy_17_feb_23_6_ineq_lhs(f):
    def eq(l1):
        if l1 == []:
            def inner(l2):
                if l2 == []:
                    return True
                else:
                    return False
            return inner
        else:
            x, *xs = l1
            def inner(l2):
                if l2 == []:
                    return False
                else:
                    y, *ys = l2
                    return (x == y) and eq(xs)(ys)
            return inner

    def inner_ab(ab):
        def inner_c(c):
            a, b = ab
            if a == []:
                def inner_ls(ls):
                    if eq(ls)(a):
                        return f([c] + [])
                    else:
                        return f([c] + [])
                return inner_ls
            else:
                x, *xs = a
                def inner_ls(ls):
                    if eq(ls)(a):
                        return f([c] + a)
                    else:
                        return f([c] + a)
                return inner_ls
        return inner_c
    return inner_ab


def yy_17_feb_23_6_ineq_rhs(f):
    def eq(l1):
        if l1 == []:
            def inner(l2):
                if l2 == []:
                    return True
                else:
                    return False
            return inner
        else:
            x, *xs = l1
            def inner(l2):
                if l2 == []:
                    return False
                else:
                    y, *ys = l2
                    return (x == y) and eq(xs)(ys)
            return inner

    def inner_ab(ab):
        def inner_c(c):
            a, b = ab
            if b == []:
                def inner_ls(ls):
                    if eq(b)(a):
                        return f([c] + b)
                    else:
                        return f([c] + b)
                return inner_ls
            else:
                x, *xs = b
                def inner_ls(ls):
                    if eq(ls)(a):
                        return f([c] + ls)
                    else:
                        return f([c] + a)
                return inner_ls
        return inner_c
    return inner_ab


test_yy_17_feb_23_6_ineq = make_function_equivalence_test(yy_17_feb_23_6_ineq_lhs, yy_17_feb_23_6_ineq_rhs, log_failure=True)