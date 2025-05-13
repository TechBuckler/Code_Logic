"""
Improved Module Explorer Script

This script provides a cleaner view of all modules in the project.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def explore_modules():
    """Explore all modules in the project and print their details."""
    print("\n===== MODULE EXPLORER =====\n")
    
    # List all Python files in src and src/modules
    src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
    modules_dir = os.path.join(src_dir, 'modules')
    
    # Core components
    core_files = []
    for file in os.listdir(src_dir):
        if file.endswith('.py') and not file.startswith('__'):
            core_files.append(os.path.join(src_dir, file))
    
    # Module components
    module_files = []
    if os.path.exists(modules_dir):
        for file in os.listdir(modules_dir):
            if file.endswith('.py') and not file.startswith('__'):
                module_files.append(os.path.join(modules_dir, file))
    
    # Print core components
    print(f"== CORE COMPONENTS ({len(core_files)}) ==\n")
    for file_path in sorted(core_files):
        file_name = os.path.basename(file_path)
        module_name = file_name[:-3]  # Remove .py extension
        
        # Get the first docstring if available
        description = "No description available"
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                if '"""' in content:
                    docstring = content.split('"""')[1].strip()
                    description = docstring.split('\n')[0]
        except Exception:
            pass
        
        print(f"- {module_name}")
        print(f"  Path: {file_path}")
        print(f"  Description: {description}")
        print()
    
    # Print module components
    print(f"== MODULE COMPONENTS ({len(module_files)}) ==\n")
    for file_path in sorted(module_files):
        file_name = os.path.basename(file_path)
        module_name = file_name[:-3]  # Remove .py extension
        
        # Get the first docstring if available
        description = "No description available"
        dependencies = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                if '"""' in content:
                    docstring = content.split('"""')[1].strip()
                    description = docstring.split('\n')[0]
                
                # Try to find dependencies
                if "self.dependencies = [" in content:
                    deps_line = content.split("self.dependencies = [")[1].split("]")[0]
                    deps = deps_line.replace('"', '').replace("'", "").split(",")
                    dependencies = [dep.strip() for dep in deps if dep.strip()]
        except Exception:
            pass
        
        print(f"- {module_name}")
        print(f"  Path: {file_path}")
        print(f"  Description: {description}")
        if dependencies:
            print(f"  Dependencies: {', '.join(dependencies)}")
        print()
    
    print("===========================\n")

if __name__ == "__main__":
    explore_modules()
