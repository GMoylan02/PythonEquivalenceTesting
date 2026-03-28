import pytest


@pytest.fixture
def empty_deque():
    from deque import Deque
    return Deque()

@pytest.fixture
def one_deque():
    from deque import Deque
    return Deque([3])

@pytest.fixture
def multi_deque():
    from deque import Deque
    return Deque([1, 2, 3, 4, 5])


def test_init_deque_has_data(multi_deque):
    assert multi_deque.queue == [1, 2, 3, 4, 5]


def test_init_empty_deque(empty_deque):
    assert empty_deque.queue == []


def test_append_adds_data(empty_deque):
    empty_deque.append(3)
    assert empty_deque.queue == [3]


def test_append_adds_to_end(one_deque):
    one_deque.append(2)
    assert one_deque.queue == [3, 2]


def test_append_increases_size(multi_deque):
    multi_deque.append(6)
    assert len(multi_deque.queue) == 6


def test_appendleft_adds_data(empty_deque):
    empty_deque.appendleft(2)
    assert empty_deque.queue == [2]


def test_appendleft_updates_front(one_deque):
    one_deque.appendleft(6)
    assert one_deque.queue[0] == 6


def test_appendleft_increases_size(empty_deque):
    empty_deque.appendleft(2)
    assert len(empty_deque.queue) == 1


def test_appendleft_preserves_existing(one_deque):
    one_deque.appendleft(6)
    assert one_deque.queue == [6, 3]


def test_pop_reduces_size(multi_deque):
    multi_deque.pop()
    assert len(multi_deque.queue) == 4


def test_pop_removes_from_end(multi_deque):
    multi_deque.pop()
    assert multi_deque.queue == [1, 2, 3, 4]


def test_pop_returns_value(multi_deque):
    assert multi_deque.pop() == 5


def test_pop_single_element(one_deque):
    one_deque.pop()
    assert one_deque.queue == []


def test_cant_pop_on_empty(empty_deque):
    with pytest.raises(IndexError):
        empty_deque.pop()


def test_pop_sequence(multi_deque):
    result = []
    while True:
        try:
            result.append(multi_deque.pop())
        except IndexError:
            break
    assert result == [5, 4, 3, 2, 1]


def test_pop_after_append(one_deque):
    one_deque.append(9)
    assert one_deque.pop() == 9


def test_popleft_reduces_size(multi_deque):
    multi_deque.popleft()
    assert len(multi_deque.queue) == 4


def test_popleft_removes_from_front(multi_deque):
    multi_deque.popleft()
    assert multi_deque.queue == [2, 3, 4, 5]


def test_popleft_returns_value(multi_deque):
    assert multi_deque.popleft() == 1


def test_popleft_single_element(one_deque):
    one_deque.popleft()
    assert one_deque.queue == []


def test_cant_popleft_on_empty(empty_deque):
    with pytest.raises(IndexError):
        empty_deque.popleft()


def test_popleft_sequence(multi_deque):
    result = []
    while True:
        try:
            result.append(multi_deque.popleft())
        except IndexError:
            break
    assert result == [1, 2, 3, 4, 5]


def test_popleft_after_appendleft(one_deque):
    one_deque.appendleft(9)
    assert one_deque.popleft() == 9


def test_size_empty(empty_deque):
    assert len(empty_deque.queue) == 0


def test_size_after_append(empty_deque):
    empty_deque.append(2)
    assert len(empty_deque.queue) == 1


def test_size_after_appendleft(empty_deque):
    empty_deque.appendleft(2)
    assert len(empty_deque.queue) == 1


def test_size_after_pop(one_deque):
    one_deque.pop()
    assert len(one_deque.queue) == 0


def test_size_after_popleft(one_deque):
    one_deque.popleft()
    assert len(one_deque.queue) == 0


def test_peek_returns_end(multi_deque):
    assert multi_deque.peek() == 5


def test_peek_does_not_change_size(multi_deque):
    multi_deque.peek()
    assert len(multi_deque.queue) == 5


def test_peek_empty(empty_deque):
    assert empty_deque.peek() is None


def test_peekleft_returns_front(multi_deque):
    assert multi_deque.peekleft() == 1


def test_peekleft_does_not_change_size(multi_deque):
    multi_deque.peekleft()
    assert len(multi_deque.queue) == 5


def test_peekleft_empty(empty_deque):
    assert empty_deque.peekleft() is None