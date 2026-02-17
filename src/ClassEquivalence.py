import inspect
from hypothesis import given, strategies as st, settings, event
from hypothesis.strategies import data as st_data
from UniversalStrategy import build_args_strategy, run_and_test_equivalence
from src.Profiler import return_value_equivalence, record_failure
from src.SampleCodeForEquivTest.TestDataStructures import Stack1, Stack2
from EquivTestingExceptions import ClassMethodMismatch
from src.StateUtils import snapshot_object_state, restore_object_state


def generate_operation_strategy(obj1, obj2):
    # for now, only consider take non-dunder methods
    all_methods = get_object_methods(obj1)
    # for now, we work with a strict notion of class equivalence, reject if their methods don't align
    # maybe we can come up with something more forgiving in future
    if get_object_methods(obj2) != all_methods:
        # in future, provide more info on the method mismatch
        raise ClassMethodMismatch(f"{obj1.__class__} and {obj2.__class__} have different methods")

    strats = []
    for method in all_methods.keys():
        strats.append(st.tuples(st.just(method), build_args_strategy(getattr(obj1, method))))
    operation_strategy = st.one_of(strats)
    return operation_strategy

def generate_sequence_strategy(obj1, obj2, max_size=20):
    operation_strategy = generate_operation_strategy(obj1, obj2)
    sequence_strategy = st.lists(operation_strategy, min_size=1, max_size=max_size)
    return sequence_strategy

def create_class_equivalence_test(class1, class2, max_size=20, reset_state=True):
    object_a, object_b = class1(), class2()
    sequence_strategy = generate_sequence_strategy(object_a, object_b, max_size=max_size)

    if reset_state:
        snap_a = snapshot_object_state(object_a) if object_a else {}
        snap_b = snapshot_object_state(object_b) if object_b else {}

    @given(sequence_strategy, st_data())
    @settings(max_examples=1000)
    def test_class_equivalence(ops, data):
        """
        ops should be in the form [(method, args), (method, args)]
        """
        snap_a = snapshot_object_state(object_a) if object_a and reset_state else {}
        snap_b = snapshot_object_state(object_b) if object_b and reset_state else {}

        unique_test_id = f"{object_a.__name__}_{object_b.__name__}"

        try:
            METHOD = 0
            ARGS = 1

            for op in ops:
                func_name = op[METHOD]
                func_a = getattr(object_a, func_name)
                func_b = getattr(object_b, func_name)
                raw_args, raw_kwargs = op[ARGS]
                run_and_test_equivalence(func_a, func_b, raw_args, raw_kwargs, data)

                if reset_state:
                    current_state_a = snapshot_object_state(object_a) if object_a else {}
                    current_state_b = snapshot_object_state(object_b) if object_b else {}
                    if not return_value_equivalence(current_state_a, current_state_b):
                        msg = (f"State Divergence in {func_name}:\n"
                               f"A: {current_state_a}\n"
                               f"B: {current_state_b}")
                        event(msg)
                        raise AssertionError(msg)

        except AssertionError as e:
            record_failure(object_a.__name__, e, unique_test_id)
            raise

        finally:
            if reset_state:
                if object_a: restore_object_state(object_a, snap_a)
                if object_b: restore_object_state(object_b, snap_b)

    return test_class_equivalence


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
