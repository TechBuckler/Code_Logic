# demo_hierarchical.py

**Path:** `legacy\src\demo_hierarchical.py`

## Description

Demo of the Hierarchical Module System

This script demonstrates the hierarchical module system by creating a simple
hierarchy of modules and showing how they interact.

## Metrics

- **Lines of Code:** 215
- **Functions:** 11
- **Classes:** 4
- **Imports:** 6
- **Complexity:** 22

## Imports

- `import os`
- `import sys`
- `import streamlit as st`
- `from src.core.hierarchical_module.HierarchicalModule`
- `from src.core.hierarchical_module.ModuleHierarchy`
- `from src.core.state_manager.state_manager`
- `import time`

## Classes

### AnalysisModule

Root module for analysis functionality

#### Methods

- `__init__`
- `render_ui`

#### Inherits From

- `HierarchicalModule`

### ParserModule

Child module for parsing code

#### Methods

- `__init__`
- `render_ui`

#### Inherits From

- `HierarchicalModule`

### OptimizationModule

Root module for optimization functionality

#### Methods

- `__init__`
- `handle_parsed_code`
- `render_ui`

#### Inherits From

- `HierarchicalModule`

### PerformanceTestModule

Child module for performance testing

#### Methods

- `__init__`
- `render_ui`

#### Inherits From

- `HierarchicalModule`

## Functions

### `main()`

Main function to run the demo

**Complexity:** 10

### `__init__(self, parent)`

**Complexity:** 1

### `render_ui(self)`

**Complexity:** 4

### `__init__(self, parent)`

**Complexity:** 1

### `render_ui(self)`

**Complexity:** 2

### `__init__(self, parent)`

**Complexity:** 1

### `handle_parsed_code(self, data)`

Handle parsed code event

**Complexity:** 2

### `render_ui(self)`

**Complexity:** 4

### `__init__(self, parent)`

**Complexity:** 1

### `render_ui(self)`

**Complexity:** 3

### `log_event(event_type, data)`

**Complexity:** 1

## Keywords

`code, state_manager, module, Module, __init__, parent, name, selected_module, session_state, write, key, register_ui_key, event_bus, success, time, hierarchy, path, HierarchicalModule, analysis, render_ui`

