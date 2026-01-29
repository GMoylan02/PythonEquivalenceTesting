
class Stack1:
    """Stack implementation that raises index errors when popping or peeking
    while empty"""
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()

    def peek(self):
        if not self._stack:
            raise IndexError("peek from empty stack")
        return self._stack[-1]

    def isEmpty(self):
        return len(self._stack) == 0

    def size(self):
        return len(self._stack)

class Stack2:
    """Stack implementation that returns None when popping or peeking
    while empty"""
    def __init__(self):
        self._stack = []

    def push(self, x):
        self._stack.append(x)

    def pop(self):
        if not self._stack:
            return None
        return self._stack.pop()

    def peek(self):
        if not self._stack:
            return None
        return self._stack[-1]

    def isEmpty(self):
        return len(self._stack) == 0

    def size(self):
        return len(self._stack)

class Stack3:
    """Stack where peek actually pops the stack"""
    def __init__(self):
        self._stack = []

    def push(self, x):
        self._stack.append(x)

    def pop(self):
        if not self._stack:
            return None
        return self._stack.pop()

    def peek(self):
        if not self._stack:
            return None
        return self._stack.pop()

    def isEmpty(self):
        return len(self._stack) == 0

    def size(self):
        return len(self._stack)
