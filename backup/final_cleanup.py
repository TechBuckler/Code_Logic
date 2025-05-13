#!/usr/bin/env python
"""
Final Cleanup

This script handles the final cleanup of files and folders that don't fit
the established directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import shutil

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions

# Files to move to appropriate locations
FILES_TO_MOVE = {
    "check_structure.py": "tools/structure_analyzer.py",
    "finalize_reorganization.py": "tools/reorganization/finalize_reorganization.py",
    "function_graph.png": "docs/diagrams/function_graph.png",
    "run_safe.bat": "tools/scripts/run_safe.bat"
}

# Folders to move or merge
FOLDERS_TO_HANDLE = {
    "src": "legacy",  # Move to legacy folder
    "_pycache_": None  # Can be safely deleted
}

def move_files(dry_run=True):
    """Move files to their appropriate locations."""
    print("\n📄 Moving files to appropriate locations")
    print("=" * 80)
    
    for src_file, dest_file in FILES_TO_MOVE.items():
        src_path = os.path.join(project_root, src_file)
        dest_path = os.path.join(project_root, dest_file)
        
        if os.path.exists(src_path):
            if dry_run:
                print(f"Would move: {src_file} -> {dest_file}")
            else:
                try:
                    # Create destination directory if it doesn't exist
                    ensure_dir(os.path.dirname(dest_path))
                    
                    # Copy the file
                    shutil.copy2(src_path, dest_path)
                    
                    # Remove the original
                    os.remove(src_path)
                    
                    print(f"Moved: {src_file} -> {dest_file}")
                except Exception as e:
                    print(f"Error moving {src_file}: {e}")
        else:
            print(f"File not found: {src_file}")
    
    print(f"\n{'Would move' if dry_run else 'Moved'} files to appropriate locations")

def handle_folders(dry_run=True):
    """Handle folders that need to be moved or deleted."""
    print("\n📁 Handling folders")
    print("=" * 80)
    
    # Create legacy folder if needed
    legacy_dir = os.path.join(project_root, "legacy")
    if not os.path.exists(legacy_dir) and not dry_run:
        os.makedirs(legacy_dir)
        # Create __init__.py
        with open(os.path.join(legacy_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write('"""\nLegacy code preserved for reference.\n"""\n')
    
    for folder, destination in FOLDERS_TO_HANDLE.items():
        folder_path = os.path.join(project_root, folder)
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            if destination is None:
                # Delete folder
                if dry_run:
                    print(f"Would delete: {folder}/")
                else:
                    try:
                        shutil.rmtree(folder_path)
                        print(f"Deleted: {folder}/")
                    except Exception as e:
                        print(f"Error deleting {folder}/: {e}")
            else:
                # Move folder
                dest_path = os.path.join(project_root, destination, folder)
                if dry_run:
                    print(f"Would move: {folder}/ -> {destination}/{folder}/")
                else:
                    try:
                        # Create destination directory
                        ensure_dir(os.path.dirname(dest_path))
                        
                        # Move directory
                        shutil.move(folder_path, dest_path)
                        print(f"Moved: {folder}/ -> {destination}/{folder}/")
                    except Exception as e:
                        print(f"Error moving {folder}/: {e}")
        else:
            print(f"Folder not found: {folder}/")
    
    print(f"\n{'Would handle' if dry_run else 'Handled'} folders")

def create_tools_reorganization_dir(dry_run=True):
    """Create tools/reorganization directory for reorganization scripts."""
    print("\n📁 Creating tools/reorganization directory")
    print("=" * 80)
    
    reorg_dir = os.path.join(project_root, "tools", "reorganization")
    if not os.path.exists(reorg_dir):
        if dry_run:
            print("Would create: tools/reorganization/")
        else:
            os.makedirs(reorg_dir, exist_ok=True)
            
            # Create __init__.py
            with open(os.path.join(reorg_dir, "__init__.py"), "w", encoding="utf-8") as f:
                f.write('"""\nReorganization tools package.\n"""\n')
            
            print("Created: tools/reorganization/")
    else:
        print("Directory already exists: tools/reorganization/")

def create_docs_diagrams_dir(dry_run=True):
    """Create docs/diagrams directory for documentation diagrams."""
    print("\n📁 Creating docs/diagrams directory")
    print("=" * 80)
    
    diagrams_dir = os.path.join(project_root, "docs", "diagrams")
    if not os.path.exists(diagrams_dir):
        if dry_run:
            print("Would create: docs/diagrams/")
        else:
            os.makedirs(diagrams_dir, exist_ok=True)
            
            # Create __init__.py
            with open(os.path.join(diagrams_dir, "__init__.py"), "w", encoding="utf-8") as f:
                f.write('"""\nDiagrams package.\n"""\n')
            
            print("Created: docs/diagrams/")
    else:
        print("Directory already exists: docs/diagrams/")

def create_tools_scripts_dir(dry_run=True):
    """Create tools/scripts directory for utility scripts."""
    print("\n📁 Creating tools/scripts directory")
    print("=" * 80)
    
    scripts_dir = os.path.join(project_root, "tools", "scripts")
    if not os.path.exists(scripts_dir):
        if dry_run:
            print("Would create: tools/scripts/")
        else:
            os.makedirs(scripts_dir, exist_ok=True)
            
            # Create __init__.py
            with open(os.path.join(scripts_dir, "__init__.py"), "w", encoding="utf-8") as f:
                f.write('"""\nUtility scripts package.\n"""\n')
            
            print("Created: tools/scripts/")
    else:
        print("Directory already exists: tools/scripts/")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Final Cleanup")
    parser.add_argument("--apply", action="store_true", help="Apply the changes")
    
    args = parser.parse_args()
    dry_run = not args.apply
    
    print("\n🧹 Final Cleanup")
    print("=" * 80)
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}")
    
    # Create necessary directories
    create_tools_reorganization_dir(dry_run)
    create_docs_diagrams_dir(dry_run)
    create_tools_scripts_dir(dry_run)
    
    # Move files
    move_files(dry_run)
    
    # Handle folders
    handle_folders(dry_run)
    
    print("\n✅ Final cleanup complete!")
    if dry_run:
        print("\nTo apply the changes, run: py final_cleanup.py --apply")

if __name__ == "__main__":
    main()
