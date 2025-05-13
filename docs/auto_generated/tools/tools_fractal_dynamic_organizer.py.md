# dynamic_organizer.py

**Path:** `tools\fractal\dynamic_organizer.py`

## Description

Dynamic Directory Organizer

This script analyzes the codebase and automatically determines the optimal
directory structure based on file relationships, dependencies, and complexity.
It uses AST analysis and clustering to create a self-balancing directory structure.

## Metrics

- **Lines of Code:** 259
- **Functions:** 10
- **Classes:** 1
- **Imports:** 16
- **Complexity:** 26

## Imports

- `import os`
- `import sys`
- `import ast`
- `import re`
- `import importlib`
- `import math`
- `import json`
- `from pathlib.Path`
- `from collections.defaultdict`
- `from collections.Counter`
- `from utils.path_utils.ensure_dir`
- `from utils.path_utils.join_paths`
- `from utils.file_utils.read_file`
- `from utils.file_utils.write_file`
- `from utils.json_utils.load_json`
- `from utils.json_utils.save_json`
- `from tools.fractal.code_analyzer.analyze_file`
- `from tools.fractal.code_analyzer.extract_dependencies`
- `from tools.fractal.clustering.cluster_files`
- `from tools.fractal.clustering.calculate_similarity`
- `from tools.fractal.structure_optimizer.optimize_structure`
- `import argparse`

## Classes

### DynamicOrganizer

Dynamic directory organizer that uses code analysis to determine optimal structure.

#### Methods

- `__init__`
- `scan_files`
- `analyze_codebase`
- `cluster_files`
- `optimize_structure`
- `generate_plan`
- `apply_plan`
- `_get_new_path`
- `_flatten_structure`

## Functions

### `main()`

Main function.

**Complexity:** 2

### `__init__(self, root_dir)`

Initialize with the root directory to organize.

**Complexity:** 1

### `scan_files(self, extensions, exclude_dirs)`

Scan the directory for files to analyze.

**Complexity:** 6

### `analyze_codebase(self)`

Analyze the codebase to extract dependencies and complexity metrics.

**Complexity:** 5

### `cluster_files(self)`

Cluster files based on dependencies and similarity.

**Complexity:** 3

### `optimize_structure(self)`

Optimize the directory structure based on clusters.

**Complexity:** 1

### `generate_plan(self, output_file)`

Generate a reorganization plan.

**Complexity:** 4

### `apply_plan(self, plan, dry_run)`

Apply the reorganization plan.

**Complexity:** 4

### `_get_new_path(self, file_path)`

Get the new path for a file based on the optimized structure.

**Complexity:** 3

### `_flatten_structure(self, structure, prefix)`

Flatten the nested structure into a dictionary of paths.

**Complexity:** 4

## Keywords

`plan, path, files, print, file_path, structure, extensions, root_dir, move, organizer, destination, file_data, clusters, file, join, source, dry_run, info, parser, moves`

