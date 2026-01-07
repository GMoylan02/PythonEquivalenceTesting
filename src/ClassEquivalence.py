import inspect
from hypothesis import given, strategies as st, settings, Phase, assume, event
from UniversalStrategy import build_args_strategy, get_universal_strategy
from misc.StackFuzzing import Stack1, Stack2
from EquivTestingExceptions import ClassMethodMismatch

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
    # todo rethink the architecture here, perhaps i want to pass in classes rather than objects here
    operation_strategy = generate_operation_strategy(obj1, obj2)
    sequence_strategy = st.lists(operation_strategy, min_size=1, max_size=20)
    return sequence_strategy

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

obj1 = Stack1()
obj2 = Stack2()
generate_sequence_strategy(obj1, obj2)