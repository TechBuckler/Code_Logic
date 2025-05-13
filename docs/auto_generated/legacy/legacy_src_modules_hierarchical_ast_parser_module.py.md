# ast_parser_module.py

**Path:** `legacy\src\modules\hierarchical\ast_parser_module.py`

## Description

Hierarchical AST Parser Module

This module extends the base AST parser module with hierarchical capabilities.
It parses Python code into an Abstract Syntax Tree (AST) for further analysis.

## Metrics

- **Lines of Code:** 114
- **Functions:** 4
- **Classes:** 1
- **Imports:** 8
- **Complexity:** 10

## Imports

- `import os`
- `import sys`
- `import ast`
- `import streamlit as st`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from src.core.hierarchical_module.HierarchicalModule`
- `from src.core.state_manager.state_manager`
- `from src.imports.extract_functions`

## Classes

### ASTParserModule

Hierarchical module for parsing Python code into AST

#### Methods

- `__init__`
- `can_process`
- `process`
- `render_ui`

#### Inherits From

- `HierarchicalModule`

## Functions

### `__init__(self, parent)`

**Complexity:** 1

### `can_process(self, data)`

Check if this module can process the given data

**Complexity:** 2

### `process(self, data, context)`

Process the code by extracting functions and AST information

**Complexity:** 3

### `render_ui(self)`

Render the UI for the AST parser module

**Complexity:** 6

## Keywords

`code, functions, path, func, error, dirname, state_manager, Code, sys, project_root, src, context, shared_state, get, error_msg, parsing, AST, write, expander, expanded`

