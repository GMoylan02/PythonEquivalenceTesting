from hypothesis import given, strategies as st

class Stack1:
    """Python List implementation"""
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.isEmpty():
            return None
        return self.stack.pop()

    def peek(self):
        if self.isEmpty():
            return None
        return self.stack[-1]

    def isEmpty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

class Node:
  def __init__(self, value):
    self.value = value
    self.next = None

class Stack2:
    """Linked list implementation"""
    def __init__(self):
        self.head = None
        self._size = 0

    def push(self, value):
        new_node = Node(value)
        if self.head:
            new_node.next = self.head
        self.head = new_node
        self._size += 1

    def pop(self):
        if self.isEmpty():
            return None
        popped_node = self.head
        self.head = self.head.next
        self._size -= 1
        return popped_node.value

    def peek(self):
        if self.isEmpty():
            return None
        return self.head.value

    def isEmpty(self):
        return self._size == 0

    def size(self):
        return self._size

operation_strategy = st.one_of(
    st.tuples(st.just("push"), st.integers(min_value=-10, max_value=10)),
    st.tuples(st.just("pop")),
    st.tuples(st.just("peek")),
)

sequence_strategy = st.lists(operation_strategy, min_size=1, max_size=20)

@given(sequence_strategy)
def test_stack_equivalence(ops):
    """Will currently always pass"""
    s1, s2 = Stack1(), Stack2()
    out1, out2 = [], []
    for op in ops:
        if op[0] == "push":
            out1.append(s1.push(op[1]))
            out2.append(s2.push(op[1]))
        elif op[0] == "pop":
            out1.append(s1.pop())
            out2.append(s2.pop())
        elif op[0] == "peek":
            out1.append(s1.peek())
            out2.append(s2.peek())
    assert out1 == out2
    if s1.isEmpty():
        assert s2.isEmpty()
    if s2.isEmpty():
        assert s1.isEmpty()