"""
Hierarchical Module Fix

This module provides a fixed version of the HierarchicalModule class that works
with the new directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
from typing import Dict, List, Any, Optional, Set, Tuple, Union, Callable

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import Module from module_system
try:
    from module_system import Module
except ImportError:
    # Define a minimal Module class if not available
    class Module:
        def __init__(self, name):
            self.name = name
            self.dependencies = []
            self.active = False

# Create a minimal state manager if needed
try:
    from core.state_manager import StateManager
    state_manager = StateManager()
except ImportError:
    # Create a minimal state manager
    class EventBus:
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
    
    class SharedState:
        def __init__(self):
            self.state = {}
        def set(self, key, value):
            self.state[key] = value
        def get(self, key, default=None):
            return self.state.get(key, default)
    
    class StateManager:
        def __init__(self):
            self._event_bus = EventBus()
            self._shared_state = SharedState()
        def get_event_bus(self):
            return self._event_bus
        def get_shared_state(self):
            return self._shared_state
    
    state_manager = StateManager()

class HierarchicalModule(Module):
    """
    Hierarchical module that extends the base Module class with parent-child relationships
    """
    def __init__(self, name, parent=None):
        super().__init__(name)
        self.parent = parent
        self.children = {}  # name -> module
        self.event_bus = state_manager.get_event_bus()
        self.shared_state = state_manager.get_shared_state()
        
        # Register with parent if provided
        if parent:
            parent.add_child(self)
    
    def add_child(self, module):
        """Add a child module"""
        self.children[module.name] = module
        return self
    
    def remove_child(self, name):
        """Remove a child module by name"""
        if name in self.children:
            del self.children[name]
        return self
    
    def get_child(self, name):
        """Get a child module by name"""
        return self.children.get(name)
    
    def get_path(self):
        """Get the path from the root to this module"""
        if self.parent:
            return self.parent.get_path() + [self.name]
        return [self.name]
    
    def get_root(self):
        """Get the root module"""
        if self.parent:
            return self.parent.get_root()
        return self
    
    def find_module(self, path):
        """Find a module by path"""
        if not path:
            return self
        
        head, *tail = path
        child = self.get_child(head)
        if not child:
            return None
        
        if not tail:
            return child
        
        return child.find_module(tail)

# Add to sys.modules to make it available for import
import types
hierarchical_module = types.ModuleType('modules.standard.hierarchical_module')
hierarchical_module.HierarchicalModule = HierarchicalModule
sys.modules['modules.standard.hierarchical_module'] = hierarchical_module

# Also make it available from core for backward compatibility
sys.modules['core.hierarchical_module'] = hierarchical_module
