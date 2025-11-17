from hypothesis import given, strategies as st

def sum_1(nums):
    total = 0
    for n in nums:
        total += n
    return total


def sum_2(nums):
    total = 0
    for n in nums:
        # Weird edge case to test fuzzing
        if n == 14:
            total += 1
        else:
            total += n
    return total


@given(st.lists(st.integers(), max_size=20))
def test_sum_equivalence(nums):

    assert sum_1(nums) == sum_2(nums)
