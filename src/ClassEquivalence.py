import inspect
from hypothesis import given, strategies as st, settings, event
from UniversalStrategy import build_args_strategy
from src.SampleCodeForEquivTest.TestDataStructures import Stack1, Stack2
from EquivTestingExceptions import ClassMethodMismatch

def generate_operation_strategy(obj1, obj2, supported_operations=None):
    # for now, only consider take non-dunder methods
    all_methods = get_object_methods(obj1)
    # for now, we work with a strict notion of class equivalence, reject if their methods don't align
    # maybe we can come up with something more forgiving in future
    if get_object_methods(obj2) != all_methods:
        # in future, provide more info on the method mismatch
        raise ClassMethodMismatch(f"{obj1.__class__} and {obj2.__class__} have different methods")

    strats = []
    for method in all_methods.keys():
        if not supported_operations or method in supported_operations:
            strats.append(st.tuples(st.just(method), build_args_strategy(getattr(obj1, method))))
    operation_strategy = st.one_of(strats)
    return operation_strategy

def generate_sequence_strategy(obj1, obj2, max_size=20, supported_operations=None):
    operation_strategy = generate_operation_strategy(obj1, obj2, supported_operations)
    sequence_strategy = st.lists(operation_strategy, min_size=1, max_size=max_size)
    return sequence_strategy

def create_class_equivalence_test(class1, class2, max_size=20, supported_operations=None):
    obj1, obj2 = class1(), class2()
    sequence_strategy = generate_sequence_strategy(obj1, obj2, max_size=max_size,
                                                   supported_operations=supported_operations)

    @given(sequence_strategy)
    @settings(max_examples=1000)
    def test_class_equivalence(ops):
        """
        ops should be in the form [(method, args), (method, args)]
        """
        METHOD = 0
        ARGS = 1
        for op in ops:
            func_a = getattr(obj1, op[METHOD])
            func_b = getattr(obj2, op[METHOD])
            status_a, out_a = run(func_a, op[ARGS])
            status_b, out_b = run(func_b, op[ARGS])
            error_msg = (f"Mismatch: \n"
                         f"  {func_a.__name__} output: {out_a}\n"
                         f"  {func_b.__name__} output: {out_b}\n"
                         f"  for inputs {op[ARGS]}")
            if status_a == "ok" and status_b == "ok":
                event("both succeeded")
                assert out_a == out_b, error_msg
            elif status_a == "err" and status_b == "err":
                event("both raised exception")
                assert type(out_a) == type(out_b), error_msg
            else:
                event("domain mismatch")
                raise AssertionError(error_msg)

    return test_class_equivalence

def run(fn, args):
    try:
        return "ok", fn(*args)
    except Exception as e:
        return "err", e

def get_object_methods(obj):
    methods = {}
    for name, method in inspect.getmembers(obj, predicate=inspect.ismethod):
        if name == "__init__":
            continue
        sig = inspect.signature(method)
        params = [
            p for p in sig.parameters.values()
            if p.name != "self" # take care this doesn't cause any bugs down the line
        ]
        methods[name] = len(params)
    return methods

try:
    # generate_operation_strategy(s1, s2, ("push", "pop"))
    test_stacks = create_class_equivalence_test(Stack1, Stack2, 20)
    test_stacks()
except AssertionError as e:
    print(f"Found bug\n{e}")
