#!/usr/bin/env python
"""
Split Standard Modules

This script splits the modules/standard directory into more specific categories
to maintain a balanced directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions

# Define module categories
MODULE_CATEGORIES = {
    "processing": [
        "ast_parser_module.py",
        "ir_generator_module.py",
        "proof_engine_module.py",
        "optimizer_module.py"
    ],
    "analysis": [
        "module_explorer_module.py",
        "optimization_testbed_module.py"
    ],
    "export": [
        "exporter_module.py",
        "graph_builder_module.py"
    ],
    "organization": [
        "project_organizer_module.py",
        "shadow_tree_module.py"
    ]
}

def split_standard_modules(dry_run=True):
    """Split the standard modules directory into categories."""
    print("\n🔄 Splitting Standard Modules")
    print("=" * 80)
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}")
    
    # Get the standard modules directory
    standard_dir = join_paths(project_root, "modules", "standard")
    if not os.path.exists(standard_dir):
        print(f"Error: Standard modules directory not found: {standard_dir}")
        return
    
    # Create category directories
    for category in MODULE_CATEGORIES:
        category_dir = join_paths(standard_dir, category)
        if not dry_run:
            ensure_dir(category_dir)
            # Create __init__.py
            init_path = join_paths(category_dir, "__init__.py")
            if not os.path.exists(init_path):
                with open(init_path, "w") as f:
                    f.write(f'"""\n{category} modules package.\n"""\n')
        print(f"Created directory: modules/standard/{category}/")
    
    # Move files to their categories
    for category, files in MODULE_CATEGORIES.items():
        for file in files:
            src_path = join_paths(standard_dir, file)
            if not os.path.exists(src_path):
                print(f"Warning: File not found: {src_path}")
                continue
                
            dest_path = join_paths(standard_dir, category, file)
            
            # Update imports in the file
            content = read_file(src_path)
            
            # Update relative imports
            updated_content = content.replace(
                "from modules.standard.",
                f"from modules.standard.{category}."
            )
            
            if dry_run:
                print(f"Would move: {file} -> modules/standard/{category}/{file}")
            else:
                # Write updated content
                write_file(dest_path, updated_content)
                
                # Remove original file
                os.remove(src_path)
                
                print(f"Moved: {file} -> modules/standard/{category}/{file}")
    
    # Update imports in other files
    if not dry_run:
        print("\nUpdating imports in other files...")
        update_imports_in_directory(project_root)
    
    print("\n✅ Standard modules splitting complete!")

def update_imports_in_directory(directory):
    """Update imports in all Python files in a directory (recursive)."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = join_paths(root, file)
                
                # Skip files in the standard modules directory (already updated)
                if "modules/standard/" in file_path.replace("\\", "/"):
                    continue
                
                # Read the file
                content = read_file(file_path)
                updated = False
                
                # Update imports for each category
                for category, module_files in MODULE_CATEGORIES.items():
                    for module_file in module_files:
                        module_name = module_file.replace(".py", "")
                        
                        # Update absolute imports
                        old_import = f"from modules.standard.{module_name}"
                        new_import = f"from modules.standard.{category}.{module_name}"
                        
                        if old_import in content:
                            content = content.replace(old_import, new_import)
                            updated = True
                
                # Write updated content if changed
                if updated:
                    write_file(file_path, content)
                    print(f"Updated imports in: {os.path.relpath(file_path, project_root)}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Split Standard Modules")
    parser.add_argument("--apply", action="store_true", help="Apply the changes")
    
    args = parser.parse_args()
    
    split_standard_modules(dry_run=not args.apply)
    
    if not args.apply:
        print("\nTo apply the changes, run: py split_standard_modules.py --apply")

if __name__ == "__main__":
    main()
