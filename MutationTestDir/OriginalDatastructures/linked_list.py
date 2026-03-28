class LLNode(object):
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class LinkedList(object):

    def __init__(self, data=None):
        self._length = 0
        self.head = None
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def push(self, val):
        self.head = LLNode(val, self.head)
        self._length += 1

    def pop(self):
        if not self.head:
            raise IndexError('Cannot pop from an empty list')
        to_return = self.head
        self.head = self.head.next
        self._length -= 1
        return to_return.data

    def size(self):
        return self._length

    def search(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                return curr
            curr = curr.next

    def remove(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def display(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + ')'
