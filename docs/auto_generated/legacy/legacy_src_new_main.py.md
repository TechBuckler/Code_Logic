# new_main.py

**Path:** `legacy\src\new_main.py`

## Description

New Main Application - Entry point for the Logic Tool with hierarchical architecture

This module serves as the main entry point for the Logic Tool, using the new
hierarchical architecture based on simple_hierarchical_core.py.

## Metrics

- **Lines of Code:** 367
- **Functions:** 19
- **Classes:** 5
- **Imports:** 6
- **Complexity:** 29

## Imports

- `import os`
- `import sys`
- `import streamlit as st`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from src.core.simple_hierarchical_core.HierarchicalModule`
- `from src.core.simple_hierarchical_core.Event`
- `from src.core.simple_hierarchical_core.EventBus`
- `from src.core.simple_hierarchical_core.StateStore`
- `from src.core.simple_hierarchical_core.ModuleRegistry`
- `from src.core.simple_hierarchical_core.ui_key_manager`
- `import datetime`

## Classes

### LogicToolApp

Main application module for the Logic Tool

#### Methods

- `__init__`
- `load_core_modules`
- `handle_navigation`
- `render`
- `render_sidebar`
- `render_home`

#### Inherits From

- `HierarchicalModule`

### AnalysisCoreModule

Core module for code analysis functionality

#### Methods

- `__init__`
- `render`
- `analyze_code`

#### Inherits From

- `HierarchicalModule`

### OptimizationCoreModule

Core module for code optimization functionality

#### Methods

- `__init__`
- `render`
- `optimize_code`

#### Inherits From

- `HierarchicalModule`

### ProjectCoreModule

Core module for project management functionality

#### Methods

- `__init__`
- `render`
- `create_project`
- `open_project`

#### Inherits From

- `HierarchicalModule`

### UICoreModule

Core module for UI components and utilities

#### Methods

- `__init__`
- `render`

#### Inherits From

- `HierarchicalModule`

## Functions

### `main()`

Main entry point for the application

**Complexity:** 1

### `__init__(self)`

**Complexity:** 2

### `load_core_modules(self)`

Load the core modules of the application

**Complexity:** 1

### `handle_navigation(self, event)`

Handle navigation events

**Complexity:** 2

### `render(self)`

Render the main application UI

**Complexity:** 5

### `render_sidebar(self)`

Render the application sidebar

**Complexity:** 5

### `render_home(self)`

Render the home page

**Complexity:** 4

### `__init__(self, module_id, parent)`

**Complexity:** 1

### `render(self)`

Render the analysis module UI

**Complexity:** 4

### `analyze_code(self, code)`

Analyze the provided code

**Complexity:** 1

### `__init__(self, module_id, parent)`

**Complexity:** 1

### `render(self)`

Render the optimization module UI

**Complexity:** 4

### `optimize_code(self, code, options)`

Optimize the provided code with the given options

**Complexity:** 1

### `__init__(self, module_id, parent)`

**Complexity:** 2

### `render(self)`

Render the project module UI

**Complexity:** 6

### `create_project(self, name, description)`

Create a new project

**Complexity:** 2

### `open_project(self, project_id)`

Open an existing project

**Complexity:** 2

### `__init__(self, module_id, parent)`

**Complexity:** 1

### `render(self)`

Render the UI module (not directly accessible)

**Complexity:** 1

## Keywords

`ui_key_manager, page, projects, key, get_unique_key, markdown, code, project_id, button, __init__, str, event_bus, render, name, navigate, get, publish, module_id, parent, Project`

