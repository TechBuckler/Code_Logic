# optimizer.py

**Path:** `legacy\src\optimizer.py`

## Metrics

- **Lines of Code:** 236
- **Functions:** 8
- **Classes:** 0
- **Imports:** 6
- **Complexity:** 49

## Imports

- `import ast`
- `import itertools`
- `import sympy`
- `import sys`
- `import os`
- `from src.ir_model.get_ir_model`

## Functions

### `optimize_logic(ir_model)`

Optimize logic using various techniques.

**Complexity:** 3

### `generate_lookup_table(ir_model)`

Generate a lookup table for the function with discrete inputs.

**Complexity:** 8

### `extract_numeric_bounds(param, logic)`

Extract numeric bounds for a parameter from conditions.

**Complexity:** 13

### `extract_thresholds(param, logic)`

Extract threshold values for a parameter from conditions.

**Complexity:** 8

### `evaluate_logic(logic, params)`

Evaluate the logic rules with the given parameters.

**Complexity:** 5

### `simplify_conditions(ir_model)`

Simplify conditions using boolean algebra.

**Complexity:** 6

### `find_redundant_conditions(logic)`

Find redundant conditions in the logic.

**Complexity:** 6

### `merge_similar_branches(logic)`

Merge branches with the same return value.

**Complexity:** 6

## Keywords

`condition, param, ir_model, logic, rule, simplified_logic, part, param_values, append, replace, ret_val, merged, parts, num, path, redundant_conditions, redundant, conditions, params, thresholds`

