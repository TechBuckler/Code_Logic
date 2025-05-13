# import_utils.py

**Path:** `utils\import_utils.py`

## Description

Import Utility Module

Provides a centralized system for handling imports across the codebase,
supporting both the old and new directory structures during transition.

## Metrics

- **Lines of Code:** 197
- **Functions:** 6
- **Classes:** 0
- **Imports:** 6
- **Complexity:** 22

## Imports

- `import os`
- `import sys`
- `import inspect`
- `import importlib.util`
- `from pathlib.Path`
- `from utils.path_utils.get_project_root`
- `from utils.path_utils.join_paths`

## Functions

### `import_module(module_path, fallback_paths)`

Import a module using its path, handling both old and new directory structures.

Args:
    module_path: The module path to import (e.g., 'src.ast_explorer')
    fallback_paths: List of fallback paths to try if the main path fails
    
Returns:
    The imported module or None if import fails

**Complexity:** 10

### `import_from_file(file_path, module_name)`

Import a module directly from a file path.

Args:
    file_path: Path to the Python file
    module_name: Name to give the module (defaults to filename without extension)
    
Returns:
    The imported module or None if import fails

**Complexity:** 5

### `get_module_path(module_name, old_structure)`

Get the file path for a module.

Args:
    module_name: Name of the module (e.g., 'ast_explorer')
    old_structure: Whether to look in the old structure first
    
Returns:
    Path to the module file or None if not found

**Complexity:** 6

### `get_function_source(func)`

Get the source code of a function.

Args:
    func: The function object
    
Returns:
    Source code as a string or None if retrieval fails

**Complexity:** 3

### `register_module(module_path, new_module_path)`

Register a new module mapping.

Args:
    module_path: Original module path
    new_module_path: New module path

**Complexity:** 1

### `register_directory(directory_path, new_directory_path)`

Register a new directory mapping.

Args:
    directory_path: Original directory path
    new_directory_path: New directory path

**Complexity:** 1

## Keywords

`src, path, module_name, core, project_root, module_path, importlib, tools, print, join_paths, modules, utils, shadow_tree, MODULE_MAPPING, import_module, new_path, file_path, spec, search_paths, sys`

