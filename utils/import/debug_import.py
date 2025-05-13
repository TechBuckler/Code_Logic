#!/usr/bin/env python
"""
Debug Import Issues

This script helps debug the specific import issues with HierarchicalModule.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import traceback

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Test HierarchicalModule import
try:
    print("Attempting to import HierarchicalModule...")
    from modules.standard.hierarchical_module import HierarchicalModule
    print("✅ Successfully imported HierarchicalModule")
except Exception as e:
    print(f"❌ Failed to import HierarchicalModule: {e}")
    print("\nDetailed traceback:")
    traceback.print_exc()
    
    # Check if core.state_manager exists
    print("\nChecking core.state_manager module...")
    try:
        import core.state_manager
        print("✅ core.state_manager module exists")
        print("Attributes in core.state_manager:")
        for attr in dir(core.state_manager):
            if not attr.startswith('__'):
                print(f"  - {attr}")
    except Exception as e:
        print(f"❌ Failed to import core.state_manager: {e}")
        
    # Check if modules.standard.hierarchical_module exists
    print("\nChecking modules.standard.hierarchical_module module...")
    try:
        import importlib.util
        spec = importlib.util.find_spec('modules.standard.hierarchical_module')
        if spec:
            print(f"✅ modules.standard.hierarchical_module module exists at {spec.origin}")
            
            # Try to load the module directly
            try:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print("✅ Successfully loaded the module")
                print("Attributes in the module:")
                for attr in dir(module):
                    if not attr.startswith('__'):
                        print(f"  - {attr}")
            except Exception as e:
                print(f"❌ Failed to load the module: {e}")
                traceback.print_exc()
        else:
            print("❌ modules.standard.hierarchical_module module not found")
    except Exception as e:
        print(f"❌ Error checking for module: {e}")
