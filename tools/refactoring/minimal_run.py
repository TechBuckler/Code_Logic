#!/usr/bin/env python
"""
Minimal Run Script

This script defines HierarchicalModule and patches sys.modules before
any imports happen, ensuring it's available to all modules.
"""

import sys
import types
import builtins  # We'll use this to make HierarchicalModule truly global


# Define HierarchicalModule
class HierarchicalModule:
    def __init__(self, name=None, root_dir=None):
        self.name = name
        self.root_dir = root_dir
        self.children = []


# Make it available as a built-in (this is the key!)
builtins.HierarchicalModule = HierarchicalModule

# Also add to sys.modules for imports
hierarchical_module = types.ModuleType("hierarchical_module")
hierarchical_module.HierarchicalModule = HierarchicalModule
sys.modules["hierarchical_module"] = hierarchical_module
sys.modules["modules.hierarchical_module"] = hierarchical_module
sys.modules["modules.standard.hierarchical_module"] = hierarchical_module
sys.modules["core.hierarchical_module"] = hierarchical_module


# Define RuntimeOptimizationModule
class RuntimeOptimizationModule:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.optimizations = []


# Add to sys.modules
runtime_module = types.ModuleType("modules.runtime_optimization")
runtime_module.RuntimeOptimizationModule = RuntimeOptimizationModule
sys.modules["modules.runtime_optimization"] = runtime_module
sys.modules["modules.runtime_optimization_module"] = runtime_module
sys.modules["modules.standard.runtime_optimization_module"] = runtime_module

print("Fixed imports")


# Define a custom import hook to handle missing imports
class ImportFixer:
    def __init__(self):
        self.original_import = __import__

    def __call__(self, name, globals=None, locals=None, fromlist=(), level=0):
        try:
            return self.original_import(name, globals, locals, fromlist, level)
        except ImportError as e:
            # If the import fails, check if it's one we can fix
            if name == "bootstrap_module" or "bootstrap" in name:
                # Create a bootstrap module
                bootstrap_module = types.ModuleType("bootstrap_module")

                # Define BootstrapModule
                class BootstrapModule(HierarchicalModule):
                    def __init__(self, name=None, root_dir=None):
                        super().__init__(name, root_dir)

                bootstrap_module.BootstrapModule = BootstrapModule
                sys.modules["bootstrap_module"] = bootstrap_module
                return bootstrap_module

            # If we can't fix it, re-raise the original error
            raise e


# Install the import hook
builtins.__import__ = ImportFixer()

# Now run the reorganization script
print("Running reorganization script...")

# Execute the script directly
exec(open("refactor_organize_simple.py").read())

print("Reorganization complete!")
