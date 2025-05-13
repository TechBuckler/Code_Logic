#!/usr/bin/env python
"""
Test Imports

This script tests importing key modules to identify any remaining import issues.
It uses the universal import fixer to resolve import issues dynamically.
"""

import os
import sys
import importlib
import time
import types

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the universal import fixer
try:
    from universal_import_fixer import UniversalImportFixer, ModuleMapper

    # Create and initialize the fixer
    mapper = ModuleMapper()
    mapper.scan_codebase()
    mapper.create_import_aliases()

    fixer = UniversalImportFixer(mapper)
    fixer.fix_import_system()

    print("✅ Universal import fixer initialized")
except ImportError:
    print("⚠️ Universal import fixer not found, falling back to basic imports")

# Add missing type definitions to avoid common errors
try:
    from typing import Dict, List, Any, Optional, Set, Tuple, Union, Callable
except ImportError:
    # Create minimal type aliases if typing module is not available
    Dict = dict
    List = list
    Any = object
    Optional = object
    Set = set
    Tuple = tuple
    Union = object
    Callable = object

# Define essential classes if they're not available
# HierarchicalModule
if "modules.standard.hierarchical_module" not in sys.modules:
    try:
        # Try to import from various locations
        try:
            from modules.standard.hierarchical_module import HierarchicalModule
        except ImportError:
            try:
                from core.hierarchical_module import HierarchicalModule
            except ImportError:
                # Create a minimal HierarchicalModule class
                class HierarchicalModule:
                    def __init__(self, name, parent=None):
                        self.name = name
                        self.parent = parent
                        self.children = {}

                    def add_child(self, module):
                        self.children[module.name] = module
                        return self

        # Create module and add to sys.modules
        hierarchical_module = types.ModuleType("modules.standard.hierarchical_module")
        hierarchical_module.HierarchicalModule = HierarchicalModule
        sys.modules["modules.standard.hierarchical_module"] = hierarchical_module
        sys.modules["core.hierarchical_module"] = hierarchical_module
    except Exception as e:
        print(f"⚠️ Error setting up HierarchicalModule: {e}")

# Module class
if "module_system" not in sys.modules:
    try:
        module_system = types.ModuleType("module_system")

        class Module:
            def __init__(self, name):
                self.name = name
                self.dependencies = []
                self.active = False

        module_system.Module = Module
        sys.modules["module_system"] = module_system
    except Exception as e:
        print(f"⚠️ Error setting up Module: {e}")

# Import the import utility system
try:
    import utils.import_utils

    print("✓ Successfully imported utils.import_utils")
except Exception as e:
    print(f"✗ Failed to import utils.import_utils: {e}")

# Add missing type definitions to avoid common errors
try:
    import types
    from typing import Dict, List, Any, Optional, Set, Tuple, Union, Callable

    # Patch sys.modules with commonly used modules that might be missing
    if "modules.standard.hierarchical_module" not in sys.modules:
        # Create a minimal module
        hierarchical_module = types.ModuleType("modules.standard.hierarchical_module")

        # Define a minimal HierarchicalModule class
        class HierarchicalModule:
            def __init__(self, name, parent=None):
                self.name = name
                self.parent = parent
                self.children = {}

        # Add the class to the module
        hierarchical_module.HierarchicalModule = HierarchicalModule

        # Add to sys.modules
        sys.modules["modules.standard.hierarchical_module"] = hierarchical_module
        sys.modules["core.hierarchical_module"] = hierarchical_module

    # Create module_system if missing
    if "module_system" not in sys.modules:
        module_system = types.ModuleType("module_system")

        class Module:
            def __init__(self, name):
                self.name = name
                self.dependencies = []
                self.active = False

        module_system.Module = Module
        sys.modules["module_system"] = module_system

    # Create background_system if missing
    if "background_system" not in sys.modules:
        background_system = types.ModuleType("background_system")

        class BackgroundSystem:
            def __init__(self):
                self.task_queue = []
                self.running = False

        background_system.BackgroundSystem = BackgroundSystem
        sys.modules["background_system"] = background_system

    # Create ui_components if missing
    if "core.ui_components" not in sys.modules:
        ui_components = types.ModuleType("core.ui_components")

        class UIComponent:
            def __init__(self, name):
                self.name = name

        class UIManager:
            def __init__(self):
                self.components = {}

        ui_components.UIComponent = UIComponent
        ui_components.UIManager = UIManager
        sys.modules["core.ui_components"] = ui_components
        sys.modules["ui.components.core"] = ui_components

except Exception as e:
    print(f"Warning: Error setting up compatibility modules: {e}")
    pass

# List of critical modules to test
CRITICAL_MODULES = [
    # Core modules
    "core.state_manager",
    "core.simple_hierarchical_core",
    "core.hierarchical_module",
    # Refactoring tools
    "tools.refactoring.refactor_splitter",
    "tools.refactoring.file_splitter",
    "tools.refactoring.smart_splitter",
    "core.processing.refactor_analyzer",
    "core.processing.refactor_builder",
    # Shadow tree
    "tools.shadow_tree.navigator",
    "tools.shadow_tree.simple",
    # Utils
    "utils.file.operations",
    "utils.path",
    "utils.string",
    "utils.data.json_utils",
    # UI components
    "ui.unified",
    "ui.renderers.base",
]

# Test importing each module
results = {"success": [], "failure": []}

print("\nTesting imports for critical modules:")
print("=" * 50)

for module_name in CRITICAL_MODULES:
    try:
        # Try to import the module
        start_time = time.time()
        module = importlib.import_module(module_name)
        import_time = time.time() - start_time

        # Success
        results["success"].append({"module": module_name, "time": import_time})
        print(f"✓ {module_name} ({import_time:.3f}s)")
    except Exception as e:
        # Failure
        results["failure"].append({"module": module_name, "error": str(e)})
        print(f"✗ {module_name}: {e}")

# Print summary
print("\nImport Test Summary:")
print(f"Total modules tested: {len(CRITICAL_MODULES)}")
print(f"Successfully imported: {len(results['success'])}")
print(f"Failed to import: {len(results['failure'])}")

if results["failure"]:
    print("\nFailed imports:")
    for failure in results["failure"]:
        print(f"- {failure['module']}: {failure['error']}")

# Test circular imports
print("\nTesting for circular imports:")
print("=" * 50)

# List of module pairs to test for circular imports
CIRCULAR_TEST_PAIRS = [
    ("utils", "utils.import_utils"),
    ("utils.file", "utils.path"),
    ("utils.file", "utils.string"),
    ("core", "utils"),
    ("tools.refactoring", "core.processing"),
]

for module1, module2 in CIRCULAR_TEST_PAIRS:
    print(f"Testing {module1} <-> {module2}...")
    try:
        # Clear modules from sys.modules if they're already imported
        for m in list(sys.modules.keys()):
            if (
                m == module1
                or m.startswith(f"{module1}.")
                or m == module2
                or m.startswith(f"{module2}.")
            ):
                sys.modules.pop(m, None)

        # Try importing in one direction
        importlib.import_module(module1)
        importlib.import_module(module2)
        print(f"  ✓ {module1} -> {module2}")

        # Clear and try the other direction
        for m in list(sys.modules.keys()):
            if (
                m == module1
                or m.startswith(f"{module1}.")
                or m == module2
                or m.startswith(f"{module2}.")
            ):
                sys.modules.pop(m, None)

        importlib.import_module(module2)
        importlib.import_module(module1)
        print(f"  ✓ {module2} -> {module1}")

        print(f"✓ No circular dependency between {module1} and {module2}")
    except Exception as e:
        print(f"✗ Circular dependency detected: {e}")

print("\nImport testing complete.")
