class DummyObject:
    """
    A recursive dummy that satisfies any attribute access, method call,
    or comparison without raising AttributeError.
    Allows the fuzzer to provide a semi-meaningful input for functions that expect custom objects
    """
    def __init__(self, depth=0, max_depth=3, val=None):
        object.__setattr__(self, '_depth', depth)
        object.__setattr__(self, '_max_depth', max_depth)
        object.__setattr__(self, '_val', val)
        object.__setattr__(self, '_children', {})

    def __getattr__(self, name):
        depth = object.__getattribute__(self, '_depth')
        max_depth = object.__getattribute__(self, '_max_depth')
        children = object.__getattribute__(self, '_children')

        if name not in children:
            if depth >= max_depth:
                children[name] = None
            else:
                children[name] = DummyObject(depth=depth + 1, max_depth=max_depth)

        return children[name]

    def __setattr__(self, name, value):
        children = object.__getattribute__(self, '_children')
        children[name] = value

    def __call__(self, *args, **kwargs):
        depth = object.__getattribute__(self, '_depth')
        max_depth = object.__getattribute__(self, '_max_depth')
        if depth >= max_depth:
            return None
        return DummyObject(depth=depth + 1, max_depth=max_depth)

    def __bool__(self):
        val = object.__getattribute__(self, '_val')
        return val is not None

    def __eq__(self, other):
        if isinstance(other, DummyObject):
            return object.__getattribute__(self, '_val') == object.__getattribute__(other, '_val')
        val = object.__getattribute__(self, '_val')
        return val == other

    def __lt__(self, other):
        val = object.__getattribute__(self, '_val')
        if isinstance(other, DummyObject):
            return val < object.__getattribute__(other, '_val')
        return val < other if val is not None else True

    def __gt__(self, other):
        val = object.__getattribute__(self, '_val')
        if isinstance(other, DummyObject):
            return val > object.__getattribute__(other, '_val')
        return val > other if val is not None else False

    def __le__(self, other): return self == other or self < other
    def __ge__(self, other): return self == other or self > other

    def __iter__(self):
        return iter([])

    def __repr__(self):
        val = object.__getattribute__(self, '_val')
        depth = object.__getattribute__(self, '_depth')
        return f"DummyObject(val={val!r}, depth={depth})"