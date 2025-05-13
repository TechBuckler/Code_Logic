"""
File Utilities for the Logic Tool

This module provides utility functions for working with files,
including copying, transforming, and loading Python modules.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import shutil
import importlib.util

def copy_file(source_path: str, target_path: str) -> bool:
    """
    Copy a file from source to target path
    
    Args:
        source_path: Path to the source file
        target_path: Path to the target file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create target directory if it doesn't exist
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Copy the file
        shutil.copy2(source_path, target_path)
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

def transform_file(source_path: str, target_path: str, 
                  transformations: Dict[str, str] = None) -> bool:
    """
    Copy a file from source to target path with text transformations
    
    Args:
        source_path: Path to the source file
        target_path: Path to the target file
        transformations: Dictionary of text replacements (old_text -> new_text)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create target directory if it doesn't exist
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Read the source file
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Apply transformations
        if transformations:
            for old_text, new_text in transformations.items():
                content = content.replace(old_text, new_text)
                
        # Write to target file
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"Error transforming file: {e}")
        return False

def load_module_from_file(file_path: str, module_name: str = None) -> Any:
    """
    Dynamically load a Python module from a file
    
    Args:
        file_path: Path to the Python file
        module_name: Name to give the module (defaults to filename without extension)
        
    Returns:
        Loaded module or None if loading fails
    """
    try:
        # Use filename as module name if not provided
        if module_name is None:
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            return None
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        return module
    except Exception as e:
        print(f"Error loading module from {file_path}: {e}")
        return None

def scan_directory_for_modules(directory: str, 
                              filter_func: Callable[[str], bool] = None) -> List[str]:
    """
    Scan a directory for Python modules
    
    Args:
        directory: Directory to scan
        filter_func: Optional function to filter files (returns True to include)
        
    Returns:
        List of paths to Python files
    """
    result = []
    
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    if filter_func is None or filter_func(file_path):
                        result.append(file_path)
    except Exception as e:
        print(f"Error scanning directory {directory}: {e}")
    
    return result
