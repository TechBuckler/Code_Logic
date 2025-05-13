"""
Import Utility Module

Provides a centralized system for handling imports across the codebase,
supporting both the old and new directory structures during transition.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import inspect
import importlib.util

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions

# Directory mappings from old to new structure
DIRECTORY_MAPPING = {
    # Core components
    'src/ast_explorer.py': 'core/ast',
    'src/ir_model.py': 'core/ir',
    'src/proof_engine.py': 'core/proof',
    'src/optimizer.py': 'core/optimization',
    'src/exporter.py': 'core/export',
    
    # Modules
    'src/modules': 'modules',
    
    # UI components
    'src/unified_ui.py': 'ui',
    'src/ui_renderers.py': 'ui/renderers',
    'src/ui_utils.py': 'ui/components',
    
    # Utilities
    'src/file_utils.py': 'utils/file',
    'src/runtime_utils.py': 'utils/runtime',
    
    # Tools
    'shadow_tree.py': 'tools/shadow_tree',
    'fractal_organizer.py': 'tools/fractal',
    'resource_splitter.py': 'tools/resource',
}

# Module mappings from old import paths to new import paths
MODULE_MAPPING = {
    'src.ast_explorer': 'core.ast.explorer',
    'src.ir_model': 'core.ir.model',
    'src.proof_engine': 'core.proof.engine',
    'src.optimizer': 'core.optimization.optimizer',
    'src.exporter': 'core.export.exporter',
    'src.module_system': 'modules.system',
    'src.background_system': 'modules.background',
    'src.unified_ui': 'ui.unified',
    'src.ui_renderers': 'ui.renderers.base',
    'src.ui_utils': 'ui.components.utils',
    'shadow_tree': 'tools.shadow_tree.navigator',
    'fractal_organizer': 'tools.fractal.organizer',
    'resource_splitter': 'tools.resource.splitter',
}

def import_module(module_path, fallback_paths=None):
    """
    Import a module using its path, handling both old and new directory structures.
    
    Args:
        module_path: The module path to import (e.g., 'src.ast_explorer')
        fallback_paths: List of fallback paths to try if the main path fails
        
    Returns:
        The imported module or None if import fails
    """
    # Try the direct import first
    try:
        return importlib.import_module(module_path)
    except ImportError as e:
        print(f"Direct import of {module_path} failed: {e}")
        
        # Try the new path if it exists in the mapping
        if module_path in MODULE_MAPPING:
            try:
                new_path = MODULE_MAPPING[module_path]
                print(f"Trying mapped path: {new_path}")
                return importlib.import_module(new_path)
            except ImportError as e:
                print(f"Mapped import of {new_path} failed: {e}")
        
        # Try fallback paths
        if fallback_paths:
            for path in fallback_paths:
                try:
                    print(f"Trying fallback path: {path}")
                    return importlib.import_module(path)
                except ImportError:
                    continue
    
    return None

def import_from_file(file_path, module_name=None):
    """
    Import a module directly from a file path.
    
    Args:
        file_path: Path to the Python file
        module_name: Name to give the module (defaults to filename without extension)
        
    Returns:
        The imported module or None if import fails
    """
    if module_name is None:
        module_name = os.path.basename(file_path).replace('.py', '')
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            return None
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error importing {module_name} from {file_path}: {e}")
        return None

def get_module_path(module_name, old_structure=True):
    """
    Get the file path for a module.
    
    Args:
        module_name: Name of the module (e.g., 'ast_explorer')
        old_structure: Whether to look in the old structure first
        
    Returns:
        Path to the module file or None if not found
    """
    # Define search paths based on priority
    search_paths = []
    
    if old_structure:
        # Old structure paths
        search_paths.extend([
            join_paths(project_root, f"{module_name}.py"),
            join_paths(project_root, "src", f"{module_name}.py"),
            join_paths(project_root, "src", "modules", f"{module_name}_module.py")
        ])
    
    # New structure paths
    for old_path, new_dir in DIRECTORY_MAPPING.items():
        if module_name in old_path:
            search_paths.append(join_paths(project_root, new_dir, f"{module_name}.py"))
    
    # Try all paths
    for path in search_paths:
        if os.path.exists(path):
            return path
    
    return None

def get_function_source(func):
    """
    Get the source code of a function.
    
    Args:
        func: The function object
        
    Returns:
        Source code as a string or None if retrieval fails
    """
    try:
        return inspect.getsource(func)
    except Exception as e:
        print(f"Error getting source for function {func.__name__}: {e}")
        return None

def register_module(module_path, new_module_path):
    """
    Register a new module mapping.
    
    Args:
        module_path: Original module path
        new_module_path: New module path
    """
    MODULE_MAPPING[module_path] = new_module_path

def register_directory(directory_path, new_directory_path):
    """
    Register a new directory mapping.
    
    Args:
        directory_path: Original directory path
        new_directory_path: New directory path
    """
    DIRECTORY_MAPPING[directory_path] = new_directory_path
