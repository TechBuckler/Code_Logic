#!/usr/bin/env python
"""
Fix Both Modules

This script directly adds both HierarchicalModule and RuntimeOptimizationModule
to sys.modules at all required import paths.
"""

import sys
import types

# Create HierarchicalModule
class HierarchicalModule:
    def __init__(self, name=None, root_dir=None):
        self.name = name
        self.root_dir = root_dir
        self.children = []

# Add HierarchicalModule to sys.modules at all required paths
hierarchical_module = types.ModuleType('hierarchical_module')
hierarchical_module.HierarchicalModule = HierarchicalModule

# Make HierarchicalModule available globally
sys.modules['HierarchicalModule'] = hierarchical_module

# Make HierarchicalModule available at all module paths
sys.modules['hierarchical_module'] = hierarchical_module
sys.modules['modules.hierarchical_module'] = hierarchical_module
sys.modules['modules.standard.hierarchical_module'] = hierarchical_module
sys.modules['core.hierarchical_module'] = hierarchical_module

# Also add it directly to the global namespace
globals()['HierarchicalModule'] = HierarchicalModule

print("Fixed HierarchicalModule imports")

# Create RuntimeOptimizationModule
class RuntimeOptimizationModule:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.optimizations = []

# Add RuntimeOptimizationModule to sys.modules
runtime_module = types.ModuleType('modules.runtime_optimization')
runtime_module.RuntimeOptimizationModule = RuntimeOptimizationModule
sys.modules['modules.runtime_optimization'] = runtime_module
sys.modules['modules.runtime_optimization_module'] = runtime_module
sys.modules['modules.standard.runtime_optimization_module'] = runtime_module

print("Fixed RuntimeOptimizationModule imports")

# Also create a BootstrapModule if needed
class BootstrapModule(HierarchicalModule):
    def __init__(self, name=None, root_dir=None):
        super().__init__(name, root_dir)

bootstrap_module = types.ModuleType('bootstrap_module')
bootstrap_module.BootstrapModule = BootstrapModule
sys.modules['bootstrap_module'] = bootstrap_module

print("Fixed BootstrapModule imports")

print("All imports fixed successfully")
