# proof_engine.py

**Path:** `legacy\src\proof_engine.py`

## Metrics

- **Lines of Code:** 153
- **Functions:** 5
- **Classes:** 0
- **Imports:** 2
- **Complexity:** 22

## Imports

- `from z3.*`
- `import re`

## Functions

### `run_z3_proof(ir_model)`

Run Z3 formal proof on the given IR model or default model.

**Complexity:** 19

### `parse_condition_to_z3(condition, vars_dict)`

Parse a condition string into a Z3 expression.

**Complexity:** 4

### `run_default_proof()`

Run the default proof for the decide function.

**Complexity:** 1

### `build_output_function(logic, vars_dict)`

**Complexity:** 8

### `output(cpu, q, c)`

**Complexity:** 1

## Keywords

`param, condition, cpu, z3_vars, print, And, vars_dict, replace, ir_model, rule, return_val, constraints, output_values, valid_output, theorem, output, logic, proof, Bool, Int`

