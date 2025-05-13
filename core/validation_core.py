#!/usr/bin/env python
"""
Validation Core

This module provides core functionality for integrating the validation system
with the dynamic module system of code_logic_tool_full.
"""

import os
import sys
import importlib
from typing import Dict, List, Any, Optional, Callable

# Add the project root to the path if needed
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to import the module system
try:
    from core.module_system import ModuleSystem
    MODULE_SYSTEM_AVAILABLE = True
except ImportError:
    MODULE_SYSTEM_AVAILABLE = False
    print("Module system not available. Make sure it's installed correctly.")

class ValidationCore:
    """Core class for integrating validation with the module system."""
    
    def __init__(self):
        """Initialize the validation core."""
        self.module_system = None
        self.validation_module = None
        
        # Initialize the module system if available
        if MODULE_SYSTEM_AVAILABLE:
            try:
                self.module_system = ModuleSystem()
                print("Module system initialized successfully.")
            except Exception as e:
                print(f"Error initializing module system: {str(e)}")
        
        # Try to load the validation module
        self._load_validation_module()
    
    def _load_validation_module(self) -> bool:
        """
        Load the validation module from the module system.
        
        Returns:
            True if the module was loaded successfully, False otherwise
        """
        if not self.module_system:
            return False
        
        try:
            # Try to get the validation module from the module system
            self.validation_module = self.module_system.get_module("validation_module")
            if self.validation_module:
                print("Validation module loaded from module system.")
                return True
            
            # If not found, try to import it directly
            try:
                from modules.validation_module import ValidationModule
                self.validation_module = ValidationModule()
                print("Validation module imported directly.")
                return True
            except ImportError:
                print("Validation module not found in modules directory.")
                return False
        except Exception as e:
            print(f"Error loading validation module: {str(e)}")
            return False
    
    def register_validation_hooks(self, hooks: Dict[str, Callable]) -> bool:
        """
        Register validation hooks with the module system.
        
        Args:
            hooks: Dictionary of hook names to hook functions
            
        Returns:
            True if the hooks were registered successfully, False otherwise
        """
        if not self.module_system:
            return False
        
        try:
            for hook_name, hook_func in hooks.items():
                self.module_system.register_hook(hook_name, hook_func)
            print(f"Registered {len(hooks)} validation hooks with the module system.")
            return True
        except Exception as e:
            print(f"Error registering validation hooks: {str(e)}")
            return False
    
    def validate_code(self, code: str, scope: str = 'all') -> Dict[str, Any]:
        """
        Validate code using the validation module.
        
        Args:
            code: The code to validate
            scope: The scope of validation ('all', 'function', 'class')
            
        Returns:
            A dictionary with validation results
        """
        if not self.validation_module:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Validation module not available",
                "suggestions": ["Install the validation module"]
            }
        
        try:
            return self.validation_module.validate_code(code, scope)
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error during validation: {str(e)}",
                "suggestions": []
            }
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a Python file.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            A dictionary with validation results
        """
        if not self.validation_module:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Validation module not available",
                "suggestions": ["Install the validation module"]
            }
        
        try:
            return self.validation_module.validate_file(file_path)
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error validating file {file_path}: {str(e)}",
                "suggestions": [],
                "file_path": file_path
            }
    
    def validate_module(self, module_name: str) -> Dict[str, Any]:
        """
        Validate a module in the module system.
        
        Args:
            module_name: Name of the module to validate
            
        Returns:
            A dictionary with validation results
        """
        if not self.module_system:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Module system not available",
                "suggestions": ["Install the module system"]
            }
        
        try:
            module = self.module_system.get_module(module_name)
            if not module:
                return {
                    "status": "ERROR",
                    "confidence": 0.0,
                    "explanation": f"Module {module_name} not found",
                    "suggestions": [f"Check if module {module_name} exists"]
                }
            
            # Get the module's file path
            module_file = getattr(module, "__file__", None)
            if not module_file:
                return {
                    "status": "ERROR",
                    "confidence": 0.0,
                    "explanation": f"Module {module_name} does not have a file path",
                    "suggestions": [f"Check if module {module_name} is a file-based module"]
                }
            
            # Validate the module file
            return self.validate_file(module_file)
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error validating module {module_name}: {str(e)}",
                "suggestions": []
            }

def test_validation_core():
    """Test the validation core with a sample file."""
    validation_core = ValidationCore()
    
    # Test with the current file
    current_file = os.path.abspath(__file__)
    print(f"Testing validation on file: {current_file}")
    
    result = validation_core.validate_file(current_file)
    print("\n" + "=" * 60)
    print("FILE VALIDATION RESULT")
    print("=" * 60)
    print(f"File: {result.get('file_path', 'unknown')}")
    print(f"Status: {result.get('status', 'UNKNOWN')}")
    print(f"Confidence: {result.get('confidence', 0.0):.2f}")
    print(f"Source: {result.get('source', 'unknown')}")
    
    if "explanation" in result:
        print(f"\nExplanation: {result['explanation']}")
        
    if "suggestions" in result and result["suggestions"]:
        print("\nSuggestions:")
        for i, suggestion in enumerate(result["suggestions"], 1):
            print(f"{i}. {suggestion}")
            
    print("=" * 60)

if __name__ == "__main__":
    test_validation_core()
