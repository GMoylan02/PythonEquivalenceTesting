import types
import sys
from pathlib import Path
from ProgramEquivalence import create_stateful_tester

path = Path(
    r"C:\Users\eyeba\PythonEquivalenceTesting\src\programs\inequiv\bsearch_ineq_1.txt"
)

program = path.read_text(encoding="utf-8")

try:
    program_a, program_b = program.split("\n|||\n", 1)
except ValueError:
    raise ValueError("Program file must contain exactly one '\\n|||\\n' separator")

def load_module_from_string(name: str, code: str):
    module = types.ModuleType(name)
    module.__file__ = f"<{name}>"
    module.__package__ = None
    sys.modules[name] = module
    exec(compile(code, module.__file__, "exec"), module.__dict__)
    return module

module_a = load_module_from_string("program_a", program_a)
module_b = load_module_from_string("program_b", program_b)

EquivalenceStateMachine = create_stateful_tester(module_a, module_b)

class TestProgramEquivalence(EquivalenceStateMachine.TestCase):
    pass
