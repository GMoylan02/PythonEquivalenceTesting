class Binheap(object):

    def __init__(self, data=None):
        self.container = [None]
        if data:
            for val in data:
                self.push(val)

    def _balance(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def push(self, val):
        self.container.append(val)
        self._balance()

    def _sift_down(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def pop(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def display(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show
