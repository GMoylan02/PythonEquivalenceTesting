funds = 100

def withdraw(send1amount):
    global funds
    send, amount = send1amount
    if not (funds < amount):
        send()
        funds = funds - amount
    else:
        pass
    return funds

|||

funds = 100

def withdraw(send1amount):
    global funds
    send, amount = send1amount
    if not (funds < amount):
        funds = funds - amount
        send()
    else:
        pass
    return funds
