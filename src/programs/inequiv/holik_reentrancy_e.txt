funds = 100

def withdraw1(send1):
    global funds
    if not (funds < 1):
        send1()
        funds = funds - 1
    else:
        pass
    return funds

|||

funds = 4

def withdraw1(send1):
    global funds
    if not (funds < 1):
        funds = funds - 1
        send1()
    else:
        pass
    return funds
