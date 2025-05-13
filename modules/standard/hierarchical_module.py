"""
Hierarchical Module System - Extends the base module system with hierarchical capabilities

This module provides a hierarchical extension to the base module system,
allowing modules to be organized in a tree structure with parent-child relationships.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
from typing import Dict, List, Any, Optional, Set, Tuple, Union, Callable

# Make sure src is in the path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.dirname(src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the Module class from module_system
try:
    from module_system import Module
except ImportError:
    # Define a minimal Module class if not available
    class Module:
        def __init__(self, name):
            self.name = name
            self.dependencies = []
            self.active = False

# Create lazy loading for state_manager to avoid circular dependencies
class LazyStateManager:
    """Lazy loader for state_manager to break circular dependencies."""
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get or create the state_manager instance."""
        if cls._instance is None:
            try:
                # Import only when needed
                import core.state_manager
                cls._instance = core.state_manager.state_manager
            except ImportError:
                # Create a minimal state manager if import fails
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
                
                cls._instance = StateManager()
        return cls._instance

# Lazy state manager accessor
def get_state_manager():
    """Get the state manager instance lazily."""
    return LazyStateManager.get_instance()

class HierarchicalModule(Module):
    """
    Hierarchical module that extends the base Module class with parent-child relationships
    """
    def __init__(self, name, parent=None):
        super().__init__(name)
        self.parent = parent
        self.children = {}  # name -> module
        
        # Use lazy loading for state_manager to avoid circular dependencies
        state_mgr = get_state_manager()
        self.event_bus = state_mgr.get_event_bus()
        self.shared_state = state_mgr.get_shared_state()
        
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
    
    def get_full_name(self):
        """Get the full name including the path"""
        return ".".join(self.get_path())
    
    def get_all_children(self, recursive=True):
        """Get all children, optionally including descendants"""
        result = list(self.children.values())
        if recursive:
            for child in self.children.values():
                result.extend(child.get_all_children(recursive=True))
        return result
    
    def find_module(self, path):
        """Find a module by path (e.g., 'parent.child.grandchild')"""
        if not path:
            return None
            
        parts = path.split('.')
        if parts[0] != self.name:
            return None
            
        current = self
        for part in parts[1:]:
            current = current.get_child(part)
            if not current:
                return None
                
        return current
    
    def initialize(self):
        """Initialize this module and all its children"""
        result = super().initialize()
        if not result:
            return False
            
        # Initialize all children
        for child in self.children.values():
            if not child.initialize():
                return False
                
        return True
    
    def shutdown(self):
        """Shutdown this module and all its children"""
        # Shutdown all children first
        for child in self.children.values():
            child.shutdown()
            
        # Then shutdown self
        super().shutdown()
    
    def can_process(self, data):
        """Check if this module can process the given data"""
        return super().can_process(data)
    
    def process(self, data, context=None):
        """Process data with this module"""
        # Default implementation just passes through
        return data
    
    def render_ui(self):
        """Render the UI for this module"""
        # Default implementation does nothing
        pass

class ModuleHierarchy:
    """
    Manager for a hierarchy of modules
    """
    def __init__(self, root_module=None):
        self.root_modules = {}
        if root_module:
            self.add_root_module(root_module)
    
    def add_root_module(self, module):
        """Add a root module to the hierarchy"""
        self.root_modules[module.name] = module
        return self
    
    def remove_root_module(self, name):
        """Remove a root module from the hierarchy"""
        if name in self.root_modules:
            del self.root_modules[name]
        return self
    
    def get_root_module(self, name):
        """Get a root module by name"""
        return self.root_modules.get(name)
    
    def get_all_modules(self):
        """Get all modules in the hierarchy"""
        result = list(self.root_modules.values())
        for root in self.root_modules.values():
            result.extend(root.get_all_children())
        return result
    
    def find_module(self, path):
        """Find a module by path (e.g., 'root.child.grandchild')"""
        if not path:
            return None
            
        parts = path.split('.')
        root_name = parts[0]
        
        if root_name not in self.root_modules:
            return None
            
        return self.root_modules[root_name].find_module(path)
    
    def initialize_all(self):
        """Initialize all modules in the hierarchy"""
        for module in self.root_modules.values():
            if not module.initialize():
                return False
        return True
    
    def shutdown_all(self):
        """Shutdown all modules in the hierarchy"""
        for module in self.root_modules.values():
            module.shutdown()
