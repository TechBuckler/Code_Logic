"""
file package.
"""
import os
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



# Define essential file utility functions directly to avoid circular imports
def read_file(file_path):
    """Read a file and return its contents."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path, content):
    """Write content to a file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def ensure_directory(directory):
    """Ensure a directory exists."""
    os.makedirs(directory, exist_ok=True)
    
def get_python_files(directory):
    """Get all Python files in a directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Import the modules after defining the essential functions
# This avoids circular imports
# These imports are commented out to prevent circular imports
# They will be imported when needed by the specific modules
#
# DO NOT UNCOMMENT THESE IMPORTS - they cause circular dependencies
# from .file_utils import *
# from .path_utils import *
# from .ai_suggester import *
# from .ast_explorer import *
# ... and so on