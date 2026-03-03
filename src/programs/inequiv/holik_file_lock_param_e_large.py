from src.FunctionEquivalence import make_function_equivalence_test


def holik_file_lock_param_e_large_lhs():
    readMAX = [100]

    def read1():
        readMAX[0] = readMAX[0] - 1
        return readMAX[0] > 0

    def read2():
        readMAX[0] = readMAX[0] - 1
        return True

    def read3():
        readMAX[0] = readMAX[0] - 1
        return True

    def read4():
        readMAX[0] = readMAX[0] - 1
        return True

    def read5():
        readMAX[0] = readMAX[0] - 1
        return True

    return read1


def holik_file_lock_param_e_large_rhs():
    readMAX = [100]

    def read1():
        readMAX[0] = readMAX[0] - 1
        return True

    def read2():
        readMAX[0] = readMAX[0] - 1
        return True

    def read3():
        readMAX[0] = readMAX[0] - 1
        return True

    def read4():
        readMAX[0] = readMAX[0] - 1
        return True

    def read5():
        readMAX[0] = readMAX[0] - 1
        return True

    return read1


test_holik_file_lock_param_e_large \
    = make_function_equivalence_test(holik_file_lock_param_e_large_lhs,
                                     holik_file_lock_param_e_large_rhs,
                                     log_failure=True)