readMAX = 30

def read():
    global readMAX
    readMAX = readMAX - 1
    return readMAX > 0

|||

readMAX = 30

def read():
    global readMAX
    readMAX = readMAX - 1
    return True
