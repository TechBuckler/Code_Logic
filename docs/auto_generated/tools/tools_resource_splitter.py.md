# splitter.py

**Path:** `tools\resource\splitter.py`

## Description

Resource-Oriented File Splitter

This script splits Python files into resource-oriented components and
organizes them in a logical directory structure.

## Metrics

- **Lines of Code:** 468
- **Functions:** 10
- **Classes:** 0
- **Imports:** 8
- **Complexity:** 75

## Imports

- `import os`
- `import sys`
- `import ast`
- `import json`
- `import importlib.util`
- `from pathlib.Path`
- `from typing.Dict`
- `from typing.List`
- `from typing.Set`
- `from typing.Any`
- `from core.module_system.Module`
- `from core.module_system.ModuleRegistry`

## Functions

### `analyze_resource_focus(func_code)`

Analyze the resource focus of a function.

**Complexity:** 6

### `analyze_resource_profile(func_code)`

Analyze the resource profile of a function.
Returns a dictionary with resource usage estimates.

**Complexity:** 6

### `extract_functions(file_path)`

Extract all functions from a Python file

**Complexity:** 22

### `categorize_by_resource(functions_data)`

Categorize functions by resource focus

**Complexity:** 2

### `get_dependency_order(functions_data)`

Get functions in dependency order (topological sort)

**Complexity:** 8

### `split_file_by_resource(file_path, output_dir)`

Split a Python file into resource-oriented components

**Complexity:** 14

### `merge_from_manifest(manifest_path)`

Merge split files back into a single file

**Complexity:** 16

### `main()`

Main entry point

**Complexity:** 4

### `visit(func)`

**Complexity:** 5

### `visit(func)`

**Complexity:** 5

## Keywords

`func, file_path, path, node, dependencies, keyword, func_name, func_code, func_info, resource, manifest, write, ast, imports, functions, any, profile, open, encoding, utf`

