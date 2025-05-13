"""
Hierarchical Core - Foundation for the self-bootstrapping architecture

This module provides the core components for a hierarchical, modular system
that can dynamically organize, load, and manage modules at multiple levels
of abstraction.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import importlib
import json
import uuid
import weakref
import threading

# -----------------------------------------------------------------------------
# Event System
# -----------------------------------------------------------------------------

class EventPriority(Enum):
    """Priority levels for event handlers"""
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()

class Event:
    """Base event class for the event system"""
    def __init__(self, event_type: str, data: Any = None, source: Any = None):
        self.event_type = event_type
        self.data = data
        self.source = source
        self.id = str(uuid.uuid4())
        self.timestamp = __import__('time').time()
        self.propagate = True  # Whether the event should propagate up the hierarchy
        self.handled = False   # Whether the event has been handled

    def __str__(self):
        return f"Event({self.event_type}, id={self.id})"

class EventBus:
    """
    Central event bus that supports hierarchical event propagation
    """
    def __init__(self, parent_bus: Optional['EventBus'] = None):
        self.subscribers = {}  # event_type -> [(callback, priority)]
        self.parent_bus = parent_bus
        self.child_buses = weakref.WeakSet()
        if parent_bus:
            parent_bus.child_buses.add(self)
        self.lock = threading.RLock()
    
    def subscribe(self, event_type: str, callback: Callable[[Event], None], 
                 priority: EventPriority = EventPriority.NORMAL):
        """Subscribe to an event type with a given priority"""
        with self.lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append((callback, priority))
            # Sort by priority (higher priority first)
            self.subscribers[event_type].sort(key=lambda x: x[1].value, reverse=True)
    
    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]):
        """Unsubscribe from an event type"""
        with self.lock:
            if event_type in self.subscribers:
                self.subscribers[event_type] = [
                    (cb, prio) for cb, prio in self.subscribers[event_type] 
                    if cb != callback
                ]
    
    def publish(self, event: Union[Event, str], data: Any = None, source: Any = None) -> Event:
        """
        Publish an event to all subscribers
        
        Args:
            event: Either an Event object or an event type string
            data: Event data (used only if event is a string)
            source: Event source (used only if event is a string)
            
        Returns:
            The published event
        """
        # Convert string to Event if needed
        if isinstance(event, str):
            event = Event(event, data, source)
            
        # Process local subscribers
        with self.lock:
            if event.event_type in self.subscribers:
                for callback, _ in self.subscribers[event.event_type]:
                    try:
                        callback(event)
                        if event.handled:
                            break
                    except Exception as e:
                        print(f"Error in event handler: {e}")
        
        # Propagate to parent if needed
        if event.propagate and self.parent_bus and not event.handled:
            self.parent_bus.publish(event)
            
        # Propagate to children if needed
        if event.propagate and not event.handled:
            for child_bus in list(self.child_buses):
                child_bus.publish(event)
                
        return event

# -----------------------------------------------------------------------------
# State Management
# -----------------------------------------------------------------------------

class StateChangeEvent(Event):
    """Event fired when state changes"""
    def __init__(self, key: str, value: Any, old_value: Any = None, source: Any = None):
        super().__init__("state_change", {
            "key": key,
            "value": value,
            "old_value": old_value
        }, source)

class StateStore:
    """
    Hierarchical state store that supports state change notifications
    """
    def __init__(self, event_bus: EventBus, parent_store: Optional['StateStore'] = None):
        self.state = {}
        self.event_bus = event_bus
        self.parent_store = parent_store
        self.watchers = {}  # key -> set of callbacks
        self.lock = threading.RLock()
        
    def set(self, key: str, value: Any, source: Any = None):
        """Set a state value and notify watchers"""
        with self.lock:
            old_value = self.state.get(key)
            self.state[key] = value
            
            # Notify watchers
            if key in self.watchers:
                for callback in list(self.watchers[key]):
                    try:
                        callback(value, old_value)
                    except Exception as e:
                        print(f"Error in state watcher: {e}")
            
            # Publish state change event
            self.event_bus.publish(StateChangeEvent(key, value, old_value, source))
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a state value, checking parent stores if not found
        """
        with self.lock:
            if key in self.state:
                return self.state[key]
            elif self.parent_store:
                return self.parent_store.get(key, default)
            else:
                return default
    
    def watch(self, key: str, callback: Callable[[Any, Any], None]):
        """Watch for changes to a specific key"""
        with self.lock:
            if key not in self.watchers:
                self.watchers[key] = set()
            self.watchers[key].add(callback)
    
    def unwatch(self, key: str, callback: Callable[[Any, Any], None]):
        """Stop watching a specific key"""
        with self.lock:
            if key in self.watchers and callback in self.watchers[key]:
                self.watchers[key].remove(callback)
                
    def get_all(self, include_parent: bool = False) -> Dict[str, Any]:
        """Get all state values"""
        with self.lock:
            if include_parent and self.parent_store:
                # Start with parent state and override with local state
                result = self.parent_store.get_all(include_parent)
                result.update(self.state)
                return result
            else:
                return self.state.copy()

# -----------------------------------------------------------------------------
# Module System
# -----------------------------------------------------------------------------

class ModuleStatus(Enum):
    """Status of a module"""
    UNINITIALIZED = auto()
    INITIALIZING = auto()
    ACTIVE = auto()
    ERROR = auto()
    DISABLED = auto()

class HierarchicalModule(ABC):
    """
    Base class for all modules in the hierarchical system
    """
    def __init__(self, module_id: str, parent: Optional['HierarchicalModule'] = None):
        self.module_id = module_id
        self.parent = parent
        self.children = {}  # id -> module
        self.status = ModuleStatus.UNINITIALIZED
        self.error = None
        
        # Create or inherit event bus and state store
        if parent:
            self.event_bus = EventBus(parent.event_bus)
            self.state_store = StateStore(self.event_bus, parent.state_store)
            parent.add_child(self)
        else:
            self.event_bus = EventBus()
            self.state_store = StateStore(self.event_bus)
    
    def add_child(self, module: 'HierarchicalModule'):
        """Add a child module"""
        self.children[module.module_id] = module
    
    def remove_child(self, module_id: str):
        """Remove a child module"""
        if module_id in self.children:
            del self.children[module_id]
    
    def get_child(self, module_id: str) -> Optional['HierarchicalModule']:
        """Get a child module by ID"""
        return self.children.get(module_id)
    
    def get_descendant(self, path: List[str]) -> Optional['HierarchicalModule']:
        """
        Get a descendant module by path
        
        Args:
            path: List of module IDs forming a path to the descendant
            
        Returns:
            The descendant module or None if not found
        """
        if not path:
            return self
            
        child_id = path[0]
        child = self.get_child(child_id)
        
        if child and len(path) > 1:
            return child.get_descendant(path[1:])
        else:
            return child
    
    def get_path(self) -> List[str]:
        """Get the path from the root to this module"""
        if self.parent:
            return self.parent.get_path() + [self.module_id]
        else:
            return [self.module_id]
    
    def get_full_id(self) -> str:
        """Get the full ID including the path"""
        return ".".join(self.get_path())
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the module
        
        Returns:
            True if initialization was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def process(self, data: Any, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process data with this module
        
        Args:
            data: The data to process
            context: Additional context for processing
            
        Returns:
            The processed data
        """
        pass
    
    def shutdown(self):
        """Shutdown the module and its children"""
        # Shutdown children first
        for child in list(self.children.values()):
            child.shutdown()
        
        # Then shutdown self
        self.status = ModuleStatus.DISABLED
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert module to dictionary representation"""
        return {
            "id": self.module_id,
            "full_id": self.get_full_id(),
            "status": self.status.name,
            "error": str(self.error) if self.error else None,
            "children": [child.to_dict() for child in self.children.values()]
        }

class ModuleRegistry:
    """
    Registry for all modules in the system
    """
    def __init__(self):
        self.root_modules = {}  # id -> module
        self.module_cache = {}  # full_id -> module
    
    def register_module(self, module: HierarchicalModule):
        """Register a root module"""
        self.root_modules[module.module_id] = module
        self._update_cache(module)
    
    def unregister_module(self, module_id: str):
        """Unregister a root module"""
        if module_id in self.root_modules:
            module = self.root_modules[module_id]
            self._remove_from_cache(module)
            del self.root_modules[module_id]
    
    def get_module(self, module_id: str) -> Optional[HierarchicalModule]:
        """Get a module by ID (can be a full path ID)"""
        # Check if it's a direct root module
        if module_id in self.root_modules:
            return self.root_modules[module_id]
        
        # Check if it's in the cache
        if module_id in self.module_cache:
            return self.module_cache[module_id]
        
        # Try to find it by path
        path = module_id.split(".")
        if len(path) > 1:
            root_id = path[0]
            if root_id in self.root_modules:
                return self.root_modules[root_id].get_descendant(path[1:])
        
        return None
    
    def _update_cache(self, module: HierarchicalModule):
        """Update the module cache with a module and its descendants"""
        self.module_cache[module.get_full_id()] = module
        for child in module.children.values():
            self._update_cache(child)
    
    def _remove_from_cache(self, module: HierarchicalModule):
        """Remove a module and its descendants from the cache"""
        if module.get_full_id() in self.module_cache:
            del self.module_cache[module.get_full_id()]
        for child in module.children.values():
            self._remove_from_cache(child)
    
    def initialize_all(self):
        """Initialize all modules"""
        for module in list(self.root_modules.values()):
            self._initialize_module(module)
    
    def _initialize_module(self, module: HierarchicalModule):
        """Initialize a module and its children"""
        try:
            module.status = ModuleStatus.INITIALIZING
            success = module.initialize()
            module.status = ModuleStatus.ACTIVE if success else ModuleStatus.ERROR
            
            # Initialize children
            for child in list(module.children.values()):
                self._initialize_module(child)
                
        except Exception as e:
            module.status = ModuleStatus.ERROR
            module.error = e
    
    def shutdown_all(self):
        """Shutdown all modules"""
        for module in list(self.root_modules.values()):
            module.shutdown()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert registry to dictionary representation"""
        return {
            "modules": [module.to_dict() for module in self.root_modules.values()]
        }

# -----------------------------------------------------------------------------
# Dynamic Loading System
# -----------------------------------------------------------------------------

class ModuleLoader:
    """
    Utility for dynamically loading modules
    """
    @staticmethod
    def load_module_class(module_path: str, class_name: str) -> Type[HierarchicalModule]:
        """
        Load a module class from a Python module
        
        Args:
            module_path: Import path to the Python module
            class_name: Name of the class to load
            
        Returns:
            The loaded class
        """
        try:
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Failed to load module class {class_name} from {module_path}: {e}")
    
    @staticmethod
    def load_module_instance(module_path: str, class_name: str, 
                           module_id: str, parent: Optional[HierarchicalModule] = None,
                           **kwargs) -> HierarchicalModule:
        """
        Load and instantiate a module
        
        Args:
            module_path: Import path to the Python module
            class_name: Name of the class to load
            module_id: ID for the new module
            parent: Parent module
            **kwargs: Additional arguments for the module constructor
            
        Returns:
            The instantiated module
        """
        cls = ModuleLoader.load_module_class(module_path, class_name)
        return cls(module_id=module_id, parent=parent, **kwargs)
    
    @staticmethod
    def load_from_config(config_path: str, registry: ModuleRegistry):
        """
        Load modules from a configuration file
        
        Args:
            config_path: Path to the configuration file
            registry: Module registry to register modules with
        """
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Load root modules
        for module_config in config.get("modules", []):
            module = ModuleLoader._load_module_from_config(module_config)
            registry.register_module(module)
    
    @staticmethod
    def _load_module_from_config(config: Dict[str, Any], 
                               parent: Optional[HierarchicalModule] = None) -> HierarchicalModule:
        """
        Load a module from a configuration dictionary
        
        Args:
            config: Module configuration
            parent: Parent module
            
        Returns:
            The loaded module
        """
        module_path = config["module_path"]
        class_name = config["class_name"]
        module_id = config["id"]
        kwargs = config.get("kwargs", {})
        
        module = ModuleLoader.load_module_instance(
            module_path, class_name, module_id, parent, **kwargs
        )
        
        # Load children
        for child_config in config.get("children", []):
            child = ModuleLoader._load_module_from_config(child_config, module)
            # No need to add_child here as it's done in the child's constructor
        
        return module

# -----------------------------------------------------------------------------
# File Management System
# -----------------------------------------------------------------------------

class FileSplitter:
    """
    Utility for splitting files based on various criteria
    """
    @staticmethod
    def split_by_class(file_path: str, output_dir: str):
        """
        Split a Python file by class definitions
        
        Args:
            file_path: Path to the Python file
            output_dir: Directory to write the split files
        """
        import ast
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Parse the file
        with open(file_path, 'r') as f:
            source = f.read()
        
        tree = ast.parse(source)
        
        # Find all class definitions
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        
        # Create a file for each class
        for cls in classes:
            # Extract the class source
            class_source = source[cls.lineno-1:cls.end_lineno]
            
            # Create the output file
            output_path = os.path.join(output_dir, f"{cls.name}.py")
            with open(output_path, 'w') as f:
                f.write(class_source)
    
    @staticmethod
    def split_by_size(file_path: str, output_dir: str, max_size: int = 1000):
        """
        Split a file by size
        
        Args:
            file_path: Path to the file
            output_dir: Directory to write the split files
            max_size: Maximum size of each split file in lines
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Read the file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Split the file
        file_base = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(file_base)
        
        for i in range(0, len(lines), max_size):
            chunk = lines[i:i+max_size]
            output_path = os.path.join(output_dir, f"{file_name}_part{i//max_size+1}{file_ext}")
            with open(output_path, 'w') as f:
                f.writelines(chunk)

# -----------------------------------------------------------------------------
# Bootstrap Utilities
# -----------------------------------------------------------------------------

class CodeAnalyzer:
    """
    Utility for analyzing code to identify module boundaries
    """
    @staticmethod
    def analyze_file(file_path: str) -> Dict[str, Any]:
        """
        Analyze a Python file to identify potential modules
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Analysis results
        """
        import ast
        
        # Parse the file with error handling for different encodings
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except UnicodeDecodeError:
            try:
                # Try with Latin-1 (which can read any byte sequence)
                with open(file_path, 'r', encoding='latin-1') as f:
                    source = f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                return {
                    "file_path": file_path,
                    "error": str(e),
                    "classes": []
                }
        
        # Parse the AST with error handling
        try:
            tree = ast.parse(source)
            
            # Find all class definitions
            classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
            return {
                "file_path": file_path,
                "error": f"Syntax error: {str(e)}",
                "classes": []
            }
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return {
                "file_path": file_path,
                "error": str(e),
                "classes": []
            }
        
        # Analyze each class
        class_info = []
        for cls in classes:
            # Check if it might be a module
            is_module = False
            for base in cls.bases:
                if isinstance(base, ast.Name) and base.id.endswith('Module'):
                    is_module = True
                    break
            
            # Get methods
            methods = [node.name for node in cls.body if isinstance(node, ast.FunctionDef)]
            
            class_info.append({
                "name": cls.name,
                "is_module": is_module,
                "methods": methods,
                "lineno": cls.lineno,
                "end_lineno": cls.end_lineno
            })
        
        return {
            "file_path": file_path,
            "classes": class_info
        }
    
    @staticmethod
    def analyze_directory(directory: str) -> List[Dict[str, Any]]:
        """
        Analyze all Python files in a directory
        
        Args:
            directory: Directory to analyze
            
        Returns:
            Analysis results for all files
        """
        results = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        result = CodeAnalyzer.analyze_file(file_path)
                        results.append(result)
                    except Exception as e:
                        print(f"Error analyzing {file_path}: {e}")
        
        return results

class ModuleGenerator:
    """
    Utility for generating module code
    """
    @staticmethod
    def generate_module_class(module_name: str, parent_class: str = "HierarchicalModule") -> str:
        """
        Generate code for a module class
        
        Args:
            module_name: Name of the module class
            parent_class: Name of the parent class
            
        Returns:
            Generated code
        """
        return f"""
class {module_name}({parent_class}):
    \"\"\"
    {module_name} module
    \"\"\"
    def __init__(self, module_id: str, parent=None, **kwargs):
        super().__init__(module_id=module_id, parent=parent)
        # Additional initialization
        
    def initialize(self) -> bool:
        \"\"\"Initialize the module\"\"\"
        try:
            # Initialization code
            return True
        except Exception as e:
            self.error = e
            return False
    
    def process(self, data, context=None):
        \"\"\"Process data with this module\"\"\"
        # Processing code
        return data
"""

    @staticmethod
    def generate_module_file(module_name: str, output_path: str, 
                           parent_class: str = "HierarchicalModule",
                           imports: List[str] = None):
        """
        Generate a module file
        
        Args:
            module_name: Name of the module class
            output_path: Path to write the file
            parent_class: Name of the parent class
            imports: Additional imports
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate imports
        import_lines = [
            "from typing import Dict, List, Any, Optional",
            f"from core.hierarchical_core import {parent_class}"
        ]
        
        if imports:
            import_lines.extend(imports)
        
        imports_str = "\n".join(import_lines)
        
        # Generate class code
        class_code = ModuleGenerator.generate_module_class(module_name, parent_class)
        
        # Write the file
        with open(output_path, 'w') as f:
            f.write(f"""\"\"\"
{module_name} module
\"\"\"

{imports_str}

{class_code}
""")
