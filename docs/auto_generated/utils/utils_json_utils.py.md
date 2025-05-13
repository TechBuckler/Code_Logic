# json_utils.py

**Path:** `utils\json_utils.py`

## Description

JSON utility functions for common JSON operations.

This module provides standardized functions for JSON parsing, serialization,
and manipulation, reducing code duplication across the codebase.

## Metrics

- **Lines of Code:** 67
- **Functions:** 6
- **Classes:** 0
- **Imports:** 2
- **Complexity:** 9

## Imports

- `import json`
- `import os`

## Functions

### `load_json(file_path)`

Load JSON from a file.

**Complexity:** 1

### `save_json(file_path, data, indent)`

Save data to a JSON file.

**Complexity:** 1

### `parse_json(json_string)`

Parse a JSON string.

**Complexity:** 1

### `to_json(data, indent)`

Convert data to a JSON string.

**Complexity:** 1

### `merge_json(base, override)`

Merge two JSON objects, with override taking precedence.

**Complexity:** 5

### `json_to_file_if_changed(file_path, data, indent)`

Save JSON to a file only if the content has changed.

**Complexity:** 5

## Keywords

`file_path, indent, json, key, path, open, encoding, utf, json_str, makedirs, dirname, abspath, exist_ok, json_string, dumps, merge_json, base, override, isinstance, dict`

