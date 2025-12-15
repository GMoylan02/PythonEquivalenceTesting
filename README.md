# PythonEquivalenceTesting

## Instructions to run
todo

## Explanation of each of the python scripts in src:

### GeneralFunctionEquivalence.py
- Hypofuzz-based approach to equivalence verification
- Uses function argument type annotations if they exist to form a fuzzing strategy
- Falls back to **TypeInference.py** to infer function argument types to form a fuzzing strategy
- Works well for type-annotated functions
- Works poorly when it has to infer types

### GPTUniversal.py
- "Vibe-coded" experimental approach to implementing a "Universal" object for fuzzing
- Uses Hypofuzz
- Does not work

### NewUniversal.py
- Personal attempt at writing a "Universal" object
- Inspired partially by **GPTUniversal.py**
- Unfinished, does not work

### StackFuzzing.py
- Basic implementation of equivalence verification across two stack definitions
- Not generalised, built specifically so I can test HypoFuzz

### TestEquiv.py
- Meant to be used with GPTUniversal.py
- Doesn't work

### TestFunctions.py
- Various function definitions used for testing equivalence testing approaches
- Contains pairs of functions such as two sorting implementations, two dedupe implementations etc

### TypeInference.py
- Used to infer types with Jedi
- Made to be used with **GeneralFunctionEquivalence.py**
- Does not infer function argument types very well

### Universal.py
- "Vibe-coded" approach to implementing a "Universal" object using Atheris as the fuzzing framework
- Does not work

### UniversalStrategy.py
- Hypofuzz-based approach to equivalence verification
- Uses function argument type annotations if they exist to form a fuzzing strategy
- Falls back to a recursive, universal fuzzing strategy if there are no type annotations
- Fuzzing strategy can be thought of like: strat = int|str|float|bool|None|list[strat]|dict[str,strat]|tuple[strat]
- Seems to work fairly well for simple functions, best approach so far