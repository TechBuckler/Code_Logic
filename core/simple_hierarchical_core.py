#!/usr/bin/env python
"""
Compatibility module for simple_hierarchical_core.py.
This file redirects imports to the new location.
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
    from utils.file.simple_hierarchical_core import *
except ImportError as e:
    try:
        from modules.standard.simple_hierarchical_core import *
    except ImportError as e2:
        print(f"Error importing simple_hierarchical_core: {e2}")
        print("Make sure the module exists in utils/file/ or modules/standard/")
        
        # Define minimal versions of critical classes
        class HierarchicalModule:
            def __init__(self, name, parent=None):
                self.name = name
                self.parent = parent
                
        class Event:
            def __init__(self, event_type, data=None):
                self.event_type = event_type
                self.data = data or {}
                
        class EventBus:
            def __init__(self):
                self.subscribers = {}
                
            def subscribe(self, event_type, callback):
                if event_type not in self.subscribers:
                    self.subscribers[event_type] = []
                self.subscribers[event_type].append(callback)
                
        class StateStore:
            def __init__(self):
                self.state = {}
                
            def get(self, key, default=None):
                return self.state.get(key, default)
                
            def set(self, key, value):
                self.state[key] = value
                
        class ModuleRegistry:
            def __init__(self):
                self.modules = {}
                
            def register(self, module):
                self.modules[module.name] = module
                
        def ui_key_manager(prefix):
            return lambda key: f"{prefix}_{key}"
