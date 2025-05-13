# hierarchical_module.py

**Path:** `legacy\src\core\hierarchical_module.py`

## Description

Hierarchical Module System - Extends the base module system with hierarchical capabilities

This module provides a hierarchical extension to the base module system,
allowing modules to be organized in a tree structure with parent-child relationships.

## Metrics

- **Lines of Code:** 176
- **Functions:** 21
- **Classes:** 2
- **Imports:** 5
- **Complexity:** 23

## Imports

- `import os`
- `import sys`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from typing.Set`
- `from typing.Union`
- `from src.module_system.Module`
- `from src.core.state_manager.state_manager`

## Classes

### HierarchicalModule

Hierarchical module that extends the base Module class with parent-child relationships

#### Methods

- `__init__`
- `add_child`
- `remove_child`
- `get_child`
- `get_path`
- `get_full_name`
- `get_all_children`
- `find_module`
- `initialize`
- `shutdown`
- `can_process`
- `process`
- `render_ui`

#### Inherits From

- `Module`

### ModuleHierarchy

Manager for a hierarchy of modules

#### Methods

- `__init__`
- `add_root_module`
- `remove_root_module`
- `get_root_module`
- `get_all_modules`
- `find_module`
- `initialize_all`
- `shutdown_all`

## Functions

### `__init__(self, name, parent)`

**Complexity:** 2

### `add_child(self, module)`

Add a child module

**Complexity:** 1

### `remove_child(self, name)`

Remove a child module by name

**Complexity:** 2

### `get_child(self, name)`

Get a child module by name

**Complexity:** 1

### `get_path(self)`

Get the path from the root to this module

**Complexity:** 2

### `get_full_name(self)`

Get the full name including the path

**Complexity:** 1

### `get_all_children(self, recursive)`

Get all children, optionally including descendants

**Complexity:** 3

### `find_module(self, path)`

Find a module by path (e.g., 'parent.child.grandchild')

**Complexity:** 5

### `initialize(self)`

Initialize this module and all its children

**Complexity:** 4

### `shutdown(self)`

Shutdown this module and all its children

**Complexity:** 2

### `can_process(self, data)`

Check if this module can process the given data

**Complexity:** 1

### `process(self, data, context)`

Process data with this module

**Complexity:** 1

### `render_ui(self)`

Render the UI for this module

**Complexity:** 1

### `__init__(self, root_module)`

**Complexity:** 2

### `add_root_module(self, module)`

Add a root module to the hierarchy

**Complexity:** 1

### `remove_root_module(self, name)`

Remove a root module from the hierarchy

**Complexity:** 2

### `get_root_module(self, name)`

Get a root module by name

**Complexity:** 1

### `get_all_modules(self)`

Get all modules in the hierarchy

**Complexity:** 2

### `find_module(self, path)`

Find a module by path (e.g., 'root.child.grandchild')

**Complexity:** 3

### `initialize_all(self)`

Initialize all modules in the hierarchy

**Complexity:** 3

### `shutdown_all(self)`

Shutdown all modules in the hierarchy

**Complexity:** 2

## Keywords

`name, path, root_modules, module, children, values, parent, child, parts, current, state_manager, super, initialize, shutdown, sys, dirname, project_root, __init__, get_path, get_all_children`

