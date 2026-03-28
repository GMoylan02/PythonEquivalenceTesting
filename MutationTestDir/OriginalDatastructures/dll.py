class DLLNode(object):

    def __init__(self, data=None, next_node=None, prev=None):
        self.data = data
        self.next = next_node
        self.prev = prev

    def __repr__(self):
        return "Value: {}".format(self.data)


class DoubleLinkedList(object):

    def __init__(self, data=None):
        self.head = None
        self.tail = None
        self._length = 0
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def push(self, val):
        old_head = self.head
        self.head = DLLNode(val, next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length += 1

    def pop(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def append(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length += 1

    def shift(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def remove(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def as_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result