# ir_generator_module.py

**Path:** `legacy\src\modules\hierarchical\ir_generator_module.py`

## Description

Hierarchical IR Generator Module

This module extends the base IR generator module with hierarchical capabilities.
It generates an Intermediate Representation (IR) model from parsed code.

## Metrics

- **Lines of Code:** 181
- **Functions:** 5
- **Classes:** 1
- **Imports:** 7
- **Complexity:** 27

## Imports

- `import os`
- `import sys`
- `import streamlit as st`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from src.core.hierarchical_module.HierarchicalModule`
- `from src.core.state_manager.state_manager`
- `from src.imports.extract_ir_from_source`
- `from src.imports.get_ir_model`

## Classes

### IRGeneratorModule

Hierarchical module for generating IR models from parsed code

#### Methods

- `__init__`
- `handle_ast_parsing_complete`
- `can_process`
- `process`
- `render_ui`

#### Inherits From

- `HierarchicalModule`

## Functions

### `__init__(self, parent)`

**Complexity:** 1

### `handle_ast_parsing_complete(self, data)`

Handle AST parsing complete events

**Complexity:** 5

### `can_process(self, data)`

Check if this module can process the given data

**Complexity:** 2

### `process(self, data, context)`

Process the data to generate an IR model

**Complexity:** 10

### `render_ui(self)`

Render the UI for the IR generator module

**Complexity:** 12

## Keywords

`ir_model, function_name, error, functions, shared_state, code, path, isinstance, get, model, ast_result, error_msg, rule, state_manager, len, write, dirname, get_ir_model, event_bus, current_code`

