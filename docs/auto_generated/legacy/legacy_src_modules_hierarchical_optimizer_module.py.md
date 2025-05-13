# optimizer_module.py

**Path:** `legacy\src\modules\hierarchical\optimizer_module.py`

## Metrics

- **Lines of Code:** 133
- **Functions:** 5
- **Classes:** 1
- **Imports:** 8
- **Complexity:** 23

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
- `from src.imports.optimize_logic`
- `from src.ir_model.get_ir_model`

## Classes

### OptimizerModule

Hierarchical module for optimizing logic code

#### Methods

- `__init__`
- `handle_ir_generation_complete`
- `can_process`
- `process`
- `render_ui`

#### Inherits From

- `HierarchicalModule`

## Functions

### `__init__(self, parent)`

**Complexity:** 1

### `handle_ir_generation_complete(self, data)`

Handle IR generation complete events

**Complexity:** 4

### `can_process(self, data)`

Check if this module can process the given data

**Complexity:** 3

### `process(self, data, context)`

Process the data to optimize the logic

**Complexity:** 3

### `render_ui(self)`

Render the UI for the optimizer module

**Complexity:** 15

## Keywords

`optimization_results, ir_model, get, path, logic, error, rule, lookup_table, dirname, src, state_manager, process, shared_state, len, merged, Logic, markdown, sys, project_root, event_bus`

