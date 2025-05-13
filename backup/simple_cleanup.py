#!/usr/bin/env python
"""
Simple Cleanup Script

This script:
1. Creates any missing __init__.py files
2. Removes original files that were copied to new locations

Very simple, direct approach to finalize the reorganization.
"""

import os
import sys
import shutil

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def print_section(title):
    """Print a section title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def create_init_files():
    """Create any missing __init__.py files."""
    print_section("CREATING __INIT__.PY FILES")
    
    # Ensure all required directories have __init__.py files
    directories = [
        'core',
        'modules',
        'modules/standard',
        'tools',
        'tools/refactoring',
        'tools/analysis',
        'utils',
        'utils/import',
        'utils/file',
        'tests'
    ]
    
    for directory in directories:
        dir_path = os.path.join(PROJECT_ROOT, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {directory}")
        
        init_path = os.path.join(dir_path, '__init__.py')
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                f.write(f'"""{os.path.basename(directory)} package.\n\nThis package contains modules related to {os.path.basename(directory)}.\n"""\n')
            print(f"Created __init__.py in {directory}")
    
    print("\nAll required directories have __init__.py files")
    return True

def remove_original_files():
    """Remove original files that were copied to new locations."""
    print_section("REMOVING ORIGINAL FILES")
    
    # Get list of files that were moved
    moved_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip the root directory
        if root == PROJECT_ROOT:
            continue
        
        for file in files:
            if file.endswith('.py'):
                # Check if the file also exists in the root directory
                if os.path.exists(os.path.join(PROJECT_ROOT, file)):
                    moved_files.append(file)
    
    # Show files that will be removed
    print(f"Found {len(moved_files)} files that were moved to subdirectories:")
    for file in moved_files:
        print(f"  - {file}")
    
    # Remove the files
    removed_count = 0
    for file in moved_files:
        try:
            # Don't remove certain critical files
            if file in ['__init__.py', 'fix_imports_simple.py', 'universal_import_fixer.py']:
                print(f"Skipping critical file: {file}")
                continue
                
            os.remove(os.path.join(PROJECT_ROOT, file))
            print(f"Removed {file}")
            removed_count += 1
        except Exception as e:
            print(f"Error removing {file}: {e}")
    
    print(f"\nRemoved {removed_count}/{len(moved_files)} original files")
    return removed_count

def main():
    """Main function to orchestrate the cleanup process."""
    print_section("STARTING SIMPLE CLEANUP")
    
    # Step 1: Create __init__.py files
    init_files_created = create_init_files()
    
    # Step 2: Remove original files
    files_removed = remove_original_files()
    
    print_section("CLEANUP COMPLETE")
    print(f"__init__.py files created: {'✓' if init_files_created else '✗'}")
    print(f"Original files removed: {files_removed}")
    
    print("\nNext steps:")
    print("1. Run test_all_imports.py to verify imports still work")
    print("2. Run fix_imports.py if any import issues persist")

if __name__ == "__main__":
    main()
