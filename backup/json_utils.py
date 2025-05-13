"""JSON utility functions for common JSON operations.

This module provides standardized functions for JSON parsing, serialization,
and manipulation, reducing code duplication across the codebase.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import json
import os

def load_json(file_path):
    """Load JSON from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data, indent=2):
    """Save data to a JSON file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)
    return True

def parse_json(json_string):
    """Parse a JSON string."""
    return json.loads(json_string)

def to_json(data, indent=2):
    """Convert data to a JSON string."""
    return json.dumps(data, indent=indent)

def merge_json(base, override):
    """Merge two JSON objects, with override taking precedence."""
    result = base.copy()
    
    for key, value in override.items():
        # If both are dictionaries, merge them recursively
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_json(result[key], value)
        else:
            result[key] = value
    
    return result

def json_to_file_if_changed(file_path, data, indent=2):
    """Save JSON to a file only if the content has changed."""
    # Convert data to JSON string
    json_str = json.dumps(data, indent=indent)
    
    # Check if file exists and content matches
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_content = f.read()
                if existing_content == json_str:
                    return False  # No changes, file not written
        except Exception:
            pass  # If there's an error reading, proceed with writing
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    # Write the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_str)
    
    return True  # File was written
