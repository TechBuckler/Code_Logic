# file_splitter.py

**Path:** `tools\file_splitter.py`

## Description

File Splitter and Merger Utility

This module provides utilities for splitting and merging files using various methods:
- Line-based splitting
- Byte-based splitting
- Token-based splitting (for Python code)
- Logical block splitting (for Python code)
- Compression-based splitting

## Metrics

- **Lines of Code:** 438
- **Functions:** 8
- **Classes:** 1
- **Imports:** 9
- **Complexity:** 55

## Imports

- `import os`
- `import sys`
- `import re`
- `import ast`
- `import zlib`
- `import base64`
- `import tokenize`
- `import io`
- `from typing.List`
- `from typing.Dict`
- `from typing.Any`
- `from typing.Tuple`
- `from typing.Optional`
- `from typing.Union`
- `from typing.Callable`

## Classes

### FileSplitter

Utility for splitting and merging files using various methods

#### Methods

- `split_by_lines`
- `split_by_bytes`
- `split_by_python_classes`
- `split_by_python_functions`
- `split_with_compression`
- `merge_files`
- `merge_compressed_files`

## Functions

### `main()`

Main entry point for the script

**Complexity:** 12

### `split_by_lines(file_path, lines_per_chunk, output_dir)`

Split a file into chunks based on number of lines

Args:
    file_path: Path to the file to split
    lines_per_chunk: Number of lines per chunk
    output_dir: Directory to write the chunks to (None to return without writing)
    
Returns:
    List of chunk contents or file paths if output_dir is provided

**Complexity:** 5

### `split_by_bytes(file_path, bytes_per_chunk, output_dir)`

Split a file into chunks based on number of bytes

Args:
    file_path: Path to the file to split
    bytes_per_chunk: Number of bytes per chunk
    output_dir: Directory to write the chunks to (None to return without writing)
    
Returns:
    List of chunk contents or file paths if output_dir is provided

**Complexity:** 5

### `split_by_python_classes(file_path, output_dir)`

Split a Python file into chunks based on class definitions

Args:
    file_path: Path to the Python file to split
    output_dir: Directory to write the chunks to (None to return without writing)
    
Returns:
    Dictionary mapping class names to their code or file paths if output_dir is provided

**Complexity:** 11

### `split_by_python_functions(file_path, output_dir)`

Split a Python file into chunks based on function definitions

Args:
    file_path: Path to the Python file to split
    output_dir: Directory to write the chunks to (None to return without writing)
    
Returns:
    Dictionary mapping function names to their code or file paths if output_dir is provided

**Complexity:** 15

### `split_with_compression(file_path, bytes_per_chunk, output_dir)`

Split a file into compressed chunks

Args:
    file_path: Path to the file to split
    bytes_per_chunk: Number of bytes per chunk before compression
    output_dir: Directory to write the chunks to (None to return without writing)
    
Returns:
    List of compressed chunk contents or file paths if output_dir is provided

**Complexity:** 5

### `merge_files(file_paths, output_path, is_binary)`

Merge multiple files into a single file

Args:
    file_paths: List of paths to the files to merge
    output_path: Path to the output file
    is_binary: Whether the files are binary
    
Returns:
    True if successful, False otherwise

**Complexity:** 4

### `merge_compressed_files(file_paths, output_path)`

Merge multiple compressed files into a single file

Args:
    file_paths: List of paths to the compressed files to merge
    output_path: Path to the output file
    
Returns:
    True if successful, False otherwise

**Complexity:** 4

## Keywords

`output_dir, file_path, print, ast, node, sys, path, str, argv, content, len, chunks, open, output_path, method, chunk, bytes_per_chunk, file_paths, append, file_name`

