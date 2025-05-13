# module_explorer_module.py

**Path:** `legacy\src\modules\module_explorer_module.py`

## Description

Module Explorer Module

This module allows exploring, editing, and running other modules in the system.
It provides a unified interface for inspecting code, running tools, and executing
the entire pipeline or specific components.

## Metrics

- **Lines of Code:** 309
- **Functions:** 13
- **Classes:** 1
- **Imports:** 8
- **Complexity:** 58

## Imports

- `import os`
- `import sys`
- `import inspect`
- `import importlib`
- `import importlib.util`
- `import subprocess`
- `from pathlib.Path`
- `from starter_pipeline.run_pipeline`

## Classes

### ModuleExplorerModule

Module for exploring, editing, and running other modules.

#### Methods

- `__init__`
- `initialize`
- `can_process`
- `process`
- `list_modules`
- `view_module`
- `edit_module`
- `run_module`
- `run_pipeline`
- `_find_project_root`
- `_find_module_path`
- `_import_module`
- `_get_module_info`

## Functions

### `__init__(self)`

**Complexity:** 1

### `initialize(self)`

Initialize the module.

**Complexity:** 1

### `can_process(self, data)`

Check if this module can process the given data.

**Complexity:** 2

### `process(self, data, context)`

Process the command.

**Complexity:** 6

### `list_modules(self)`

List all available modules in the project.

**Complexity:** 9

### `view_module(self, module_name)`

View the source code of a module.

**Complexity:** 5

### `edit_module(self, module_name, changes)`

Edit a module's source code.

**Complexity:** 12

### `run_module(self, module_name, args)`

Run a specific module with the given arguments.

**Complexity:** 11

### `run_pipeline(self, source_code, function_name, options)`

Run the entire processing pipeline on the given source code.

**Complexity:** 3

### `_find_project_root(self)`

Find the project root directory.

**Complexity:** 3

### `_find_module_path(self, module_name)`

Find the path to a module file.

**Complexity:** 4

### `_import_module(self, module_name)`

Import a module by name.

**Complexity:** 5

### `_get_module_info(self, module_name)`

Get information about a module.

**Complexity:** 8

## Keywords

`module_name, path, module_path, module, error, name, get, command, changes, file, modules, join, _find_module_path, module_class, project_root, Module, current_dir, run_pipeline, source_code, src`

