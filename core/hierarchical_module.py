#!/usr/bin/env python
"""
Fix HierarchicalModule Imports

This script creates the necessary modules in sys.modules to fix import issues
with HierarchicalModule.
"""

import sys
import types

# Create HierarchicalModule
hierarchical_module = types.ModuleType('modules.standard.hierarchical_module')

class HierarchicalModule:
    def __init__(self, name=None, root_dir=None):
        self.name = name
        self.root_dir = root_dir
        self.children = []

hierarchical_module.HierarchicalModule = HierarchicalModule
sys.modules['modules.standard.hierarchical_module'] = hierarchical_module
sys.modules['modules.hierarchical_module'] = hierarchical_module
sys.modules['hierarchical_module'] = hierarchical_module

print("Fixed HierarchicalModule imports")

# Create RuntimeOptimizationModule
runtime_module = types.ModuleType('modules.runtime_optimization')

class RuntimeOptimizationModule:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.optimizations = []

runtime_module.RuntimeOptimizationModule = RuntimeOptimizationModule
sys.modules['modules.runtime_optimization'] = runtime_module
sys.modules['modules.runtime_optimization_module'] = runtime_module
sys.modules['modules.standard.runtime_optimization_module'] = runtime_module

print("Fixed RuntimeOptimizationModule imports")

# Create utils.import_utils if needed
utils_module = types.ModuleType('utils')
sys.modules['utils'] = utils_module

import_utils_module = types.ModuleType('utils.import_utils')
sys.modules['utils.import_utils'] = import_utils_module

print("Fixed utils.import_utils imports")

print("All imports fixed successfully")
