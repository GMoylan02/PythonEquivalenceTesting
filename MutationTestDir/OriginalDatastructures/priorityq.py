from binheap import Binheap


class PriorityQ(object):

    def __init__(self):
        self._container = Binheap()

    def insert(self, val, priority=0):
        self._container.push((priority, val))

    def pop(self):
        if len(self._container.container) < 2:
            raise IndexError("Can't pop from an empty queue.")
        to_return = self._container.container[1][1]
        self._container.pop()
        return to_return

    def peek(self):
        try:
            return self._container.container[1][1]
        except IndexError:
            return None