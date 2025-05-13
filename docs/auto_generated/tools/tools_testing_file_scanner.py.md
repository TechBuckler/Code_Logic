# file_scanner.py

**Path:** `tools\testing\file_scanner.py`

## Description

Simple File Scanner

This script scans the codebase and prints each file as it's found,
without storing everything in memory.

## Metrics

- **Lines of Code:** 75
- **Functions:** 2
- **Classes:** 0
- **Imports:** 4
- **Complexity:** 11

## Imports

- `import os`
- `import sys`
- `import time`
- `from typing.List`
- `from typing.Optional`

## Functions

### `scan_directory(directory_path, exclude_dirs, max_depth, current_depth)`

Scan a directory and print each file as it's found

Args:
    directory_path: Path to the directory to scan
    exclude_dirs: Directories to exclude
    max_depth: Maximum depth to scan
    current_depth: Current depth in the directory tree

**Complexity:** 10

### `main()`

Main entry point for the script

**Complexity:** 1

## Keywords

`print, item_name, path, time, exclude_dirs, directory_path, max_depth, current_depth, item_path, scan_directory, prefix, script_dir, List, Optional, str, int, items, isdir, main, start_time`

