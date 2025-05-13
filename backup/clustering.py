"""
Clustering Module

Provides functions for clustering files based on their similarity
and relationships to create a balanced directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase




def calculate_similarity(file1_data, file2_data, deps1, deps2):
    """
    Calculate similarity between two files based on their analysis data.
    
    Args:
        file1_data: Analysis data for file 1
        file2_data: Analysis data for file 2
        deps1: Dependencies of file 1
        deps2: Dependencies of file 2
        
    Returns:
        Similarity score (0-1)
    """
    # Initialize weights for different similarity factors
    weights = {
        "dependencies": 0.3,
        "imports": 0.2,
        "keywords": 0.2,
        "structure": 0.3
    }
    
    # Calculate dependency similarity
    deps_similarity = len(deps1.intersection(deps2)) / max(1, len(deps1.union(deps2)))
    
    # Calculate import similarity
    imports1 = set(imp["module"] for imp in file1_data["semantics"]["imports"])
    imports2 = set(imp["module"] for imp in file2_data["semantics"]["imports"])
    imports_similarity = len(imports1.intersection(imports2)) / max(1, len(imports1.union(imports2)))
    
    # Calculate keyword similarity
    keywords1 = set(file1_data["semantics"]["keywords"])
    keywords2 = set(file2_data["semantics"]["keywords"])
    keywords_similarity = len(keywords1.intersection(keywords2)) / max(1, len(keywords1.union(keywords2)))
    
    # Calculate structure similarity
    structure1 = (
        file1_data["metrics"]["functions"],
        file1_data["metrics"]["classes"],
        file1_data["metrics"]["complexity"]
    )
    structure2 = (
        file2_data["metrics"]["functions"],
        file2_data["metrics"]["classes"],
        file2_data["metrics"]["complexity"]
    )
    
    # Normalize structure metrics
    max_funcs = max(structure1[0], structure2[0]) or 1
    max_classes = max(structure1[1], structure2[1]) or 1
    max_complexity = max(structure1[2], structure2[2]) or 1
    
    structure_diff = (
        abs(structure1[0] - structure2[0]) / max_funcs,
        abs(structure1[1] - structure2[1]) / max_classes,
        abs(structure1[2] - structure2[2]) / max_complexity
    )
    
    structure_similarity = 1 - sum(structure_diff) / 3
    
    # Calculate weighted similarity
    similarity = (
        weights["dependencies"] * deps_similarity +
        weights["imports"] * imports_similarity +
        weights["keywords"] * keywords_similarity +
        weights["structure"] * structure_similarity
    )
    
    return similarity

def cluster_files(files, similarity_matrix, min_cluster_size=3, max_cluster_size=20):
    """
    Cluster files based on similarity.
    
    Args:
        files: List of file paths
        similarity_matrix: Dictionary mapping (file1, file2) tuples to similarity scores
        min_cluster_size: Minimum size of a cluster
        max_cluster_size: Maximum size of a cluster
        
    Returns:
        List of clusters, where each cluster is a list of file paths
    """
    # Create a graph where nodes are files and edges are weighted by similarity
    G = nx.Graph()
    
    # Add nodes
    for file in files:
        G.add_node(file)
    
    # Add edges
    for (file1, file2), similarity in similarity_matrix.items():
        if similarity > 0.3:  # Only add edges for files with significant similarity
            G.add_edge(file1, file2, weight=similarity)
    
    # Use community detection to find clusters
    communities = _detect_communities(G)
    
    # Balance cluster sizes
    balanced_clusters = _balance_clusters(communities, min_cluster_size, max_cluster_size)
    
    return balanced_clusters

def _detect_communities(graph):
    """Detect communities in the graph using the Louvain method."""
    try:
        partition = community_louvain.best_partition(graph)
        
        # Group files by community
        communities = defaultdict(list)
        for node, community_id in partition.items():
            communities[community_id].append(node)
            
        return list(communities.values())
    except ImportError:
        # Fallback to connected components if community detection is not available
        return [list(c) for c in nx.connected_components(graph)]

def _balance_clusters(clusters, min_size, max_size):
    """Balance cluster sizes to be within the specified range."""
    result = []
    
    for cluster in clusters:
        if len(cluster) < min_size:
            # Cluster is too small, add to result as is (will be merged later)
            result.append(cluster)
        elif len(cluster) > max_size:
            # Cluster is too large, split it
            subclusters = _split_cluster(cluster, max_size)
            result.extend(subclusters)
        else:
            # Cluster is just right
            result.append(cluster)
    
    # Merge small clusters
    return _merge_small_clusters(result, min_size)

def _split_cluster(cluster, max_size):
    """Split a large cluster into smaller subclusters."""
    if len(cluster) <= max_size:
        return [cluster]
    
    # Calculate number of subclusters needed
    num_subclusters = (len(cluster) + max_size - 1) // max_size
    
    # Use k-means to split the cluster
    try:
        # Create a feature matrix from filenames (as a simple heuristic)
        filenames = [os.path.basename(f) for f in cluster]
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
        X = vectorizer.fit_transform(filenames)
        
        # Apply clustering
        clustering = AgglomerativeClustering(n_clusters=num_subclusters)
        labels = clustering.fit_predict(X.toarray())
        
        # Group files by cluster
        subclusters = defaultdict(list)
        for i, label in enumerate(labels):
            subclusters[label].append(cluster[i])
            
        return list(subclusters.values())
    except Exception:
        # Fallback to simple chunking if clustering fails
        return [cluster[i:i+max_size] for i in range(0, len(cluster), max_size)]

def _merge_small_clusters(clusters, min_size):
    """Merge small clusters to meet the minimum size requirement."""
    # Sort clusters by size (smallest first)
    sorted_clusters = sorted(clusters, key=len)
    
    result = []
    current_cluster = []
    
    for cluster in sorted_clusters:
        if len(current_cluster) + len(cluster) <= min_size * 2:
            # Merge clusters
            current_cluster.extend(cluster)
        else:
            # Current cluster is large enough, add to result
            if current_cluster:
                result.append(current_cluster)
            current_cluster = cluster
    
    # Add the last cluster
    if current_cluster:
        result.append(current_cluster)
    
    return result
