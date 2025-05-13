# shadow_tree_module.py

**Path:** `modules\standard\organization\shadow_tree_module.py`

## Description

Shadow Tree Module

This module integrates the Shadow Tree system with the unified UI,
allowing for natural language navigation of the codebase.

## Metrics

- **Lines of Code:** 349
- **Functions:** 13
- **Classes:** 1
- **Imports:** 5
- **Complexity:** 66

## Imports

- `import os`
- `import sys`
- `import json`
- `from pathlib.Path`
- `from shadow_tree.ShadowTreeGenerator`
- `from shadow_tree.ShadowTreeNavigator`
- `from shadow_tree.ShadowNode`
- `from shadow_tree.ShadowTreeAPI`

## Classes

### ShadowTreeModule

Module for integrating the Shadow Tree with the unified UI.

#### Methods

- `__init__`
- `initialize`
- `_load_or_generate_tree`
- `can_process`
- `process`
- `_search`
- `_bubble_up`
- `_drill_down`
- `_show_children`
- `_show_current_location`
- `_format_node_info`
- `get_help`
- `_regenerate_tree`

## Functions

### `__init__(self)`

**Complexity:** 1

### `initialize(self)`

Initialize the module.

**Complexity:** 1

### `_load_or_generate_tree(self)`

Load the shadow tree if it exists, or generate it if not.

**Complexity:** 8

### `can_process(self, command)`

Check if this module can process the given command.

**Complexity:** 1

### `process(self, command)`

Process a command related to the Shadow Tree.

**Complexity:** 18

### `_search(self, query)`

Search the shadow tree for the given query.

**Complexity:** 5

### `_bubble_up(self, levels)`

Bubble up to a higher level in the tree.

**Complexity:** 7

### `_drill_down(self, target)`

Drill down to a child node.

**Complexity:** 5

### `_show_children(self)`

Show the children of the current node.

**Complexity:** 7

### `_show_current_location(self)`

Show the current location in the shadow tree.

**Complexity:** 5

### `_format_node_info(self, node)`

Format information about a node.

**Complexity:** 12

### `get_help(self)`

Get help information for this module.

**Complexity:** 1

### `_regenerate_tree(self)`

Regenerate the shadow tree.

**Complexity:** 5

## Keywords

`navigator, output, command, node, Shadow, Tree, summary, print, str, path, shadow_dir, tree, child, name, levels, children, Error, current_node, code_dir, Exception`

