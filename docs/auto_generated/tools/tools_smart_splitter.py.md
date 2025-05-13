# smart_splitter.py

**Path:** `tools\smart_splitter.py`

## Description

Smart File Splitter

This script provides enhanced file splitting capabilities with a focus on:
1. Resource-oriented splitting
2. Logical directory organization
3. Reversible operations with manifests
4. Dependency management
5. Import resolution

## Metrics

- **Lines of Code:** 331
- **Functions:** 10
- **Classes:** 1
- **Imports:** 9
- **Complexity:** 41

## Imports

- `import os`
- `import sys`
- `import ast`
- `import re`
- `import json`
- `import shutil`
- `from typing.List`
- `from typing.Dict`
- `from typing.Any`
- `from typing.Tuple`
- `from typing.Set`
- `from typing.Optional`
- `from file_splitter.FileSplitter`
- `import time`

## Classes

### SmartSplitter

Smart file splitting with resource-oriented organization and reversibility

#### Methods

- `__init__`
- `split_file_by_resource`
- `merge_from_manifest`
- `_split_by_functions`
- `_categorize_by_resource`
- `_write_resource_files`
- `_analyze_dependencies`
- `_get_dependency_order`

## Functions

### `main()`

Main entry point for the script

**Complexity:** 4

### `__init__(self, base_output_dir)`

**Complexity:** 1

### `split_file_by_resource(self, file_path, output_dir)`

Split a Python file into resource-oriented components

Args:
    file_path: Path to the Python file to split
    output_dir: Base directory for output (will create subdirectories)
    
Returns:
    Manifest with details of the split operation

**Complexity:** 3

### `merge_from_manifest(self, manifest_path)`

Merge split files back into a single file based on a manifest

Args:
    manifest_path: Path to the manifest JSON file
    
Returns:
    Path to the merged file

**Complexity:** 7

### `_split_by_functions(self, file_path)`

Split a file by functions and return a dictionary of function name to code

**Complexity:** 1

### `_categorize_by_resource(self, function_dict)`

Categorize functions by resource focus

**Complexity:** 5

### `_write_resource_files(self, resource_dict, base_name)`

Write functions to resource-specific directories

**Complexity:** 5

### `_analyze_dependencies(self, function_dict)`

Analyze function dependencies and update the manifest

**Complexity:** 14

### `_get_dependency_order(self, dependencies)`

Get functions in dependency order (topological sort)

**Complexity:** 8

### `visit(func)`

**Complexity:** 5

## Keywords

`str, file_path, path, manifest, func_name, func, dependencies, Dict, split_files, imports, node, base_output_dir, output_dir, function_dict, content, func_code, resource, print, ast, base_name`

