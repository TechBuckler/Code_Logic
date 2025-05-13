# complete_cleanup.py

**Path:** `tools\reorganization\complete_cleanup.py`

## Description

Complete Cleanup

This script handles the final remaining items that need to be cleaned up.

## Metrics

- **Lines of Code:** 205
- **Functions:** 5
- **Classes:** 0
- **Imports:** 7
- **Complexity:** 40

## Imports

- `import os`
- `import sys`
- `import shutil`
- `from pathlib.Path`
- `from utils.path_utils.ensure_dir`
- `from utils.path_utils.join_paths`
- `from utils.file_utils.read_file`
- `from utils.file_utils.write_file`
- `import argparse`

## Functions

### `cleanup_pycache(dry_run)`

Remove __pycache__ directories.

**Complexity:** 8

### `handle_templates_dir(dry_run)`

Move templates directory to appropriate location.

**Complexity:** 22

### `move_cleanup_scripts(dry_run)`

Move cleanup scripts to tools/reorganization/.

**Complexity:** 7

### `self_destruct(dry_run)`

Remove this script after execution.

**Complexity:** 2

### `main()`

Main function.

**Complexity:** 3

## Keywords

`path, print, dry_run, script, project_root, join, dest_dir, shutil, templates, templates_dir, exists, src_item, dest_item, pycache_dir, Would, dest_path, dest_subitem, tools, reorganization, pycache_dirs`

