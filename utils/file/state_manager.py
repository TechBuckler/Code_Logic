"""
State Manager - Core component for managing shared state and event communication
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import json

class EventBus:
    """
    Central event bus for communication between modules
    """
    def __init__(self):
        self.subscribers = {}
        
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = set()
        self.subscribers[event_type].add(callback)
        
    def unsubscribe(self, event_type: str, callback: Callable):
        """Unsubscribe from an event type"""
        if event_type in self.subscribers and callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
            
    def publish(self, event_type: str, data: Any = None):
        """Publish an event to all subscribers"""
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)

class SharedState:
    """
    Shared state manager for the application
    """
    def __init__(self, event_bus: EventBus):
        self.state = {}
        self.event_bus = event_bus
        self.watchers = {}
        
    def set(self, key: str, value: Any):
        """Set a state value and notify watchers"""
        self.state[key] = value
        # Notify watchers
        if key in self.watchers:
            for callback in self.watchers[key]:
                callback(value)
        # Publish state change event
        self.event_bus.publish("state_change", {"key": key, "value": value})
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value"""
        return self.state.get(key, default)
    
    def watch(self, key: str, callback: Callable):
        """Watch for changes to a specific key"""
        if key not in self.watchers:
            self.watchers[key] = set()
        self.watchers[key].add(callback)
        
    def unwatch(self, key: str, callback: Callable):
        """Stop watching a specific key"""
        if key in self.watchers and callback in self.watchers[key]:
            self.watchers[key].remove(callback)
            
    def get_all(self) -> Dict[str, Any]:
        """Get the entire state"""
        return self.state.copy()
    
    def clear(self):
        """Clear the entire state"""
        old_state = self.state.copy()
        self.state = {}
        # Notify about cleared state
        self.event_bus.publish("state_cleared", old_state)

class StateManager:
    """
    Main state manager that combines EventBus and SharedState
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance.event_bus = EventBus()
            cls._instance.shared_state = SharedState(cls._instance.event_bus)
            cls._instance.ui_keys = set()  # Track UI component keys
        return cls._instance
    
    def register_ui_key(self, key: str) -> str:
        """
        Register a UI component key to prevent duplicates
        Returns the key if it's unique, or a modified key if it already exists
        """
        original_key = key
        counter = 1
        
        while key in self.ui_keys:
            key = f"{original_key}_{counter}"
            counter += 1
            
        self.ui_keys.add(key)
        return key
    
    def release_ui_key(self, key: str):
        """Release a UI component key when no longer needed"""
        if key in self.ui_keys:
            self.ui_keys.remove(key)
    
    def get_event_bus(self) -> EventBus:
        """Get the event bus instance"""
        return self.event_bus
    
    def get_shared_state(self) -> SharedState:
        """Get the shared state instance"""
        return self.shared_state
    
    def save_state(self, filepath: str):
        """Save the current state to a file"""
        serializable_state = {}
        for key, value in self.shared_state.get_all().items():
            # Only save serializable values
            try:
                json.dumps(value)
                serializable_state[key] = value
            except (TypeError, OverflowError):
                pass  # Skip non-serializable values
                
        with open(filepath, 'w') as f:
            json.dump(serializable_state, f, indent=2)
    
    def load_state(self, filepath: str):
        """Load state from a file"""
        try:
            with open(filepath, 'r') as f:
                loaded_state = json.load(f)
                
            for key, value in loaded_state.items():
                self.shared_state.set(key, value)
                
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False

# Singleton instance
state_manager = StateManager()
