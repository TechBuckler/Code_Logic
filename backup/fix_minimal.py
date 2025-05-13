#!/usr/bin/env python
"""
Minimal Import Fixer

This script adds the HierarchicalModule to sys.modules directly.
"""

import sys
import types

# Create HierarchicalModule
class HierarchicalModule:
    def __init__(self, name=None, root_dir=None):
        self.name = name
        self.root_dir = root_dir
        self.children = []

# Add to sys.modules at all required paths
hierarchical_module = types.ModuleType('hierarchical_module')
hierarchical_module.HierarchicalModule = HierarchicalModule
sys.modules['hierarchical_module'] = hierarchical_module
sys.modules['modules.hierarchical_module'] = hierarchical_module
sys.modules['modules.standard.hierarchical_module'] = hierarchical_module

print("Fixed HierarchicalModule imports")

# Now run the refactor_organize_simple script
import refactor_organize_simple

print("Refactoring and organization complete")
