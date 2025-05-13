# final_cleanup.py

**Path:** `tools\reorganization\final_cleanup.py`

## Description

Final Cleanup

This script handles the final cleanup of files and folders that don't fit
the established directory structure.

## Metrics

- **Lines of Code:** 205
- **Functions:** 6
- **Classes:** 0
- **Imports:** 7
- **Complexity:** 27

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

### `move_files(dry_run)`

Move files to their appropriate locations.

**Complexity:** 6

### `handle_folders(dry_run)`

Handle folders that need to be moved or deleted.

**Complexity:** 13

### `create_tools_reorganization_dir(dry_run)`

Create tools/reorganization directory for reorganization scripts.

**Complexity:** 3

### `create_docs_diagrams_dir(dry_run)`

Create docs/diagrams directory for documentation diagrams.

**Complexity:** 3

### `create_tools_scripts_dir(dry_run)`

Create tools/scripts directory for utility scripts.

**Complexity:** 3

### `main()`

Main function.

**Complexity:** 2

## Keywords

`print, path, dry_run, tools, join, folder, project_root, exists, Would, reorganization, docs, diagrams, scripts, src_file, dest_path, destination, folder_path, shutil, dest_file, src_path`

