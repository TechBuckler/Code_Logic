#!/usr/bin/env python
"""
Test Validation Integration

This script tests the integration of the Shadow validation system with the module system.
"""

import os
import sys

# Add the project root to the path if needed
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Run the import fixer first to ensure all modules are available
print("Running import fixer...")

# Import the fix_imports_simple module directly
exec(open(os.path.join(project_root, 'fix_imports_simple.py')).read())
print("Import fixer executed successfully.")

# Now we can safely import the module system
from utils.system.module_system import module_system

def test_validation_on_file():
    """Test validation on a specific file."""
    print("\n=== Testing Validation on File ===")
    
    # Choose a Python file to validate
    file_path = os.path.join(project_root, "utils", "system", "module_system.py")
    
    # Validate the file
    result = module_system.validate_file(file_path)
    
    # Print the results
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

def test_validation_on_code():
    """Test validation on a code snippet."""
    print("\n=== Testing Validation on Code Snippet ===")
    
    # Create a test code snippet with some issues
    code = """
def badFunction():
    # Missing docstring
    x = 10
    y = 20
    return x+y

class badClass:
    # Missing docstring and wrong naming convention
    def __init__(self):
        self.value = 42
    
    def getValue(self):
        # Wrong naming convention
        return self.value
    """
    
    # Validate the code
    result = module_system.validate_code(code)
    
    # Print the results
    print(f"Status: {result.get('status', 'UNKNOWN')}")
    print(f"Confidence: {result.get('confidence', 0.0):.2f}")
    print(f"Source: {result.get('source', 'unknown')}")
    
    if "explanation" in result:
        print(f"\nExplanation: {result['explanation']}")
        
    if "suggestions" in result and result["suggestions"]:
        print("\nSuggestions:")
        for i, suggestion in enumerate(result["suggestions"], 1):
            print(f"{i}. {suggestion}")

def main():
    """Main function to run the tests."""
    print("=== Shadow Validation Integration Test ===")
    
    # Test validation on a file
    test_validation_on_file()
    
    # Test validation on a code snippet
    test_validation_on_code()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
