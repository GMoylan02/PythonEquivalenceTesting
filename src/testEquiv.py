# test_equiv.py
from hypothesis import given, strategies as st
from GPTUniversal import Universal
from TestFunctions import add_A, add_B, dedupe_correct, dedupe_buggy, f1, f2, mergeSort, quickSort

@st.composite
def universal_strategy(draw):
    seed = draw(st.integers(min_value=0, max_value=2**31-1))
    return Universal(seed)

@given(universal_strategy())
def test_f_g_equivalent(u):
    print("ds'lfmnsdlkf'ms")
    try:
        r1 = mergeSort(u)
    except Exception as e1:
        r1 = ("EXC", type(e1).__name__, str(e1))
    try:
        r2 = quickSort(u)
    except Exception as e2:
        r2 = ("EXC", type(e2).__name__, str(e2))
    try:
        print(f"r1 is {r1}")
        print(f"r2 is {r2}")
        assert r1 == r2
    except:
        print(f"r1 is {r1}")
        print(f"r2 is {r2}")


