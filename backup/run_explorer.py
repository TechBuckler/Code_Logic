"""
Module Explorer Script

This script runs the module explorer to list all modules in the project.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the module explorer
from modules.standard.analysis.module_explorer_module import ModuleExplorerModule

def main():
    # Create the module explorer
    explorer = ModuleExplorerModule()
    
    # List all modules
    modules = explorer.list_modules()
    
    # Print the results in a readable format
    print("\n===== MODULE EXPLORER =====\n")
    
    if "modules" in modules:
        print(f"Found {len(modules['modules'])} modules:\n")
        
        # Group modules by type
        module_types = {}
        for module in modules["modules"]:
            module_type = module.get("type", "unknown")
            if module_type not in module_types:
                module_types[module_type] = []
            module_types[module_type].append(module)
        
        # Print modules by type
        for module_type, type_modules in module_types.items():
            print(f"\n== {module_type.upper()} MODULES ==")
            for module in type_modules:
                print(f"\n- {module.get('name', 'Unknown')}")
                print(f"  Path: {module.get('path', 'Unknown')}")
                if "description" in module:
                    print(f"  Description: {module.get('description', 'No description')}")
                if "dependencies" in module and module["dependencies"]:
                    print(f"  Dependencies: {', '.join(module['dependencies'])}")
    else:
        print("No modules found or error occurred.")
    
    print("\n===========================\n")

if __name__ == "__main__":
    main()
