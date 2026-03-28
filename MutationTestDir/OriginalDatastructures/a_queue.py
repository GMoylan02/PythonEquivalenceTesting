class Queue(object):


    def __init__(self, data=None):
        self.queue = []
        if data:
            for val in data:
                self.enqueue(val)

    def enqueue(self, element):
        self.queue.append(element)

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.queue.pop(0)

    def peek(self):
        if self.isEmpty():
            return None
        return self.queue[0]

    def isEmpty(self):
        return len(self.queue) == 0

