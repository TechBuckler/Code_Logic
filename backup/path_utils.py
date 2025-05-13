"""Path utility functions for common path operations.

This module provides standardized functions for path manipulation and
directory handling, reducing code duplication across the codebase.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

def get_project_root():
    """Get the absolute path to the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ensure_dir(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)
    return directory

def get_relative_path(path, base=None):
    """Get a path relative to the base directory."""
    if base is None:
        base = get_project_root()
    return os.path.relpath(path, base)

def normalize_path(path):
    """Normalize a path to use consistent separators and resolve relative components."""
    return os.path.normpath(path)

def join_paths(*paths):
    """Join paths using the correct separator for the current OS."""
    return os.path.join(*paths)

def get_parent_dir(path):
    """Get the parent directory of a path."""
    return os.path.dirname(path)

def get_file_name(path):
    """Get the file name from a path."""
    return os.path.basename(path)

def get_file_extension(path):
    """Get the file extension from a path."""
    return os.path.splitext(path)[1]

def get_file_stem(path):
    """Get the file name without extension."""
    return os.path.splitext(os.path.basename(path))[0]

def is_subpath(path, parent):
    """Check if path is a subpath of parent."""
    path = os.path.abspath(path)
    parent = os.path.abspath(parent)
    return path.startswith(parent)

def add_to_python_path(path):
    """Add a path to the Python path if it's not already there."""
    path = os.path.abspath(path)
    if path not in sys.path:
        sys.path.append(path)
    return path
