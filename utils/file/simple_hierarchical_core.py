"""
Simple Hierarchical Core - A lightweight foundation for hierarchical modules

This module provides a simplified hierarchical module system with event-based
communication and state management. It's designed to be easy to understand and use.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import uuid
import time
import weakref
from typing import Dict, List, Any, Optional, Set, Tuple, Union, Callable

class Event:
    """Base event class for the event system"""
    def __init__(self, event_type: str, data: Any = None, source: Any = None):
        self.event_type = event_type
        self.data = data
        self.source = source
        self.id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.propagate = True  # Whether the event should propagate up the hierarchy

class EventBus:
    """Simple event bus for communication between modules"""
    def __init__(self, parent_bus=None):
        self.subscribers = {}  # event_type -> list of callbacks
        self.parent_bus = parent_bus
        self.child_buses = weakref.WeakSet()
        
        if parent_bus:
            parent_bus.child_buses.add(self)
    
    def subscribe(self, event_type: str, callback: Callable[[Event], None]):
        """Subscribe to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]):
        """Unsubscribe from an event type"""
        if event_type in self.subscribers:
            self.subscribers[event_type] = [
                cb for cb in self.subscribers[event_type] if cb != callback
            ]
    
    def publish(self, event: Union[Event, str], data: Any = None, source: Any = None, _visited_buses=None):
        """Publish an event to all subscribers"""
        # Initialize visited buses set to prevent infinite recursion
        if _visited_buses is None:
            _visited_buses = set()
        
        # If this bus has already been visited, return immediately
        bus_id = id(self)
        if bus_id in _visited_buses:
            return
        
        # Mark this bus as visited
        _visited_buses.add(bus_id)
        
        # Convert string to Event if needed
        if isinstance(event, str):
            event = Event(event, data, source)
        
        # Process local subscribers
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in event handler: {e}")
        
        # Propagate to parent if needed
        if event.propagate and self.parent_bus:
            self.parent_bus.publish(event, _visited_buses=_visited_buses)
        
        # Propagate to children
        for child_bus in list(self.child_buses):
            child_bus.publish(event, _visited_buses=_visited_buses)

class StateStore:
    """Simple state store for managing module state"""
    def __init__(self, event_bus: EventBus, parent_store=None):
        self.state = {}
        self.event_bus = event_bus
        self.parent_store = parent_store
        self.watchers = {}  # key -> list of callbacks
    
    def set(self, key: str, value: Any, source: Any = None):
        """Set a state value and notify watchers"""
        old_value = self.state.get(key)
        self.state[key] = value
        
        # Notify watchers
        if key in self.watchers:
            for callback in self.watchers[key]:
                try:
                    callback(value, old_value)
                except Exception as e:
                    print(f"Error in state watcher: {e}")
        
        # Publish state change event
        self.event_bus.publish("state_change", {
            "key": key,
            "value": value,
            "old_value": old_value
        }, source)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value, checking parent stores if not found"""
        if key in self.state:
            return self.state[key]
        elif self.parent_store:
            return self.parent_store.get(key, default)
        else:
            return default
    
    def watch(self, key: str, callback: Callable[[Any, Any], None]):
        """Watch for changes to a specific key"""
        if key not in self.watchers:
            self.watchers[key] = []
        self.watchers[key].append(callback)
    
    def unwatch(self, key: str, callback: Callable[[Any, Any], None]):
        """Stop watching a specific key"""
        if key in self.watchers:
            self.watchers[key] = [
                cb for cb in self.watchers[key] if cb != callback
            ]

class HierarchicalModule:
    """Base class for all hierarchical modules"""
    def __init__(self, module_id: str, parent=None):
        self.module_id = module_id
        self.parent = parent
        self.children = {}  # id -> module
        self.active = True
        
        # Create or inherit event bus and state store
        if parent:
            self.event_bus = EventBus(parent.event_bus)
            self.state_store = StateStore(self.event_bus, parent.state_store)
            parent.add_child(self)
        else:
            self.event_bus = EventBus()
            self.state_store = StateStore(self.event_bus)
    
    def add_child(self, module):
        """Add a child module"""
        self.children[module.module_id] = module
    
    def remove_child(self, module_id: str):
        """Remove a child module"""
        if module_id in self.children:
            del self.children[module_id]
    
    def get_child(self, module_id: str):
        """Get a child module by ID"""
        return self.children.get(module_id)
    
    def get_path(self) -> List[str]:
        """Get the path from the root to this module"""
        if self.parent:
            return self.parent.get_path() + [self.module_id]
        else:
            return [self.module_id]
    
    def get_full_id(self) -> str:
        """Get the full ID including the path"""
        return ".".join(self.get_path())
    
    def initialize(self) -> bool:
        """Initialize the module"""
        # Default implementation just initializes children
        for child in self.children.values():
            if not child.initialize():
                return False
        return True
    
    def process(self, data: Any, context: Optional[Dict[str, Any]] = None) -> Any:
        """Process data with this module"""
        # Default implementation does nothing
        return data
    
    def shutdown(self):
        """Shutdown the module and its children"""
        # Shutdown children first
        for child in list(self.children.values()):
            child.shutdown()
        
        # Then shutdown self
        self.active = False

class ModuleRegistry:
    """Registry for all modules in the system"""
    def __init__(self):
        self.root_modules = {}  # id -> module
    
    def register_module(self, module: HierarchicalModule):
        """Register a root module"""
        self.root_modules[module.module_id] = module
    
    def unregister_module(self, module_id: str):
        """Unregister a root module"""
        if module_id in self.root_modules:
            del self.root_modules[module_id]
    
    def get_module(self, module_id: str) -> Optional[HierarchicalModule]:
        """Get a module by ID (can be a full path ID)"""
        # Check if it's a direct root module
        if module_id in self.root_modules:
            return self.root_modules[module_id]
        
        # Try to find it by path
        path = module_id.split(".")
        if len(path) > 1:
            root_id = path[0]
            if root_id in self.root_modules:
                module = self.root_modules[root_id]
                for part in path[1:]:
                    module = module.get_child(part)
                    if not module:
                        return None
                return module
        
        return None
    
    def initialize_all(self):
        """Initialize all modules"""
        for module in self.root_modules.values():
            module.initialize()
    
    def shutdown_all(self):
        """Shutdown all modules"""
        for module in self.root_modules.values():
            module.shutdown()

# UI Key Management for Streamlit
class UIKeyManager:
    """Manager for UI component keys to prevent duplicates"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UIKeyManager, cls).__new__(cls)
            cls._instance.used_keys = set()
        return cls._instance
    
    def get_unique_key(self, base_key: str) -> str:
        """Get a unique key based on the base key"""
        if base_key not in self.used_keys:
            self.used_keys.add(base_key)
            return base_key
        
        counter = 1
        while f"{base_key}_{counter}" in self.used_keys:
            counter += 1
        
        unique_key = f"{base_key}_{counter}"
        self.used_keys.add(unique_key)
        return unique_key
    
    def clear_keys(self):
        """Clear all registered keys"""
        self.used_keys = set()

# Singleton instance
ui_key_manager = UIKeyManager()
