"""
Core UI Components

This module provides core UI components for the application.
It is the new location for functionality previously in core.ui_components.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import from the compatibility module to ensure backward compatibility
try:
except ImportError:
    # Define the classes here if the compatibility module is not available
    class UIManager:
        """Simple UI manager for the application."""
        
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

# Additional UI components specific to the new structure
class Panel(UIComponent):
    """A panel component that can contain other components."""
    
    def __init__(self, name, title=""):
        """Initialize the panel."""
        super().__init__(name)
        self.title = title
        self.collapsed = False
    
    def toggle(self):
        """Toggle the collapsed state."""
        self.collapsed = not self.collapsed
        return self.collapsed

class Button(UIComponent):
    """A button component."""
    
    def __init__(self, name, label="", on_click=None):
        """Initialize the button."""
        super().__init__(name)
        self.label = label
        self.on_click = on_click
    
    def click(self):
        """Simulate a click on the button."""
        if callable(self.on_click):
            return self.on_click()
        return None

class TextField(UIComponent):
    """A text field component."""
    
    def __init__(self, name, value="", placeholder=""):
        """Initialize the text field."""
        super().__init__(name)
        self.value = value
        self.placeholder = placeholder
    
    def set_value(self, value):
        """Set the value of the text field."""
        self.value = value
        return self.value

# Export symbols
__all__ = [
    'ui_manager', 'UIManager', 'UIComponent',
    'Panel', 'Button', 'TextField'
]
