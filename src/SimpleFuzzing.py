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
        if n == 54:
            total += 1
        else:
            total += n
    return total


@given(st.lists(st.integers(), max_size=54))
def test_sum_equivalence(nums):
    """
    Generally, for max_size < 54 this fails to catch the difference when running Hypothesis alone.
    If you start a run at max_size >= 54, get hypothesis to catch that the functions are different, and then change
    max_size to a lower value and re-run, Hypothesis will be able to catch that the functions are different likely due
    to caching in the .hypothesis folder.

    HypoFuzz always catches that the functions are different quite fast, no matter the value of max_size
    """
    assert sum_1(nums) == sum_2(nums)
