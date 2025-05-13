"""
UI Components Module

This compatibility module provides UI component functionality for the codebase.
It serves as a bridge during the transition to the new directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# UI Manager class
class UIManager:
    """Simple UI manager for compatibility."""
    
    def __init__(self):
        """Initialize the UI manager."""
        self.components = {}
        self.active_component = None
    
    def register_component(self, name, component):
        """Register a UI component."""
        self.components[name] = component
        return component
    
    def get_component(self, name):
        """Get a registered UI component."""
        return self.components.get(name)
    
    def set_active(self, name):
        """Set the active component."""
        if name in self.components:
            self.active_component = name
            return True
        return False
    
    def get_active(self):
        """Get the active component."""
        if self.active_component:
            return self.components.get(self.active_component)
        return None

# Create a singleton instance
ui_manager = UIManager()

# Component base class
class UIComponent:
    """Base class for UI components."""
    
    def __init__(self, name):
        """Initialize the component."""
        self.name = name
        self.visible = True
        self.parent = None
        self.children = []
    
    def render(self):
        """Render the component."""
        pass
    
    def add_child(self, child):
        """Add a child component."""
        self.children.append(child)
        child.parent = self
        return child
    
    def remove_child(self, child):
        """Remove a child component."""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            return True
        return False
    
    def show(self):
        """Show the component."""
        self.visible = True
    
    def hide(self):
        """Hide the component."""
        self.visible = False

# Export symbols
__all__ = ['ui_manager', 'UIManager', 'UIComponent']
