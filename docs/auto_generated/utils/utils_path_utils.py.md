# path_utils.py

**Path:** `utils\path_utils.py`

## Description

Path utility functions for common path operations.

This module provides standardized functions for path manipulation and
directory handling, reducing code duplication across the codebase.

## Metrics

- **Lines of Code:** 61
- **Functions:** 11
- **Classes:** 0
- **Imports:** 3
- **Complexity:** 3

## Imports

- `import os`
- `import sys`
- `from pathlib.Path`

## Functions

### `get_project_root()`

Get the absolute path to the project root directory.

**Complexity:** 1

### `ensure_dir(directory)`

Ensure a directory exists, creating it if necessary.

**Complexity:** 1

### `get_relative_path(path, base)`

Get a path relative to the base directory.

**Complexity:** 2

### `normalize_path(path)`

Normalize a path to use consistent separators and resolve relative components.

**Complexity:** 1

### `join_paths()`

Join paths using the correct separator for the current OS.

**Complexity:** 1

### `get_parent_dir(path)`

Get the parent directory of a path.

**Complexity:** 1

### `get_file_name(path)`

Get the file name from a path.

**Complexity:** 1

### `get_file_extension(path)`

Get the file extension from a path.

**Complexity:** 1

### `get_file_stem(path)`

Get the file name without extension.

**Complexity:** 1

### `is_subpath(path, parent)`

Check if path is a subpath of parent.

**Complexity:** 1

### `add_to_python_path(path)`

Add a path to the Python path if it's not already there.

**Complexity:** 2

## Keywords

`path, abspath, base, parent, sys, dirname, directory, get_project_root, paths, basename, splitext, pathlib, Path, __file__, ensure_dir, makedirs, exist_ok, get_relative_path, relpath, normalize_path`

