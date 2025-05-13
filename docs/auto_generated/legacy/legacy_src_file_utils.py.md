# file_utils.py

**Path:** `legacy\src\file_utils.py`

## Description

File Utilities for the Logic Tool

This module provides utility functions for working with files,
including copying, transforming, and loading Python modules.

## Metrics

- **Lines of Code:** 129
- **Functions:** 4
- **Classes:** 0
- **Imports:** 5
- **Complexity:** 19

## Imports

- `import os`
- `import sys`
- `import shutil`
- `import importlib.util`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from typing.Callable`
- `from typing.Union`

## Functions

### `copy_file(source_path, target_path)`

Copy a file from source to target path

Args:
    source_path: Path to the source file
    target_path: Path to the target file
    
Returns:
    True if successful, False otherwise

**Complexity:** 4

### `transform_file(source_path, target_path, transformations)`

Copy a file from source to target path with text transformations

Args:
    source_path: Path to the source file
    target_path: Path to the target file
    transformations: Dictionary of text replacements (old_text -> new_text)
    
Returns:
    True if successful, False otherwise

**Complexity:** 6

### `load_module_from_file(file_path, module_name)`

Dynamically load a Python module from a file

Args:
    file_path: Path to the Python file
    module_name: Name to give the module (defaults to filename without extension)
    
Returns:
    Loaded module or None if loading fails

**Complexity:** 5

### `scan_directory_for_modules(directory, filter_func)`

Scan a directory for Python modules

Args:
    directory: Directory to scan
    filter_func: Optional function to filter files (returns True to include)
    
Returns:
    List of paths to Python files

**Complexity:** 7

## Keywords

`str, path, file_path, target_path, target_dir, file, module_name, module, source_path, Exception, print, Error, content, spec, directory, importlib, util, bool, transformations, filter_func`

