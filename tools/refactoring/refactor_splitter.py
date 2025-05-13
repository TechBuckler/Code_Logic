#!/usr/bin/env python
"""
Compatibility module for refactor_splitter.py.
This file redirects imports to the new location in tools/refactoring/.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase


import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import from the new location
try:
    from tools.refactoring.refactor_splitter import *
except ImportError as e:
    print(f"Error importing from tools.refactoring.refactor_splitter: {e}")
    print("Make sure the module exists in tools/refactoring/")
    sys.exit(1)
