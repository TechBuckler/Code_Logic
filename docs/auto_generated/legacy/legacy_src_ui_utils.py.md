# ui_utils.py

**Path:** `legacy\src\ui_utils.py`

## Description

UI Utilities for the Logic Tool

## Metrics

- **Lines of Code:** 47
- **Functions:** 4
- **Classes:** 0
- **Imports:** 2
- **Complexity:** 5

## Imports

- `import streamlit as st`
- `from typing.Dict`
- `from typing.Any`
- `from typing.Set`

## Functions

### `get_unique_key(base_key)`

Generate a unique key for UI components to avoid duplicate key errors.

Args:
    base_key: The base key to use
    
Returns:
    A unique key based on the base key

**Complexity:** 3

### `clear_keys()`

Clear all registered UI keys

**Complexity:** 1

### `register_keys(keys)`

Register multiple keys at once

**Complexity:** 2

### `is_key_used(key)`

Check if a key is already used

**Complexity:** 1

## Keywords

`used_ui_keys, session_state, base_key, str, counter, key, add, unique_key, Set, set, keys, streamlit, typing, Dict, Any, get_unique_key, clear_keys, register_keys, is_key_used, bool`

