# hierarchical_core.py

**Path:** `legacy\src\core\hierarchical_core.py`

## Description

Hierarchical Core - Foundation for the self-bootstrapping architecture

This module provides the core components for a hierarchical, modular system
that can dynamically organize, load, and manage modules at multiple levels
of abstraction.

## Metrics

- **Lines of Code:** 747
- **Functions:** 44
- **Classes:** 12
- **Imports:** 15
- **Complexity:** 70

## Imports

- `import os`
- `import sys`
- `import importlib`
- `import inspect`
- `import json`
- `import uuid`
- `import weakref`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Callable`
- `from typing.Optional`
- `from typing.Set`
- `from typing.Union`
- `from typing.Type`
- `from typing.Tuple`
- `from abc.ABC`
- `from abc.abstractmethod`
- `from enum.Enum`
- `from enum.auto`
- `import threading`
- `import asyncio`
- `from concurrent.futures.ThreadPoolExecutor`
- `import ast`
- `import ast`

## Classes

### EventPriority

Priority levels for event handlers

#### Inherits From

- `Enum`

### Event

Base event class for the event system

#### Methods

- `__init__`
- `__str__`

### EventBus

Central event bus that supports hierarchical event propagation

#### Methods

- `__init__`
- `subscribe`
- `unsubscribe`
- `publish`

### StateChangeEvent

Event fired when state changes

#### Methods

- `__init__`

#### Inherits From

- `Event`

### StateStore

Hierarchical state store that supports state change notifications

#### Methods

- `__init__`
- `set`
- `get`
- `watch`
- `unwatch`
- `get_all`

### ModuleStatus

Status of a module

#### Inherits From

- `Enum`

### HierarchicalModule

Base class for all modules in the hierarchical system

#### Methods

- `__init__`
- `add_child`
- `remove_child`
- `get_child`
- `get_descendant`
- `get_path`
- `get_full_id`
- `initialize`
- `process`
- `shutdown`
- `to_dict`

#### Inherits From

- `ABC`

### ModuleRegistry

Registry for all modules in the system

#### Methods

- `__init__`
- `register_module`
- `unregister_module`
- `get_module`
- `_update_cache`
- `_remove_from_cache`
- `initialize_all`
- `_initialize_module`
- `shutdown_all`
- `to_dict`

### ModuleLoader

Utility for dynamically loading modules

#### Methods

- `load_module_class`
- `load_module_instance`
- `load_from_config`
- `_load_module_from_config`

### FileSplitter

Utility for splitting files based on various criteria

#### Methods

- `split_by_class`
- `split_by_size`

### CodeAnalyzer

Utility for analyzing code to identify module boundaries

#### Methods

- `analyze_file`
- `analyze_directory`

### ModuleGenerator

Utility for generating module code

#### Methods

- `generate_module_class`
- `generate_module_file`

## Functions

### `__init__(self, event_type, data, source)`

**Complexity:** 1

### `__str__(self)`

**Complexity:** 1

### `__init__(self, parent_bus)`

**Complexity:** 2

### `subscribe(self, event_type, callback, priority)`

Subscribe to an event type with a given priority

**Complexity:** 2

### `unsubscribe(self, event_type, callback)`

Unsubscribe from an event type

**Complexity:** 2

### `publish(self, event, data, source)`

Publish an event to all subscribers

Args:
    event: Either an Event object or an event type string
    data: Event data (used only if event is a string)
    source: Event source (used only if event is a string)
    
Returns:
    The published event

**Complexity:** 13

### `__init__(self, key, value, old_value, source)`

**Complexity:** 1

### `__init__(self, event_bus, parent_store)`

**Complexity:** 1

### `set(self, key, value, source)`

Set a state value and notify watchers

**Complexity:** 5

### `get(self, key, default)`

Get a state value, checking parent stores if not found

**Complexity:** 3

### `watch(self, key, callback)`

Watch for changes to a specific key

**Complexity:** 2

### `unwatch(self, key, callback)`

Stop watching a specific key

**Complexity:** 3

### `get_all(self, include_parent)`

Get all state values

**Complexity:** 3

### `__init__(self, module_id, parent)`

**Complexity:** 2

### `add_child(self, module)`

Add a child module

**Complexity:** 1

### `remove_child(self, module_id)`

Remove a child module

**Complexity:** 2

### `get_child(self, module_id)`

Get a child module by ID

**Complexity:** 1

### `get_descendant(self, path)`

Get a descendant module by path

Args:
    path: List of module IDs forming a path to the descendant
    
Returns:
    The descendant module or None if not found

**Complexity:** 4

### `get_path(self)`

Get the path from the root to this module

**Complexity:** 2

### `get_full_id(self)`

Get the full ID including the path

**Complexity:** 1

### `initialize(self)`

Initialize the module

Returns:
    True if initialization was successful, False otherwise

**Complexity:** 1

### `process(self, data, context)`

Process data with this module

Args:
    data: The data to process
    context: Additional context for processing
    
Returns:
    The processed data

**Complexity:** 1

### `shutdown(self)`

Shutdown the module and its children

**Complexity:** 2

### `to_dict(self)`

Convert module to dictionary representation

**Complexity:** 1

### `__init__(self)`

**Complexity:** 1

### `register_module(self, module)`

Register a root module

**Complexity:** 1

### `unregister_module(self, module_id)`

Unregister a root module

**Complexity:** 2

### `get_module(self, module_id)`

Get a module by ID (can be a full path ID)

**Complexity:** 5

### `_update_cache(self, module)`

Update the module cache with a module and its descendants

**Complexity:** 2

### `_remove_from_cache(self, module)`

Remove a module and its descendants from the cache

**Complexity:** 3

### `initialize_all(self)`

Initialize all modules

**Complexity:** 2

### `_initialize_module(self, module)`

Initialize a module and its children

**Complexity:** 4

### `shutdown_all(self)`

Shutdown all modules

**Complexity:** 2

### `to_dict(self)`

Convert registry to dictionary representation

**Complexity:** 1

### `load_module_class(module_path, class_name)`

Load a module class from a Python module

Args:
    module_path: Import path to the Python module
    class_name: Name of the class to load
    
Returns:
    The loaded class

**Complexity:** 3

### `load_module_instance(module_path, class_name, module_id, parent)`

Load and instantiate a module

Args:
    module_path: Import path to the Python module
    class_name: Name of the class to load
    module_id: ID for the new module
    parent: Parent module
    **kwargs: Additional arguments for the module constructor
    
Returns:
    The instantiated module

**Complexity:** 1

### `load_from_config(config_path, registry)`

Load modules from a configuration file

Args:
    config_path: Path to the configuration file
    registry: Module registry to register modules with

**Complexity:** 2

### `_load_module_from_config(config, parent)`

Load a module from a configuration dictionary

Args:
    config: Module configuration
    parent: Parent module
    
Returns:
    The loaded module

**Complexity:** 2

### `split_by_class(file_path, output_dir)`

Split a Python file by class definitions

Args:
    file_path: Path to the Python file
    output_dir: Directory to write the split files

**Complexity:** 2

### `split_by_size(file_path, output_dir, max_size)`

Split a file by size

Args:
    file_path: Path to the file
    output_dir: Directory to write the split files
    max_size: Maximum size of each split file in lines

**Complexity:** 2

### `analyze_file(file_path)`

Analyze a Python file to identify potential modules

Args:
    file_path: Path to the Python file
    
Returns:
    Analysis results

**Complexity:** 12

### `analyze_directory(directory)`

Analyze all Python files in a directory

Args:
    directory: Directory to analyze
    
Returns:
    Analysis results for all files

**Complexity:** 6

### `generate_module_class(module_name, parent_class)`

Generate code for a module class

Args:
    module_name: Name of the module class
    parent_class: Name of the parent class
    
Returns:
    Generated code

**Complexity:** 1

### `generate_module_file(module_name, output_path, parent_class, imports)`

Generate a module file

Args:
    module_name: Name of the module class
    output_path: Path to write the file
    parent_class: Name of the parent class
    imports: Additional imports

**Complexity:** 2

## Keywords

`str, module, module_id, Any, key, file_path, HierarchicalModule, event, event_type, source, path, child, parent, callback, children, root_modules, Optional, auto, subscribers, lock`

