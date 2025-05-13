"""
Compatibility module for hierarchical_module.
This file redirects imports to the new location in modules/standard/hierarchical_module.py

Auto-generated test cases for core.hierarchical_module
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase

import os
import sys
import unittest

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import the module to test
try:
except ImportError as e:
    print(f"Error importing core.hierarchical_module: {e}")
    print("Make sure the module exists and imports are correct.")
    sys.exit(1)


if __name__ == "__main__":
    unittest.main()
