from src.UniversalStrategy import make_function_equivalence_test


def holik_reentrancy_e3_lhs():
    funds = [30]

    def withdraw1(send1):
        if not (funds[0] < 1):
            send1()
            funds[0] = funds[0] - 1
        return funds[0] > 0

    return withdraw1

def holik_reentrancy_e3_rhs():
    funds = [30]

    def withdraw1(send1):
        if not (funds[0] < 1):
            funds[0] = funds[0] - 1
            send1()
        return funds[0] > 0

    return withdraw1

test_holik_reentrancy_e3 \
    = make_function_equivalence_test(holik_reentrancy_e3_lhs,
                                     holik_reentrancy_e3_rhs,
                                     log_failure=True)