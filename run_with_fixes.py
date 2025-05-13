#!/usr/bin/env python
"""
Run With Fixes

A script that applies all necessary fixes and then runs the reorganization script.
"""

import sys
import types
import builtins
import os
from typing import Dict, List, Tuple, Set, Optional, Any  # Import all typing modules

# Define HierarchicalModule
class HierarchicalModule:
    def __init__(self, name=None, root_dir=None):
        self.name = name
        self.root_dir = root_dir
        self.children = []

# Make it available globally and in sys.modules
builtins.HierarchicalModule = HierarchicalModule
hierarchical_module = types.ModuleType('hierarchical_module')
hierarchical_module.HierarchicalModule = HierarchicalModule
sys.modules['hierarchical_module'] = hierarchical_module
sys.modules['modules.hierarchical_module'] = hierarchical_module
sys.modules['modules.standard.hierarchical_module'] = hierarchical_module

print("Fixed HierarchicalModule imports")

# Define RuntimeOptimizationModule
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

# Define BootstrapModule
class BootstrapModule(HierarchicalModule):
    def __init__(self, name=None, root_dir=None):
        super().__init__(name, root_dir)
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
    def process(self, command: str, context: Optional[Dict[str, Any]] = None):
        return {"status": "success"}

# Add BootstrapModule to sys.modules
bootstrap_module = types.ModuleType('bootstrap_module')
bootstrap_module.BootstrapModule = BootstrapModule
sys.modules['bootstrap_module'] = bootstrap_module
sys.modules['utils.string.bootstrap'] = bootstrap_module

print("Fixed BootstrapModule imports")

# Create utils.import_utils if needed
utils_module = types.ModuleType('utils')
sys.modules['utils'] = utils_module

import_utils_module = types.ModuleType('utils.import_utils')
sys.modules['utils.import_utils'] = import_utils_module

print("Fixed utils.import_utils imports")

# Now run the reorganization script
print("\nRunning reorganization script...")

# Add tools directory to path if needed
import os
import sys
tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

# Import from the new location
try:
    from tools.refactoring.refactor_organize_simple import main
except ImportError:
    # Fall back to the old location if not found
    try:
        from refactor_organize_simple import main
    except ImportError:
        print("Could not import refactor_organize_simple from either location")
        sys.exit(1)

# Run the reorganization
main()

print("\nReorganization complete!")
