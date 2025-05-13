"""
State manager module.
This provides a simple state management system with event bus and shared state.
"""
from typing import Dict, List, Any, Optional, Callable
# Fix imports for reorganized codebase
import utils.import_utils



class Event:
    """Event class for the event bus."""
    def __init__(self, event_type: str, data: Any = None, source: Any = None):
        self.event_type = event_type
        self.data = data
        self.source = source
        self.propagate = True

class EventBus:
    """Event bus for publishing and subscribing to events."""
    def __init__(self):
        self.listeners = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to an event type."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def publish(self, event: Event):
        """Publish an event to all subscribers."""
        if event.event_type in self.listeners:
            for callback in self.listeners[event.event_type]:
                callback(event)

class SharedState:
    """Shared state for components."""
    def __init__(self):
        self.state = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the state."""
        return self.state.get(key, default)
    
    def set(self, key: str, value: Any) -> Any:
        """Set a value in the state."""
        self.state[key] = value
        return value

class StateManager:
    """State manager with event bus and shared state."""
    def __init__(self):
        self._event_bus = EventBus()
        self._shared_state = SharedState()
    
    def get_event_bus(self) -> EventBus:
        """Get the event bus."""
        return self._event_bus
    
    def get_shared_state(self) -> SharedState:
        """Get the shared state."""
        return self._shared_state
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the shared state."""
        return self._shared_state.get(key, default)
    
    def set(self, key: str, value: Any) -> Any:
        """Set a value in the shared state."""
        return self._shared_state.set(key, value)

# Create a singleton instance
state_manager = StateManager()
