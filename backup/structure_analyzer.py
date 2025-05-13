#!/usr/bin/env python
"""
Check Directory Structure

This script checks the current directory structure and reports on the files
in each top-level directory.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os

def count_files(directory):
    """Count the number of files in a directory (recursive)."""
    count = 0
    for root, _, files in os.walk(directory):
        count += len(files)
    return count

def print_directory_structure(base_dir, max_depth=3, indent=0):
    """Print the directory structure up to a maximum depth."""
    if indent > max_depth:
        return
        
    # Get all items in the directory
    try:
        items = os.listdir(base_dir)
    except Exception as e:
        print(f"{' ' * indent}Error listing directory {base_dir}: {e}")
        return
        
    # Sort items: directories first, then files
    dirs = [item for item in items if os.path.isdir(os.path.join(base_dir, item))]
    files = [item for item in items if os.path.isfile(os.path.join(base_dir, item))]
    
    # Sort alphabetically
    dirs.sort()
    files.sort()
    
    # Print directories
    for dir_name in dirs:
        # Skip __pycache__ directories
        if dir_name == "__pycache__":
            continue
            
        dir_path = os.path.join(base_dir, dir_name)
        file_count = count_files(dir_path)
        print(f"{' ' * indent}📁 {dir_name}/ ({file_count} files)")
        print_directory_structure(dir_path, max_depth, indent + 2)
    
    # Print files (only at the deepest level or if there are no subdirectories)
    if indent == max_depth or not dirs:
        for file_name in files:
            if file_name.endswith(".py") or file_name == "__init__.py":
                print(f"{' ' * indent}📄 {file_name}")

def main():
    """Main function."""
    print("\n📊 Current Directory Structure")
    print("=" * 80)
    
    # Get the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Define the top-level directories to check
    top_dirs = ["core", "modules", "ui", "utils", "tools", "docs", "tests"]
    
    # Print the structure of each top-level directory
    for dir_name in top_dirs:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            file_count = count_files(dir_path)
            print(f"\n📁 {dir_name}/ ({file_count} files)")
            print_directory_structure(dir_path, max_depth=3, indent=2)
        else:
            print(f"\n❌ {dir_name}/ (directory not found)")
    
    print("\n✅ Directory structure check complete!")

if __name__ == "__main__":
    main()
