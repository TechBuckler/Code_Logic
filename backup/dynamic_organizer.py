#!/usr/bin/env python
"""
Dynamic Directory Organizer

This script analyzes the codebase and automatically determines the optimal
directory structure based on file relationships, dependencies, and complexity.
It uses AST analysis and clustering to create a self-balancing directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import json

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions

# Import analyzer modules

# Constants
MIN_FILES_PER_DIR = 5
MAX_FILES_PER_DIR = 20
MAX_DEPTH = 4
BALANCE_FACTOR = 0.7  # Weight between depth and breadth (0-1)

class DynamicOrganizer:
    """Dynamic directory organizer that uses code analysis to determine optimal structure."""
    
    def __init__(self, root_dir):
        """Initialize with the root directory to organize."""
        self.root_dir = Path(root_dir)
        self.files = []
        self.file_data = {}
        self.dependencies = defaultdict(set)
        self.clusters = []
        self.structure = {}
        
    def scan_files(self, extensions=None, exclude_dirs=None):
        """Scan the directory for files to analyze."""
        if extensions is None:
            extensions = ['.py']
        if exclude_dirs is None:
            exclude_dirs = ['__pycache__', '.git', 'venv', 'env', 'node_modules']
            
        print(f"Scanning directory: {self.root_dir}")
        
        for root, dirs, files in os.walk(self.root_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.root_dir)
                    self.files.append(rel_path)
                    
        print(f"Found {len(self.files)} files to analyze")
        return self.files
    
    def analyze_codebase(self):
        """Analyze the codebase to extract dependencies and complexity metrics."""
        print("Analyzing codebase...")
        
        for i, file_path in enumerate(self.files):
            if i % 10 == 0:
                print(f"Analyzing file {i+1}/{len(self.files)}")
                
            full_path = os.path.join(self.root_dir, file_path)
            
            try:
                # Analyze the file
                analysis = analyze_file(full_path)
                self.file_data[file_path] = analysis
                
                # Extract dependencies
                deps = extract_dependencies(full_path)
                self.dependencies[file_path] = deps
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        
        print("Codebase analysis complete")
        return self.file_data
    
    def cluster_files(self):
        """Cluster files based on dependencies and similarity."""
        print("Clustering files...")
        
        # Calculate similarity matrix
        similarity_matrix = {}
        for i, file1 in enumerate(self.files):
            for j, file2 in enumerate(self.files[i+1:], i+1):
                sim = calculate_similarity(
                    self.file_data[file1],
                    self.file_data[file2],
                    self.dependencies[file1],
                    self.dependencies[file2]
                )
                similarity_matrix[(file1, file2)] = sim
        
        # Cluster files
        self.clusters = cluster_files(self.files, similarity_matrix)
        
        print(f"Created {len(self.clusters)} clusters")
        return self.clusters
    
    def optimize_structure(self):
        """Optimize the directory structure based on clusters."""
        print("Optimizing directory structure...")
        
        # Create initial structure from clusters
        self.structure = optimize_structure(
            self.clusters,
            self.file_data,
            min_files=MIN_FILES_PER_DIR,
            max_files=MAX_FILES_PER_DIR,
            max_depth=MAX_DEPTH,
            balance_factor=BALANCE_FACTOR
        )
        
        print("Directory structure optimization complete")
        return self.structure
    
    def generate_plan(self, output_file=None):
        """Generate a reorganization plan."""
        print("Generating reorganization plan...")
        
        plan = {
            "structure": self.structure,
            "moves": []
        }
        
        # Generate file moves
        for file_path in self.files:
            new_path = self._get_new_path(file_path)
            if new_path != file_path:
                plan["moves"].append({
                    "source": file_path,
                    "destination": new_path
                })
        
        # Save plan if output file specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(plan, f, indent=2)
            print(f"Reorganization plan saved to {output_file}")
        
        print(f"Generated plan with {len(plan['moves'])} file moves")
        return plan
    
    def apply_plan(self, plan=None, dry_run=True):
        """Apply the reorganization plan."""
        if plan is None:
            plan = self.generate_plan()
            
        print(f"{'Simulating' if dry_run else 'Applying'} reorganization plan...")
        
        for move in plan["moves"]:
            source = os.path.join(self.root_dir, move["source"])
            destination = os.path.join(self.root_dir, move["destination"])
            
            # Create destination directory
            dest_dir = os.path.dirname(destination)
            
            if dry_run:
                print(f"Would move: {move['source']} -> {move['destination']}")
            else:
                ensure_dir(dest_dir)
                
                # Read source file
                content = read_file(source)
                
                # Write to destination
                write_file(destination, content)
                
                print(f"Moved: {move['source']} -> {move['destination']}")
        
        print(f"{'Simulation' if dry_run else 'Application'} complete")
    
    def _get_new_path(self, file_path):
        """Get the new path for a file based on the optimized structure."""
        # Find the directory for this file
        for dir_path, dir_info in self._flatten_structure(self.structure).items():
            if file_path in dir_info["files"]:
                # Keep the filename, change the directory
                filename = os.path.basename(file_path)
                return os.path.join(dir_path, filename)
        
        # If not found in structure, keep original path
        return file_path
    
    def _flatten_structure(self, structure, prefix=""):
        """Flatten the nested structure into a dictionary of paths."""
        result = {}
        
        for name, info in structure.items():
            path = os.path.join(prefix, name)
            
            if "files" in info:
                result[path] = {
                    "files": info["files"],
                    "description": info.get("description", "")
                }
            
            if "subdirs" in info:
                result.update(self._flatten_structure(info["subdirs"], path))
        
        return result

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dynamic Directory Organizer")
    parser.add_argument("--root", type=str, default=project_root, help="Root directory to analyze")
    parser.add_argument("--output", type=str, help="Output file for reorganization plan")
    parser.add_argument("--apply", action="store_true", help="Apply the reorganization plan")
    parser.add_argument("--extensions", type=str, default=".py", help="File extensions to analyze (comma-separated)")
    
    args = parser.parse_args()
    
    # Parse extensions
    extensions = [ext.strip() for ext in args.extensions.split(",")]
    
    # Create organizer
    organizer = DynamicOrganizer(args.root)
    
    # Run the analysis and optimization
    organizer.scan_files(extensions=extensions)
    organizer.analyze_codebase()
    organizer.cluster_files()
    organizer.optimize_structure()
    
    # Generate and optionally apply the plan
    plan = organizer.generate_plan(args.output)
    
    if args.apply:
        organizer.apply_plan(plan, dry_run=False)
    else:
        organizer.apply_plan(plan, dry_run=True)
        print("\nTo apply the plan, run with --apply")

if __name__ == "__main__":
    main()
