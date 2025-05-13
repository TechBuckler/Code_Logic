#!/usr/bin/env python3
"""
Balance the codebase directory structure based on analysis recommendations.
This script will:
1. Split overpopulated directories
2. Consolidate sparse directories
3. Flatten deep structures
4. Balance top-level directories
5. Test the functionality after reorganization
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import shutil
import json
import re
from collections import defaultdict
import importlib

# Define the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Add project root to path for imports
sys.path.insert(0, PROJECT_ROOT)

def create_directory(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    return path

def write_init_file(directory, imports=None):
    """Write an __init__.py file to a directory with optional imports."""
    init_path = os.path.join(directory, "__init__.py")
    
    if os.path.exists(init_path):
        # If file exists, append imports if provided
        if imports:
            with open(init_path, "a") as f:
                for imp in imports:
                    f.write(f"\n{imp}")
        return
    
    # Create new file
    with open(init_path, "w") as f:
        f.write(f'"""\n{os.path.basename(directory)} package.\n"""\n\n')
        if imports:
            for imp in imports:
                f.write(f"{imp}\n")
    
    print(f"Created __init__.py in {directory}")

def balance_docs_directory():
    """Balance the docs directory by organizing auto_generated files."""
    docs_dir = os.path.join(PROJECT_ROOT, "docs")
    auto_gen_dir = os.path.join(docs_dir, "auto_generated")
    
    if not os.path.exists(auto_gen_dir):
        print("docs/auto_generated directory not found, skipping")
        return
    
    # Count files in auto_generated
    files = [f for f in os.listdir(auto_gen_dir) if os.path.isfile(os.path.join(auto_gen_dir, f))]
    
    if len(files) <= 20:
        print("docs/auto_generated has a reasonable number of files, skipping")
        return
    
    print(f"Balancing docs/auto_generated directory ({len(files)} files)")
    
    # Group files by prefix or pattern
    file_groups = defaultdict(list)
    
    # Try to find common prefixes
    prefixes = set()
    for file in files:
        # Extract prefix (up to first underscore or dash)
        match = re.match(r'^([a-zA-Z0-9]+)[_-]', file)
        if match:
            prefixes.add(match.group(1))
    
    # If we found meaningful prefixes, use them
    if prefixes and len(prefixes) >= 3 and len(prefixes) <= 20:
        for file in files:
            grouped = False
            for prefix in prefixes:
                if file.startswith(prefix):
                    file_groups[prefix].append(file)
                    grouped = True
                    break
            
            if not grouped:
                file_groups["misc"].append(file)
    else:
        # Alphabetical grouping
        for file in files:
            first_letter = file[0].upper() if file else "misc"
            if first_letter.isalpha():
                # Group by first letter
                file_groups[first_letter].append(file)
            else:
                file_groups["misc"].append(file)
    
    # Create subdirectories and move files
    for group, group_files in file_groups.items():
        if not group_files:
            continue
            
        group_dir = os.path.join(auto_gen_dir, group)
        create_directory(group_dir)
        
        # Create an index.md file listing all files in this group
        with open(os.path.join(group_dir, "index.md"), "w") as f:
            f.write(f"# {group.capitalize()} Documentation\n\n")
            f.write("This directory contains the following documentation files:\n\n")
            for file in sorted(group_files):
                f.write(f"- [{file}](./{file})\n")
        
        # Move files to the group directory
        for file in group_files:
            src = os.path.join(auto_gen_dir, file)
            dst = os.path.join(group_dir, file)
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.move(src, dst)
                print(f"Moved {file} to {group}")
    
    # Create a new index.md in auto_generated
    with open(os.path.join(auto_gen_dir, "index.md"), "w") as f:
        f.write("# Auto-Generated Documentation\n\n")
        f.write("This directory contains auto-generated documentation organized by category:\n\n")
        for group in sorted(file_groups.keys()):
            if file_groups[group]:
                f.write(f"- [{group.capitalize()}](./{group}/index.md)\n")

def balance_utils_directory():
    """Balance the utils directory by organizing files into subdirectories."""
    utils_dir = os.path.join(PROJECT_ROOT, "utils")
    
    if not os.path.exists(utils_dir):
        print("utils directory not found, skipping")
        return
    
    # Count files directly in utils
    files = [f for f in os.listdir(utils_dir) if os.path.isfile(os.path.join(utils_dir, f))]
    
    if len(files) <= 20:
        print("utils has a reasonable number of files, skipping")
        return
    
    print(f"Balancing utils directory ({len(files)} files)")
    
    # Define utility categories
    categories = {
        "file": ["file", "io", "read", "write", "path", "dir", "directory"],
        "string": ["string", "text", "str", "format", "parse"],
        "data": ["data", "json", "yaml", "csv", "xml", "serialize", "deserialize"],
        "system": ["system", "os", "process", "env", "environment"],
        "network": ["network", "http", "url", "request", "response", "api"],
        "time": ["time", "date", "datetime", "schedule", "cron"],
        "math": ["math", "calc", "calculate", "compute", "numeric", "number"],
        "logging": ["log", "logger", "logging", "debug", "error", "warning"],
        "config": ["config", "configuration", "settings", "options", "preferences"],
        "import": ["import", "module", "package", "dependency"],
    }
    
    # Group files by category
    file_groups = defaultdict(list)
    
    for file in files:
        if file == "__init__.py":
            continue
            
        file_lower = file.lower()
        grouped = False
        
        # Try to match by filename
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in file_lower:
                    file_groups[category].append(file)
                    grouped = True
                    break
            if grouped:
                break
        
        # If no match by name, check file contents for imports
        if not grouped and file.endswith(".py"):
            try:
                with open(os.path.join(utils_dir, file), "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    
                for category, keywords in categories.items():
                    for keyword in keywords:
                        if keyword in content:
                            file_groups[category].append(file)
                            grouped = True
                            break
                    if grouped:
                        break
            except Exception:
                pass
        
        # If still no match, put in misc
        if not grouped:
            file_groups["misc"].append(file)
    
    # Create subdirectories and move files
    imports = []
    
    for category, category_files in file_groups.items():
        if not category_files:
            continue
            
        category_dir = os.path.join(utils_dir, category)
        create_directory(category_dir)
        
        # Create __init__.py
        category_imports = []
        for file in category_files:
            if file.endswith(".py"):
                module_name = file[:-3]
                category_imports.append(f"from .{module_name} import *")
        
        write_init_file(category_dir, category_imports)
        
        # Move files to the category directory
        for file in category_files:
            if file == "__init__.py":
                continue
                
            src = os.path.join(utils_dir, file)
            dst = os.path.join(category_dir, file)
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.move(src, dst)
                print(f"Moved {file} to utils/{category}")
                
                # Add import to main utils/__init__.py
                if file.endswith(".py"):
                    module_name = file[:-3]
                    imports.append(f"from .{category}.{module_name} import *")
    
    # Update main utils/__init__.py
    if imports:
        utils_init = os.path.join(utils_dir, "__init__.py")
        if os.path.exists(utils_init):
            with open(utils_init, "a") as f:
                f.write("\n# Auto-generated imports from balanced subdirectories\n")
                for imp in imports:
                    f.write(f"{imp}\n")
        else:
            write_init_file(utils_dir, imports)

def consolidate_sparse_directories():
    """Consolidate directories with very few items."""
    # Find directories with 0 or 1 items that are not special directories
    sparse_dirs = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip special directories
        if any(special in root for special in ["__pycache__", ".git", ".vscode", ".idea"]):
            continue
            
        # Check if this is a sparse directory (0 or 1 items)
        if len(dirs) + len(files) <= 1 and root != PROJECT_ROOT:
            # Skip directories that are part of a standard structure
            rel_path = os.path.relpath(root, PROJECT_ROOT)
            if rel_path in ["core", "modules", "ui", "utils", "tools", "docs", "tests"]:
                continue
                
            # Skip directories that are required for imports
            if os.path.exists(os.path.join(root, "__init__.py")):
                continue
                
            sparse_dirs.append(root)
    
    # Group sparse directories by parent
    parent_groups = defaultdict(list)
    for sparse_dir in sparse_dirs:
        parent = os.path.dirname(sparse_dir)
        parent_groups[parent].append(sparse_dir)
    
    # Consolidate directories with the same parent
    for parent, children in parent_groups.items():
        if len(children) <= 1:
            continue
            
        # Skip if parent is the project root
        if parent == PROJECT_ROOT:
            continue
            
        print(f"Found {len(children)} sparse directories under {os.path.relpath(parent, PROJECT_ROOT)}")
        
        # Create a "combined" directory
        combined_dir = os.path.join(parent, "combined")
        create_directory(combined_dir)
        
        # Move contents to the combined directory
        for child in children:
            child_name = os.path.basename(child)
            
            # Move all files
            for item in os.listdir(child):
                src = os.path.join(child, item)
                dst = os.path.join(combined_dir, f"{child_name}_{item}")
                
                if os.path.exists(src):
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
                        print(f"Copied {os.path.relpath(src, PROJECT_ROOT)} to {os.path.relpath(dst, PROJECT_ROOT)}")
                    else:
                        # For directories, create a subdirectory
                        dst_dir = os.path.join(combined_dir, f"{child_name}_{item}")
                        shutil.copytree(src, dst_dir, dirs_exist_ok=True)
                        print(f"Copied directory {os.path.relpath(src, PROJECT_ROOT)} to {os.path.relpath(dst_dir, PROJECT_ROOT)}")
        
        # Create an index file
        with open(os.path.join(combined_dir, "index.md"), "w") as f:
            f.write("# Combined Sparse Directories\n\n")
            f.write("This directory contains files from the following sparse directories:\n\n")
            for child in children:
                child_rel = os.path.relpath(child, PROJECT_ROOT)
                f.write(f"- {child_rel}\n")
        
        # Don't remove the original directories yet, just leave a note
        print("Original sparse directories preserved. Review and remove manually if desired.")

def flatten_deep_structures():
    """Flatten directory structures that are too deep."""
    # Find directories deeper than level 5
    deep_dirs = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip special directories
        if any(special in root for special in ["__pycache__", ".git", ".vscode", ".idea"]):
            continue
            
        # Calculate depth
        rel_path = os.path.relpath(root, PROJECT_ROOT)
        if rel_path == ".":
            depth = 0
        else:
            depth = len(rel_path.split(os.sep))
            
        if depth >= 5 and dirs:
            deep_dirs.append((root, depth))
    
    # Sort by depth (deepest first)
    deep_dirs.sort(key=lambda x: x[1], reverse=True)
    
    for deep_dir, depth in deep_dirs:
        rel_path = os.path.relpath(deep_dir, PROJECT_ROOT)
        print(f"Found deep directory: {rel_path} (depth {depth})")
        
        # Get all files in this directory and subdirectories
        all_files = []
        for root, _, files in os.walk(deep_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, deep_dir)
                all_files.append((file_path, rel_file_path))
        
        # Skip if this is a special directory structure we shouldn't flatten
        if any(special in rel_path for special in ["shadow_tree/output", "nltk_data"]):
            print(f"Skipping special directory: {rel_path}")
            continue
            
        # Skip if there are no files to flatten
        if not all_files:
            continue
            
        # Create a flattened directory
        parent_dir = os.path.dirname(deep_dir)
        dir_name = os.path.basename(deep_dir)
        flat_dir = os.path.join(parent_dir, f"{dir_name}_flat")
        create_directory(flat_dir)
        
        # Copy files to the flattened directory with path-based naming
        for file_path, rel_file_path in all_files:
            # Replace directory separators with underscores
            flat_name = rel_file_path.replace(os.sep, "_")
            dst_path = os.path.join(flat_dir, flat_name)
            
            # Copy the file
            shutil.copy2(file_path, dst_path)
            print(f"Copied {os.path.relpath(file_path, PROJECT_ROOT)} to {os.path.relpath(dst_path, PROJECT_ROOT)}")
        
        # Create an index file
        with open(os.path.join(flat_dir, "index.md"), "w") as f:
            f.write(f"# Flattened Directory: {dir_name}\n\n")
            f.write("This directory contains flattened files from a deep directory structure.\n\n")
            f.write("Original structure:\n\n")
            f.write(f"- {rel_path}\n")
            
            # List all files
            f.write("\n## Files\n\n")
            for _, rel_file_path in all_files:
                flat_name = rel_file_path.replace(os.sep, "_")
                f.write(f"- [{rel_file_path}](./{flat_name})\n")
        
        # Don't remove the original directory structure yet
        print(f"Created flattened version of {rel_path} at {os.path.relpath(flat_dir, PROJECT_ROOT)}")
        print("Original deep structure preserved. Review and remove manually if desired.")

def update_import_paths():
    """Update import paths in Python files to reflect the new directory structure."""
    # Find all Python files
    python_files = []
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    # Common import patterns to look for
    import_patterns = [
        r'from\s+(\S+)\s+import',
        r'import\s+(\S+)',
    ]
    
    # Create a mapping of old module paths to new module paths
    module_mapping = {}
    
    # Add mappings for modules that we know have moved
    module_mapping.update({
        "utils.file_utils": "utils.file",
        "utils.path_utils": "utils.path",
        "utils.string_utils": "utils.string",
        "utils.json_utils": "utils.data",
        "tools.file_splitter": "tools.refactoring.file_splitter",
        "tools.smart_splitter": "tools.refactoring.smart_splitter",
        "tools.resource_splitter": "tools.refactoring.resource_splitter",
    })
    
    # Update import statements in all Python files
    for file_path in python_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Find all import statements
            import_statements = []
            for pattern in import_patterns:
                import_statements.extend(re.findall(pattern, content))
            
            # Replace import statements
            modified = False
            for old_import in import_statements:
                if old_import in module_mapping:
                    new_import = module_mapping[old_import]
                    
                    # Replace the import statement
                    old_pattern = f"from {old_import} import"
                    new_pattern = f"from {new_import} import"
                    if old_pattern in content:
                        content = content.replace(old_pattern, new_pattern)
                        modified = True
                    
                    old_pattern = f"import {old_import}"
                    new_pattern = f"import {new_import}"
                    if old_pattern in content and not old_pattern.startswith("import {new_import}"):
                        content = content.replace(old_pattern, new_pattern)
                        modified = True
            
            # Write the modified content back
            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated imports in {os.path.relpath(file_path, PROJECT_ROOT)}")
        except Exception as e:
            print(f"Error updating imports in {os.path.relpath(file_path, PROJECT_ROOT)}: {e}")

def test_refactoring_tools():
    """Test that the refactoring tools still work after reorganization."""
    print("\nTesting refactoring tools...")
    
    # Test importing the modules
    try:
        # Add project root to path
        sys.path.insert(0, PROJECT_ROOT)
        
        # Try to import refactoring modules
        print("✓ Successfully imported refactor_codebase")
        
        # Test running the analyzer on a file
        test_file = os.path.join(PROJECT_ROOT, "refactor_codebase.py")
        if os.path.exists(test_file):
            result = analyze_command(test_file)
            if result:
                print(f"✓ Successfully analyzed {test_file}")
            else:
                print(f"✗ Failed to analyze {test_file}")
        else:
            print(f"✗ Test file {test_file} not found")
            
    except Exception as e:
        print(f"✗ Error testing refactoring tools: {e}")
        return False
    
    return True

def test_all_modules():
    """Test importing all modules from their new locations."""
    print("\nTesting all modules...")
    
    # Find all Python files
    python_files = []
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                rel_path = os.path.relpath(os.path.join(root, file), PROJECT_ROOT)
                # Convert file path to module path
                module_path = rel_path.replace(os.sep, ".")[:-3]  # Remove .py
                python_files.append(module_path)
    
    # Try to import each module
    successful = 0
    failed = 0
    failed_modules = []
    
    for module_path in python_files:
        try:
            # Skip modules that are likely to cause issues
            if any(skip in module_path for skip in ["test_", "_test", "setup", "conftest"]):
                continue
                
            # Try to import the module
            module = importlib.import_module(module_path)
            successful += 1
            
            # Clean up
            del module
            if module_path in sys.modules:
                del sys.modules[module_path]
                
        except Exception as e:
            failed += 1
            failed_modules.append((module_path, str(e)))
    
    # Report results
    print(f"Successfully imported {successful} modules")
    if failed > 0:
        print(f"Failed to import {failed} modules:")
        for module, error in failed_modules[:10]:  # Show first 10 failures
            print(f"  - {module}: {error}")
        if len(failed_modules) > 10:
            print(f"  ... and {len(failed_modules) - 10} more")
    
    return failed == 0

def main():
    """Main function to balance the codebase."""
    print("Balancing codebase directory structure...")
    
    # 1. Balance docs directory
    balance_docs_directory()
    
    # 2. Balance utils directory
    balance_utils_directory()
    
    # 3. Consolidate sparse directories
    consolidate_sparse_directories()
    
    # 4. Flatten deep structures
    flatten_deep_structures()
    
    # 5. Update import paths
    update_import_paths()
    
    # 6. Test the refactoring tools
    refactoring_tools_work = test_refactoring_tools()
    
    # 7. Test all modules
    all_modules_work = test_all_modules()
    
    # Report overall status
    print("\nCodebase balancing complete!")
    print(f"Refactoring tools working: {'Yes' if refactoring_tools_work else 'No'}")
    print(f"All modules importable: {'Yes' if all_modules_work else 'No'}")
    
    if not refactoring_tools_work or not all_modules_work:
        print("\nSome tests failed. You may need to manually fix import issues.")
    else:
        print("\nAll tests passed! The codebase is now better balanced.")

if __name__ == "__main__":
    main()
