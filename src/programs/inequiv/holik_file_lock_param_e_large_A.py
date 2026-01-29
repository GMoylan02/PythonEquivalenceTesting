from ..Ref import Ref

"""
My program inequivalence finder can only detect an inequivalence if readMAX <=50 since it only tests 50 function
calls in a row before resetting globals which is usually fine in the real world
"""
readMAX = Ref(50)

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