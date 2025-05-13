"""
Compatibility module for hierarchical_module.
This file redirects imports to the new location in modules/standard/hierarchical_module.py
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import from the new location
try:
    from modules.standard.hierarchical_module import *
except ImportError as e:
    print(f"Error importing hierarchical_module from new location: {e}")
    # Define minimal versions of required classes to prevent errors
    class HierarchicalModule:
        """Minimal implementation of HierarchicalModule for compatibility."""
        def __init__(self, *args, **kwargs):
            pass
    
    class ModuleHierarchy:
        """Minimal implementation of ModuleHierarchy for compatibility."""
        def __init__(self, *args, **kwargs):
            pass
