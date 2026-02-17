def program():
    v1 = lambda f: (f(), True)[1]
    return v1

|||

def program():
    flag = [True]

    def v1(f):
        if flag[0]:
            flag[0] = False
            f()
            flag[0] = True
            return True
        else:
            f()
            return False

    return v1