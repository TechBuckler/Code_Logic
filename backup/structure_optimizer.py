"""
Structure Optimizer Module

Optimizes the directory structure based on file clusters and analysis
to create a balanced, fractal organization.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import re

def optimize_structure(clusters, file_data, min_files=5, max_files=20, max_depth=4, balance_factor=0.7):
    """
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
    """
    # Create initial structure from clusters
    initial_structure = _create_initial_structure(clusters, file_data)
    
    # Optimize the structure
    optimized_structure = _optimize_tree(
        initial_structure,
        min_files=min_files,
        max_files=max_files,
        max_depth=max_depth,
        balance_factor=balance_factor
    )
    
    # Generate directory names
    named_structure = _generate_directory_names(optimized_structure, file_data)
    
    return named_structure

def _create_initial_structure(clusters, file_data):
    """Create an initial directory structure from file clusters."""
    structure = {}
    
    for i, cluster in enumerate(clusters):
        # Create a directory for each cluster
        dir_name = f"cluster_{i}"
        
        # Extract keywords from files in the cluster
        keywords = _extract_cluster_keywords(cluster, file_data)
        
        # Create directory entry
        structure[dir_name] = {
            "files": cluster,
            "keywords": keywords,
            "description": _generate_description(cluster, file_data, keywords)
        }
    
    return structure

def _extract_cluster_keywords(cluster, file_data):
    """Extract common keywords from files in a cluster."""
    # Collect all keywords
    all_keywords = []
    for file_path in cluster:
        if file_path in file_data:
            all_keywords.extend(file_data[file_path]["semantics"]["keywords"])
    
    # Count keyword frequencies
    keyword_counts = defaultdict(int)
    for keyword in all_keywords:
        keyword_counts[keyword] += 1
    
    # Sort by frequency
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Return top keywords
    return [k for k, _ in sorted_keywords[:10]]

def _generate_description(cluster, file_data, keywords):
    """Generate a description for a directory based on its files."""
    # Extract docstrings
    docstrings = []
    for file_path in cluster:
        if file_path in file_data:
            docstring = file_data[file_path]["semantics"]["docstring"]
            if docstring:
                docstrings.append(docstring.split("\n")[0])  # First line of docstring
    
    # If we have docstrings, use them
    if docstrings:
        return " / ".join(docstrings[:3])
    
    # Otherwise, use keywords
    return "Contains files related to: " + ", ".join(keywords[:5])

def _optimize_tree(structure, min_files, max_files, max_depth, balance_factor):
    """Optimize the directory tree structure."""
    # Check if we need to split or merge directories
    total_files = sum(len(info["files"]) for info in structure.values())
    
    if total_files <= max_files:
        # Small enough to be a single directory
        return structure
    
    if max_depth <= 1:
        # Reached maximum depth, can't split further
        return structure
    
    # Check if any directories are too large
    large_dirs = {name: info for name, info in structure.items() if len(info["files"]) > max_files}
    
    if large_dirs:
        # Split large directories
        new_structure = {}
        
        for name, info in structure.items():
            if name in large_dirs:
                # Split this directory
                files = info["files"]
                
                # Group files by common prefixes or patterns
                groups = _group_files_by_pattern(files, file_data)
                
                # Create subdirectories
                subdirs = {}
                for subname, subfiles in groups.items():
                    subdirs[subname] = {
                        "files": subfiles,
                        "keywords": _extract_cluster_keywords(subfiles, file_data),
                        "description": _generate_description(subfiles, file_data, [])
                    }
                
                # Optimize subdirectories recursively
                optimized_subdirs = _optimize_tree(
                    subdirs,
                    min_files=min_files,
                    max_files=max_files,
                    max_depth=max_depth - 1,
                    balance_factor=balance_factor
                )
                
                # Add to new structure
                new_structure[name] = {
                    "files": [],  # No files directly in this directory
                    "keywords": info["keywords"],
                    "description": info["description"],
                    "subdirs": optimized_subdirs
                }
            else:
                # Keep this directory as is
                new_structure[name] = info
        
        return new_structure
    
    # Check if we have too many small directories
    if len(structure) > max_files:
        # Group similar directories
        return _group_directories(structure, min_files, max_files, max_depth, balance_factor)
    
    # Structure is already balanced
    return structure

def _group_files_by_pattern(files, file_data):
    """Group files by common patterns or prefixes."""
    groups = defaultdict(list)
    
    # Try to find common prefixes
    prefixes = _find_common_prefixes(files)
    
    if prefixes:
        # Group by prefix
        for file in files:
            filename = os.path.basename(file)
            for prefix in prefixes:
                if filename.startswith(prefix):
                    groups[prefix].append(file)
                    break
            else:
                # No matching prefix
                groups["other"].append(file)
    else:
        # Group by file type or purpose
        for file in files:
            if file in file_data:
                # Check if it's a test file
                if "test" in os.path.basename(file).lower():
                    groups["tests"].append(file)
                # Check if it's a utility file
                elif "util" in os.path.basename(file).lower():
                    groups["utils"].append(file)
                # Check if it's a model/data file
                elif any(kw in file_data[file]["semantics"]["keywords"] for kw in ["model", "data", "schema"]):
                    groups["models"].append(file)
                # Check if it's a view/UI file
                elif any(kw in file_data[file]["semantics"]["keywords"] for kw in ["view", "ui", "render"]):
                    groups["views"].append(file)
                else:
                    # Default group
                    groups["core"].append(file)
            else:
                # No analysis data
                groups["other"].append(file)
    
    # Ensure all files are grouped
    if sum(len(g) for g in groups.values()) != len(files):
        # Fallback to simple chunking
        chunk_size = max(min_files, len(files) // (max_files // 2))
        groups = {f"group_{i}": files[i:i+chunk_size] for i in range(0, len(files), chunk_size)}
    
    return groups

def _find_common_prefixes(files):
    """Find common prefixes among filenames."""
    filenames = [os.path.basename(f) for f in files]
    
    # Extract word prefixes
    prefixes = set()
    for filename in filenames:
        # Split by common separators
        parts = re.split(r'[_\-.]', filename)
        if parts:
            prefixes.add(parts[0])
    
    # Filter out short or too common prefixes
    valid_prefixes = []
    for prefix in prefixes:
        if len(prefix) >= 3:  # Minimum prefix length
            count = sum(1 for f in filenames if f.startswith(prefix))
            if count >= 2 and count <= len(files) * 0.8:  # Not too rare or too common
                valid_prefixes.append(prefix)
    
    return valid_prefixes

def _group_directories(structure, min_files, max_files, max_depth, balance_factor):
    """Group similar directories together to reduce the total number."""
    # Create a graph where nodes are directories and edges are weighted by similarity
    G = nx.Graph()
    
    # Add nodes
    for name in structure:
        G.add_node(name)
    
    # Add edges
    for name1 in structure:
        for name2 in structure:
            if name1 != name2:
                similarity = _calculate_directory_similarity(
                    structure[name1],
                    structure[name2]
                )
                if similarity > 0.3:  # Only add edges for directories with significant similarity
                    G.add_edge(name1, name2, weight=similarity)
    
    # Use community detection to find groups
    try:
        partition = community_louvain.best_partition(G)
        
        # Group directories by community
        groups = defaultdict(list)
        for node, community_id in partition.items():
            groups[community_id].append(node)
    except ImportError:
        # Fallback to connected components
        groups = [list(c) for c in nx.connected_components(G)]
    
    # Create new structure with grouped directories
    new_structure = {}
    
    # Handle groups appropriately based on its type
    group_items = groups.values() if isinstance(groups, dict) else groups
    
    for i, group in enumerate(group_items):
        if len(group) == 1:
            # Single directory, keep as is
            name = group[0]
            new_structure[name] = structure[name]
        else:
            # Multiple directories, create a parent directory
            group_name = f"group_{i}"
            
            # Collect all files
            all_files = []
            all_keywords = []
            descriptions = []
            
            for name in group:
                info = structure[name]
                all_files.extend(info["files"])
                all_keywords.extend(info["keywords"])
                descriptions.append(info["description"])
            
            # Create subdirectories
            subdirs = {name: structure[name] for name in group}
            
            # Add to new structure
            new_structure[group_name] = {
                "files": [],  # No files directly in this directory
                "keywords": list(set(all_keywords)),
                "description": " / ".join(descriptions[:3]),
                "subdirs": subdirs
            }
    
    return new_structure

def _calculate_directory_similarity(dir1_info, dir2_info):
    """Calculate similarity between two directories."""
    # Calculate keyword similarity
    keywords1 = set(dir1_info["keywords"])
    keywords2 = set(dir2_info["keywords"])
    
    if not keywords1 or not keywords2:
        return 0
    
    return len(keywords1.intersection(keywords2)) / max(1, len(keywords1.union(keywords2)))

def _generate_directory_names(structure, file_data):
    """Generate meaningful names for directories based on their content."""
    named_structure = {}
    
    for name, info in structure.items():
        # Generate a better name if possible
        if name.startswith(("cluster_", "group_")):
            # Try to generate a better name
            new_name = _generate_name_from_keywords(info["keywords"])
            if not new_name:
                new_name = _generate_name_from_files(info.get("files", []), file_data)
            
            if new_name:
                name = new_name
        
        # Process subdirectories recursively
        if "subdirs" in info:
            subdirs = _generate_directory_names(info["subdirs"], file_data)
            named_structure[name] = {
                "files": info.get("files", []),
                "description": info["description"],
                "subdirs": subdirs
            }
        else:
            named_structure[name] = info
    
    return named_structure

def _generate_name_from_keywords(keywords):
    """Generate a directory name from keywords."""
    if not keywords:
        return ""
    
    # Use the most common keyword
    return keywords[0]

def _generate_name_from_files(files, file_data):
    """Generate a directory name from file names."""
    if not files:
        return ""
    
    # Extract common prefix
    filenames = [os.path.basename(f) for f in files]
    
    # Find common prefix
    prefix = os.path.commonprefix(filenames)
    
    # Clean up prefix
    prefix = re.sub(r'[_\-.]$', '', prefix)
    
    if len(prefix) >= 3:
        return prefix
    
    # No good prefix, use a keyword from the first file
    if files[0] in file_data and file_data[files[0]]["semantics"]["keywords"]:
        return file_data[files[0]]["semantics"]["keywords"][0]
    
    return ""
