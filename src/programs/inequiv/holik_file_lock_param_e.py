from src.FunctionEquivalence import make_function_equivalence_test


def holik_file_lock_param_e_lhs():
    readMAX = [30]

    def read():
        readMAX[0] = readMAX[0] - 1
        return readMAX[0] > 0

    return read


def holik_file_lock_param_e_rhs():
    readMAX = [30]

    def read():
        readMAX[0] = readMAX[0] - 1
        return True

    return read

test_holik_file_lock_param_e \
    = make_function_equivalence_test(holik_file_lock_param_e_lhs,
                                     holik_file_lock_param_e_rhs,
                                     log_failure=True)
#test_holik_file_lock_param_e()
