# refactor_modules.py

**Path:** `tools\refactor_modules.py`

## Description

Module Refactoring Script

This script refactors all modules according to the reorganization plan,
moving files to their new locations and updating imports.

## Metrics

- **Lines of Code:** 196
- **Functions:** 4
- **Classes:** 0
- **Imports:** 7
- **Complexity:** 14

## Imports

- `import os`
- `import sys`
- `import re`
- `import shutil`
- `from pathlib.Path`
- `from utils.path_utils.ensure_dir`
- `from utils.path_utils.join_paths`
- `from utils.file_utils.read_file`
- `from utils.file_utils.write_file`

## Functions

### `create_init_files(directory)`

Create __init__.py files in all subdirectories.

**Complexity:** 3

### `update_imports(content, module_type)`

Update import statements in the content.

**Complexity:** 3

### `refactor_module(old_path, new_path, module_type, dry_run)`

Refactor a module by moving it and updating imports.

**Complexity:** 3

### `main()`

Main function.

**Complexity:** 6

## Keywords

`new_path, module_type, old_path, src, modules, tools, core, standard, path, utils, print, module, updated_content, dry_run, sys, project_root, entry, content, renderers, directory`

