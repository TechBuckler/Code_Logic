# test_shadow_tree.py

**Path:** `tests\integration\test_shadow_tree.py`

## Description

Integration test for the Shadow Tree module.

This test verifies that the Shadow Tree functionality works correctly
with the reorganized codebase structure.

## Metrics

- **Lines of Code:** 91
- **Functions:** 5
- **Classes:** 1
- **Imports:** 7
- **Complexity:** 7

## Imports

- `import os`
- `import sys`
- `import unittest`
- `from pathlib.Path`
- `from tools.shadow_tree.shadow_tree.ShadowTreeGenerator`
- `from tools.shadow_tree.shadow_tree.ShadowTreeNavigator`
- `from tools.shadow_tree.shadow_tree.ShadowTreeAPI`
- `from utils.path_utils.ensure_dir`
- `from utils.path_utils.join_paths`
- `from utils.file_utils.read_file`
- `from utils.file_utils.write_file`

## Classes

### TestShadowTree

Test the Shadow Tree functionality.

#### Methods

- `setUp`
- `test_shadow_tree_generation`
- `test_shadow_tree_navigation`
- `test_shadow_tree_search`
- `test_shadow_tree_visualization`

#### Inherits From


## Functions

### `setUp(self)`

Set up the test environment.

**Complexity:** 1

### `test_shadow_tree_generation(self)`

Test that the Shadow Tree can be generated.

**Complexity:** 1

### `test_shadow_tree_navigation(self)`

Test that the Shadow Tree can be navigated.

**Complexity:** 3

### `test_shadow_tree_search(self)`

Test that the Shadow Tree can be searched.

**Complexity:** 2

### `test_shadow_tree_visualization(self)`

Test that the Shadow Tree can be visualized.

**Complexity:** 2

## Keywords

`api, path, shadow_dir, shadow_tree, join_paths, project_root, assertTrue, exists, regenerate, json, should, navigate, results, sys, unittest, dirname, assertIsNotNone, child_name, ShadowTreeAPI, utils`

