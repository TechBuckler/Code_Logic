# fractal_organizer.py

**Path:** `tools\fractal\fractal_organizer.py`

## Description

Fractal Code Organizer

This module enforces extreme modularity by recursively breaking down code into
smaller and smaller components, while providing mechanisms to navigate and
"bubble up" the structure when needed.

## Metrics

- **Lines of Code:** 554
- **Functions:** 21
- **Classes:** 5
- **Imports:** 10
- **Complexity:** 91

## Imports

- `import os`
- `import sys`
- `import ast`
- `import json`
- `import importlib`
- `import inspect`
- `import re`
- `from pathlib.Path`
- `from typing.Dict`
- `from typing.List`
- `from typing.Set`
- `from typing.Any`
- `from typing.Tuple`
- `from typing.Optional`
- `from typing.Union`
- `from typing.Callable`
- `import argparse`

## Classes

### FractalNode

Represents a node in the fractal code structure.

#### Methods

- `__init__`
- `add_child`
- `add_function`
- `to_dict`
- `__str__`

### FractalAnalyzer

Analyzes code to create a fractal structure.

#### Methods

- `__init__`
- `analyze_directory`
- `_analyze_file`

### FractalSplitter

Splits code into a fractal structure.

#### Methods

- `__init__`
- `split_directory`
- `split_file`

### FractalNavigator

Navigates a fractal code structure.

#### Methods

- `__init__`
- `go_up`
- `go_down`
- `list_current`
- `find_function`

### FractalBubbler

Bubbles up code from a fractal structure.

#### Methods

- `__init__`
- `bubble_up`
- `create_index`

## Functions

### `main()`

Main function for the fractal organizer.

**Complexity:** 5

### `__init__(self, name, path, parent)`

**Complexity:** 1

### `add_child(self, child)`

Add a child node to this node.

**Complexity:** 1

### `add_function(self, name, code, resource_type)`

Add a function to this node.

**Complexity:** 1

### `to_dict(self)`

Convert the node to a dictionary.

**Complexity:** 1

### `__str__(self)`

**Complexity:** 1

### `__init__(self)`

**Complexity:** 1

### `analyze_directory(self, directory)`

Analyze a directory and create a fractal structure.

**Complexity:** 5

### `_analyze_file(self, file_path, rel_path)`

Analyze a Python file and add it to the fractal structure.

**Complexity:** 10

### `__init__(self, max_functions, max_lines, max_depth)`

**Complexity:** 1

### `split_directory(self, src_dir, dest_dir)`

Split a directory into a fractal structure.

**Complexity:** 5

### `split_file(self, src_file, dest_file)`

Split a file into a fractal structure.

**Complexity:** 28

### `__init__(self, root_dir)`

**Complexity:** 1

### `go_up(self)`

Go up one level in the fractal structure.

**Complexity:** 2

### `go_down(self, name)`

Go down into a child directory.

**Complexity:** 2

### `list_current(self)`

List the contents of the current directory.

**Complexity:** 12

### `find_function(self, name)`

Find a function in the fractal structure.

**Complexity:** 12

### `__init__(self, root_dir)`

**Complexity:** 1

### `bubble_up(self, target_dir, max_depth)`

Bubble up code from deeper levels to a maximum depth.

**Complexity:** 9

### `create_index(self, target_dir)`

Create an index of all functions in the fractal structure.

**Complexity:** 10

### `search_dir(directory)`

**Complexity:** 12

## Keywords

`name, node, path, write, functions, ast, content, root, file, file_path, open, encoding, utf, directory, join, target_dir, append, index, tree, func_name`

