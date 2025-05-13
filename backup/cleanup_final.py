"""
Final cleanup script to remove unnecessary files and combine duplicates.
"""
import os
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



# Files to delete
files_to_delete = [
    # Example files
    "src/original_decision.py",
    "src/notification_logic.py",
    
    # Keep safe_runner.py and remove safe_run.py
    "safe_run.py"
]

# Count of files deleted
deleted_count = 0

# Delete the files
for file_path in files_to_delete:
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(full_path):
        try:
            os.remove(full_path)
            print(f"Deleted: {file_path}")
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    else:
        print(f"File not found: {file_path}")

print(f"\nCleanup complete. Deleted {deleted_count} files.")
