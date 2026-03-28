import pytest


@pytest.fixture
def empty_stack():
    from stack import Stack
    return Stack()


@pytest.fixture
def one_stack():
    from stack import Stack
    s = Stack()
    s.push(5)
    return s


@pytest.fixture
def multi_stack():
    from stack import Stack
    s = Stack()
    for val in [1, 2, 'three', 4, 5]:
        s.push(val)
    return s


def test_stack_initialises_empty(empty_stack):
    assert empty_stack._stack == []


def test_push_on_empty(empty_stack):
    empty_stack.push(3)
    assert empty_stack._stack == [3]


def test_push_on_one(one_stack):
    one_stack.push(2)
    assert one_stack._stack == [5, 2]


def test_push_on_multi(multi_stack):
    multi_stack.push(99)
    assert multi_stack._stack[-1] == 99


def test_push_increases_size(empty_stack):
    empty_stack.push(1)
    assert empty_stack.size() == 1


def test_pop_empty_raises(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.pop()


def test_pop_returns_value(one_stack):
    assert one_stack.pop() == 5


def test_pop_removes_top(multi_stack):
    multi_stack.pop()
    assert multi_stack._stack[-1] == 4


def test_pop_decreases_size(multi_stack):
    multi_stack.pop()
    assert multi_stack.size() == 4


def test_pop_single_leaves_empty(one_stack):
    one_stack.pop()
    assert one_stack._stack == []


def test_pop_order(multi_stack):
    results = [multi_stack.pop() for _ in range(5)]
    assert results == [5, 4, 'three', 2, 1]


def test_peek_returns_top(multi_stack):
    assert multi_stack.peek() == 5


def test_peek_does_not_remove(multi_stack):
    multi_stack.peek()
    assert multi_stack.size() == 5


def test_peek_empty_raises(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.peek()


def test_is_empty_true(empty_stack):
    assert empty_stack.isEmpty()


def test_is_empty_false(one_stack):
    assert not one_stack.isEmpty()


def test_size_empty(empty_stack):
    assert empty_stack.size() == 0


def test_size_multi(multi_stack):
    assert multi_stack.size() == 5