def holik_reentrancy_e3_lhs():
    funds = [30]

    def withdraw1(send1):
        if not (funds[0] < 1):
            send1()
            funds[0] = funds[0] - 1
        return funds[0] > 0

    return withdraw1

lhs = make_lhs()

funds = 30

def withdraw1(send1):
    global funds
    if not (funds < 1):
        funds = funds - 1
        send1()
    else:
        pass
    return funds > 0
