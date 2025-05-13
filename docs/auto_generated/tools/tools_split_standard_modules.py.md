# split_standard_modules.py

**Path:** `tools\split_standard_modules.py`

## Description

Split Standard Modules

This script splits the modules/standard directory into more specific categories
to maintain a balanced directory structure.

## Metrics

- **Lines of Code:** 154
- **Functions:** 3
- **Classes:** 0
- **Imports:** 7
- **Complexity:** 21

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

### `split_standard_modules(dry_run)`

Split the standard modules directory into categories.

**Complexity:** 10

### `update_imports_in_directory(directory)`

Update imports in all Python files in a directory (recursive).

**Complexity:** 9

### `main()`

Main function.

**Complexity:** 2

## Keywords

`print, modules, category, file, standard, path, join_paths, content, project_root, dry_run, standard_dir, files, src_path, file_path, apply, MODULE_CATEGORIES, Standard, directory, replace, sys`

