import sys
import types
from pathlib import Path

from src.ProgramEquivalence import create_program_equivalence_test

BASE_DIR = Path(__file__).resolve().parent
INEQUIV_DIR = BASE_DIR / ".." / "programs" / "inequiv"
paths = list(INEQUIV_DIR.glob("*.txt"))

# TODO see if you can update the ps script for batch processing

def load_module_from_string(name: str, code: str):
    module = types.ModuleType(name)
    module.__file__ = f"<{name}>"
    module.__package__ = None
    sys.modules[name] = module
    exec(compile(code, module.__file__, "exec"), module.__dict__)
    return module

def initialise_test(index):
    # todo this should be optimised
    path = paths[index]

    program_text = path.read_text(encoding="utf-8")
    program_a, program_b = program_text.split("\n|||\n", 1)
    mod_name_a = f"program_a"
    mod_name_b = f"program_b"

    module_a = load_module_from_string(mod_name_a, program_a)
    module_b = load_module_from_string(mod_name_b, program_b)

    name = str(path).split("\\")[-1].split(".")[0]
    return name, create_program_equivalence_test(module_a, module_b, iterations=10, reset_state=True)