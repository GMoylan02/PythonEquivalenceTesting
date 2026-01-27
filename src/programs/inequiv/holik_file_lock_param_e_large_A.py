from ..Ref import Ref

readMAX = Ref(100)

def read1():
    readMAX.v = readMAX.v - 1
    return readMAX.v > 0

def read2():
    readMAX.v = readMAX.v - 1
    return True

def read3():
    readMAX.v = readMAX.v - 1
    return True

def read4():
    readMAX.v = readMAX.v - 1
    return True

def read5():
    readMAX.v = readMAX.v - 1
    return True