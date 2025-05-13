"""
Module Factory System

This module provides a factory pattern for dynamically creating and managing modules
during the codebase reorganization. It handles compatibility issues, circular dependencies,
and missing modules by creating proxy modules on-demand.

Usage:
    from utils.module_factory import ModuleFactory
    
    # Create a module factory
    factory = ModuleFactory()
    
    # Register module mappings
    factory.register_mapping("old.module.path", "new.module.path")
    
    # Import a module using the factory
    my_module = factory.import_module("module_name")
    
    # Create a compatibility module
    factory.create_compatibility_module("module_name", template_dict)
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import types
import importlib
import importlib.util
import inspect
import logging
from typing import Dict, List, Any, Optional, Union, Callable, Set, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ModuleFactory")

# Get the project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class ModuleSpec:
    """Specification for a module to be created or imported."""
    
    def __init__(self, name: str, path: Optional[str] = None, 
                 template: Optional[Dict[str, Any]] = None):
        """
        Initialize a module specification.
        
        Args:
            name: The name of the module
            path: Optional path to the module file
            template: Optional template for module content
        """
        self.name = name
        self.path = path
        self.template = template or {}
        self.dependencies = set()
        
    def add_dependency(self, module_name: str):
        """Add a dependency to this module."""
        self.dependencies.add(module_name)
        
    def __repr__(self):
        return f"ModuleSpec(name={self.name}, path={self.path}, deps={len(self.dependencies)})"


class ModuleCache:
    """Cache for loaded and generated modules."""
    
    def __init__(self):
        """Initialize the module cache."""
        self.modules = {}
        self.specs = {}
        self.import_attempts = set()
        
    def has_module(self, name: str) -> bool:
        """Check if a module is in the cache."""
        return name in self.modules
    
    def get_module(self, name: str) -> Optional[types.ModuleType]:
        """Get a module from the cache."""
        return self.modules.get(name)
    
    def add_module(self, name: str, module: types.ModuleType):
        """Add a module to the cache."""
        self.modules[name] = module
        
    def has_spec(self, name: str) -> bool:
        """Check if a module spec is in the cache."""
        return name in self.specs
    
    def get_spec(self, name: str) -> Optional[ModuleSpec]:
        """Get a module spec from the cache."""
        return self.specs.get(name)
    
    def add_spec(self, name: str, spec: ModuleSpec):
        """Add a module spec to the cache."""
        self.specs[name] = spec
        
    def record_import_attempt(self, name: str):
        """Record an import attempt to prevent circular imports."""
        self.import_attempts.add(name)
        
    def is_import_attempted(self, name: str) -> bool:
        """Check if an import has been attempted."""
        return name in self.import_attempts
    
    def clear_import_attempt(self, name: str):
        """Clear an import attempt."""
        if name in self.import_attempts:
            self.import_attempts.remove(name)


class ModuleFactory:
    """Factory for creating and managing modules."""
    
    def __init__(self):
        """Initialize the module factory."""
        self.cache = ModuleCache()
        self.mappings = {}
        self.legacy_paths = {}
        self.templates = {}
        self.fallbacks = {}
        
        # Add project root to sys.path
        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)
            
        # Initialize with default templates
        self._init_default_templates()
        
    def _init_default_templates(self):
        """Initialize default templates for common module types."""
        # Basic module template
        self.templates["basic"] = {
            "__doc__": "Auto-generated compatibility module.",
            "__all__": []
        }
        
        # Class template
        self.templates["class"] = {
            "__doc__": "Auto-generated class for compatibility.",
            "methods": {
                "__init__": "def __init__(self, *args, **kwargs): pass",
                "__str__": "def __str__(self): return f'{self.__class__.__name__}()'",
            }
        }
        
    def register_mapping(self, old_path: str, new_path: str):
        """
        Register a mapping from an old module path to a new one.
        
        Args:
            old_path: The old import path
            new_path: The new import path
        """
        self.mappings[old_path] = new_path
        logger.debug(f"Registered mapping: {old_path} -> {new_path}")
        
    def register_legacy_path(self, name: str, path: str):
        """
        Register a legacy path for a module.
        
        Args:
            name: A name for the path
            path: The absolute path
        """
        self.legacy_paths[name] = path
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, path)
            logger.debug(f"Added legacy path to sys.path: {path}")
            
    def register_template(self, name: str, template: Dict[str, Any]):
        """
        Register a template for module generation.
        
        Args:
            name: The name of the template
            template: The template dictionary
        """
        self.templates[name] = template
        logger.debug(f"Registered template: {name}")
        
    def register_fallback(self, module_name: str, fallback_func: Callable):
        """
        Register a fallback function for a module.
        
        Args:
            module_name: The name of the module
            fallback_func: A function that returns a module
        """
        self.fallbacks[module_name] = fallback_func
        logger.debug(f"Registered fallback for: {module_name}")
        
    def _try_direct_import(self, module_name: str) -> Optional[types.ModuleType]:
        """
        Try to import a module directly.
        
        Args:
            module_name: The name of the module
            
        Returns:
            The imported module or None
        """
        try:
            return importlib.import_module(module_name)
        except ImportError:
            return None
        
    def _try_mapped_import(self, module_name: str) -> Optional[types.ModuleType]:
        """
        Try to import a module using mappings.
        
        Args:
            module_name: The name of the module
            
        Returns:
            The imported module or None
        """
        # Check exact mappings
        if module_name in self.mappings:
            mapped_name = self.mappings[module_name]
            try:
                return importlib.import_module(mapped_name)
            except ImportError:
                pass
                
        # Check prefix mappings
        for old_prefix, new_prefix in self.mappings.items():
            if module_name.startswith(old_prefix + "."):
                suffix = module_name[len(old_prefix)+1:]
                try:
                    mapped_name = f"{new_prefix}.{suffix}"
                    return importlib.import_module(mapped_name)
                except ImportError:
                    pass
                    
        return None
        
    def _try_special_cases(self, module_name: str) -> Optional[types.ModuleType]:
        """
        Try special case imports.
        
        Args:
            module_name: The name of the module
            
        Returns:
            The imported module or None
        """
        # Try without src prefix
        if module_name.startswith("src."):
            try:
                new_name = module_name[4:]  # Remove "src."
                return importlib.import_module(new_name)
            except ImportError:
                pass
                
        # Handle hierarchical modules
        if "hierarchical" in module_name:
            try:
                new_name = module_name.replace("hierarchical", "standard")
                return importlib.import_module(new_name)
            except ImportError:
                pass
                
        return None
        
    def _try_fallback(self, module_name: str) -> Optional[types.ModuleType]:
        """
        Try to use a fallback for a module.
        
        Args:
            module_name: The name of the module
            
        Returns:
            The fallback module or None
        """
        if module_name in self.fallbacks:
            try:
                return self.fallbacks[module_name]()
            except Exception as e:
                logger.warning(f"Fallback for {module_name} failed: {e}")
                
        return None
        
    def import_module(self, module_name: str) -> Optional[types.ModuleType]:
        """
        Import a module using all available methods.
        
        Args:
            module_name: The name of the module
            
        Returns:
            The imported module or None
        """
        # Check if we've already loaded this module
        if self.cache.has_module(module_name):
            return self.cache.get_module(module_name)
            
        # Check if we're in a circular import
        if self.cache.is_import_attempted(module_name):
            logger.warning(f"Circular import detected for {module_name}")
            # Return a proxy module to break the cycle
            return self._create_proxy_module(module_name)
            
        # Record that we're attempting to import this module
        self.cache.record_import_attempt(module_name)
        
        # Try all import methods
        module = (self._try_direct_import(module_name) or
                 self._try_mapped_import(module_name) or
                 self._try_special_cases(module_name) or
                 self._try_fallback(module_name))
        
        # If we found a module, cache it
        if module:
            self.cache.add_module(module_name, module)
            self.cache.clear_import_attempt(module_name)
            return module
            
        # If we couldn't import the module, create a proxy
        logger.warning(f"Could not import {module_name}, creating proxy")
        proxy = self._create_proxy_module(module_name)
        self.cache.add_module(module_name, proxy)
        self.cache.clear_import_attempt(module_name)
        return proxy
        
    def _create_proxy_module(self, module_name: str) -> types.ModuleType:
        """
        Create a proxy module for a missing module.
        
        Args:
            module_name: The name of the module
            
        Returns:
            A proxy module
        """
        # Create a new module
        module = types.ModuleType(module_name)
        module.__file__ = f"<{module_name}>"
        module.__name__ = module_name
        module.__package__ = module_name.rpartition('.')[0]
        module.__path__ = []
        module.__doc__ = f"Proxy module for {module_name}"
        
        # Add it to sys.modules
        sys.modules[module_name] = module
        
        return module
        
    def create_compatibility_module(self, module_name: str, 
                                   template_name: str = "basic",
                                   **template_args) -> types.ModuleType:
        """
        Create a compatibility module.
        
        Args:
            module_name: The name of the module
            template_name: The name of the template to use
            **template_args: Arguments to pass to the template
            
        Returns:
            The created module
        """
        # Check if we already have this module
        if self.cache.has_module(module_name):
            return self.cache.get_module(module_name)
            
        # Get the template
        template = self.templates.get(template_name, self.templates["basic"]).copy()
        
        # Update the template with args
        for key, value in template_args.items():
            if key in template and isinstance(template[key], dict) and isinstance(value, dict):
                template[key].update(value)
            else:
                template[key] = value
                
        # Create the module
        module = types.ModuleType(module_name)
        module.__file__ = f"<{module_name}>"
        module.__name__ = module_name
        module.__package__ = module_name.rpartition('.')[0]
        module.__path__ = []
        
        # Add template attributes
        for key, value in template.items():
            if key != "methods" and key != "classes":
                setattr(module, key, value)
                
        # Add methods as functions
        if "methods" in template:
            for name, code in template["methods"].items():
                if callable(code):
                    setattr(module, name, code)
                else:
                    # Compile the code and add it to the module
                    compiled = compile(code, f"<{module_name}.{name}>", "exec")
                    namespace = {}
                    exec(compiled, namespace)
                    setattr(module, name, namespace[name])
                    
        # Add classes
        if "classes" in template:
            for name, class_def in template["classes"].items():
                if isinstance(class_def, type):
                    setattr(module, name, class_def)
                else:
                    # Create the class
                    cls_dict = {}
                    if isinstance(class_def, dict):
                        for method_name, method_code in class_def.get("methods", {}).items():
                            if callable(method_code):
                                cls_dict[method_name] = method_code
                            else:
                                # Compile the method
                                compiled = compile(method_code, f"<{module_name}.{name}.{method_name}>", "exec")
                                namespace = {}
                                exec(compiled, namespace)
                                cls_dict[method_name] = namespace[method_name]
                                
                        # Add attributes
                        for attr_name, attr_value in class_def.get("attributes", {}).items():
                            cls_dict[attr_name] = attr_value
                            
                    # Create the class
                    cls = type(name, (object,), cls_dict)
                    setattr(module, name, cls)
                    
                    # Add to __all__
                    if hasattr(module, "__all__"):
                        module.__all__.append(name)
                    
        # Add the module to sys.modules and cache
        sys.modules[module_name] = module
        self.cache.add_module(module_name, module)
        
        logger.info(f"Created compatibility module: {module_name}")
        return module
        
    def create_module_from_spec(self, spec: ModuleSpec) -> types.ModuleType:
        """
        Create a module from a specification.
        
        Args:
            spec: The module specification
            
        Returns:
            The created module
        """
        # Check if we already have this module
        if self.cache.has_module(spec.name):
            return self.cache.get_module(spec.name)
            
        # Create the module
        module = types.ModuleType(spec.name)
        module.__file__ = spec.path or f"<{spec.name}>"
        module.__name__ = spec.name
        module.__package__ = spec.name.rpartition('.')[0]
        module.__path__ = []
        
        # Add template attributes
        for key, value in spec.template.items():
            if key != "methods" and key != "classes":
                setattr(module, key, value)
                
        # Add the module to sys.modules and cache
        sys.modules[spec.name] = module
        self.cache.add_module(spec.name, module)
        
        logger.info(f"Created module from spec: {spec.name}")
        return module
        
    def load_mappings_from_dict(self, mappings: Dict[str, str]):
        """
        Load mappings from a dictionary.
        
        Args:
            mappings: A dictionary of old to new mappings
        """
        for old_path, new_path in mappings.items():
            self.register_mapping(old_path, new_path)
            
    def load_legacy_paths_from_dict(self, paths: Dict[str, str]):
        """
        Load legacy paths from a dictionary.
        
        Args:
            paths: A dictionary of name to path mappings
        """
        for name, path in paths.items():
            self.register_legacy_path(name, path)
            
    def generate_compatibility_module(self, module_name: str, file_path: str, 
                                     template_name: str = "basic", 
                                     **template_args) -> bool:
        """
        Generate a compatibility module file.
        
        Args:
            module_name: The name of the module
            file_path: The path to write the module to
            template_name: The name of the template to use
            **template_args: Arguments to pass to the template
            
        Returns:
            True if successful, False otherwise
        """
        # Make sure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Get the template
        template = self.templates.get(template_name, self.templates["basic"]).copy()
        
        # Update the template with args
        for key, value in template_args.items():
            if key in template and isinstance(template[key], dict) and isinstance(value, dict):
                template[key].update(value)
            else:
                template[key] = value
                
        # Generate the module code
        code = [f'"""\n{template.get("__doc__", "Auto-generated compatibility module.")}\n"""']
        
        # Add imports
        if "imports" in template:
            for imp in template["imports"]:
                code.append(imp)
                
        code.append("")  # Empty line after imports
        
        # Add functions
        if "methods" in template:
            for name, func_code in template["methods"].items():
                if isinstance(func_code, str):
                    code.append(func_code)
                    code.append("")  # Empty line after function
                    
        # Add classes
        if "classes" in template:
            for name, class_def in template["classes"].items():
                if isinstance(class_def, dict):
                    # Generate class code
                    class_code = [f"class {name}:"]
                    
                    # Add docstring
                    if "__doc__" in class_def:
                        class_code.append(f'    """{class_def["__doc__"]}"""')
                        
                    # Add methods
                    for method_name, method_code in class_def.get("methods", {}).items():
                        if isinstance(method_code, str):
                            # Indent the method code
                            indented_code = "\n".join(f"    {line}" for line in method_code.split("\n"))
                            class_code.append(indented_code)
                            
                    # Add the class to the module code
                    code.extend(class_code)
                    code.append("")  # Empty line after class
                    
        # Add __all__
        if "__all__" in template:
            all_list = ", ".join(f"'{item}'" for item in template["__all__"])
            code.append(f"__all__ = [{all_list}]")
            
        # Write the code to the file
        try:
            with open(file_path, "w") as f:
                f.write("\n".join(code))
            logger.info(f"Generated compatibility module at {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate module {module_name} at {file_path}: {e}")
            return False
            
    @classmethod
    def create_instance_with_defaults(cls):
        """
        Create a ModuleFactory instance with default settings.
        
        Returns:
            A configured ModuleFactory instance
        """
        factory = cls()
        
        # Add project root and common directories to sys.path
        for directory in ["core", "modules", "utils", "tools", "ui"]:
            path = os.path.join(PROJECT_ROOT, directory)
            if os.path.exists(path) and path not in sys.path:
                sys.path.insert(0, path)
                
        # Register common module templates
        factory.register_template("module_system", {
            "__doc__": "Compatibility module for the module system.",
            "classes": {
                "Module": {
                    "__doc__": "Basic module class for compatibility.",
                    "methods": {
                        "__init__": "def __init__(self, name):\n    self.name = name\n    self.dependencies = []\n    self.active = False",
                        "activate": "def activate(self):\n    self.active = True\n    return True",
                        "deactivate": "def deactivate(self):\n    self.active = False\n    return True",
                        "is_active": "def is_active(self):\n    return self.active",
                        "add_dependency": "def add_dependency(self, module):\n    if module not in self.dependencies:\n        self.dependencies.append(module)\n    return True",
                        "get_dependencies": "def get_dependencies(self):\n    return self.dependencies"
                    }
                },
                "ModuleSystem": {
                    "__doc__": "System for managing modules.",
                    "methods": {
                        "__init__": "def __init__(self):\n    self.modules = {}",
                        "register_module": "def register_module(self, module):\n    self.modules[module.name] = module\n    return True",
                        "get_module": "def get_module(self, name):\n    return self.modules.get(name)",
                        "activate_module": "def activate_module(self, name):\n    module = self.get_module(name)\n    if module:\n        return module.activate()\n    return False",
                        "deactivate_module": "def deactivate_module(self, name):\n    module = self.get_module(name)\n    if module:\n        return module.deactivate()\n    return False",
                        "get_active_modules": "def get_active_modules(self):\n    return [m for m in self.modules.values() if m.is_active()]"
                    }
                }
            },
            "methods": {
                "create_module": "def create_module(name):\n    return Module(name)"
            },
            "__all__": ["Module", "ModuleSystem", "create_module"]
        })
        
        factory.register_template("background_system", {
            "__doc__": "Compatibility module for the background system.",
            "imports": [
                "import os",
                "import sys",
                "import threading",
                "import time",
                "import queue"
            ],
            "classes": {
                "BackgroundSystem": {
                    "__doc__": "System for running tasks in the background.",
                    "methods": {
                        "__init__": "def __init__(self):\n    self.task_queue = queue.PriorityQueue()\n    self.running = False\n    self.thread = None\n    self.log = []",
                        "start": "def start(self):\n    if not self.running:\n        self.running = True\n        self.thread = threading.Thread(target=self._worker)\n        self.thread.daemon = True\n        self.thread.start()\n        return True\n    return False",
                        "stop": "def stop(self):\n    if self.running:\n        self.running = False\n        if self.thread:\n            self.thread.join(timeout=1.0)\n        return True\n    return False",
                        "add_task": "def add_task(self, task, priority=0):\n    self.task_queue.put((priority, task))\n    return True",
                        "_worker": "def _worker(self):\n    while self.running:\n        try:\n            if not self.task_queue.empty():\n                priority, task = self.task_queue.get(block=False)\n                try:\n                    result = task()\n                    self.log.append({\n                        'task': task.__name__ if hasattr(task, '__name__') else str(task),\n                        'priority': priority,\n                        'result': result,\n                        'time': time.time()\n                    })\n                except Exception as e:\n                    self.log.append({\n                        'task': task.__name__ if hasattr(task, '__name__') else str(task),\n                        'priority': priority,\n                        'error': str(e),\n                        'time': time.time()\n                    })\n            else:\n                time.sleep(0.1)\n        except Exception:\n            time.sleep(0.1)",
                        "get_log": "def get_log(self):\n    return self.log"
                    }
                }
            },
            "methods": {
                "create_background_system": "def create_background_system():\n    return BackgroundSystem()"
            },
            "__all__": ["BackgroundSystem", "create_background_system"]
        })
        
        factory.register_template("ui_components", {
            "__doc__": "Compatibility module for UI components.",
            "classes": {
                "UIComponent": {
                    "__doc__": "Base class for UI components.",
                    "methods": {
                        "__init__": "def __init__(self, name):\n    self.name = name\n    self.visible = True\n    self.parent = None\n    self.children = []",
                        "render": "def render(self):\n    pass",
                        "add_child": "def add_child(self, child):\n    self.children.append(child)\n    child.parent = self",
                        "remove_child": "def remove_child(self, child):\n    if child in self.children:\n        self.children.remove(child)\n        child.parent = None",
                        "show": "def show(self):\n    self.visible = True",
                        "hide": "def hide(self):\n    self.visible = False"
                    }
                },
                "UIManager": {
                    "__doc__": "Manager for UI components.",
                    "methods": {
                        "__init__": "def __init__(self):\n    self.components = {}\n    self.active_component = None",
                        "register_component": "def register_component(self, name, component):\n    self.components[name] = component\n    return component",
                        "get_component": "def get_component(self, name):\n    return self.components.get(name)",
                        "set_active": "def set_active(self, name):\n    if name in self.components:\n        self.active_component = self.components[name]\n        return True\n    return False",
                        "render_all": "def render_all(self):\n    for component in self.components.values():\n        if component.visible:\n            component.render()"
                    }
                }
            },
            "methods": {
                "create_component": "def create_component(name):\n    return UIComponent(name)",
                "create_manager": "def create_manager():\n    return UIManager()"
            },
            "__all__": ["UIComponent", "UIManager", "create_component", "create_manager"]
        })
        
        # Register common module mappings
        common_mappings = {
            # Core modules
            "core.state_manager": "utils.file.state_manager",
            "core.hierarchical_module": "modules.standard.hierarchical_module",
            "core.simple_hierarchical_core": "modules.standard.simple_hierarchical_core",
            "src.modules.hierarchical": "modules.standard",
            "module_system": "modules.system",
            "background_system": "modules.background",
            "modules.code_analysis_module": "modules.standard.code_analysis_module",
            
            # Refactoring tools
            "tools.file_splitter": "tools.refactoring.file_splitter",
            "tools.smart_splitter": "tools.refactoring.smart_splitter",
            "tools.resource_splitter": "tools.refactoring.resource_splitter",
            "refactor_splitter": "tools.refactoring.refactor_splitter",
            "refactor_analyzer": "core.processing.refactor_analyzer",
            "refactor_builder": "core.processing.refactor_builder",
            
            # Additional mappings for commonly used modules
            "file_utils": "utils.file.operations",
            "path_utils": "utils.path",
            "string_utils": "utils.string",
            "json_utils": "utils.data.json_utils",
            "runtime_utils": "utils.runtime.operations",
            
            # Shadow tree and related tools
            "shadow_tree": "tools.shadow_tree.navigator",
            "simple_shadow_tree": "tools.shadow_tree.simple",
            "fractal_organizer": "tools.fractal.organizer",
            
            # UI components
            "unified_ui": "ui.unified",
            "ui_renderers": "ui.renderers.base",
            "ui_utils": "ui.components.utils",
            "core.ui_components": "ui.components.core",
        }
        
        factory.load_mappings_from_dict(common_mappings)
        
        return factory


# Create a global factory instance
module_factory = ModuleFactory.create_instance_with_defaults()

# Export symbols
__all__ = ['ModuleFactory', 'ModuleSpec', 'ModuleCache', 'module_factory']
