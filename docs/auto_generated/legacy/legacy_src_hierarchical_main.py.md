# hierarchical_main.py

**Path:** `legacy\src\hierarchical_main.py`

## Description

Hierarchical Logic Tool - Main Application

This is the main entry point for the Logic Tool using the hierarchical module architecture.
It sets up the core modules and handles the main UI rendering.

## Metrics

- **Lines of Code:** 183
- **Functions:** 8
- **Classes:** 1
- **Imports:** 8
- **Complexity:** 21

## Imports

- `import os`
- `import sys`
- `import streamlit as st`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from src.core.hierarchical_module.HierarchicalModule`
- `from src.core.hierarchical_module.ModuleHierarchy`
- `from src.core.state_manager.state_manager`
- `from src.modules.hierarchical.analysis_core_module.AnalysisCoreModule`
- `from src.modules.hierarchical.optimization_core_module.OptimizationCoreModule`

## Classes

### LogicToolApp

Main application module for the Logic Tool

#### Methods

- `__init__`
- `load_core_modules`
- `handle_navigation`
- `log_event`
- `render_ui`
- `render_sidebar`
- `render_home`

#### Inherits From

- `HierarchicalModule`

## Functions

### `main()`

Main entry point for the application

**Complexity:** 1

### `__init__(self)`

**Complexity:** 4

### `load_core_modules(self)`

Load the core modules of the application

**Complexity:** 1

### `handle_navigation(self, data)`

Handle navigation events

**Complexity:** 3

### `log_event(self, data)`

Log an event to the event log

**Complexity:** 3

### `render_ui(self)`

Render the main application UI

**Complexity:** 4

### `render_sidebar(self)`

Render the application sidebar

**Complexity:** 7

### `render_home(self)`

Render the home page

**Complexity:** 3

## Keywords

`page, session_state, state_manager, markdown, event_bus, event_log, navigate, key, register_ui_key, path, event_type, modules, button, publish, src, Logic, Tool, render_ui, sys, project_root`

