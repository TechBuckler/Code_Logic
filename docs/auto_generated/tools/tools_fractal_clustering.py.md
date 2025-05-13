# clustering.py

**Path:** `tools\fractal\clustering.py`

## Description

Clustering Module

Provides functions for clustering files based on their similarity
and relationships to create a balanced directory structure.

## Metrics

- **Lines of Code:** 202
- **Functions:** 6
- **Classes:** 0
- **Imports:** 6
- **Complexity:** 18

## Imports

- `import numpy as np`
- `from collections.defaultdict`
- `import networkx as nx`
- `from sklearn.feature_extraction.text.TfidfVectorizer`
- `from sklearn.cluster.AgglomerativeClustering`
- `import community as community_louvain`

## Functions

### `calculate_similarity(file1_data, file2_data, deps1, deps2)`

Calculate similarity between two files based on their analysis data.

Args:
    file1_data: Analysis data for file 1
    file2_data: Analysis data for file 2
    deps1: Dependencies of file 1
    deps2: Dependencies of file 2
    
Returns:
    Similarity score (0-1)

**Complexity:** 1

### `cluster_files(files, similarity_matrix, min_cluster_size, max_cluster_size)`

Cluster files based on similarity.

Args:
    files: List of file paths
    similarity_matrix: Dictionary mapping (file1, file2) tuples to similarity scores
    min_cluster_size: Minimum size of a cluster
    max_cluster_size: Maximum size of a cluster
    
Returns:
    List of clusters, where each cluster is a list of file paths

**Complexity:** 4

### `_detect_communities(graph)`

Detect communities in the graph using the Louvain method.

**Complexity:** 4

### `_balance_clusters(clusters, min_size, max_size)`

Balance cluster sizes to be within the specified range.

**Complexity:** 4

### `_split_cluster(cluster, max_size)`

Split a large cluster into smaller subclusters.

**Complexity:** 5

### `_merge_small_clusters(clusters, min_size)`

Merge small clusters to meet the minimum size requirement.

**Complexity:** 5

## Keywords

`cluster, len, max_size, current_cluster, structure1, structure2, file1_data, file2_data, max, metrics, append, weights, similarity, communities, list, min_size, subclusters, imports, keywords, set`

