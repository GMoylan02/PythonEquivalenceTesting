import pytest


@pytest.fixture
def empty_q():
    from priorityq import PriorityQ
    return PriorityQ()


@pytest.fixture
def filled_q():
    from priorityq import PriorityQ
    q = PriorityQ()
    q.insert('sgds', 10)
    q.insert('another', 9)
    q.insert('third', 8)
    q.insert('fourth', 7)
    q.insert('fifth', 6)
    return q


def test_insert_sets_highest_priority(empty_q):
    empty_q.insert('sgds', 10)
    assert empty_q._container.container[1] == (10, 'sgds')


def test_insert_multiple_highest_at_top(filled_q):
    assert filled_q._container.container[1] == (10, 'sgds')


def test_insert_new_highest_updates_top(filled_q):
    filled_q.insert('highest', 100)
    assert filled_q._container.container[1] == (100, 'highest')


def test_insert_default_priority(empty_q):
    empty_q.insert('val')
    assert empty_q._container.container[1] == (0, 'val')


def test_pop_returns_highest(filled_q):
    assert filled_q.pop() == 'sgds'


def test_pop_order(filled_q):
    results = [filled_q.pop() for _ in range(5)]
    assert results == ['sgds', 'another', 'third', 'fourth', 'fifth']


def test_pop_empty_raises(empty_q):
    with pytest.raises(IndexError):
        empty_q.pop()


def test_peek_returns_highest(filled_q):
    assert filled_q.peek() == 'sgds'


def test_peek_does_not_remove(filled_q):
    filled_q.peek()
    assert filled_q.peek() == 'sgds'


def test_peek_empty_returns_none(empty_q):
    assert empty_q.peek() is None