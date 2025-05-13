# simple_hierarchical_core.py

**Path:** `legacy\src\core\simple_hierarchical_core.py`

## Description

Simple Hierarchical Core - A lightweight foundation for hierarchical modules

This module provides a simplified hierarchical module system with event-based
communication and state management. It's designed to be easy to understand and use.

## Metrics

- **Lines of Code:** 270
- **Functions:** 28
- **Classes:** 6
- **Imports:** 7
- **Complexity:** 39

## Imports

- `import os`
- `import sys`
- `import uuid`
- `import json`
- `import time`
- `import weakref`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Callable`
- `from typing.Optional`
- `from typing.Set`
- `from typing.Union`
- `from typing.Type`

## Classes

### Event

Base event class for the event system

#### Methods

- `__init__`

### EventBus

Simple event bus for communication between modules

#### Methods

- `__init__`
- `subscribe`
- `unsubscribe`
- `publish`

### StateStore

Simple state store for managing module state

#### Methods

- `__init__`
- `set`
- `get`
- `watch`
- `unwatch`

### HierarchicalModule

Base class for all hierarchical modules

#### Methods

- `__init__`
- `add_child`
- `remove_child`
- `get_child`
- `get_path`
- `get_full_id`
- `initialize`
- `process`
- `shutdown`

### ModuleRegistry

Registry for all modules in the system

#### Methods

- `__init__`
- `register_module`
- `unregister_module`
- `get_module`
- `initialize_all`
- `shutdown_all`

### UIKeyManager

Manager for UI component keys to prevent duplicates

#### Methods

- `__new__`
- `get_unique_key`
- `clear_keys`

## Functions

### `__init__(self, event_type, data, source)`

**Complexity:** 1

### `__init__(self, parent_bus)`

**Complexity:** 2

### `subscribe(self, event_type, callback)`

Subscribe to an event type

**Complexity:** 2

### `unsubscribe(self, event_type, callback)`

Unsubscribe from an event type

**Complexity:** 2

### `publish(self, event, data, source, _visited_buses)`

Publish an event to all subscribers

**Complexity:** 11

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

**Complexity:** 2

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

### `get_path(self)`

Get the path from the root to this module

**Complexity:** 2

### `get_full_id(self)`

Get the full ID including the path

**Complexity:** 1

### `initialize(self)`

Initialize the module

**Complexity:** 3

### `process(self, data, context)`

Process data with this module

**Complexity:** 1

### `shutdown(self)`

Shutdown the module and its children

**Complexity:** 2

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

**Complexity:** 6

### `initialize_all(self)`

Initialize all modules

**Complexity:** 2

### `shutdown_all(self)`

Shutdown all modules

**Complexity:** 2

### `__new__(cls)`

**Complexity:** 2

### `get_unique_key(self, base_key)`

Get a unique key based on the base key

**Complexity:** 3

### `clear_keys(self)`

Clear all registered keys

**Complexity:** 1

## Keywords

`str, key, module_id, Any, module, event_type, callback, event, root_modules, subscribers, _visited_buses, event_bus, watchers, parent, source, parent_bus, children, state, used_keys, base_key`

