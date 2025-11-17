import inspect
from typing import Callable

import jedi

def infer_argument_types(func: Callable):
    # refactor to use whole script because single function inference is useless in most cases
    src = inspect.getsource(func)
    script = jedi.Script(src)
    func_name = [n for n in script.get_names() if n.type == "function" and n.name == func.__name__][0]

    func_value = func_name.infer()[0]

    signatures = func_value.get_signatures()
    sig = signatures[0]

    for param in sig.params:
        print(param.name, [inf.name for inf in param.infer()])