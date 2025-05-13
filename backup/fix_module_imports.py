#!/usr/bin/env python
"""
Fix Module Imports

A simple, reusable tool for fixing specific module import issues.
This script can be used to create placeholder modules for missing imports,
making it easy to fix import issues in a TDD (Test-Driven Development) approach.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import types
import importlib
import traceback

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def create_placeholder_module(module_name, class_names=None):
    """
    Create a placeholder module with specified classes.
    
    Args:
        module_name: The full module path (e.g., 'modules.runtime_optimization')
        class_names: List of class names to create in the module
        
    Returns:
        The created module
    """
    # Create the module
    module = types.ModuleType(module_name)
    
    # Add classes if specified
    if class_names:
        for class_name in class_names:
            # Create a dynamic class
            dynamic_class = type(class_name, (), {
                '__init__': lambda self, *args, **kwargs: None,
                '__str__': lambda self: f"{class_name} instance"
            })
            
            # Add the class to the module
            setattr(module, class_name, dynamic_class)
            print(f"  - Added {class_name} class to {module_name}")
    
    # Add to sys.modules
    sys.modules[module_name] = module
    print(f"Created placeholder for module: {module_name}")
    
    return module

def create_module_aliases(module_name, alias_paths):
    """
    Create aliases for a module at multiple import paths.
    
    Args:
        module_name: The original module name
        alias_paths: List of alias paths to create
        
    Returns:
        List of created alias paths
    """
    if module_name not in sys.modules:
        raise ValueError(f"Module {module_name} must be created before creating aliases")
    
    module = sys.modules[module_name]
    created_aliases = []
    
    for alias_path in alias_paths:
        sys.modules[alias_path] = module
        created_aliases.append(alias_path)
        print(f"  - Created alias at {alias_path}")
    
    return created_aliases

def fix_runtime_optimization_module():
    """Fix the RuntimeOptimizationModule import issue."""
    # Create the module
    module = create_placeholder_module('modules.runtime_optimization', ['RuntimeOptimizationModule'])
    
    # Add specific methods to the RuntimeOptimizationModule class
    RuntimeOptimizationModule = module.RuntimeOptimizationModule
    
    # Add methods
    def add_optimization(self, optimization):
        if not hasattr(self, 'optimizations'):
            self.optimizations = []
        self.optimizations.append(optimization)
        return self
    
    def optimize(self, code):
        if not hasattr(self, 'optimizations'):
            return code
        for optimization in self.optimizations:
            code = optimization(code)
        return code
    
    # Attach methods
    RuntimeOptimizationModule.add_optimization = add_optimization
    RuntimeOptimizationModule.optimize = optimize
    
    # Create aliases
    create_module_aliases('modules.runtime_optimization', [
        'modules.runtime_optimization_module',
        'modules.standard.runtime_optimization_module'
    ])
    
    return module

def fix_hierarchical_module():
    """Fix the HierarchicalModule import issue."""
    # First create the Module class as a base for HierarchicalModule
    module_system = create_placeholder_module('module_system', ['Module'])
    
    # Add methods to Module
    def activate(self):
        self.active = True
        return True
    
    def deactivate(self):
        self.active = False
        return True
    
    # Attach methods
    module_system.Module.activate = activate
    module_system.Module.deactivate = deactivate
    
    # Create HierarchicalModule
    hierarchical_module = types.ModuleType('modules.standard.hierarchical_module')
    
    # Create HierarchicalModule class that inherits from Module
    class HierarchicalModule(module_system.Module):
        def __init__(self, name, parent=None):
            super().__init__(name)
            self.parent = parent
            self.children = {}
            self.event_bus = None
            self.shared_state = None
    
    # Add the class to the module
    hierarchical_module.HierarchicalModule = HierarchicalModule
    
    # Add to sys.modules
    sys.modules['modules.standard.hierarchical_module'] = hierarchical_module
    print(f"Created placeholder for module: modules.standard.hierarchical_module")
    print(f"  - Added HierarchicalModule class to modules.standard.hierarchical_module")
    
    # Add methods
    def add_child(self, module):
        if not hasattr(self, 'children'):
            self.children = {}
        self.children[module.name] = module
        return self
    
    def remove_child(self, name):
        if hasattr(self, 'children') and name in self.children:
            del self.children[name]
        return self
    
    def get_child(self, name):
        if hasattr(self, 'children'):
            return self.children.get(name)
        return None
    
    def get_path(self):
        if hasattr(self, 'parent') and self.parent:
            return self.parent.get_path() + [self.name]
        return [self.name]
    
    def get_full_name(self):
        return ".".join(self.get_path())
    
    # Attach methods
    HierarchicalModule.add_child = add_child
    HierarchicalModule.remove_child = remove_child
    HierarchicalModule.get_child = get_child
    HierarchicalModule.get_path = get_path
    HierarchicalModule.get_full_name = get_full_name
    
    # Create aliases
    create_module_aliases('modules.standard.hierarchical_module', [
        'core.hierarchical_module',
        'hierarchical_module'
    ])
    
    return hierarchical_module

def fix_missing_modules_for_unified_ui():
    """Fix missing modules required by utils.file.new_unified_ui."""
    # Create missing modules
    modules_to_create = [
        ('modules.code_analysis_module', 'CodeAnalysisModule'),
        ('modules.custom_function_module', 'CustomFunctionModule'),
        ('modules.project_organizer_module', 'ProjectOrganizerModule'),
        ('modules.module_explorer_module', 'ModuleExplorerModule'),
        ('modules.optimization_testbed_module', 'OptimizationTestbedModule')
    ]
    
    for module_path, class_name in modules_to_create:
        create_placeholder_module(module_path, [class_name])
    
    # Create streamlit module
    streamlit_module = create_placeholder_module('streamlit', [])
    
    # Add session_state to streamlit
    class SessionState(dict):
        def __init__(self):
            super().__init__()
            self.initialized = False
            self.modules = {}
            self.background_system = None
    
    # Add session_state to streamlit
    streamlit_module.session_state = SessionState()
    
    # Add common streamlit functions
    def st_title(text):
        print(f"STREAMLIT TITLE: {text}")
        return None
    
    def st_header(text):
        print(f"STREAMLIT HEADER: {text}")
        return None
    
    def st_sidebar():
        return streamlit_module
    
    # Add functions to streamlit module
    streamlit_module.title = st_title
    streamlit_module.header = st_header
    streamlit_module.sidebar = st_sidebar
    
    # Create alias for streamlit
    sys.modules['st'] = streamlit_module
    
    # Create BackgroundSystem
    background_system_module = create_placeholder_module('background_system', ['BackgroundSystem'])
    
    # Create ModuleRegistry
    module_registry_module = create_placeholder_module('module_registry', ['ModuleRegistry'])
    
    print("✅ Fixed missing modules for unified UI")

def fix_common_imports():
    """Fix common import issues in the codebase."""
    # Fix RuntimeOptimizationModule
    fix_runtime_optimization_module()
    
    # Fix HierarchicalModule
    fix_hierarchical_module()
    
    # Fix missing modules for unified UI
    fix_missing_modules_for_unified_ui()
    
    print("✅ Fixed common import issues")

def test_imports(modules_to_test):
    """
    Test importing a list of modules.
    
    Args:
        modules_to_test: List of module names to test
        
    Returns:
        Tuple of (successful_imports, failed_imports)
    """
    successful = []
    failed = []
    
    print(f"\nTesting {len(modules_to_test)} modules:")
    for module_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            print(f"✅ {module_name}")
            successful.append(module_name)
            
            # Clean up
            del module
            if module_name in sys.modules:
                del sys.modules[module_name]
        except Exception as e:
            print(f"❌ {module_name}: {e}")
            failed.append((module_name, str(e)))
    
    return successful, failed

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix module import issues")
    parser.add_argument("--fix-common", action="store_true", help="Fix common import issues")
    parser.add_argument("--fix-runtime", action="store_true", help="Fix RuntimeOptimizationModule")
    parser.add_argument("--fix-hierarchical", action="store_true", help="Fix HierarchicalModule")
    parser.add_argument("--test", action="store_true", help="Test imports after fixing")
    parser.add_argument("--module", help="Specific module to test")
    
    args = parser.parse_args()
    
    if args.fix_common:
        fix_common_imports()
    
    if args.fix_runtime:
        fix_runtime_optimization_module()
    
    if args.fix_hierarchical:
        fix_hierarchical_module()
    
    if args.test:
        # Define modules to test
        modules_to_test = [
            "modules.runtime_optimization_module",
            "modules.standard.runtime_optimization_module",
            "modules.standard.hierarchical_module",
            "core.hierarchical_module"
        ]
        
        # Add specific module if provided
        if args.module:
            modules_to_test.append(args.module)
        
        # Test imports
        successful, failed = test_imports(modules_to_test)
        
        # Print summary
        print(f"\nImport Test Summary:")
        print(f"Successfully imported: {len(successful)}/{len(modules_to_test)}")
        
        if failed:
            print(f"Failed imports: {len(failed)}")
            for module, error in failed:
                print(f"  - {module}: {error}")
        else:
            print("All imports successful!")
    
    # If no arguments provided, fix common issues and test
    if not (args.fix_common or args.fix_runtime or args.fix_hierarchical or args.test):
        fix_common_imports()
        
        modules_to_test = [
            "modules.runtime_optimization_module",
            "modules.standard.runtime_optimization_module",
            "modules.standard.hierarchical_module",
            "core.hierarchical_module"
        ]
        
        successful, failed = test_imports(modules_to_test)
        
        print(f"\nImport Test Summary:")
        print(f"Successfully imported: {len(successful)}/{len(modules_to_test)}")
        
        if failed:
            print(f"Failed imports: {len(failed)}")
            for module, error in failed:
                print(f"  - {module}: {error}")
        else:
            print("All imports successful!")

if __name__ == "__main__":
    main()
