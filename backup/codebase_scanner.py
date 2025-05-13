"""
Codebase Scanner

This script scans the entire codebase and provides a comprehensive report
of the directory structure, file types, and code organization.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import json
import time

class CodebaseScanner:
    """Utility for scanning and analyzing a codebase"""
    
    def __init__(self, root_dir: str):
        """Initialize with the root directory of the codebase"""
        self.root_dir = os.path.abspath(root_dir)
        self.file_count = 0
        self.dir_count = 0
        self.file_types = {}
        self.file_sizes = {}
        self.structure = {}
        
    def scan(self, max_depth: int = None, exclude_dirs: List[str] = None) -> Dict[str, Any]:
        """
        Scan the codebase and return its structure
        
        Args:
            max_depth: Maximum depth to scan (None for unlimited)
            exclude_dirs: Directories to exclude (e.g., "__pycache__")
            
        Returns:
            Dictionary containing the codebase structure
        """
        if exclude_dirs is None:
            exclude_dirs = ["__pycache__", ".git", "pdict-cache"]
            
        start_time = time.time()
        
        # Reset counters
        self.file_count = 0
        self.dir_count = 1  # Count the root directory
        self.file_types = {}
        self.file_sizes = {}
        
        # Build the structure
        self.structure = self._scan_directory(self.root_dir, 0, max_depth, exclude_dirs)
        
        # Add scan statistics
        self.structure["stats"] = {
            "file_count": self.file_count,
            "dir_count": self.dir_count,
            "file_types": self.file_types,
            "scan_duration": time.time() - start_time
        }
        
        return self.structure
    
    def _scan_directory(self, dir_path: str, current_depth: int, 
                       max_depth: Optional[int], exclude_dirs: List[str]) -> Dict[str, Any]:
        """
        Recursively scan a directory
        
        Args:
            dir_path: Path to the directory
            current_depth: Current depth in the directory tree
            max_depth: Maximum depth to scan
            exclude_dirs: Directories to exclude
            
        Returns:
            Dictionary containing the directory structure
        """
        # Check if we've reached the maximum depth
        if max_depth is not None and current_depth > max_depth:
            return {
                "name": os.path.basename(dir_path),
                "type": "directory",
                "path": dir_path,
                "truncated": True
            }
        
        # Create the directory structure
        dir_structure = {
            "name": os.path.basename(dir_path),
            "type": "directory",
            "path": dir_path,
            "children": []
        }
        
        try:
            # List all items in the directory
            items = os.listdir(dir_path)
            
            # Process each item
            for item_name in sorted(items):
                item_path = os.path.join(dir_path, item_name)
                
                # Skip excluded directories
                if os.path.isdir(item_path) and item_name in exclude_dirs:
                    continue
                
                if os.path.isdir(item_path):
                    # Process subdirectory
                    self.dir_count += 1
                    subdir_structure = self._scan_directory(
                        item_path, current_depth + 1, max_depth, exclude_dirs
                    )
                    dir_structure["children"].append(subdir_structure)
                else:
                    # Process file
                    self.file_count += 1
                    file_size = os.path.getsize(item_path)
                    file_ext = os.path.splitext(item_name)[1].lower()
                    
                    # Update file type statistics
                    if file_ext in self.file_types:
                        self.file_types[file_ext]["count"] += 1
                        self.file_types[file_ext]["size"] += file_size
                    else:
                        self.file_types[file_ext] = {
                            "count": 1,
                            "size": file_size
                        }
                    
                    # Add file to structure
                    file_structure = {
                        "name": item_name,
                        "type": "file",
                        "path": item_path,
                        "size": file_size,
                        "extension": file_ext
                    }
                    dir_structure["children"].append(file_structure)
        
        except Exception as e:
            print(f"Error scanning {dir_path}: {e}")
        
        return dir_structure
    
    def print_structure(self, structure: Optional[Dict[str, Any]] = None, 
                       indent: int = 0, max_depth: Optional[int] = None) -> None:
        """
        Print the codebase structure in a tree-like format
        
        Args:
            structure: Structure to print (defaults to self.structure)
            indent: Current indentation level
            max_depth: Maximum depth to print
        """
        if structure is None:
            structure = self.structure
            
        # Check if we've reached the maximum depth
        if max_depth is not None and indent > max_depth:
            return
        
        # Print the current item
        prefix = "│   " * (indent - 1) + "├── " if indent > 0 else ""
        
        if structure["type"] == "directory":
            print(f"{prefix}{structure['name']}/")
            
            # Print children
            if "children" in structure:
                for i, child in enumerate(structure["children"]):
                    is_last = i == len(structure["children"]) - 1
                    
                    # Modify the prefix for the last item
                    if is_last and indent > 0:
                        new_prefix = "    " * (indent - 1) + "└── "
                        print(f"{new_prefix}{child['name']}{'' if child['type'] == 'file' else '/'}")
                    else:
                        self.print_structure(child, indent + 1, max_depth)
        else:
            print(f"{prefix}{structure['name']}")
    
    def print_summary(self) -> None:
        """Print a summary of the codebase"""
        if not self.structure or "stats" not in self.structure:
            print("No scan data available. Run scan() first.")
            return
        
        stats = self.structure["stats"]
        
        print("\n=== Codebase Summary ===")
        print(f"Root Directory: {self.root_dir}")
        print(f"Total Files: {stats['file_count']}")
        print(f"Total Directories: {stats['dir_count']}")
        print(f"Scan Duration: {stats['scan_duration']:.2f} seconds")
        
        print("\n=== File Types ===")
        for ext, ext_stats in sorted(stats["file_types"].items(), 
                                    key=lambda x: x[1]["count"], reverse=True):
            ext_name = ext if ext else "(no extension)"
            print(f"{ext_name}: {ext_stats['count']} files, {self._format_size(ext_stats['size'])}")
    
    def _format_size(self, size_bytes: int) -> str:
        """Format a size in bytes to a human-readable string"""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    
    def export_to_json(self, output_path: str) -> None:
        """Export the codebase structure to a JSON file"""
        with open(output_path, "w") as f:
            json.dump(self.structure, f, indent=2)
    
    def find_files_by_extension(self, extension: str) -> List[str]:
        """Find all files with a specific extension"""
        results = []
        
        def search_in_structure(structure):
            if structure["type"] == "file" and structure["extension"] == extension:
                results.append(structure["path"])
            elif structure["type"] == "directory" and "children" in structure:
                for child in structure["children"]:
                    search_in_structure(child)
        
        search_in_structure(self.structure)
        return results
    
    def analyze_code_organization(self) -> Dict[str, Any]:
        """Analyze the organization of the codebase"""
        # Find Python modules and packages
        python_files = self.find_files_by_extension(".py")
        
        # Count files in each directory
        dir_counts = {}
        
        for file_path in python_files:
            dir_path = os.path.dirname(file_path)
            rel_dir = os.path.relpath(dir_path, self.root_dir)
            
            if rel_dir in dir_counts:
                dir_counts[rel_dir] += 1
            else:
                dir_counts[rel_dir] = 1
        
        # Find potential packages (directories with __init__.py)
        packages = set()
        
        for file_path in python_files:
            if os.path.basename(file_path) == "__init__.py":
                dir_path = os.path.dirname(file_path)
                rel_dir = os.path.relpath(dir_path, self.root_dir)
                packages.add(rel_dir)
        
        return {
            "python_file_count": len(python_files),
            "directory_file_counts": dir_counts,
            "packages": list(packages)
        }

def main():
    """Main entry point for the script"""
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the scanner
    scanner = CodebaseScanner(script_dir)
    
    # Scan the codebase
    scanner.scan()
    
    # Print the structure
    print("=== Codebase Structure ===")
    scanner.print_structure(max_depth=2)
    
    # Print a summary
    scanner.print_summary()
    
    # Analyze code organization
    organization = scanner.analyze_code_organization()
    
    print("\n=== Code Organization ===")
    print(f"Python Files: {organization['python_file_count']}")
    
    print("\nPackages:")
    for package in sorted(organization["packages"]):
        print(f"- {package}")
    
    print("\nDirectory File Counts:")
    for dir_path, count in sorted(organization["directory_file_counts"].items(), 
                                 key=lambda x: x[1], reverse=True)[:10]:
        print(f"- {dir_path}: {count} files")
    
    # Export to JSON
    scanner.export_to_json("codebase_structure.json")
    print("\nExported structure to codebase_structure.json")

if __name__ == "__main__":
    main()
