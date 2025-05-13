#!/usr/bin/env python
"""
Dynamic Import Resolver

This tool dynamically scans the entire codebase and builds a map of all modules.
It then uses this map to resolve imports at runtime, adapting to the actual structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import importlib
import time
import re
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

class DynamicImportResolver:
    """Dynamically resolves imports by scanning the codebase structure."""
    
    def __init__(self, root_dir=None):
        """Initialize the resolver with the root directory."""
        self.root_dir = root_dir or PROJECT_ROOT
        self.module_map = {}  # Maps module names to file paths
        self.class_map = {}   # Maps class names to module paths
        self.import_cache = {}  # Cache for successful imports
        self.scan_start_time = None
        
    def scan_codebase(self, max_workers=4):
        """Scan the entire codebase to build the module and class maps."""
        self.scan_start_time = time.time()
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
        
        scan_time = time.time() - self.scan_start_time
        print(f"✅ Scan complete in {scan_time:.3f}s")
        print(f"   Found {len(self.module_map)} modules and {len(self.class_map)} classes")
        
    def _process_file(self, file_path):
        """Process a Python file to extract module and class information."""
        rel_path = os.path.relpath(file_path, self.root_dir)
        
        # Skip __pycache__ and virtual environments
        if '__pycache__' in rel_path or 'venv' in rel_path:
            return
        
        # Convert file path to potential module path
        module_path = self._file_to_module_path(file_path)
        if module_path:
            self.module_map[module_path] = file_path
            
            # Extract class definitions
            self._extract_classes(file_path, module_path)
    
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
    
    def _extract_classes(self, file_path, module_path):
        """Extract class definitions from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple regex to find class definitions
            class_pattern = r'class\s+(\w+)'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                self.class_map[class_name] = module_path
        except Exception as e:
            print(f"Warning: Error extracting classes from {file_path}: {e}")
    
    @lru_cache(maxsize=1024)
    def resolve_import(self, name):
        """Resolve an import by name, trying various paths."""
        # Check if we've already successfully imported this
        if name in self.import_cache:
            return self.import_cache[name]
        
        # Try direct import first
        try:
            module = importlib.import_module(name)
            self.import_cache[name] = module
            return module
        except ImportError:
            pass
        
        # If it's a class name, try to find its module
        if '.' not in name and name in self.class_map:
            module_path = self.class_map[name]
            try:
                module = importlib.import_module(module_path)
                self.import_cache[name] = getattr(module, name)
                return getattr(module, name)
            except (ImportError, AttributeError):
                pass
        
        # Try alternative paths
        parts = name.split('.')
        
        # Try with different prefixes
        prefixes = ['', 'core.', 'modules.', 'modules.standard.', 'tools.', 'utils.']
        for prefix in prefixes:
            try_name = prefix + name
            if try_name in self.module_map:
                try:
                    module = importlib.import_module(try_name)
                    self.import_cache[name] = module
                    return module
                except ImportError:
                    pass
        
        # If it's a multi-part name, try to import the parent and get the attribute
        if len(parts) > 1:
            parent_name = '.'.join(parts[:-1])
            attr_name = parts[-1]
            try:
                parent = self.resolve_import(parent_name)
                if parent and hasattr(parent, attr_name):
                    self.import_cache[name] = getattr(parent, attr_name)
                    return getattr(parent, attr_name)
            except (ImportError, AttributeError):
                pass
        
        # Try all modules for a matching class
        if len(parts) == 1:  # It's a single name, might be a class
            class_name = parts[0]
            for module_path in self.module_map:
                try:
                    module = importlib.import_module(module_path)
                    if hasattr(module, class_name):
                        self.import_cache[name] = getattr(module, class_name)
                        return getattr(module, class_name)
                except ImportError:
                    pass
        
        # If all else fails, raise ImportError
        raise ImportError(f"Cannot import {name}")
    
    def patch_import_system(self):
        """Patch the import system to use our resolver."""
        # Store the original __import__ function
        original_import = __builtins__['__import__']
        
        # Define our custom import function
        def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
            # For relative imports, use the original import
            if level != 0:
                return original_import(name, globals, locals, fromlist, level)
            
            try:
                # Try the original import first
                return original_import(name, globals, locals, fromlist, level)
            except ImportError:
                # If that fails, try our resolver
                if not fromlist:
                    # Import the module itself
                    return self.resolve_import(name)
                else:
                    # Import from the module
                    module = self.resolve_import(name)
                    for attr in fromlist:
                        try:
                            getattr(module, attr)
                        except AttributeError:
                            # Try to find the attribute in our class map
                            if attr in self.class_map:
                                attr_module = self.resolve_import(self.class_map[attr])
                                setattr(module, attr, getattr(attr_module, attr))
                    return module
        
        # Replace the built-in __import__ with our custom one
        __builtins__['__import__'] = custom_import
        
        print("✅ Import system patched to use dynamic resolver")
    
    def fix_imports_in_file(self, file_path):
        """Fix imports in a Python file."""
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
            for module_name in imports:
                try:
                    # Try to resolve the import
                    self.resolve_import(module_name)
                    fixed_imports.append(module_name)
                except ImportError:
                    # If it fails, try to find an alternative
                    for prefix in ['', 'core.', 'modules.', 'modules.standard.', 'tools.', 'utils.']:
                        try_name = prefix + module_name
                        if try_name in self.module_map:
                            # Replace the import in the file
                            old_import = f"from {module_name} import"
                            new_import = f"from {try_name} import"
                            content = content.replace(old_import, new_import)
                            
                            old_import = f"import {module_name}"
                            new_import = f"import {try_name}"
                            content = content.replace(old_import, new_import)
                            
                            fixed_imports.append(try_name)
                            break
            
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return fixed_imports
        except Exception as e:
            print(f"Warning: Error fixing imports in {file_path}: {e}")
            return []

# Create a global instance
resolver = DynamicImportResolver()

def import_module_dynamic(name):
    """Dynamically import a module by name, trying various paths."""
    return resolver.resolve_import(name)

def scan_and_patch():
    """Scan the codebase and patch the import system."""
    resolver.scan_codebase()
    resolver.patch_import_system()

def fix_all_imports():
    """Fix imports in all Python files."""
    print("🔧 Fixing imports in all Python files...")
    
    # Scan the codebase if not already done
    if not resolver.module_map:
        resolver.scan_codebase()
    
    # Get all Python files
    python_files = []
    for root, _, files in os.walk(resolver.root_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    # Fix imports in each file
    fixed_count = 0
    for file_path in python_files:
        fixed_imports = resolver.fix_imports_in_file(file_path)
        if fixed_imports:
            fixed_count += 1
            print(f"  ✓ Fixed imports in {os.path.relpath(file_path, resolver.root_dir)}")
    
    print(f"✅ Fixed imports in {fixed_count} files")

def fix_critical_modules():
    """Fix imports in critical modules only."""
    print("🔧 Fixing imports in critical modules...")
    
    # Scan the codebase if not already done
    if not resolver.module_map:
        resolver.scan_codebase()
    
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
        "shadow_tree.py",
        
        # Utils
        "utils/import_utils.py",
        "utils/file/operations.py",
        "utils/path.py",
        "utils/string.py",
        "utils/data/json_utils.py",
        
        # UI
        "ui/unified.py"
    ]
    
    # Fix imports in each critical module
    fixed_count = 0
    for module_path in critical_modules:
        full_path = os.path.join(resolver.root_dir, module_path)
        if os.path.exists(full_path):
            fixed_imports = resolver.fix_imports_in_file(full_path)
            if fixed_imports:
                fixed_count += 1
                print(f"  ✓ Fixed imports in {module_path}")
        else:
            print(f"  ! Module not found: {module_path}")
    
    print(f"✅ Fixed imports in {fixed_count} critical modules")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Dynamic Import Resolver")
    parser.add_argument("--scan", action="store_true", help="Scan the codebase")
    parser.add_argument("--fix", action="store_true", help="Fix imports in all Python files")
    parser.add_argument("--fix-critical", action="store_true", help="Fix imports in critical modules only")
    parser.add_argument("--patch", action="store_true", help="Patch the import system")
    parser.add_argument("--dry-run", action="store_true", help="Don't modify files, just report issues")
    
    args = parser.parse_args()
    
    if args.scan or args.fix or args.fix_critical or args.patch:
        if args.scan:
            resolver.scan_codebase()
        if args.patch:
            resolver.patch_import_system()
        if args.fix_critical:
            fix_critical_modules()
        if args.fix:
            fix_all_imports()
    else:
        # Default: scan and fix critical modules
        resolver.scan_codebase()
        fix_critical_modules()
