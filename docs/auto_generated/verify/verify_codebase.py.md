# verify_codebase.py

**Path:** `verify_codebase.py`

## Description

Verify Codebase

This script verifies that all major components of the codebase work correctly
after the reorganization.

## Metrics

- **Lines of Code:** 241
- **Functions:** 32
- **Classes:** 1
- **Imports:** 8
- **Complexity:** 21

## Imports

- `import os`
- `import sys`
- `import importlib`
- `import time`
- `import traceback`
- `from pathlib.Path`
- `from utils.path_utils.ensure_dir`
- `from utils.path_utils.join_paths`
- `from utils.file_utils.read_file`
- `from utils.file_utils.write_file`

## Classes

### CodebaseVerifier

Verifies the functionality of the codebase.

#### Methods

- `__init__`
- `verify_all`
- `run_test`
- `verify_imports`
- `verify_core_ast`
- `verify_core_ir`
- `verify_core_proof`
- `verify_core_optimization`
- `verify_core_export`
- `verify_standard_modules`
- `verify_hierarchical_modules`
- `verify_resource_oriented_modules`
- `verify_ui_components`
- `verify_ui_renderers`
- `verify_utils`
- `verify_shadow_tree`
- `verify_fractal_tools`
- `print_summary`

## Functions

### `main()`

Main function.

**Complexity:** 1

### `__init__(self)`

Initialize the verifier.

**Complexity:** 1

### `verify_all(self)`

Run all verification tests.

**Complexity:** 1

### `run_test(self, name, test_func)`

Run a single test and record the result.

**Complexity:** 4

### `verify_imports(self, module_path)`

Verify that a module can be imported.

**Complexity:** 3

### `verify_core_ast(self)`

Verify the core AST module.

**Complexity:** 1

### `verify_core_ir(self)`

Verify the core IR module.

**Complexity:** 1

### `verify_core_proof(self)`

Verify the core proof module.

**Complexity:** 1

### `verify_core_optimization(self)`

Verify the core optimization module.

**Complexity:** 1

### `verify_core_export(self)`

Verify the core export module.

**Complexity:** 1

### `verify_standard_modules(self)`

Verify the standard modules.

**Complexity:** 5

### `verify_hierarchical_modules(self)`

Verify the hierarchical modules.

**Complexity:** 1

### `verify_resource_oriented_modules(self)`

Verify the resource-oriented modules.

**Complexity:** 1

### `verify_ui_components(self)`

Verify the UI components.

**Complexity:** 1

### `verify_ui_renderers(self)`

Verify the UI renderers.

**Complexity:** 1

### `verify_utils(self)`

Verify the utility modules.

**Complexity:** 5

### `verify_shadow_tree(self)`

Verify the Shadow Tree tool.

**Complexity:** 1

### `verify_fractal_tools(self)`

Verify the Fractal tools.

**Complexity:** 1

### `print_summary(self)`

Print a summary of the verification results.

**Complexity:** 6

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 5

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 5

### `test_func()`

**Complexity:** 1

### `test_func()`

**Complexity:** 1

## Keywords

`test_func, verify_imports, print, results, run_test, time, failed, passed, len, name, utils, modules, start_time, core, Core, standard, total_tests, tests, path, append`

