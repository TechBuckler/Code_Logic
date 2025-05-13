"""
Path utility functions.
"""
import os
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



def ensure_dir(directory):
    """Ensure a directory exists."""
    os.makedirs(directory, exist_ok=True)
    return directory

def get_python_files(directory):
    """Get all Python files in a directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def get_project_root():
    """Get the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def normalize_path(path):
    """Normalize a path to use forward slashes."""
    return str(Path(path)).replace('\\', '/')

def is_python_file(file_path):
    """Check if a file is a Python file."""
    return file_path.endswith('.py')

def get_relative_path(path, base_path=None):
    """Get the relative path from base_path."""
    if base_path is None:
        base_path = get_project_root()
    return os.path.relpath(path, base_path)
