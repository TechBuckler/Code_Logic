# simple.py

**Path:** `tools\shadow_tree\simple.py`

## Metrics

- **Lines of Code:** 535
- **Functions:** 21
- **Classes:** 3
- **Imports:** 6
- **Complexity:** 67

## Imports

- `import os`
- `import sys`
- `import json`
- `import ast`
- `import argparse`
- `from pathlib.Path`

## Classes

### ShadowNode

A node in the shadow tree.

#### Methods

- `__init__`
- `add_child`
- `to_dict`

### SimpleShadowTreeGenerator

Generates a natural language shadow tree from a code tree.

#### Methods

- `__init__`
- `generate_from_directory`
- `_process_directory`
- `_process_file`
- `_generate_descriptions`
- `_make_readable`
- `_save_shadow_tree`
- `_save_node`

### ShadowTreeNavigator

Navigate the shadow tree.

#### Methods

- `__init__`
- `bubble_up`
- `drill_down`
- `get_path_to_root`
- `search`
- `_search_node`

## Functions

### `generate_html_visualization(root_node, output_path)`

Generate an HTML visualization of the shadow tree.

**Complexity:** 1

### `_generate_node_html(node, node_id)`

Generate HTML for a node and its children.

**Complexity:** 5

### `main()`

**Complexity:** 11

### `_create_node_from_dict(data, parent)`

Create a shadow node from a dictionary.

**Complexity:** 2

### `__init__(self, name, path, code_path, parent)`

**Complexity:** 1

### `add_child(self, child)`

Add a child node.

**Complexity:** 1

### `to_dict(self)`

Convert the node to a dictionary.

**Complexity:** 1

### `__init__(self)`

**Complexity:** 1

### `generate_from_directory(self, code_dir, output_dir)`

Generate a shadow tree from a code directory.

**Complexity:** 2

### `_process_directory(self, directory, parent_node)`

Process a directory and add it to the shadow tree.

**Complexity:** 9

### `_process_file(self, file_path, node)`

Process a Python file and extract information.

**Complexity:** 6

### `_generate_descriptions(self, node)`

Generate natural language descriptions for nodes without docstrings.

**Complexity:** 14

### `_make_readable(self, name)`

Convert a snake_case or camelCase name to a readable string.

**Complexity:** 4

### `_save_shadow_tree(self, output_dir)`

Save the shadow tree to files.

**Complexity:** 1

### `_save_node(self, node, base_dir)`

Save a node to a file.

**Complexity:** 9

### `__init__(self, root_node)`

**Complexity:** 1

### `bubble_up(self, levels)`

Bubble up to a higher level in the tree.

**Complexity:** 3

### `drill_down(self, child_name)`

Drill down to a child node.

**Complexity:** 3

### `get_path_to_root(self)`

Get the path from the current node to the root.

**Complexity:** 2

### `search(self, query)`

Search for nodes matching the query.

**Complexity:** 1

### `_search_node(self, node, query, results)`

Search a node and its children for the query.

**Complexity:** 8

## Keywords

`node, name, print, child, summary, root, path, html, description, output_dir, code_path, tree, children, directory, tree_path, write, results, Path, parent, keywords`

