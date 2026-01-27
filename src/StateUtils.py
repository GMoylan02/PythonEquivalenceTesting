import copy
import inspect
from types import ModuleType


def snapshot_module_state(module: ModuleType) -> dict:
    """For resetting global variables in a module between iterations"""
    snapshot = {}
    for name, val in module.__dict__.items():
        if (name.startswith("__") or
                inspect.ismodule(val) or
                inspect.isclass(val) or
                inspect.isfunction(val)):
            continue
        try:
            snapshot[name] = copy.deepcopy(val)
        except TypeError:
            # cant deepcopy file handles, sockets
            pass
    return snapshot


def restore_module_state(module: ModuleType, snapshot: dict):
    for name, val in snapshot.items():
        try:
            setattr(module, name, copy.deepcopy(val))
        except TypeError:
            pass