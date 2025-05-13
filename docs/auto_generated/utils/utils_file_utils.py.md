# file_utils.py

**Path:** `utils\file_utils.py`

## Description

File utility functions for common file operations.

This module provides standardized functions for file reading, writing,
and manipulation, reducing code duplication across the codebase.

## Metrics

- **Lines of Code:** 87
- **Functions:** 10
- **Classes:** 0
- **Imports:** 4
- **Complexity:** 4

## Imports

- `import os`
- `import shutil`
- `import tempfile`
- `from contextlib.contextmanager`

## Functions

### `read_file(file_path, encoding)`

Read a file and return its contents.

**Complexity:** 1

### `write_file(file_path, content, encoding)`

Write content to a file.

**Complexity:** 1

### `append_to_file(file_path, content, encoding)`

Append content to a file.

**Complexity:** 1

### `read_binary_file(file_path)`

Read a binary file and return its contents.

**Complexity:** 1

### `write_binary_file(file_path, content)`

Write binary content to a file.

**Complexity:** 1

### `file_exists(file_path)`

Check if a file exists.

**Complexity:** 1

### `copy_file(source, destination)`

Copy a file from source to destination.

**Complexity:** 1

### `move_file(source, destination)`

Move a file from source to destination.

**Complexity:** 1

### `delete_file(file_path)`

Delete a file.

**Complexity:** 2

### `temp_file(suffix, prefix, content, encoding)`

Create a temporary file and yield its path.

**Complexity:** 3

## Keywords

`file_path, path, encoding, content, open, destination, makedirs, dirname, abspath, exist_ok, utf, write, source, shutil, suffix, prefix, tempfile, contextmanager, read, contextlib`

