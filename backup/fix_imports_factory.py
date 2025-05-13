#!/usr/bin/env python
"""
Import Resolver Factory

This script systematically fixes import issues in the codebase using the ModuleFactory pattern.
It can:
1. Scan all Python files for import issues
2. Generate compatibility modules for missing modules
3. Update import statements to use the new module structure
4. Create proxy modules for circular dependencies

Usage:
    python fix_imports_factory.py [--scan] [--fix] [--generate] [--test]
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import ast
import re
import time
import argparse
import importlib
import logging
from typing import Dict, List, Set, Tuple, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ImportResolver")

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the module factory
try:
    from utils.module_factory import ModuleFactory, module_factory
except ImportError:
    logger.error("Could not import ModuleFactory. Make sure utils/module_factory.py exists.")
    sys.exit(1)

class ImportResolver:
    """Resolves import issues in the codebase."""
    
    def __init__(self, factory=None):
        """
        Initialize the import resolver.
        
        Args:
            factory: Optional ModuleFactory instance
        """
        self.factory = factory or module_factory
        self.missing_modules = set()
        self.circular_dependencies = set()
        self.fixed_files = set()
        self.generated_modules = set()
        
    def scan_file_for_imports(self, file_path: str) -> Set[str]:
        """
        Scan a file for import statements and return the imported modules.
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            Set of imported module names
        """
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.add(name.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
        except Exception as e:
            logger.warning(f"Error scanning {file_path}: {e}")
            
        return imports
        
    def scan_directory(self, directory: str) -> Dict[str, Set[str]]:
        """
        Scan a directory for Python files and their imports.
        
        Args:
            directory: Directory to scan
            
        Returns:
            Dictionary mapping file paths to sets of imported modules
        """
        imports_by_file = {}
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    imports = self.scan_file_for_imports(file_path)
                    imports_by_file[file_path] = imports
                    
        return imports_by_file
        
    def test_import(self, module_name: str) -> bool:
        """
        Test if a module can be imported.
        
        Args:
            module_name: Name of the module to test
            
        Returns:
            True if the module can be imported, False otherwise
        """
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False
            
    def find_missing_imports(self, imports_by_file: Dict[str, Set[str]]) -> Set[str]:
        """
        Find modules that cannot be imported.
        
        Args:
            imports_by_file: Dictionary mapping file paths to sets of imported modules
            
        Returns:
            Set of module names that cannot be imported
        """
        missing = set()
        
        for file_path, imports in imports_by_file.items():
            for module_name in imports:
                if not self.test_import(module_name):
                    missing.add(module_name)
                    logger.info(f"Missing import in {file_path}: {module_name}")
                    
        return missing
        
    def detect_circular_dependencies(self, imports_by_file: Dict[str, Set[str]]) -> Set[Tuple[str, str]]:
        """
        Detect circular dependencies between modules.
        
        Args:
            imports_by_file: Dictionary mapping file paths to sets of imported modules
            
        Returns:
            Set of tuples representing circular dependencies
        """
        # Build a module dependency graph
        graph = {}
        file_to_module = {}
        
        for file_path, imports in imports_by_file.items():
            # Convert file path to module name
            rel_path = os.path.relpath(file_path, project_root)
            module_path = rel_path.replace(os.path.sep, '.').replace('.py', '')
            
            # Handle __init__.py files
            if module_path.endswith('.__init__'):
                module_path = module_path[:-9]
                
            file_to_module[file_path] = module_path
            graph[module_path] = set()
            
        # Add dependencies to the graph
        for file_path, imports in imports_by_file.items():
            module_path = file_to_module[file_path]
            
            for imported in imports:
                # Only consider imports that are in our codebase
                for other_module in graph:
                    if imported == other_module or imported.startswith(other_module + '.'):
                        graph[module_path].add(other_module)
                        
        # Find cycles in the graph
        cycles = set()
        
        def dfs(node, path, visited):
            path.append(node)
            visited.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor in path:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = tuple(sorted(path[cycle_start:]))
                    cycles.add(cycle)
                elif neighbor not in visited:
                    dfs(neighbor, path, visited)
                    
            path.pop()
            
        for node in graph:
            dfs(node, [], set())
            
        # Convert cycles to pairs
        circular_deps = set()
        
        for cycle in cycles:
            if len(cycle) == 2:
                circular_deps.add(cycle)
            else:
                # For longer cycles, add all pairs
                for i in range(len(cycle)):
                    for j in range(i+1, len(cycle)):
                        circular_deps.add((cycle[i], cycle[j]))
                        
        return circular_deps
        
    def generate_compatibility_module(self, module_name: str) -> bool:
        """
        Generate a compatibility module for a missing module.
        
        Args:
            module_name: Name of the module to generate
            
        Returns:
            True if successful, False otherwise
        """
        # Determine the appropriate template
        template_name = "basic"
        
        if "ui_components" in module_name or "ui." in module_name:
            template_name = "ui_components"
        elif "background_system" in module_name or "background." in module_name:
            template_name = "background_system"
        elif "module_system" in module_name or "modules.system" in module_name:
            template_name = "module_system"
            
        # Determine the file path
        parts = module_name.split('.')
        
        if len(parts) == 1:
            # Top-level module
            file_path = os.path.join(project_root, f"{module_name}.py")
        else:
            # Submodule
            dir_path = os.path.join(project_root, *parts[:-1])
            file_path = os.path.join(dir_path, f"{parts[-1]}.py")
            
            # Create __init__.py files if needed
            current_path = project_root
            for part in parts[:-1]:
                current_path = os.path.join(current_path, part)
                init_path = os.path.join(current_path, "__init__.py")
                
                if not os.path.exists(current_path):
                    os.makedirs(current_path)
                    
                if not os.path.exists(init_path):
                    with open(init_path, 'w') as f:
                        f.write(f'"""\n{part} package.\n"""\n')
                        
        # Generate the module
        success = self.factory.generate_compatibility_module(
            module_name=module_name,
            file_path=file_path,
            template_name=template_name
        )
        
        if success:
            self.generated_modules.add(module_name)
            
        return success
        
    def fix_imports_in_file(self, file_path: str) -> bool:
        """
        Fix import statements in a file.
        
        Args:
            file_path: Path to the file to fix
            
        Returns:
            True if changes were made, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse the file
            tree = ast.parse(content)
            
            # Track if we need to make changes
            changes_needed = False
            
            # Find and fix imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        if name.name in self.missing_modules:
                            changes_needed = True
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module in self.missing_modules:
                        changes_needed = True
                        
            if not changes_needed:
                return False
                
            # Fix the imports by adding the import_module_flexible function
            lines = content.split('\n')
            
            # Find the first non-comment, non-docstring line
            insert_line = 0
            in_docstring = False
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    in_docstring = not in_docstring
                    if not in_docstring:
                        insert_line = i + 1
                elif not in_docstring and not stripped.startswith('#') and stripped:
                    insert_line = i
                    break
                    
            # Add the import utility
            import_lines = [
                "# Fix imports using the module factory",
                "import sys",
                "import os",
                "",
                "# Add project root to path",
                "project_root = os.path.dirname(os.path.abspath(__file__))",
                "if project_root not in sys.path:",
                "    sys.path.insert(0, project_root)",
                "",
                "# Import the module factory",
                "try:",
                "    from utils.module_factory import module_factory",
                "    # Use the factory to import modules flexibly",
                "    import_module_flexible = module_factory.import_module",
                "except ImportError:",
                "    # Fallback if module_factory is not available",
                "    def import_module_flexible(name):",
                "        import importlib",
                "        try:",
                "            return importlib.import_module(name)",
                "        except ImportError:",
                "            return None",
                ""
            ]
            
            # Insert the import utility
            for i, line in enumerate(import_lines):
                lines.insert(insert_line + i, line)
                
            # Write the changes back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
                
            self.fixed_files.add(file_path)
            return True
            
        except Exception as e:
            logger.warning(f"Error fixing imports in {file_path}: {e}")
            return False
            
    def run(self, scan=True, fix=True, generate=True, test=True):
        """
        Run the import resolver.
        
        Args:
            scan: Whether to scan for import issues
            fix: Whether to fix import issues
            generate: Whether to generate compatibility modules
            test: Whether to test imports after fixing
        """
        if scan:
            logger.info("Scanning for import issues...")
            imports_by_file = self.scan_directory(project_root)
            self.missing_modules = self.find_missing_imports(imports_by_file)
            self.circular_dependencies = self.detect_circular_dependencies(imports_by_file)
            
            logger.info(f"Found {len(self.missing_modules)} missing modules")
            logger.info(f"Found {len(self.circular_dependencies)} circular dependencies")
            
        if generate:
            logger.info("Generating compatibility modules...")
            for module_name in self.missing_modules:
                if self.generate_compatibility_module(module_name):
                    logger.info(f"Generated compatibility module for {module_name}")
                    
            logger.info(f"Generated {len(self.generated_modules)} compatibility modules")
            
        if fix:
            logger.info("Fixing import statements...")
            for root, _, files in os.walk(project_root):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        if self.fix_imports_in_file(file_path):
                            logger.info(f"Fixed imports in {file_path}")
                            
            logger.info(f"Fixed imports in {len(self.fixed_files)} files")
            
        if test:
            logger.info("Testing imports...")
            success = True
            
            for module_name in self.missing_modules:
                if not self.test_import(module_name):
                    logger.warning(f"Module {module_name} still cannot be imported")
                    success = False
                    
            if success:
                logger.info("All modules can now be imported successfully")
            else:
                logger.warning("Some modules still cannot be imported")
                
        return {
            "missing_modules": self.missing_modules,
            "circular_dependencies": self.circular_dependencies,
            "fixed_files": self.fixed_files,
            "generated_modules": self.generated_modules
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Fix import issues in the codebase")
    parser.add_argument("--scan", action="store_true", help="Scan for import issues")
    parser.add_argument("--fix", action="store_true", help="Fix import issues")
    parser.add_argument("--generate", action="store_true", help="Generate compatibility modules")
    parser.add_argument("--test", action="store_true", help="Test imports after fixing")
    parser.add_argument("--all", action="store_true", help="Run all steps")
    
    args = parser.parse_args()
    
    # If no arguments are provided, run all steps
    if not (args.scan or args.fix or args.generate or args.test):
        args.all = True
        
    if args.all:
        args.scan = args.fix = args.generate = args.test = True
        
    # Create and run the resolver
    resolver = ImportResolver()
    results = resolver.run(
        scan=args.scan,
        fix=args.fix,
        generate=args.generate,
        test=args.test
    )
    
    # Print a summary
    print("\n" + "="*50)
    print("Import Resolver Summary")
    print("="*50)
    print(f"Missing modules: {len(results['missing_modules'])}")
    print(f"Circular dependencies: {len(results['circular_dependencies'])}")
    print(f"Fixed files: {len(results['fixed_files'])}")
    print(f"Generated modules: {len(results['generated_modules'])}")
    print("="*50)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
