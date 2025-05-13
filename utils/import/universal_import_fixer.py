#!/usr/bin/env python
"""
Universal Import Fixer

A dynamic tool that fixes import issues by creating a universal import system
that can find modules regardless of their location in the codebase.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import importlib
import types
import inspect
import re
import ast
from concurrent.futures import ThreadPoolExecutor

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

class ModuleMapper:
    """Maps modules and classes across the codebase."""
    
    def __init__(self, root_dir=None):
        """Initialize with the root directory."""
        self.root_dir = root_dir or PROJECT_ROOT
        self.module_map = {}  # Maps module names to file paths
        self.class_map = {}   # Maps class names to module paths
        self.function_map = {}  # Maps function names to module paths
        self.import_aliases = {}  # Maps old import paths to new ones
        
    def scan_codebase(self, max_workers=4):
        """Scan the entire codebase to build the module and class maps."""
        print(f"🔍 Scanning codebase at {self.root_dir}...")
        
        # Get all Python files
        python_files = []
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self._process_file, python_files)
        
        print(f"✅ Found {len(self.module_map)} modules, {len(self.class_map)} classes, and {len(self.function_map)} functions")
        
    def _process_file(self, file_path):
        """Process a Python file to extract module, class, and function information."""
        rel_path = os.path.relpath(file_path, self.root_dir)
        
        # Skip __pycache__ and virtual environments
        if '__pycache__' in rel_path or 'venv' in rel_path:
            return
        
        # Convert file path to potential module path
        module_path = self._file_to_module_path(file_path)
        if module_path:
            self.module_map[module_path] = file_path
            
            # Extract class and function definitions
            self._extract_definitions(file_path, module_path)
    
    def _file_to_module_path(self, file_path):
        """Convert a file path to a module path."""
        rel_path = os.path.relpath(file_path, self.root_dir)
        
        # Handle __init__.py files
        if os.path.basename(file_path) == '__init__.py':
            rel_path = os.path.dirname(rel_path)
        else:
            # Remove .py extension
            rel_path = os.path.splitext(rel_path)[0]
        
        # Convert path separators to dots
        module_path = rel_path.replace(os.path.sep, '.')
        
        return module_path
    
    def _extract_definitions(self, file_path, module_path):
        """Extract class and function definitions from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                # Parse the file with ast
                tree = ast.parse(content)
                
                # Extract class definitions
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        class_name = node.name
                        self.class_map[class_name] = module_path
                    elif isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        self.function_map[func_name] = module_path
            except SyntaxError:
                # Fall back to regex for files with syntax errors
                class_pattern = r'class\s+(\w+)'
                for match in re.finditer(class_pattern, content):
                    class_name = match.group(1)
                    self.class_map[class_name] = module_path
                
                func_pattern = r'def\s+(\w+)'
                for match in re.finditer(func_pattern, content):
                    func_name = match.group(1)
                    self.function_map[func_name] = module_path
        except Exception as e:
            print(f"Warning: Error extracting definitions from {file_path}: {e}")
    
    def find_module(self, name):
        """Find a module by name, trying various paths."""
        # Direct match
        if name in self.module_map:
            return name
        
        # Try different prefixes
        prefixes = ['', 'core.', 'modules.', 'modules.standard.', 'tools.', 'utils.']
        for prefix in prefixes:
            try_name = prefix + name
            if try_name in self.module_map:
                return try_name
        
        # Try different suffixes
        suffixes = ['', '.core', '.utils', '.main']
        for suffix in suffixes:
            try_name = name + suffix
            if try_name in self.module_map:
                return try_name
        
        # Try combinations
        for prefix in prefixes:
            for suffix in suffixes:
                try_name = prefix + name + suffix
                if try_name in self.module_map:
                    return try_name
        
        return None
    
    def find_class(self, name):
        """Find a class by name."""
        if name in self.class_map:
            return self.class_map[name]
        return None
    
    def find_function(self, name):
        """Find a function by name."""
        if name in self.function_map:
            return self.function_map[name]
        return None
    
    def create_import_aliases(self):
        """Create import aliases for common modules."""
        # Map old import paths to new ones
        common_modules = [
            'module_system',
            'background_system',
            'hierarchical_module',
            'simple_hierarchical_core',
            'shadow_tree',
            'navigator',
            'state_manager',
            'import_utils',
            'file_operations',
            'path_utils',
            'string_utils',
            'json_utils',
            'unified',
        ]
        
        for module_name in common_modules:
            # Find the module
            module_path = self.find_module(module_name)
            if module_path:
                # Create aliases for common import paths
                if module_name == 'hierarchical_module':
                    self.import_aliases['core.hierarchical_module'] = module_path
                    self.import_aliases['modules.standard.hierarchical_module'] = module_path
                    self.import_aliases['hierarchical_module'] = module_path
                elif module_name == 'simple_hierarchical_core':
                    self.import_aliases['core.simple_hierarchical_core'] = module_path
                    self.import_aliases['modules.standard.simple_hierarchical_core'] = module_path
                    self.import_aliases['simple_hierarchical_core'] = module_path
                elif module_name == 'shadow_tree':
                    self.import_aliases['tools.shadow_tree'] = module_path
                    self.import_aliases['shadow_tree'] = module_path
                elif module_name == 'navigator':
                    self.import_aliases['tools.shadow_tree.navigator'] = module_path
                    self.import_aliases['shadow_tree.navigator'] = module_path
                elif module_name == 'state_manager':
                    self.import_aliases['core.state_manager'] = module_path
                    self.import_aliases['state_manager'] = module_path
                else:
                    # Create generic aliases
                    self.import_aliases[module_name] = module_path
                    
                    # Try to guess common locations
                    if module_name.endswith('_utils'):
                        base_name = module_name[:-6]  # Remove _utils
                        self.import_aliases[f'utils.{base_name}'] = module_path
                        self.import_aliases[f'utils.{base_name}.utils'] = module_path
        
        print(f"✅ Created {len(self.import_aliases)} import aliases")

class UniversalImportFixer:
    """Fixes import issues by creating a universal import system."""
    
    def __init__(self, mapper=None):
        """Initialize with a module mapper."""
        self.mapper = mapper or ModuleMapper()
        if not self.mapper.module_map:
            self.mapper.scan_codebase()
            self.mapper.create_import_aliases()
        
        self.fixed_modules = set()
        self.proxy_modules = {}
    
    def create_proxy_module(self, name):
        """Create a proxy module that can be imported from any path."""
        # Skip if already created
        if name in self.proxy_modules:
            return self.proxy_modules[name]
        
        # Find the actual module
        actual_module_path = None
        if name in self.mapper.import_aliases:
            actual_module_path = self.mapper.import_aliases[name]
        else:
            actual_module_path = self.mapper.find_module(name)
        
        if not actual_module_path:
            return None
        
        # Try to import the actual module
        try:
            actual_module = importlib.import_module(actual_module_path)
        except ImportError:
            return None
        
        # Create a proxy module
        proxy = types.ModuleType(name)
        
        # Copy all attributes from the actual module
        for attr_name in dir(actual_module):
            if not attr_name.startswith('_'):  # Skip private attributes
                try:
                    setattr(proxy, attr_name, getattr(actual_module, attr_name))
                except (AttributeError, ImportError):
                    pass
        
        # Store the proxy module
        self.proxy_modules[name] = proxy
        
        return proxy
    
    def fix_import_system(self):
        """Patch the import system to use our universal import fixer."""
        print("🔧 Patching import system...")
        
        # Store the original __import__ function
        try:
            # Handle different ways __builtins__ might be exposed
            if isinstance(__builtins__, dict):
                original_import = __builtins__['__import__']
            else:
                original_import = __builtins__.__import__
        except (AttributeError, TypeError):
            # Fall back to the built-in __import__
            original_import = __import__
        
        # Define our custom import function
        def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
            # For relative imports, use the original import
            if level != 0:
                return original_import(name, globals, locals, fromlist, level)
            
            try:
                # Try the original import first
                return original_import(name, globals, locals, fromlist, level)
            except ImportError as e:
                # If that fails, try our proxy system
                if name in self.mapper.import_aliases:
                    actual_name = self.mapper.import_aliases[name]
                    try:
                        module = importlib.import_module(actual_name)
                        
                        # If fromlist is specified, make sure those attributes are available
                        if fromlist:
                            for attr in fromlist:
                                if not hasattr(module, attr):
                                    # Try to find the class or function
                                    if attr in self.mapper.class_map:
                                        class_module_path = self.mapper.class_map[attr]
                                        try:
                                            class_module = importlib.import_module(class_module_path)
                                            if hasattr(class_module, attr):
                                                setattr(module, attr, getattr(class_module, attr))
                                        except ImportError:
                                            pass
                                    elif attr in self.mapper.function_map:
                                        func_module_path = self.mapper.function_map[attr]
                                        try:
                                            func_module = importlib.import_module(func_module_path)
                                            if hasattr(func_module, attr):
                                                setattr(module, attr, getattr(func_module, attr))
                                        except ImportError:
                                            pass
                        
                        return module
                    except ImportError:
                        pass
                
                # Try to create a proxy module
                proxy = self.create_proxy_module(name)
                if proxy:
                    # If fromlist is specified, make sure those attributes are available
                    if fromlist:
                        for attr in fromlist:
                            if not hasattr(proxy, attr):
                                # Try to find the class or function
                                if attr in self.mapper.class_map:
                                    class_module_path = self.mapper.class_map[attr]
                                    try:
                                        class_module = importlib.import_module(class_module_path)
                                        if hasattr(class_module, attr):
                                            setattr(proxy, attr, getattr(class_module, attr))
                                    except ImportError:
                                        pass
                                elif attr in self.mapper.function_map:
                                    func_module_path = self.mapper.function_map[attr]
                                    try:
                                        func_module = importlib.import_module(func_module_path)
                                        if hasattr(func_module, attr):
                                            setattr(proxy, attr, getattr(func_module, attr))
                                    except ImportError:
                                        pass
                    
                    return proxy
                
                # If all else fails, raise the original ImportError
                raise e
        
        # Replace the built-in __import__ with our custom one
        try:
            # Handle different ways __builtins__ might be exposed
            if isinstance(__builtins__, dict):
                __builtins__['__import__'] = custom_import
            else:
                __builtins__.__import__ = custom_import
        except (AttributeError, TypeError):
            # Fall back to using sys.modules
            import builtins
            builtins.__import__ = custom_import
        
        print("✅ Import system patched")
    
    def fix_imports_in_file(self, file_path, dry_run=False):
        """Fix imports in a Python file."""
        if file_path in self.fixed_modules:
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find import statements
            import_pattern = r'^(?:from\s+([\w.]+)\s+import\s+(?:[\w,\s]+)|import\s+([\w.]+))(?:\s+as\s+\w+)?$'
            imports = []
            for line in content.split('\n'):
                match = re.match(import_pattern, line.strip())
                if match:
                    module_name = match.group(1) or match.group(2)
                    imports.append(module_name)
            
            # Check each import
            fixed_imports = []
            modified = False
            
            for module_name in imports:
                # Skip if already in our aliases
                if module_name in self.mapper.import_aliases:
                    continue
                
                # Try to find an alternative
                alternative = self.mapper.find_module(module_name)
                if alternative and alternative != module_name:
                    # Add to our aliases
                    self.mapper.import_aliases[module_name] = alternative
                    
                    if not dry_run:
                        # Replace the import in the file
                        old_import = f"from {module_name} import"
                        new_import = f"from {alternative} import"
                        if old_import in content:
                            content = content.replace(old_import, new_import)
                            modified = True
                        
                        old_import = f"import {module_name}"
                        new_import = f"import {alternative}"
                        if old_import in content:
                            content = content.replace(old_import, new_import)
                            modified = True
                    
                    fixed_imports.append((module_name, alternative))
            
            # Write the updated content back to the file
            if modified and not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_modules.add(file_path)
            
            return fixed_imports
        except Exception as e:
            print(f"Warning: Error fixing imports in {file_path}: {e}")
            return []
    
    def fix_all_imports(self, dry_run=False):
        """Fix imports in all Python files."""
        print(f"{'🔍 Analyzing' if dry_run else '🔧 Fixing'} imports in all Python files...")
        
        # Get all Python files
        python_files = []
        for root, _, files in os.walk(self.mapper.root_dir):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        # Fix imports in each file
        fixed_count = 0
        for file_path in python_files:
            fixed_imports = self.fix_imports_in_file(file_path, dry_run)
            if fixed_imports:
                fixed_count += 1
                rel_path = os.path.relpath(file_path, self.mapper.root_dir)
                print(f"  {'🔍' if dry_run else '✓'} {rel_path}: {len(fixed_imports)} imports {'would be' if dry_run else 'were'} fixed")
                for old, new in fixed_imports:
                    print(f"    {old} -> {new}")
        
        print(f"{'🔍 Analysis' if dry_run else '✅ Fixing'} complete: {fixed_count} files {'would be' if dry_run else 'were'} modified")
    
    def fix_critical_modules(self, dry_run=False):
        """Fix imports in critical modules only."""
        print(f"{'🔍 Analyzing' if dry_run else '🔧 Fixing'} imports in critical modules...")
        
        # List of critical modules to fix
        critical_modules = [
            # Core modules
            "core/simple_hierarchical_core.py",
            "core/hierarchical_module.py",
            "core/state_manager.py",
            
            # Module system
            "module_system.py",
            "background_system.py",
            
            # Shadow Tree
            "tools/shadow_tree/navigator.py",
            
            # Utils
            "utils/import_utils.py",
            "utils/file/operations.py",
            
            # UI
            "ui/unified.py"
        ]
        
        # Fix imports in each critical module
        fixed_count = 0
        for module_path in critical_modules:
            full_path = os.path.join(self.mapper.root_dir, module_path)
            if os.path.exists(full_path):
                fixed_imports = self.fix_imports_in_file(full_path, dry_run)
                if fixed_imports:
                    fixed_count += 1
                    print(f"  {'🔍' if dry_run else '✓'} {module_path}: {len(fixed_imports)} imports {'would be' if dry_run else 'were'} fixed")
                    for old, new in fixed_imports:
                        print(f"    {old} -> {new}")
            else:
                print(f"  ! Module not found: {module_path}")
        
        print(f"{'🔍 Analysis' if dry_run else '✅ Fixing'} complete: {fixed_count} critical modules {'would be' if dry_run else 'were'} modified")

def create_missing_modules():
    """Create missing modules that are commonly needed."""
    print("🔧 Creating missing modules...")
    
    # List of modules to create if missing
    missing_modules = [
        # Core modules
        {
            'name': 'modules.code_analysis_module',
            'classes': [
                {
                    'name': 'CodeAnalysisModule',
                    'attributes': ['name', 'parent', 'children']
                }
            ]
        },
        # Hierarchical Module
        {
            'name': 'modules.standard.hierarchical_module',
            'classes': [
                {
                    'name': 'HierarchicalModule',
                    'attributes': ['name', 'parent', 'children', 'event_bus', 'shared_state'],
                    'special': 'hierarchical_module'
                }
            ]
        },
        # State Manager
        {
            'name': 'core.state_manager',
            'classes': [
                {
                    'name': 'StateManager',
                    'attributes': ['_event_bus', '_shared_state'],
                    'special': 'state_manager'
                },
                {
                    'name': 'EventBus',
                    'attributes': ['listeners'],
                    'special': 'event_bus'
                },
                {
                    'name': 'SharedState',
                    'attributes': ['state'],
                    'special': 'shared_state'
                }
            ]
        }
    ]
    
    # Create each missing module
    for module_info in missing_modules:
        module_name = module_info['name']
        if module_name not in sys.modules:
            # Create the module
            module = types.ModuleType(module_name)
            
            # Create classes
            for class_info in module_info['classes']:
                class_name = class_info['name']
                attributes = class_info['attributes']
                special_type = class_info.get('special', None)
                
                # Handle special cases
                if special_type == 'hierarchical_module':
                    # First, check if the file exists and try to use it
                    hier_module_path = os.path.join(PROJECT_ROOT, 'modules', 'standard', 'hierarchical_module.py')
                    if os.path.exists(hier_module_path):
                        try:
                            # Try to import directly from the file
                            import importlib.util
                            spec = importlib.util.spec_from_file_location('hierarchical_module', hier_module_path)
                            hier_module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(hier_module)
                            
                            # Get the HierarchicalModule class
                            if hasattr(hier_module, 'HierarchicalModule'):
                                HierarchicalModule = hier_module.HierarchicalModule
                                setattr(module, class_name, HierarchicalModule)
                                print(f"    Using existing HierarchicalModule from {hier_module_path}")
                                
                                # Make it available from core for backward compatibility
                                sys.modules['core.hierarchical_module'] = module
                                continue
                        except Exception as e:
                            print(f"    Warning: Error importing existing HierarchicalModule: {e}")
                    
                    # If we couldn't import from the file, create a minimal version
                    # Try to import Module from module_system
                    try:
                        from module_system import Module
                    except ImportError:
                        # Define a minimal Module class
                        class Module:
                            def __init__(self, name):
                                self.name = name
                                self.dependencies = []
                                self.active = False
                    
                    # Define HierarchicalModule class
                    class HierarchicalModule(Module):
                        def __init__(self, name, parent=None):
                            super().__init__(name)
                            self.parent = parent
                            self.children = {}  # name -> module
                            
                            # Get event_bus and shared_state from state_manager if available
                            try:
                                from core.state_manager import StateManager
                                state_manager = StateManager()
                                self.event_bus = state_manager.get_event_bus()
                                self.shared_state = state_manager.get_shared_state()
                            except ImportError:
                                self.event_bus = None
                                self.shared_state = None
                            
                            # Register with parent if provided
                            if parent:
                                parent.add_child(self)
                        
                        def add_child(self, module):
                            """Add a child module"""
                            self.children[module.name] = module
                            return self
                        
                        def remove_child(self, name):
                            """Remove a child module by name"""
                            if name in self.children:
                                del self.children[name]
                            return self
                        
                        def get_child(self, name):
                            """Get a child module by name"""
                            return self.children.get(name)
                        
                        def get_path(self):
                            """Get the path from the root to this module"""
                            if self.parent:
                                return self.parent.get_path() + [self.name]
                            return [self.name]
                            
                        def get_full_name(self):
                            """Get the full name including the path"""
                            return ".".join(self.get_path())
                    
                    # Add the class to the module
                    setattr(module, class_name, HierarchicalModule)
                    
                    # Also make it available from core for backward compatibility
                    sys.modules['core.hierarchical_module'] = module
                    
                elif special_type == 'state_manager':
                    # Define StateManager class
                    class StateManager:
                        def __init__(self):
                            self._event_bus = EventBus()
                            self._shared_state = SharedState()
                        
                        def get_event_bus(self):
                            return self._event_bus
                        
                        def get_shared_state(self):
                            return self._shared_state
                    
                    # Add the class to the module
                    setattr(module, class_name, StateManager)
                    
                elif special_type == 'event_bus':
                    # Define EventBus class
                    class EventBus:
                        def __init__(self):
                            self.listeners = {}
                        
                        def subscribe(self, event_type, callback):
                            if event_type not in self.listeners:
                                self.listeners[event_type] = []
                            self.listeners[event_type].append(callback)
                        
                        def publish(self, event):
                            if event.event_type in self.listeners:
                                for callback in self.listeners[event.event_type]:
                                    callback(event)
                    
                    # Add the class to the module
                    setattr(module, class_name, EventBus)
                    
                elif special_type == 'shared_state':
                    # Define SharedState class
                    class SharedState:
                        def __init__(self):
                            self.state = {}
                        
                        def set(self, key, value):
                            self.state[key] = value
                        
                        def get(self, key, default=None):
                            return self.state.get(key, default)
                    
                    # Add the class to the module
                    setattr(module, class_name, SharedState)
                    
                else:
                    # Create a dynamic class with the specified attributes
                    attrs = {}
                    for attr in attributes:
                        attrs[attr] = None
                    
                    # Create __init__ method
                    def create_init(attrs):
                        def __init__(self, **kwargs):
                            for attr in attrs:
                                setattr(self, attr, kwargs.get(attr))
                        return __init__
                    
                    # Create the class
                    cls = type(class_name, (), {'__init__': create_init(attributes)})
                    
                    # Add the class to the module
                    setattr(module, class_name, cls)
            
            # Add to sys.modules
            sys.modules[module_name] = module
            print(f"  ✓ Created missing module: {module_name}")
    
    print("✅ Missing modules created")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Import Fixer")
    parser.add_argument("--scan", action="store_true", help="Scan the codebase")
    parser.add_argument("--fix", action="store_true", help="Fix imports in all Python files")
    parser.add_argument("--fix-critical", action="store_true", help="Fix imports in critical modules only")
    parser.add_argument("--patch", action="store_true", help="Patch the import system")
    parser.add_argument("--create-missing", action="store_true", help="Create missing modules")
    parser.add_argument("--dry-run", action="store_true", help="Don't modify files, just report issues")
    
    args = parser.parse_args()
    
    # Create the mapper and fixer
    mapper = ModuleMapper()
    fixer = UniversalImportFixer(mapper)
    
    if args.scan or args.fix or args.fix_critical or args.patch or args.create_missing:
        if args.scan or args.fix or args.fix_critical:
            mapper.scan_codebase()
            mapper.create_import_aliases()
        if args.create_missing:
            create_missing_modules()
        if args.patch:
            fixer.fix_import_system()
        if args.fix_critical:
            fixer.fix_critical_modules(args.dry_run)
        if args.fix:
            fixer.fix_all_imports(args.dry_run)
    else:
        # Default: scan, create missing modules, patch, and fix critical modules
        mapper.scan_codebase()
        mapper.create_import_aliases()
        create_missing_modules()
        fixer.fix_import_system()
        fixer.fix_critical_modules(False)

if __name__ == "__main__":
    main()
