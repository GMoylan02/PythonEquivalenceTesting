from hypothesis import given, strategies as st
from src.TestDataStructures import Stack1, Stack2

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