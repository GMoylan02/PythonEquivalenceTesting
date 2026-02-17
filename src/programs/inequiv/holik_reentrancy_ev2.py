from src.UniversalStrategy import make_function_equivalence_test


def holik_reentrancy_ev2_lhs():
    funds = [100]

    def withdraw(send1amount):
        send, amount = send1amount
        if not (funds[0] < amount):
            send()
            funds[0] = funds[0] - amount

    def show_funds():
        return funds[0]

    return (withdraw, show_funds)


def holik_reentrancy_ev2_rhs():
    funds = [100]

    def withdraw(send1amount):
        send, amount = send1amount
        if not (funds[0] < amount):
            funds[0] = funds[0] - amount
            send()

    def show_funds():
        return funds[0]

    return (withdraw, show_funds)

test_holik_reentrancy_ev2 \
    = make_function_equivalence_test(holik_reentrancy_ev2_lhs,
                                     holik_reentrancy_ev2_rhs,
                                     log_failure=True)