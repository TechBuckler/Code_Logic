# code_mapper.py

**Path:** `modules\standard\code_mapper.py`

## Description

Code Mapper Module

This module provides tools for analyzing and mapping the codebase structure,
dependencies, and resource usage patterns. It uses AST (Abstract Syntax Tree)
to parse Python files and extract detailed information about their structure.

## Metrics

- **Lines of Code:** 524
- **Functions:** 20
- **Classes:** 4
- **Imports:** 12
- **Complexity:** 57

## Imports

- `import os`
- `import sys`
- `import ast`
- `import json`
- `import importlib`
- `import inspect`
- `from pathlib.Path`
- `from typing.Dict`
- `from typing.List`
- `from typing.Set`
- `from typing.Any`
- `from typing.Tuple`
- `from typing.Optional`
- `from typing.Union`
- `from typing.Callable`
- `from src.module_system.Module`
- `from src.module_system.ModuleRegistry`
- `from resource_splitter.analyze_resource_focus`
- `from resource_splitter.analyze_resource_profile`
- `import importlib.util`
- `import argparse`

## Classes

### ImportVisitor

AST visitor that collects all imports in a Python file.

#### Methods

- `__init__`
- `visit_Import`
- `visit_ImportFrom`

#### Inherits From


### FunctionVisitor

AST visitor that collects all functions in a Python file.

#### Methods

- `__init__`
- `set_source`
- `visit_ClassDef`
- `visit_FunctionDef`

#### Inherits From


### FunctionCallVisitor

AST visitor that collects all function calls within a function.

#### Methods

- `__init__`
- `visit_Call`

#### Inherits From


### ClassVisitor

AST visitor that collects all classes in a Python file.

#### Methods

- `__init__`
- `set_source`
- `visit_ClassDef`

#### Inherits From


## Functions

### `analyze_file(file_path)`

Analyze a Python file and extract its structure.

**Complexity:** 4

### `find_python_files(directory)`

Find all Python files in a directory and its subdirectories.

**Complexity:** 4

### `map_codebase(directory)`

Map the entire codebase structure.

**Complexity:** 9

### `generate_codebase_report(map_data, output_file)`

Generate a human-readable report of the codebase structure.

**Complexity:** 13

### `split_codebase(directory, output_dir)`

Split the entire codebase into resource-oriented components.

**Complexity:** 9

### `main()`

Main function for the code mapper.

**Complexity:** 4

### `__init__(self)`

**Complexity:** 1

### `visit_Import(self, node)`

**Complexity:** 2

### `visit_ImportFrom(self, node)`

**Complexity:** 2

### `__init__(self)`

**Complexity:** 1

### `set_source(self, source)`

Set the source code for extracting function definitions.

**Complexity:** 1

### `visit_ClassDef(self, node)`

**Complexity:** 1

### `visit_FunctionDef(self, node)`

**Complexity:** 4

### `__init__(self)`

**Complexity:** 1

### `visit_Call(self, node)`

**Complexity:** 4

### `__init__(self)`

**Complexity:** 1

### `set_source(self, source)`

Set the source code for extracting class definitions.

**Complexity:** 1

### `visit_ClassDef(self, node)`

**Complexity:** 6

### `analyze_resource_focus(func_code)`

Analyze the resource focus of a function.

**Complexity:** 1

### `analyze_resource_profile(func_code)`

Analyze the resource profile of a function.

**Complexity:** 1

## Keywords

`node, append, report, name, rel_path, file_path, analysis, ast, files, path, start_line, functions, source, docstring, source_lines, end_line, bases, directory, join, classes`

