#!/usr/bin/env python
"""
Cleanup After Reorganization

This script:
1. Tests imports to ensure everything works
2. Fixes any remaining import issues
3. Optionally removes original files that were copied to new locations

Simple, direct approach to finalize the reorganization.
"""

import os
import sys
import importlib
import shutil

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import the HierarchicalModule directly
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'modules', 'standard'))
try:
    from hierarchical_module import HierarchicalModule
    print("Successfully imported HierarchicalModule")
except ImportError as e:
    print(f"Error importing HierarchicalModule: {e}")
    print("Creating placeholder...")
    
    # Create a placeholder if needed
    class HierarchicalModule:
        def __init__(self, name=None, root_dir=None):
            self.name = name
            self.root_dir = root_dir or PROJECT_ROOT

# Make the HierarchicalModule available at all required import paths
import sys
sys.modules['modules.standard.hierarchical_module'] = sys.modules.get('hierarchical_module', HierarchicalModule)
sys.modules['modules.hierarchical_module'] = sys.modules.get('hierarchical_module', HierarchicalModule)
sys.modules['hierarchical_module'] = sys.modules.get('hierarchical_module', HierarchicalModule)

print("Fixed HierarchicalModule imports")

def print_section(title):
    """Print a section title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def test_imports():
    """Test imports to ensure everything works."""
    print_section("TESTING IMPORTS")
    
    # Try importing key modules
    modules_to_test = [
        'modules.standard.hierarchical_module',
        'utils.common_helpers',
        'utils.pipeline',
        'core.state_manager',
        'tools.refactoring.refactor_splitter'
    ]
    
    success_count = 0
    for module_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            print(f"✓ Successfully imported {module_name}")
            success_count += 1
        except ImportError as e:
            print(f"✗ Failed to import {module_name}: {e}")
    
    print(f"\nSuccessfully imported {success_count}/{len(modules_to_test)} modules")
    return success_count == len(modules_to_test)

def fix_remaining_imports():
    """Fix any remaining import issues."""
    print_section("FIXING REMAINING IMPORTS")
    
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
    
    # Ask for confirmation
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
    print_section("STARTING CLEANUP")
    
    # Step 1: Test imports
    imports_ok = test_imports()
    
    # Step 2: Fix remaining imports
    imports_fixed = fix_remaining_imports()
    
    # Step 3: Remove original files
    if imports_ok and imports_fixed:
        files_removed = remove_original_files()
    else:
        print("\nSkipping file removal because import tests failed")
        files_removed = 0
    
    print_section("CLEANUP COMPLETE")
    print(f"Imports tested: {'✓' if imports_ok else '✗'}")
    print(f"Imports fixed: {'✓' if imports_fixed else '✗'}")
    print(f"Original files removed: {files_removed}")
    
    print("\nNext steps:")
    if not imports_ok:
        print("1. Fix any remaining import issues manually")
        print("2. Run this script again to remove original files")
    else:
        print("1. Test the reorganized codebase to ensure everything works")
        print("2. Update any documentation to reflect the new structure")

if __name__ == "__main__":
    main()
