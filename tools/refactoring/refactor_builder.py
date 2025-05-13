#!/usr/bin/env python
"""
Refactor Builder

This module rebuilds optimized Python files from components:
- Combines split files while maintaining functionality
- Optimizes imports and removes unused code
- Ensures proper dependency management
- Generates clean, well-structured code

Part of a 3-file refactoring system:
1. refactor_analyzer.py - Analyzes code and identifies refactoring opportunities
2. refactor_splitter.py - Breaks down complex files and functions
3. refactor_builder.py - Rebuilds optimized files from components
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import ast
import re

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions
try:
except ImportError as e:
    print(f"Error importing utilities: {e}")
    print("Make sure you've run the reorganization scripts first.")
    sys.exit(1)

# Import the analyzer
try:
except ImportError as e:
    print(f"Error importing CodeAnalyzer: {e}")
    print("Make sure refactor_analyzer.py is in the same directory.")
    sys.exit(1)

class ImportOptimizer:
    """Optimizes imports in Python files."""
    
    def __init__(self):
        """Initialize the import optimizer."""
        self.standard_libs = set([
            'abc', 'argparse', 'ast', 'asyncio', 'collections', 'contextlib', 'copy',
            'datetime', 'enum', 'functools', 'glob', 'io', 'itertools', 'json',
            'logging', 'math', 'os', 'pathlib', 'pickle', 're', 'shutil', 'sys',
            'tempfile', 'time', 'traceback', 'typing', 'uuid', 'warnings'
        ])
    
    def optimize_imports(self, content):
        """Optimize imports in a Python file."""
        try:
            # Parse the AST
            tree = ast.parse(content)
            
            # Find all imports
            imports = self._find_imports(tree)
            
            # Find all used names
            used_names = self._find_used_names(tree)
            
            # Filter out unused imports
            used_imports = self._filter_unused_imports(imports, used_names)
            
            # Group imports by type
            grouped_imports = self._group_imports(used_imports)
            
            # Generate optimized import statements
            import_statements = self._generate_import_statements(grouped_imports)
            
            # Replace imports in the original content
            return self._replace_imports(content, tree, import_statements)
        except Exception as e:
            print(f"Error optimizing imports: {e}")
            return content
    
    def _find_imports(self, tree):
        """Find all imports in an AST."""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append({
                        "type": "import",
                        "module": name.name,
                        "name": name.asname or name.name,
                        "asname": name.asname,
                        "lineno": node.lineno,
                        "node": node
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for name in node.names:
                    imports.append({
                        "type": "from",
                        "module": module,
                        "name": name.name,
                        "asname": name.asname,
                        "lineno": node.lineno,
                        "node": node
                    })
        
        return imports
    
    def _find_used_names(self, tree):
        """Find all used names in an AST."""
        used_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                # This could be a module attribute access (e.g., os.path)
                used_names.add(node.value.id)
        
        return used_names
    
    def _filter_unused_imports(self, imports, used_names):
        """Filter out unused imports."""
        used_imports = []
        
        for imp in imports:
            # Check if the import is used
            if imp["name"] in used_names:
                used_imports.append(imp)
            elif imp["type"] == "import" and "." in imp["module"]:
                # Check if any part of the module is used
                parts = imp["module"].split(".")
                for i in range(len(parts)):
                    if ".".join(parts[:i+1]) in used_names:
                        used_imports.append(imp)
                        break
            elif imp["type"] == "from" and imp["asname"] is None:
                # Check if the imported name is used
                if imp["name"] in used_names:
                    used_imports.append(imp)
            elif imp["type"] == "from" and imp["asname"] is not None:
                # Check if the alias is used
                if imp["asname"] in used_names:
                    used_imports.append(imp)
        
        return used_imports
    
    def _group_imports(self, imports):
        """Group imports by type."""
        grouped = {
            "stdlib": [],
            "thirdparty": [],
            "local": []
        }
        
        for imp in imports:
            if imp["type"] == "import":
                module = imp["module"].split(".")[0]
                if module in self.standard_libs:
                    grouped["stdlib"].append(imp)
                elif module.startswith(("src", "utils", "core", "modules", "tools")):
                    grouped["local"].append(imp)
                else:
                    grouped["thirdparty"].append(imp)
            elif imp["type"] == "from":
                module = imp["module"].split(".")[0]
                if module in self.standard_libs:
                    grouped["stdlib"].append(imp)
                elif module.startswith(("src", "utils", "core", "modules", "tools")):
                    grouped["local"].append(imp)
                else:
                    grouped["thirdparty"].append(imp)
        
        return grouped
    
    def _generate_import_statements(self, grouped_imports):
        """Generate optimized import statements."""
        import_statements = []
        
        # Standard library imports
        if grouped_imports["stdlib"]:
            # Group by module
            by_module = defaultdict(list)
            for imp in grouped_imports["stdlib"]:
                if imp["type"] == "import":
                    by_module[imp["module"]].append(imp)
                else:
                    by_module[imp["module"]].append(imp)
            
            # Generate import statements
            for module, imps in sorted(by_module.items()):
                if all(imp["type"] == "import" for imp in imps):
                    # Use 'import module' syntax
                    names = []
                    for imp in imps:
                        if imp["asname"]:
                            names.append(f"{imp['module']} as {imp['asname']}")
                        else:
                            names.append(imp["module"])
                    import_statements.append(f"import {', '.join(sorted(names))}")
                else:
                    # Use 'from module import name' syntax
                    from_imports = [imp for imp in imps if imp["type"] == "from"]
                    if from_imports:
                        names = []
                        for imp in from_imports:
                            if imp["asname"]:
                                names.append(f"{imp['name']} as {imp['asname']}")
                            else:
                                names.append(imp["name"])
                        import_statements.append(f"from {module} import {', '.join(sorted(names))}")
            
            import_statements.append("")  # Add a blank line
        
        # Third-party imports
        if grouped_imports["thirdparty"]:
            # Group by module
            by_module = defaultdict(list)
            for imp in grouped_imports["thirdparty"]:
                if imp["type"] == "import":
                    by_module[imp["module"]].append(imp)
                else:
                    by_module[imp["module"]].append(imp)
            
            # Generate import statements
            for module, imps in sorted(by_module.items()):
                if all(imp["type"] == "import" for imp in imps):
                    # Use 'import module' syntax
                    names = []
                    for imp in imps:
                        if imp["asname"]:
                            names.append(f"{imp['module']} as {imp['asname']}")
                        else:
                            names.append(imp["module"])
                    import_statements.append(f"import {', '.join(sorted(names))}")
                else:
                    # Use 'from module import name' syntax
                    from_imports = [imp for imp in imps if imp["type"] == "from"]
                    if from_imports:
                        names = []
                        for imp in from_imports:
                            if imp["asname"]:
                                names.append(f"{imp['name']} as {imp['asname']}")
                            else:
                                names.append(imp["name"])
                        import_statements.append(f"from {module} import {', '.join(sorted(names))}")
            
            import_statements.append("")  # Add a blank line
        
        # Local imports
        if grouped_imports["local"]:
            # Group by module
            by_module = defaultdict(list)
            for imp in grouped_imports["local"]:
                if imp["type"] == "import":
                    by_module[imp["module"]].append(imp)
                else:
                    by_module[imp["module"]].append(imp)
            
            # Generate import statements
            for module, imps in sorted(by_module.items()):
                if all(imp["type"] == "import" for imp in imps):
                    # Use 'import module' syntax
                    names = []
                    for imp in imps:
                        if imp["asname"]:
                            names.append(f"{imp['module']} as {imp['asname']}")
                        else:
                            names.append(imp["module"])
                    import_statements.append(f"import {', '.join(sorted(names))}")
                else:
                    # Use 'from module import name' syntax
                    from_imports = [imp for imp in imps if imp["type"] == "from"]
                    if from_imports:
                        names = []
                        for imp in from_imports:
                            if imp["asname"]:
                                names.append(f"{imp['name']} as {imp['asname']}")
                            else:
                                names.append(imp["name"])
                        import_statements.append(f"from {module} import {', '.join(sorted(names))}")
        
        return import_statements
    
    def _replace_imports(self, content, tree, import_statements):
        """Replace imports in the original content."""
        # Find the range of lines containing imports
        import_lines = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_lines.add(node.lineno)
        
        if not import_lines:
            # No imports to replace
            return content
        
        # Find the first and last import line
        first_import = min(import_lines)
        last_import = max(import_lines)
        
        # Split the content into lines
        lines = content.splitlines()
        
        # Check if there's a docstring
        has_docstring = False
        docstring_end = 0
        
        if lines and lines[0].strip().startswith('"""'):
            has_docstring = True
            for i, line in enumerate(lines):
                if i > 0 and line.strip().endswith('"""'):
                    docstring_end = i
                    break
        
        # Insert the optimized imports after the docstring or at the beginning
        if has_docstring:
            # Insert after the docstring
            new_lines = lines[:docstring_end+1] + [""] + import_statements + lines[last_import:]
        else:
            # Insert at the beginning
            new_lines = import_statements + lines[last_import:]
        
        return "\n".join(new_lines)

class CodeBuilder:
    """Rebuilds optimized Python files from components."""
    
    def __init__(self, project_root):
        """Initialize the builder."""
        self.project_root = project_root
        self.analyzer = CodeAnalyzer(project_root)
        self.import_optimizer = ImportOptimizer()
    
    def rebuild_from_parts(self, parts_dir, output_file=None, optimize_imports=True, dry_run=True):
        """Rebuild a file from its split parts."""
        # Check if the parts directory exists
        if not os.path.exists(parts_dir) or not os.path.isdir(parts_dir):
            print(f"Parts directory not found: {parts_dir}")
            return None
        
        # Find the __init__.py file
        init_file = os.path.join(parts_dir, "__init__.py")
        if not os.path.exists(init_file):
            print(f"__init__.py not found in {parts_dir}")
            return None
        
        # Read the __init__.py file
        try:
            with open(init_file, 'r', encoding='utf-8') as f:
                init_content = f.read()
        except Exception as e:
            print(f"Error reading {init_file}: {e}")
            return None
        
        # Parse the __init__.py file to find the imports
        imports = []
        for line in init_content.splitlines():
            if line.startswith("from ."):
                # Extract the module name and imported items
                match = re.match(r"from \.([a-zA-Z0-9_]+) import (.+)", line)
                if match:
                    module_name = match.group(1)
                    items = [item.strip() for item in match.group(2).split(",")]
                    imports.append({
                        "module": module_name,
                        "items": items
                    })
        
        # Find all part files
        part_files = []
        for module in imports:
            part_file = os.path.join(parts_dir, f"{module['module']}.py")
            if os.path.exists(part_file):
                part_files.append({
                    "path": part_file,
                    "module": module["module"],
                    "items": module["items"]
                })
            else:
                print(f"Part file not found: {part_file}")
        
        if not part_files:
            print(f"No part files found in {parts_dir}")
            return None
        
        # Determine the output file
        if output_file is None:
            # Use the name of the parts directory
            dir_name = os.path.basename(parts_dir)
            if dir_name.endswith("_parts"):
                output_name = dir_name[:-6] + ".py"
            else:
                output_name = dir_name + ".py"
            output_file = os.path.join(os.path.dirname(parts_dir), output_name)
        
        # Read all part files
        parts_content = []
        for part in part_files:
            try:
                with open(part["path"], 'r', encoding='utf-8') as f:
                    content = f.read()
                parts_content.append({
                    "module": part["module"],
                    "items": part["items"],
                    "content": content
                })
            except Exception as e:
                print(f"Error reading {part['path']}: {e}")
        
        # Extract docstrings, imports, and code from each part
        extracted_parts = []
        for part in parts_content:
            try:
                tree = ast.parse(part["content"])
                docstring = ast.get_docstring(tree) or ""
                
                # Extract imports
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        imports.append(ast.unparse(node))
                
                # Extract code (excluding docstring and imports)
                code_nodes = []
                for node in tree.body:
                    if not isinstance(node, (ast.Expr, ast.Import, ast.ImportFrom)):
                        code_nodes.append(node)
                
                code = "\n".join(ast.unparse(node) for node in code_nodes)
                
                extracted_parts.append({
                    "module": part["module"],
                    "items": part["items"],
                    "docstring": docstring,
                    "imports": imports,
                    "code": code
                })
            except Exception as e:
                print(f"Error extracting from {part['module']}: {e}")
        
        # Build the combined file
        combined_content = ""
        
        # Add the main docstring (from the first part)
        if extracted_parts and extracted_parts[0]["docstring"]:
            combined_content += f'"""{extracted_parts[0]["docstring"]}"""\n\n'
        else:
            # Create a default docstring
            combined_content += f'"""\n{os.path.basename(output_file)}\n\nThis file was automatically rebuilt from split components.\n"""\n\n'
        
        # Combine all imports
        all_imports = []
        for part in extracted_parts:
            all_imports.extend(part["imports"])
        
        # Remove duplicate imports
        unique_imports = []
        for imp in all_imports:
            if imp not in unique_imports:
                unique_imports.append(imp)
        
        combined_content += "\n".join(unique_imports) + "\n\n"
        
        # Add all code
        for part in extracted_parts:
            combined_content += part["code"] + "\n\n"
        
        # Optimize imports if requested
        if optimize_imports:
            combined_content = self.import_optimizer.optimize_imports(combined_content)
        
        # Write the combined file
        if dry_run:
            print(f"Would create file: {output_file}")
            print(f"Combined {len(part_files)} part files")
        else:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(combined_content)
                print(f"Created file: {output_file}")
            except Exception as e:
                print(f"Error writing {output_file}: {e}")
                return None
        
        return {
            "output_file": output_file,
            "part_files": [part["path"] for part in part_files],
            "items": [item for part in part_files for item in part["items"]]
        }
    
    def rebuild_codebase(self, parts_dir, output_dir=None, optimize_imports=True, dry_run=True):
        """Rebuild the entire codebase from split parts."""
        # Check if the parts directory exists
        if not os.path.exists(parts_dir) or not os.path.isdir(parts_dir):
            print(f"Parts directory not found: {parts_dir}")
            return None
        
        # Determine the output directory
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(parts_dir), "rebuilt")
        
        # Create the output directory
        if not dry_run:
            ensure_dir(output_dir)
        
        # Find all parts directories
        parts_dirs = []
        for root, dirs, files in os.walk(parts_dir):
            for dir_name in dirs:
                if dir_name.endswith("_parts"):
                    parts_dirs.append(os.path.join(root, dir_name))
        
        print(f"Found {len(parts_dirs)} parts directories")
        
        # Rebuild each parts directory
        rebuilt_files = []
        for i, parts_dir in enumerate(parts_dirs):
            print(f"Rebuilding {i+1}/{len(parts_dirs)}: {os.path.relpath(parts_dir, self.project_root)}")
            
            # Determine the output file path
            rel_path = os.path.relpath(parts_dir, parts_dir)
            dir_name = os.path.basename(parts_dir)
            if dir_name.endswith("_parts"):
                output_name = dir_name[:-6] + ".py"
            else:
                output_name = dir_name + ".py"
            
            output_file = os.path.join(output_dir, rel_path, output_name)
            
            # Rebuild the file
            result = self.rebuild_from_parts(parts_dir, output_file, optimize_imports, dry_run)
            if result:
                rebuilt_files.append(result)
        
        return {
            "output_dir": output_dir,
            "rebuilt_files": len(rebuilt_files),
            "results": rebuilt_files
        }
    
    def apply_fixes(self, file_path, fix_unused_imports=True, fix_error_handling=True, 
                   fix_resource_issues=True, dry_run=True):
        """Apply fixes to a Python file."""
        # Analyze the file
        analysis = self.analyzer.analyze_file(file_path)
        if not analysis:
            print(f"Error analyzing {file_path}")
            return None
        
        # Read the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
        
        # Apply fixes
        fixed_content = content
        fixes_applied = []
        
        # Fix unused imports
        if fix_unused_imports and analysis["unused_imports"]:
            try:
                fixed_content = self.import_optimizer.optimize_imports(fixed_content)
                fixes_applied.append(f"Removed {len(analysis['unused_imports'])} unused imports")
            except Exception as e:
                print(f"Error fixing unused imports in {file_path}: {e}")
        
        # Fix error handling
        if fix_error_handling and analysis["error_handling_issues"]:
            try:
                # Replace bare except clauses with except Exception
                for issue in analysis["error_handling_issues"]:
                    if issue["type"] == "bare_except":
                        fixed_content = fixed_content.replace("except Exception:", "except Exception:")
                
                fixes_applied.append(f"Fixed {len(analysis['error_handling_issues'])} error handling issues")
            except Exception as e:
                print(f"Error fixing error handling in {file_path}: {e}")
        
        # Fix resource issues
        if fix_resource_issues and analysis["resource_issues"]:
            try:
                # This is a more complex fix that would require AST manipulation
                # For now, just report the issues
                fixes_applied.append(f"Found {len(analysis['resource_issues'])} resource issues (manual fixing required)")
            except Exception as e:
                print(f"Error fixing resource issues in {file_path}: {e}")
        
        # Write the fixed file
        if dry_run:
            print(f"Would fix {file_path}:")
            for fix in fixes_applied:
                print(f"- {fix}")
        else:
            if fixes_applied:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    print(f"Fixed {file_path}:")
                    for fix in fixes_applied:
                        print(f"- {fix}")
                except Exception as e:
                    print(f"Error writing {file_path}: {e}")
                    return None
            else:
                print(f"No fixes applied to {file_path}")
        
        return {
            "file_path": file_path,
            "fixes_applied": fixes_applied
        }
    
    def fix_codebase(self, fix_unused_imports=True, fix_error_handling=True, 
                    fix_resource_issues=True, dry_run=True):
        """Apply fixes to the entire codebase."""
        # Find all Python files
        python_files = []
        for root, _, files in os.walk(self.project_root):
            # Skip certain directories
            if any(skip in root for skip in ['.git', '__pycache__', '.vscode', '.idea']):
                continue
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        print(f"Found {len(python_files)} Python files")
        
        # Apply fixes to each file
        fixed_files = []
        for i, file_path in enumerate(python_files):
            if (i + 1) % 20 == 0 or i == len(python_files) - 1:
                print(f"Fixing file {i+1}/{len(python_files)}: {os.path.relpath(file_path, self.project_root)}")
            
            result = self.apply_fixes(file_path, fix_unused_imports, fix_error_handling, 
                                     fix_resource_issues, dry_run)
            if result and result["fixes_applied"]:
                fixed_files.append(result)
        
        return {
            "fixed_files": len(fixed_files),
            "results": fixed_files
        }

# Main function for standalone usage
def main():
    """Main function for standalone usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Rebuild optimized Python files from components")
    parser.add_argument("--parts", help="Directory containing split parts")
    parser.add_argument("--output", help="Output file or directory")
    parser.add_argument("--fix", action="store_true", help="Fix issues in the codebase")
    parser.add_argument("--no-optimize-imports", action="store_true", help="Disable import optimization")
    parser.add_argument("--apply", action="store_true", help="Apply the changes (default: dry run)")
    
    args = parser.parse_args()
    
    builder = CodeBuilder(project_root)
    
    if args.parts:
        # Rebuild from parts
        parts_dir = os.path.abspath(args.parts)
        print(f"Rebuilding from parts: {parts_dir}")
        
        if os.path.isdir(parts_dir) and os.path.exists(os.path.join(parts_dir, "__init__.py")):
            # Rebuild a single file
            result = builder.rebuild_from_parts(parts_dir, args.output, 
                                               not args.no_optimize_imports, not args.apply)
            if result:
                print(f"File successfully rebuilt from {len(result['part_files'])} parts")
        else:
            # Rebuild multiple files
            result = builder.rebuild_codebase(parts_dir, args.output, 
                                             not args.no_optimize_imports, not args.apply)
            if result:
                print(f"Codebase successfully rebuilt: {result['rebuilt_files']} files")
    elif args.fix:
        # Fix issues in the codebase
        print("Fixing issues in the codebase")
        result = builder.fix_codebase(True, True, True, not args.apply)
        
        print(f"Fixed {result['fixed_files']} files")
    else:
        parser.print_help()
    
    if not args.apply:
        print("\nTo apply the changes, run with --apply")

if __name__ == "__main__":
    main()
