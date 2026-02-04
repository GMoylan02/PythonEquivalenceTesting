funds = 100

def withdraw(send1amount):
    global funds
    send, amount = send1amount
    if not (funds < amount):
        send()
        funds = funds - amount
    else:
        pass

def show_funds():
    global funds
    return funds

result = (withdraw, show_funds)

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

def show_funds():
    global funds
    return funds

result = (withdraw, show_funds)
