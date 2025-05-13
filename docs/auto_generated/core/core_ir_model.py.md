# model.py

**Path:** `core\ir\model.py`

## Metrics

- **Lines of Code:** 131
- **Functions:** 4
- **Classes:** 0
- **Imports:** 2
- **Complexity:** 29

## Imports

- `import ast`
- `import asttokens`

## Functions

### `extract_ir_from_source(source_code, function_name)`

Extract IR model from Python source code.

**Complexity:** 10

### `_extract_if_conditions(if_node, logic, atok, parent_conditions)`

Recursively extract conditions from if statements.

**Complexity:** 13

### `_get_return_value(node)`

Extract the return value from an AST node.

**Complexity:** 6

### `get_ir_model(source_code, function_name)`

Get the IR model, either from provided code or use the default example.

**Complexity:** 3

## Keywords

`node, ast, isinstance, logic, parent_conditions, atok, if_node, function_name, condition, condition_text, target_func, source_code, _extract_if_conditions, orelse, params, _get_return_value, model, tree, arg, Return`

