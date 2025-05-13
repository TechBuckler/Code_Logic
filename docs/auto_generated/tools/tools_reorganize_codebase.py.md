# reorganize_codebase.py

**Path:** `tools\reorganize_codebase.py`

## Description

Codebase Reorganization Tool

This script reorganizes the codebase according to the plan outlined in
reorganization_plan.md, using the existing fractal organizer and resource
splitter tools.

## Metrics

- **Lines of Code:** 644
- **Functions:** 11
- **Classes:** 0
- **Imports:** 7
- **Complexity:** 56

## Imports

- `import os`
- `import sys`
- `import shutil`
- `from pathlib.Path`
- `import importlib.util`
- `import re`
- `import argparse`

## Functions

### `create_directory_structure(base_dir, structure, level)`

Create the target directory structure.

**Complexity:** 4

### `classify_file(file_path)`

Classify a file based on its name and content.

**Complexity:** 9

### `copy_file_to_target(src_file, target_dir, dry_run)`

Copy a file to its target directory.

**Complexity:** 3

### `scan_and_classify_files(src_dir, target_base_dir, dry_run)`

Scan the source directory and classify files.

**Complexity:** 6

### `update_imports(file_path, old_to_new_mapping)`

Update import statements in a file.

**Complexity:** 2

### `reorganize_codebase(dry_run)`

Reorganize the codebase according to the plan.

**Complexity:** 10

### `apply_fractal_organization(target_dir)`

Apply fractal organization to the reorganized codebase.

**Complexity:** 2

### `apply_resource_splitting(target_dir)`

Apply resource splitting to the reorganized codebase.

**Complexity:** 2

### `identify_duplicate_functionality(src_dir)`

Identify duplicate functionality across the codebase.

**Complexity:** 15

### `create_helper_files(target_dir, duplicates)`

Create helper files to consolidate duplicate functionality.

**Complexity:** 6

### `main(dry_run)`

Main function.

**Complexity:** 3

## Keywords

`print, path, file_path, target_dir, files, join, dry_run, helper_file, file, duplicates, target_base_dir, project_root, src_file, src_dir, core, utils, open, root, content, util`

