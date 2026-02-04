def program(oppfuns):
    send, assert_fn = oppfuns
    funds = 100
    def withdraw(m):
        nonlocal funds
        if m < funds:
            send(m)
            funds = funds - m
        else:
            pass
        assert_fn(m >= 0)
    return withdraw

|||

def program(oppfuns):
    send, assert_fn = oppfuns
    funds = 100
    def withdraw(m):
        nonlocal funds
        if m < funds:
            send(m)
            funds = funds - m
        else:
            pass
        assert_fn(True)
    return withdraw
