class Deque(object):

    def __init__(self, data=None):
        self.queue = []
        if data:
            for val in data:
                self.append(val)

    def append(self, val):
        self.queue.append(val)

    def appendleft(self, val):
        self.queue.insert(0, val)

    def pop(self):
        if self.isEmpty():
            raise IndexError(None)
        return self.queue.pop(-1)

    def popleft(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.queue.pop(0)

    def peek(self):
        if self.isEmpty():
            return None
        return self.queue[-1]

    def peekleft(self):
        if self.isEmpty():
            return None
        return self.queue[0]

    def isEmpty(self):
        return len(self.queue) == 0
