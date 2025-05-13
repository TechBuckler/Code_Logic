"""
core package.

Auto-generated test cases for core.__init__
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
    print(f"Error importing core.__init__: {e}")
    print("Make sure the module exists and imports are correct.")
    sys.exit(1)


if __name__ == "__main__":
    unittest.main()
