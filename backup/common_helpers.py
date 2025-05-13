
"""Common Helper Functions

This module contains common utility functions extracted from repeated patterns
in the codebase.
"""

import os
import sys
import json
import re

def ensure_dir(directory):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def read_file(file_path, encoding='utf-8'):
    """Read a file and return its contents."""
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()

def write_file(file_path, content, encoding='utf-8'):
    """Write content to a file."""
    ensure_dir(os.path.dirname(file_path))
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)
    return file_path

def find_files(directory, pattern='*', recursive=True):
    """Find files matching a pattern in a directory."""
    import glob
    if recursive:
        return glob.glob(os.path.join(directory, '**', pattern), recursive=True)
    return glob.glob(os.path.join(directory, pattern))

def parse_json(json_string):
    """Parse a JSON string into a Python object."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def to_json(obj, indent=2):
    """Convert a Python object to a JSON string."""
    return json.dumps(obj, indent=indent)
