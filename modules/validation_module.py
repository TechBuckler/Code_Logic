#!/usr/bin/env python
"""
Validation Module

This module integrates the Shadow validator into the module system
for code validation and quality checking.
"""

import os
import sys
import importlib
from typing import Dict, List, Any, Optional

# Add the project root to the path if needed
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to import the Shadow validator
try:
    from tools.validation.shadow_validator import ShadowValidator
    VALIDATOR_AVAILABLE = True
except ImportError:
    VALIDATOR_AVAILABLE = False
    print("Shadow validator not available. Install it from the tools/validation directory.")

class ValidationModule:
    """Module for code validation using the Shadow validator."""
    
    def __init__(self, name="validation_module", parent=None):
        """Initialize the validation module."""
        self.name = name
        self.parent = parent
        self.validator = None
        
        # Initialize the Shadow validator if available
        if VALIDATOR_AVAILABLE:
            try:
                self.validator = ShadowValidator()
                print("Shadow validator initialized successfully.")
            except Exception as e:
                print(f"Error initializing Shadow validator: {str(e)}")
    
    def validate_code(self, code: str, scope: str = 'all') -> Dict[str, Any]:
        """
        Validate code using the Shadow validator.
        
        Args:
            code: The code to validate
            scope: The scope of validation ('all', 'function', 'class')
            
        Returns:
            A dictionary with validation results
        """
        if not self.validator:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Shadow validator not available",
                "suggestions": ["Install the Shadow validator"]
            }
        
        try:
            result = self.validator.validate_code(code, scope)
            return result
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error during validation: {str(e)}",
                "suggestions": []
            }
    
    def validate_function(self, code: str, function_name: str) -> Dict[str, Any]:
        """
        Validate a specific function in the code.
        
        Args:
            code: The full code containing the function
            function_name: The name of the function to validate
            
        Returns:
            A dictionary with validation results
        """
        if not self.validator:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Shadow validator not available",
                "suggestions": ["Install the Shadow validator"]
            }
        
        try:
            result = self.validator.validate_function(code, function_name)
            return result
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
        if not self.validator:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Shadow validator not available",
                "suggestions": ["Install the Shadow validator"]
            }
        
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            result = self.validator.validate_code(code)
            result['file_path'] = file_path
            return result
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error validating file {file_path}: {str(e)}",
                "suggestions": [],
                "file_path": file_path
            }
    
    def validate_directory(self, directory_path: str, recursive: bool = True) -> Dict[str, List[Dict[str, Any]]]:
        """
        Validate all Python files in a directory.
        
        Args:
            directory_path: Path to the directory to validate
            recursive: Whether to recursively validate subdirectories
            
        Returns:
            A dictionary with validation results for each file
        """
        if not self.validator:
            return {
                "status": "ERROR",
                "explanation": "Shadow validator not available",
                "files": []
            }
        
        results = {
            "status": "SUCCESS",
            "files": []
        }
        
        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        result = self.validate_file(file_path)
                        results['files'].append(result)
                
                if not recursive:
                    break
            
            return results
        except Exception as e:
            return {
                "status": "ERROR",
                "explanation": f"Error validating directory {directory_path}: {str(e)}",
                "files": []
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get validation statistics."""
        if not self.validator:
            return {
                "total_validations": 0,
                "rule_based_validations": 0,
                "pattern_validations": 0,
                "execution_time": 0.0
            }
        
        return self.validator.get_stats()

def test_module():
    """Test the validation module with a sample file."""
    module = ValidationModule()
    
    # Test with the current file
    current_file = os.path.abspath(__file__)
    print(f"Testing validation on file: {current_file}")
    
    result = module.validate_file(current_file)
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
            
    print("\n" + "=" * 60)
    
    # Get stats
    stats = module.get_stats()
    print("\n" + "=" * 60)
    print("VALIDATION STATS")
    print("=" * 60)
    for key, value in stats.items():
        print(f"{key}: {value}")
    print("=" * 60)

if __name__ == "__main__":
    test_module()
