#!/usr/bin/env python
"""
Minimal Fix for Import Issues

A truly minimal script that fixes the HierarchicalModule import issue.
"""

import sys
import types
import builtins  # To make the class globally available

# Define HierarchicalModule first
class HierarchicalModule:
    def __init__(self, name=None, root_dir=None):
        self.name = name
        self.root_dir = root_dir
        self.children = []

# Make it available globally
builtins.HierarchicalModule = HierarchicalModule

# Now run fix_imports_simple.py
print("Running fix_imports_simple.py...")
exec(open("fix_imports_simple.py").read())

print("\nAll imports fixed successfully!")
