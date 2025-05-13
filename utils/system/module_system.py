"""
Module System Compatibility Module

This module provides compatibility for the module_system module during the transition
to the new directory structure. It now includes validation capabilities.
"""
# Fix imports for reorganized codebase
try:
    import utils.import_utils
except ImportError:
    # If utils.import_utils is not available, continue without it
    pass

import os
import sys
import importlib
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to import from the new location
try:
    from modules.system import *
except ImportError:
    # Define minimal functionality to satisfy imports
    class Module:
        """Basic module class for compatibility."""
        
        def __init__(self, name, parent=None):
            """Initialize with a name."""
            self.name = name
            self.parent = parent
            self.dependencies = []
            self.active = False
            self.resource_profile = {
                'cpu': 0.5,     # Default CPU usage (0.0-1.0)
                'memory': 0.5,  # Default memory usage (0.0-1.0)
                'io': 0.3,      # Default I/O usage (0.0-1.0)
                'gpu': 0.0      # Default GPU usage (0.0-1.0)
            }
            self.validation_enabled = False
        
        def activate(self):
            """Activate the module."""
            self.active = True
            return True
        
        def deactivate(self):
            """Deactivate the module."""
            self.active = False
            return True
        
        def is_active(self):
            """Check if the module is active."""
            return self.active
        
        def add_dependency(self, module):
            """Add a dependency to the module."""
            if module not in self.dependencies:
                self.dependencies.append(module)
            return True
        
        def get_dependencies(self):
            """Get the module's dependencies."""
            return self.dependencies

class ModuleSystem:
    """System for managing modules."""
    
    def __init__(self):
        """Initialize the module system."""
        self.modules = {}
        self.hooks = {}
        self.validation_module = None
        
        # Try to load the validation module
        self._load_validation_module()
    
    def register_module(self, module):
        """Register a module with the system."""
        self.modules[module.name] = module
        return True
    
    def get_module(self, name):
        """Get a module by name."""
        return self.modules.get(name)
    
    def activate_module(self, name):
        """Activate a module by name."""
        module = self.get_module(name)
        if module:
            # Validate the module before activation if validation is enabled
            if module.validation_enabled and self.validation_module:
                validation_result = self.validate_module(module)
                if validation_result.get("status") != "VALID":
                    print(f"Module {name} failed validation: {validation_result.get('explanation')}")
                    return False
            
            return module.activate()
        return False
    
    def deactivate_module(self, name):
        """Deactivate a module by name."""
        module = self.get_module(name)
        if module:
            return module.deactivate()
        return False
    
    def get_active_modules(self):
        """Get all active modules."""
        return [m for m in self.modules.values() if m.is_active()]
    
    def _load_validation_module(self):
        """Load the validation module."""
        try:
            # First try to import from the tools directory
            spec = importlib.util.find_spec("tools.validation.shadow_validator")
            if spec:
                validation_module = importlib.import_module("tools.validation.shadow_validator")
                self.validation_module = validation_module.ShadowValidator()
                print("Loaded Shadow validator from tools.validation")
                return True
            
            # Then try to import from the modules directory
            spec = importlib.util.find_spec("modules.validation_module")
            if spec:
                validation_module = importlib.import_module("modules.validation_module")
                self.validation_module = validation_module.ValidationModule()
                print("Loaded validation module from modules directory")
                return True
            
            print("Validation module not found")
            return False
        except Exception as e:
            print(f"Error loading validation module: {str(e)}")
            return False
    
    def register_hook(self, hook_name: str, hook_function):
        """Register a hook function."""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(hook_function)
        return True
    
    def trigger_hook(self, hook_name: str, *args, **kwargs):
        """Trigger a hook by name."""
        if hook_name in self.hooks:
            results = []
            for hook_function in self.hooks[hook_name]:
                try:
                    result = hook_function(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Error in hook {hook_name}: {str(e)}")
            return results
        return []
    
    def validate_module(self, module) -> Dict[str, Any]:
        """Validate a module."""
        if not self.validation_module:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Validation module not available",
                "suggestions": ["Install the validation module"]
            }
        
        try:
            # Get the module's file path
            module_file = getattr(module, "__file__", None)
            if not module_file:
                return {
                    "status": "ERROR",
                    "confidence": 0.0,
                    "explanation": f"Module {module.name} does not have a file path",
                    "suggestions": [f"Check if module {module.name} is a file-based module"]
                }
            
            # Validate the module file
            if hasattr(self.validation_module, "validate_file"):
                return self.validation_module.validate_file(module_file)
            elif hasattr(self.validation_module, "validate_code"):
                with open(module_file, 'r') as f:
                    code = f.read()
                return self.validation_module.validate_code(code)
            else:
                return {
                    "status": "ERROR",
                    "confidence": 0.0,
                    "explanation": "Validation module does not have validate_file or validate_code methods",
                    "suggestions": ["Check the validation module implementation"]
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error validating module {module.name}: {str(e)}",
                "suggestions": []
            }
    
    def validate_code(self, code: str, scope: str = 'all') -> Dict[str, Any]:
        """Validate code using the validation module."""
        if not self.validation_module:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Validation module not available",
                "suggestions": ["Install the validation module"]
            }
        
        try:
            if hasattr(self.validation_module, "validate_code"):
                return self.validation_module.validate_code(code, scope)
            else:
                return {
                    "status": "ERROR",
                    "confidence": 0.0,
                    "explanation": "Validation module does not have validate_code method",
                    "suggestions": ["Check the validation module implementation"]
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error during validation: {str(e)}",
                "suggestions": []
            }
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a file using the validation module."""
        if not self.validation_module:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Validation module not available",
                "suggestions": ["Install the validation module"]
            }
        
        try:
            if hasattr(self.validation_module, "validate_file"):
                return self.validation_module.validate_file(file_path)
            elif hasattr(self.validation_module, "validate_code"):
                with open(file_path, 'r') as f:
                    code = f.read()
                result = self.validation_module.validate_code(code)
                result['file_path'] = file_path
                return result
            else:
                return {
                    "status": "ERROR",
                    "confidence": 0.0,
                    "explanation": "Validation module does not have validate_file or validate_code methods",
                    "suggestions": ["Check the validation module implementation"]
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error validating file {file_path}: {str(e)}",
                "suggestions": [],
                "file_path": file_path
            }

# Create a singleton instance
module_system = ModuleSystem()

# Export symbols
__all__ = ['Module', 'ModuleSystem', 'module_system']

# Try to initialize validation module
try:
    # Register validation module if it exists
    from modules.validation_module import ValidationModule
    validation_module = ValidationModule(parent=module_system)
    module_system.register_module(validation_module)
    print("Registered validation module with module system")
except ImportError:
    print("Validation module not available for registration")
