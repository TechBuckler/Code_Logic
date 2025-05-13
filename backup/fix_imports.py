#!/usr/bin/env python3
"""
Fix import issues after codebase reorganization.
This script will:
1. Create a proper import utility system
2. Update import statements in all Python files
3. Create necessary __init__.py files
4. Test that all modules can be imported
"""

import os
import sys
import importlib

# Define the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def create_directory(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    return path

def create_import_utility():
    """Create an import utility module to handle both old and new import paths."""
    # Create in the main utils directory instead of a subdirectory
    utils_dir = os.path.join(PROJECT_ROOT, "utils")
    create_directory(utils_dir)
    
    # Create import_utils.py directly in the utils directory
    utils_path = os.path.join(utils_dir, "import_utils.py")
    with open(utils_path, "w") as f:
        f.write('''"""
Utilities for handling imports during the transition to the new directory structure.
"""

import sys
import os
import importlib.util
from pathlib import Path

# Get the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Legacy paths
LEGACY_PATHS = {
    "src": os.path.join(PROJECT_ROOT, "legacy", "src"),
    "modules": os.path.join(PROJECT_ROOT, "legacy", "src", "modules"),
    "hierarchical": os.path.join(PROJECT_ROOT, "legacy", "src", "modules", "hierarchical"),
}

def add_legacy_paths_to_sys_path():
    """Add legacy paths to sys.path to enable old imports to work."""
    for path in LEGACY_PATHS.values():
        if path not in sys.path and os.path.exists(path):
            sys.path.insert(0, path)

def import_module_flexible(module_name):
    """
    Import a module using both new and old import paths.
    
    Args:
        module_name: The name of the module to import
        
    Returns:
        The imported module or None if not found
    """
    # Try direct import first
    try:
        return importlib.import_module(module_name)
    except ImportError:
        pass
    
    # Try with legacy paths
    add_legacy_paths_to_sys_path()
    try:
        return importlib.import_module(module_name)
    except ImportError:
        pass
    
    # Try to handle special cases
    if module_name.startswith("src."):
        # Try without the src prefix
        try:
            new_name = module_name[4:]  # Remove "src."
            return importlib.import_module(new_name)
        except ImportError:
            pass
    
    # Handle hierarchical modules
    if "hierarchical" in module_name:
        # Try in the modules.standard package
        try:
            new_name = module_name.replace("hierarchical", "standard")
            return importlib.import_module(new_name)
        except ImportError:
            pass
    
    return None

def patch_imports():
    """
    Patch the import system to handle both old and new import paths.
    Call this at the beginning of your main script.
    """
    add_legacy_paths_to_sys_path()
    
    # Add the project root to sys.path
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

# Automatically patch imports when this module is imported
patch_imports()
''')
    
    print(f"Created import utility at {os.path.relpath(utils_path, PROJECT_ROOT)}")
    return utils_path

def create_init_files():
    """Create __init__.py files in all directories that need them."""
    # Find all directories that should have __init__.py files
    dirs_needing_init = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip special directories
        if any(special in root for special in ["__pycache__", ".git", ".vscode", ".idea"]):
            continue
        
        # Check if this directory contains Python files
        has_py_files = any(f.endswith(".py") and f != "__init__.py" for f in files)
        
        # Check if this directory already has an __init__.py
        has_init = "__init__.py" in files
        
        # If it has Python files but no __init__.py, add it to the list
        if has_py_files and not has_init:
            dirs_needing_init.append(root)
    
    # Create __init__.py files
    for directory in dirs_needing_init:
        init_path = os.path.join(directory, "__init__.py")
        
        # Get all Python modules in this directory
        modules = []
        for file in os.listdir(directory):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                modules.append(module_name)
        
        # Create __init__.py with imports
        with open(init_path, "w") as f:
            dir_name = os.path.basename(directory)
            f.write(f'"""\n{dir_name} package.\n"""\n\n')
            
            # Import all modules
            for module in modules:
                f.write(f"from . import {module}\n")
        
        print(f"Created __init__.py in {os.path.relpath(directory, PROJECT_ROOT)}")

def fix_src_imports():
    """Fix imports that reference the old 'src' module."""
    # Find all Python files
    python_files = []
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    # Update import statements in all Python files
    for file_path in python_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Replace imports from the old src module
            modified = False
            
            # Replace "from modules.standard" with "from modules.standard"
            if "from modules.standard" in content:
                content = content.replace("from modules.standard", "from modules.standard")
                modified = True
            
            # Replace "import modules.standard" with "import modules.standard"
            if "import modules.standard" in content:
                content = content.replace("import modules.standard", "import modules.standard")
                modified = True
            
            # Replace other src imports
            if "from " in content:
                content = content.replace("from ", "from ")
                modified = True
            
            if "import " in content:
                content = content.replace("import ", "import ")
                modified = True
            
            # Add import for the import utility if needed
            if modified and "import utils.import_utils" not in content:
                # Add import at the top of the file
                import_statement = "# Fix imports for reorganized codebase\nimport utils.import_utils\n\n"
                
                # Find the right place to insert (after any docstrings and other imports)
                lines = content.split("\n")
                insert_pos = 0
                
                # Skip shebang if present
                if lines and lines[0].startswith("#!"):
                    insert_pos = 1
                
                # Skip docstring if present
                if insert_pos < len(lines) and lines[insert_pos].strip().startswith('"""'):
                    insert_pos += 1
                    while insert_pos < len(lines) and '"""' not in lines[insert_pos]:
                        insert_pos += 1
                    if insert_pos < len(lines):
                        insert_pos += 1
                
                # Insert after any existing imports
                while insert_pos < len(lines) and (
                    lines[insert_pos].strip().startswith("import ") or 
                    lines[insert_pos].strip().startswith("from ")
                ):
                    insert_pos += 1
                
                # Insert the import statement
                lines.insert(insert_pos, import_statement)
                content = "\n".join(lines)
            
            # Write the modified content back
            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Fixed imports in {os.path.relpath(file_path, PROJECT_ROOT)}")
        except Exception as e:
            print(f"Error fixing imports in {os.path.relpath(file_path, PROJECT_ROOT)}: {e}")

def create_legacy_symlinks():
    """Create symbolic links or directory structure to maintain backward compatibility."""
    # Create the legacy src directory structure if it doesn't exist
    legacy_src = os.path.join(PROJECT_ROOT, "legacy", "src")
    create_directory(legacy_src)
    
    # Create modules directory under legacy/src
    legacy_modules = os.path.join(legacy_src, "modules")
    create_directory(legacy_modules)
    
    # Create hierarchical directory under legacy/src/modules
    legacy_hierarchical = os.path.join(legacy_modules, "hierarchical")
    create_directory(legacy_hierarchical)
    
    # Create __init__.py files
    for directory in [legacy_src, legacy_modules, legacy_hierarchical]:
        init_path = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w") as f:
                f.write('"""\nLegacy compatibility package.\n"""\n')
    
    # Create a special __init__.py in hierarchical that imports from modules.standard
    with open(os.path.join(legacy_hierarchical, "__init__.py"), "w") as f:
        f.write('''"""
Legacy compatibility package for hierarchical modules.
This imports from the new modules.standard package.
"""

# Import from the new location
try:
    from modules.standard import *
except ImportError:
    pass
''')
    
    print("Created legacy directory structure for backward compatibility")

def test_imports():
    """Test that all modules can be imported."""
    print("\nTesting imports...")
    
    # Add the import utility to sys.path
    sys.path.insert(0, PROJECT_ROOT)
    
    # Import the import utility
    try:
        # First make sure utils is in the path
        utils_path = os.path.join(PROJECT_ROOT, "utils")
        if utils_path not in sys.path:
            sys.path.insert(0, utils_path)
            
        # Then try to import the module
        patch_imports()
        print("✓ Successfully imported import utility")
    except ImportError as e:
        print(f"✗ Failed to import import utility: {e}")
        return False
    
    # Test importing key modules
    test_modules = [
        "refactor_codebase",
        "refactor_splitter",
        "refactor_analyzer",
        "tools.refactoring.file_splitter",
        "tools.refactoring.smart_splitter",
        "modules.standard.ast_parser_module",
    ]
    
    successful = 0
    failed = 0
    failed_modules = []
    
    for module_name in test_modules:
        try:
            module = importlib.import_module(module_name)
            print(f"✓ Successfully imported {module_name}")
            successful += 1
            
            # Clean up
            del module
            if module_name in sys.modules:
                del sys.modules[module_name]
        except Exception as e:
            print(f"✗ Failed to import {module_name}: {e}")
            failed += 1
            failed_modules.append((module_name, str(e)))
    
    # Report results
    print(f"\nSuccessfully imported {successful}/{len(test_modules)} test modules")
    if failed > 0:
        print(f"Failed to import {failed} modules:")
        for module, error in failed_modules:
            print(f"  - {module}: {error}")
    
    return failed == 0

def main():
    """Main function to fix import issues."""
    print("Fixing import issues after codebase reorganization...")
    
    # 1. Create import utility
    create_import_utility()
    
    # 2. Create __init__.py files
    create_init_files()
    
    # 3. Fix src imports
    fix_src_imports()
    
    # 4. Create legacy symlinks
    create_legacy_symlinks()
    
    # 5. Test imports
    imports_work = test_imports()
    
    # Report overall status
    print("\nImport fixes complete!")
    print(f"Imports working: {'Yes' if imports_work else 'No'}")
    
    if not imports_work:
        print("\nSome imports still fail. You may need to manually fix specific modules.")
    else:
        print("\nAll imports working! The codebase is now properly structured.")

if __name__ == "__main__":
    main()
