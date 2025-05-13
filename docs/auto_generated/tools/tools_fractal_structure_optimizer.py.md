# structure_optimizer.py

**Path:** `tools\fractal\structure_optimizer.py`

## Description

Structure Optimizer Module

Optimizes the directory structure based on file clusters and analysis
to create a balanced, fractal organization.

## Metrics

- **Lines of Code:** 380
- **Functions:** 12
- **Classes:** 0
- **Imports:** 6
- **Complexity:** 55

## Imports

- `import os`
- `import re`
- `from collections.defaultdict`
- `import networkx as nx`
- `from pathlib.Path`
- `import community as community_louvain`

## Functions

### `optimize_structure(clusters, file_data, min_files, max_files, max_depth, balance_factor)`

Optimize the directory structure based on file clusters.

Args:
    clusters: List of file clusters
    file_data: Dictionary mapping file paths to analysis data
    min_files: Minimum number of files per directory
    max_files: Maximum number of files per directory
    max_depth: Maximum directory depth
    balance_factor: Weight between depth and breadth (0-1)
    
Returns:
    Dictionary representing the optimized directory structure

**Complexity:** 1

### `_create_initial_structure(clusters, file_data)`

Create an initial directory structure from file clusters.

**Complexity:** 2

### `_extract_cluster_keywords(cluster, file_data)`

Extract common keywords from files in a cluster.

**Complexity:** 4

### `_generate_description(cluster, file_data, keywords)`

Generate a description for a directory based on its files.

**Complexity:** 5

### `_optimize_tree(structure, min_files, max_files, max_depth, balance_factor)`

Optimize the directory tree structure.

**Complexity:** 8

### `_group_files_by_pattern(files, file_data)`

Group files by common patterns or prefixes.

**Complexity:** 12

### `_find_common_prefixes(files)`

Find common prefixes among filenames.

**Complexity:** 7

### `_group_directories(structure, min_files, max_files, max_depth, balance_factor)`

Group similar directories together to reduce the total number.

**Complexity:** 12

### `_calculate_directory_similarity(dir1_info, dir2_info)`

Calculate similarity between two directories.

**Complexity:** 2

### `_generate_directory_names(structure, file_data)`

Generate meaningful names for directories based on their content.

**Complexity:** 6

### `_generate_name_from_keywords(keywords)`

Generate a directory name from keywords.

**Complexity:** 2

### `_generate_name_from_files(files, file_data)`

Generate a directory name from file names.

**Complexity:** 5

## Keywords

`files, file_data, structure, keywords, info, name, groups, file, len, max_files, append, subdirs, prefix, min_files, max_depth, balance_factor, cluster, description, new_structure, named_structure`

