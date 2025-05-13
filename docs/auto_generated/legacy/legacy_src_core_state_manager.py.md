# state_manager.py

**Path:** `legacy\src\core\state_manager.py`

## Description

State Manager - Core component for managing shared state and event communication

## Metrics

- **Lines of Code:** 147
- **Functions:** 18
- **Classes:** 3
- **Imports:** 2
- **Complexity:** 20

## Imports

- `import json`
- `from typing.Dict`
- `from typing.Any`
- `from typing.Callable`
- `from typing.List`
- `from typing.Set`

## Classes

### EventBus

Central event bus for communication between modules

#### Methods

- `__init__`
- `subscribe`
- `unsubscribe`
- `publish`

### SharedState

Shared state manager for the application

#### Methods

- `__init__`
- `set`
- `get`
- `watch`
- `unwatch`
- `get_all`
- `clear`

### StateManager

Main state manager that combines EventBus and SharedState

#### Methods

- `__new__`
- `register_ui_key`
- `release_ui_key`
- `get_event_bus`
- `get_shared_state`
- `save_state`
- `load_state`

## Functions

### `__init__(self)`

**Complexity:** 1

### `subscribe(self, event_type, callback)`

Subscribe to an event type

**Complexity:** 2

### `unsubscribe(self, event_type, callback)`

Unsubscribe from an event type

**Complexity:** 3

### `publish(self, event_type, data)`

Publish an event to all subscribers

**Complexity:** 3

### `__init__(self, event_bus)`

**Complexity:** 1

### `set(self, key, value)`

Set a state value and notify watchers

**Complexity:** 3

### `get(self, key, default)`

Get a state value

**Complexity:** 1

### `watch(self, key, callback)`

Watch for changes to a specific key

**Complexity:** 2

### `unwatch(self, key, callback)`

Stop watching a specific key

**Complexity:** 3

### `get_all(self)`

Get the entire state

**Complexity:** 1

### `clear(self)`

Clear the entire state

**Complexity:** 1

### `__new__(cls)`

**Complexity:** 2

### `register_ui_key(self, key)`

Register a UI component key to prevent duplicates
Returns the key if it's unique, or a modified key if it already exists

**Complexity:** 2

### `release_ui_key(self, key)`

Release a UI component key when no longer needed

**Complexity:** 2

### `get_event_bus(self)`

Get the event bus instance

**Complexity:** 1

### `get_shared_state(self)`

Get the shared state instance

**Complexity:** 1

### `save_state(self, filepath)`

Save the current state to a file

**Complexity:** 4

### `load_state(self, filepath)`

Load state from a file

**Complexity:** 4

## Keywords

`key, callback, str, event_type, subscribers, watchers, event_bus, _instance, Any, state, json, Callable, set, ui_keys, EventBus, shared_state, filepath, add, remove, publish`

