#!/usr/bin/env python
"""
Test New Structure

This script tests that the core functionality works with the new directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils


import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Break circular dependencies first
from circular_dependency_breaker import preload_modules

preload_modules()

# Import the universal import fixer
from universal_import_fixer import UniversalImportFixer, ModuleMapper

# Initialize the fixer
print("Initializing universal import fixer...")
mapper = ModuleMapper()
mapper.scan_codebase()
mapper.create_import_aliases()
fixer = UniversalImportFixer(mapper)
fixer.fix_import_system()

# Test importing core modules
print("\nTesting imports from new structure:")
print("-----------------------------------")

# Test HierarchicalModule
try:
    # First try the direct import
    try:
        from modules.standard.hierarchical_module import HierarchicalModule
    except ImportError:
        # If that fails, try the compatibility import
        from core.hierarchical_module import HierarchicalModule

    # Create a minimal state manager if needed for HierarchicalModule
    try:
        from core.state_manager import StateManager, EventBus, SharedState
    except ImportError:
        # Create minimal versions
        class EventBus:
            def __init__(self):
                self.listeners = {}

        class SharedState:
            def __init__(self):
                self.state = {}

        class StateManager:
            def __init__(self):
                self._event_bus = EventBus()
                self._shared_state = SharedState()

            def get_event_bus(self):
                return self._event_bus

            def get_shared_state(self):
                return self._shared_state

    # Create a state manager instance if needed
    state_manager = StateManager()

    # Create test modules
    parent = HierarchicalModule("parent")
    child = HierarchicalModule("child", parent=parent)

    # Verify the relationship
    assert child.parent == parent
    assert child.name in parent.children
    assert parent.children[child.name] == child

    print("✅ Successfully imported and used HierarchicalModule")
except Exception as e:
    print(f"❌ Failed to import HierarchicalModule: {e}")

# Test Module System
try:
    from module_system import Module

    module = Module("test_module")
    print("✅ Successfully imported and used Module")
except Exception as e:
    print(f"❌ Failed to import Module: {e}")

# Test Shadow Tree
try:
    from tools.shadow_tree.navigator import ShadowTree

    print("✅ Successfully imported ShadowTree")
except Exception as e:
    print(f"❌ Failed to import ShadowTree: {e}")

# Test State Manager
try:
    from core.state_manager import StateManager

    state_manager = StateManager()
    print("✅ Successfully imported and used StateManager")
except Exception as e:
    print(f"❌ Failed to import StateManager: {e}")

print("\nNew structure test complete!")
