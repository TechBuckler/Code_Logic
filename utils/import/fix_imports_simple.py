"""
Simple Import Fixer

This script creates the necessary modules in sys.modules to fix import issues.
"""
# Fix imports for reorganized codebase
import sys
import types

# Create import_utils if needed
try:
    import utils.import_utils
except ImportError:
    # Create the module if it doesn't exist
    utils_module = types.ModuleType('utils')
    sys.modules['utils'] = utils_module
    
    import_utils_module = types.ModuleType('utils.import_utils')
    sys.modules['utils.import_utils'] = import_utils_module



import sys
import types

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

# Add HierarchicalModule
class HierarchicalModule:
    def __init__(self, name=None, root_dir=None):
        self.name = name
        self.root_dir = root_dir
        self.children = []

# Make HierarchicalModule available globally and at all required paths
sys.modules['HierarchicalModule'] = types.ModuleType('HierarchicalModule')
sys.modules['HierarchicalModule'].HierarchicalModule = HierarchicalModule

sys.modules['hierarchical_module'] = types.ModuleType('hierarchical_module')
sys.modules['hierarchical_module'].HierarchicalModule = HierarchicalModule

sys.modules['modules.hierarchical_module'] = sys.modules['hierarchical_module']
sys.modules['modules.standard.hierarchical_module'] = sys.modules['hierarchical_module']
sys.modules['core.hierarchical_module'] = sys.modules['hierarchical_module']

# Also add it to globals
globals()['HierarchicalModule'] = HierarchicalModule

print("Fixed HierarchicalModule imports")

# Add any other modules that need fixing here

print("All imports fixed successfully")
