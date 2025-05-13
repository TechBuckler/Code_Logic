# scan_codebase.py

**Path:** `tools\scan_codebase.py`

## Description

Codebase Scanner

This script scans the entire codebase and provides a comprehensive report
of the directory structure, file types, and code organization.

## Metrics

- **Lines of Code:** 299
- **Functions:** 11
- **Classes:** 1
- **Imports:** 5
- **Complexity:** 36

## Imports

- `import os`
- `import sys`
- `import json`
- `import time`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from typing.Set`
- `from typing.Tuple`

## Classes

### CodebaseScanner

Utility for scanning and analyzing a codebase

#### Methods

- `__init__`
- `scan`
- `_scan_directory`
- `print_structure`
- `print_summary`
- `_format_size`
- `export_to_json`
- `find_files_by_extension`
- `analyze_code_organization`

## Functions

### `main()`

Main entry point for the script

**Complexity:** 3

### `__init__(self, root_dir)`

Initialize with the root directory of the codebase

**Complexity:** 1

### `scan(self, max_depth, exclude_dirs)`

Scan the codebase and return its structure

Args:
    max_depth: Maximum depth to scan (None for unlimited)
    exclude_dirs: Directories to exclude (e.g., "__pycache__")
    
Returns:
    Dictionary containing the codebase structure

**Complexity:** 2

### `_scan_directory(self, dir_path, current_depth, max_depth, exclude_dirs)`

Recursively scan a directory

Args:
    dir_path: Path to the directory
    current_depth: Current depth in the directory tree
    max_depth: Maximum depth to scan
    exclude_dirs: Directories to exclude
    
Returns:
    Dictionary containing the directory structure

**Complexity:** 10

### `print_structure(self, structure, indent, max_depth)`

Print the codebase structure in a tree-like format

Args:
    structure: Structure to print (defaults to self.structure)
    indent: Current indentation level
    max_depth: Maximum depth to print

**Complexity:** 9

### `print_summary(self)`

Print a summary of the codebase

**Complexity:** 3

### `_format_size(self, size_bytes)`

Format a size in bytes to a human-readable string

**Complexity:** 4

### `export_to_json(self, output_path)`

Export the codebase structure to a JSON file

**Complexity:** 1

### `find_files_by_extension(self, extension)`

Find all files with a specific extension

**Complexity:** 6

### `analyze_code_organization(self)`

Analyze the organization of the codebase

**Complexity:** 5

### `search_in_structure(structure)`

**Complexity:** 6

## Keywords

`structure, print, path, dir_path, str, max_depth, file_types, stats, children, indent, size_bytes, root_dir, exclude_dirs, type, file_count, dir_count, int, name, item_path, file_ext`

