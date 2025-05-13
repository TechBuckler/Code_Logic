#!/usr/bin/env python3
"""
Cleanup script to remove redundant documentation files from the Logic Tool project.
These files have been consolidated into plan_1.md and README.md.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os

# Files to be removed
files_to_remove = [
    "integration_plan.md",
    "quick_implementation_plan.md",
    "unified_system_design.md",
    "implementation_steps.md"
]

def main():
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Print information about what will be deleted
    print("The following files will be deleted:")
    for file in files_to_remove:
        file_path = os.path.join(script_dir, file)
        if os.path.exists(file_path):
            print(f"  - {file}")
    
    # Delete the files
    for file in files_to_remove:
        file_path = os.path.join(script_dir, file)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file}")
            else:
                print(f"File not found: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")
    
    print("\nCleanup completed successfully.")

if __name__ == "__main__":
    main()
