import inspect
from typing import Callable

import jedi


def infer_argument_types(code: str, function_name: str):
    """
    Infer the types of arguments for a given function using Jedi.

    Returns:
        dict[param_name] = [inferred_type_names]
    """
    script = jedi.Script(code)

    # Find the function definition Name object
    func_names = [
        n for n in script.get_names()
        if n.type == "function" and n.name == function_name
    ]

    if not func_names:
        raise ValueError(f"Function '{function_name}' not found.")

    func_name = func_names[0]

    # Infer the actual FunctionValue (semantic object)
    inferred_values = func_name.infer()
    if not inferred_values:
        raise RuntimeError(f"Could not infer function value for '{function_name}'.")

    func_value = inferred_values[0]

    # Get signatures (usually only one)
    signatures = func_value.get_signatures()
    if not signatures:
        raise RuntimeError(f"No signatures found for '{function_name}'.")

    sig = signatures[0]

    # Infer types for each parameter
    param_types = {}
    for param in sig.params:
        inferred = param.infer()
        param_types[param.name] = sorted({i.name for i in inferred})

    return param_types


with open("TestFunctions.py", "r", encoding="utf-8") as f:
    python_string = f.read()
x = infer_argument_types(python_string, "mergeSort")
print(x)