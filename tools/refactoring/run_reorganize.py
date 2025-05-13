#!/usr/bin/env python
"""
Run Reorganization

This script fixes imports and then runs the reorganization script.
Simple, direct approach as preferred.
"""

import sys
import types
import importlib


# Define HierarchicalModule first
class HierarchicalModule:
    def __init__(self, name=None, root_dir=None):
        self.name = name
        self.root_dir = root_dir
        self.children = []


# Make it available globally
globals()["HierarchicalModule"] = HierarchicalModule

# Add to sys.modules
hierarchical_module = types.ModuleType("hierarchical_module")
hierarchical_module.HierarchicalModule = HierarchicalModule
sys.modules["hierarchical_module"] = hierarchical_module
sys.modules["modules.hierarchical_module"] = hierarchical_module
sys.modules["modules.standard.hierarchical_module"] = hierarchical_module
sys.modules["core.hierarchical_module"] = hierarchical_module
sys.modules["HierarchicalModule"] = hierarchical_module

print("Fixed HierarchicalModule imports")


# Create RuntimeOptimizationModule
class RuntimeOptimizationModule:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.optimizations = []


# Add RuntimeOptimizationModule to sys.modules
runtime_module = types.ModuleType("modules.runtime_optimization")
runtime_module.RuntimeOptimizationModule = RuntimeOptimizationModule
sys.modules["modules.runtime_optimization"] = runtime_module
sys.modules["modules.runtime_optimization_module"] = runtime_module
sys.modules["modules.standard.runtime_optimization_module"] = runtime_module

print("Fixed RuntimeOptimizationModule imports")

# Now run the reorganization script
print("\nRunning reorganization script...")
import refactor_organize_simple

print("\nReorganization complete!")
