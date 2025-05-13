#!/usr/bin/env python
"""
List Directory Structure

This script displays the directory structure in a tree-like format.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os

def print_directory_tree(root_dir, prefix="", is_last=True, max_depth=3, current_depth=0, exclude_dirs=None):
    """Print a directory tree structure."""
    if exclude_dirs is None:
        exclude_dirs = ["__pycache__", ".git", ".idea", ".vscode"]
    
    if current_depth > max_depth:
        return
    
    # Get the basename of the directory
    basename = os.path.basename(root_dir)
    
    # Skip excluded directories
    if basename in exclude_dirs:
        return
    
    # Print the current directory
    if current_depth == 0:
        print(f"📁 {basename}/")
    else:
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}📁 {basename}/")
    
    # Prepare the prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")
    
    # Get all items in the directory
    try:
        items = sorted(os.listdir(root_dir))
        
        # Count directories and files
        dirs = [item for item in items if os.path.isdir(os.path.join(root_dir, item)) and item not in exclude_dirs]
        files = [item for item in items if os.path.isfile(os.path.join(root_dir, item))]
        
        # Print directories first
        for i, item in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and len(files) == 0
            print_directory_tree(
                os.path.join(root_dir, item),
                child_prefix,
                is_last_dir,
                max_depth,
                current_depth + 1,
                exclude_dirs
            )
        
        # Then print files
        for i, item in enumerate(files):
            is_last_file = i == len(files) - 1
            connector = "└── " if is_last_file else "├── "
            
            # Determine file icon based on extension
            if item.endswith((".py", ".pyw")):
                icon = "🐍"  # Python file
            elif item.endswith((".md", ".txt", ".rst")):
                icon = "📄"  # Documentation
            elif item.endswith((".json", ".yaml", ".yml", ".toml")):
                icon = "⚙️"  # Configuration
            elif item.endswith((".html", ".css", ".js")):
                icon = "🌐"  # Web file
            elif item.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")):
                icon = "🖼️"  # Image
            elif item.endswith((".bat", ".sh", ".cmd")):
                icon = "⚡"  # Script
            else:
                icon = "📄"  # Generic file
            
            print(f"{child_prefix}{connector}{icon} {item}")
    
    except PermissionError:
        print(f"{child_prefix}└── ⚠️ Permission denied")
    except Exception as e:
        print(f"{child_prefix}└── ⚠️ Error: {str(e)}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="List Directory Structure")
    parser.add_argument("--depth", type=int, default=3, help="Maximum depth to display")
    parser.add_argument("--dir", type=str, default=".", help="Directory to list")
    
    args = parser.parse_args()
    
    # Get the absolute path of the directory
    root_dir = os.path.abspath(args.dir)
    
    print("\n📊 Directory Structure")
    print("=" * 80)
    
    # Print the directory tree
    print_directory_tree(root_dir, max_depth=args.depth)
    
    print("\n✅ Directory listing complete!")

if __name__ == "__main__":
    main()
