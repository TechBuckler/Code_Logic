# shadow_tree.py

**Path:** `tools\shadow_tree.py`

## Description

Shadow Tree Generator

Creates a natural language shadow tree that mirrors the code structure,
allowing intuitive navigation through the fractal codebase.

## Metrics

- **Lines of Code:** 899
- **Functions:** 44
- **Classes:** 6
- **Imports:** 16
- **Complexity:** 120

## Imports

- `import os`
- `import sys`
- `import ast`
- `import re`
- `import nltk`
- `import importlib`
- `from pathlib.Path`
- `from typing.Dict`
- `from typing.List`
- `from typing.Set`
- `from typing.Any`
- `from typing.Tuple`
- `from typing.Optional`
- `from typing.Union`
- `from typing.Callable`
- `from utils.path_utils.ensure_dir`
- `from utils.path_utils.join_paths`
- `from utils.path_utils.get_file_name`
- `from utils.file_utils.read_file`
- `from utils.file_utils.write_file`
- `from utils.json_utils.load_json`
- `from utils.json_utils.save_json`
- `from utils.string_utils.clean_text`
- `from utils.string_utils.normalize_string`
- `from nltk.tokenize.word_tokenize`
- `from nltk.corpus.wordnet`
- `from nltk.stem.WordNetLemmatizer`
- `import argparse`

## Classes

### ShadowNode

A node in the shadow tree.

#### Methods

- `__init__`
- `add_child`
- `to_dict`
- `__str__`

### ShadowTreeGenerator

Generates a natural language shadow tree from a code tree.

#### Methods

- `__init__`
- `generate_from_directory`
- `_process_directory`
- `_process_file`
- `_generate_descriptions`
- `_summarize_text`
- `_extract_keywords`
- `_make_readable`
- `_save_shadow_tree`
- `_save_node`

### ShadowTreeNavigator

Navigates the shadow tree.

#### Methods

- `__init__`
- `_load_tree`
- `_dict_to_node`
- `go_up`
- `go_down`
- `go_to_path`
- `search`
- `get_current_view`
- `get_bubble_up_view`
- `get_path_to_root`

### ShadowTreeVisualizer

Visualizes the shadow tree.

#### Methods

- `__init__`
- `generate_markdown`
- `_write_node_markdown`
- `_write_node_details`
- `generate_html`
- `_write_node_html`

### ShadowTreeAPI

API for interacting with the shadow tree.

#### Methods

- `__init__`
- `regenerate`
- `get_current_view`
- `get_bubble_up_view`
- `search`
- `navigate`
- `visualize`
- `get_code_path`
- `get_shadow_path`

### WordNetLemmatizer

#### Methods

- `lemmatize`

## Functions

### `main()`

Main function for the shadow tree.

**Complexity:** 5

### `__init__(self, name, path, code_path, parent)`

**Complexity:** 1

### `add_child(self, child)`

Add a child node to this node.

**Complexity:** 1

### `to_dict(self)`

Convert the node to a dictionary.

**Complexity:** 1

### `__str__(self)`

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

**Complexity:** 4

### `_generate_descriptions(self, node)`

Generate natural language descriptions for nodes without docstrings.

**Complexity:** 14

### `_summarize_text(self, text)`

Summarize a text to a short description.

**Complexity:** 3

### `_extract_keywords(self, content)`

Extract keywords from content.

**Complexity:** 5

### `_make_readable(self, name)`

Convert a code name to a readable string.

**Complexity:** 1

### `_save_shadow_tree(self, output_dir)`

Save the shadow tree to files.

**Complexity:** 2

### `_save_node(self, node, base_dir)`

Save a node to a file.

**Complexity:** 7

### `__init__(self, shadow_tree_path)`

Initialize with the path to the shadow tree JSON file.

**Complexity:** 2

### `_load_tree(self)`

Load the shadow tree from JSON.

**Complexity:** 4

### `_dict_to_node(self, node_dict, parent)`

Convert a dictionary to a ShadowNode.

**Complexity:** 6

### `go_up(self)`

Go up one level in the shadow tree.

**Complexity:** 3

### `go_down(self, name)`

Go down to a child node.

**Complexity:** 14

### `go_to_path(self, path)`

Go to a specific path in the shadow tree.

**Complexity:** 8

### `search(self, query)`

Search the shadow tree for nodes matching the query.

**Complexity:** 6

### `get_current_view(self)`

Get the current view of the shadow tree.

**Complexity:** 1

### `get_bubble_up_view(self, levels)`

Get a bubble-up view of the shadow tree.

**Complexity:** 5

### `get_path_to_root(self)`

Get the path from current node to root.

**Complexity:** 5

### `__init__(self, shadow_tree)`

Initialize with a shadow tree.

**Complexity:** 1

### `generate_markdown(self, output_path, max_depth)`

Generate a markdown representation of the shadow tree.

**Complexity:** 1

### `_write_node_markdown(self, file, node, level, max_depth)`

Write a node to the markdown file.

**Complexity:** 4

### `_write_node_details(self, file, node)`

Write node details to the markdown file.

**Complexity:** 5

### `generate_html(self, output_path, max_depth)`

Generate an HTML visualization of the shadow tree.

**Complexity:** 1

### `_write_node_html(self, file, node, level, max_depth, node_id)`

Write a node to the HTML file.

**Complexity:** 8

### `__init__(self, code_dir, shadow_dir)`

Initialize the API.

**Complexity:** 8

### `regenerate(self)`

Regenerate the shadow tree.

**Complexity:** 1

### `get_current_view(self)`

Get the current view of the shadow tree.

**Complexity:** 1

### `get_bubble_up_view(self, levels)`

Get a bubble-up view of the shadow tree.

**Complexity:** 1

### `search(self, query)`

Search the shadow tree.

**Complexity:** 1

### `navigate(self, path, up, down)`

Navigate the shadow tree.

**Complexity:** 4

### `visualize(self, format, max_depth)`

Visualize the shadow tree.

**Complexity:** 2

### `get_code_path(self)`

Get the code path for the current node.

**Complexity:** 1

### `get_shadow_path(self)`

Get the shadow path for the current node.

**Complexity:** 1

### `word_tokenize(text)`

**Complexity:** 1

### `search_node(node)`

**Complexity:** 6

### `add_descendants(node, level)`

**Complexity:** 3

### `lemmatize(self, word)`

**Complexity:** 1

## Keywords

`node, print, name, child, current_node, path, children, tree, summary, parent, code_path, current, description, level, file, str, write, append, keywords, output_dir`

