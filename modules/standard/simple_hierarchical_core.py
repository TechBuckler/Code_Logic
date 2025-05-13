"""
Simple Hierarchical Core - Compatibility Module

This module redirects imports to the actual implementation in core/simple_hierarchical_core.py.
It serves as a bridge during the transition to the new directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
from typing import Dict, List, Any, Optional, Set, Tuple, Union

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import from the actual implementation
try:
    from core.simple_hierarchical_core import *
except ImportError as e:
    print(f"Error importing from core.simple_hierarchical_core: {e}")
    
    # Define minimal functionality to prevent import errors
    class HierarchicalModule:
        """Basic hierarchical module."""
        def __init__(self, name):
            self.name = name
            self.children = []
            self.parent = None
            
        def add_child(self, child):
            self.children.append(child)
            child.parent = self
            
        def remove_child(self, child):
            if child in self.children:
                self.children.remove(child)
                child.parent = None
    
    class Event:
        """Event class for the event system."""
        def __init__(self, event_type: str, data: Any = None, source: Any = None):
            self.event_type = event_type
            self.data = data
            self.source = source
            self.propagate = True
    
    class EventBus:
        """Event bus for dispatching events."""
        def __init__(self):
            self.listeners = {}
            
        def subscribe(self, event_type, callback):
            if event_type not in self.listeners:
                self.listeners[event_type] = []
            self.listeners[event_type].append(callback)
            
        def publish(self, event):
            if event.event_type in self.listeners:
                for callback in self.listeners[event.event_type]:
                    callback(event)
    
    class StateStore:
        """Store for application state."""
        def __init__(self):
            self.state = {}
            
        def set(self, key, value):
            self.state[key] = value
            
        def get(self, key, default=None):
            return self.state.get(key, default)
    
    class ModuleRegistry:
        """Registry for modules."""
        def __init__(self):
            self.modules = {}
            
        def register(self, module):
            self.modules[module.name] = module
            
        def get(self, name):
            return self.modules.get(name)
    
    # Create default instances
    ui_key_manager = StateStore()
