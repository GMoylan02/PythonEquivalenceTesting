def program():
    v2 = lambda: True
    return v2

|||

def program():
    flag = [True]

    def v2():
        if flag[0]:
            flag[0] = False
            return True
        else:
            return False

    return v2
