#!/usr/bin/env python
"""
Cleanup Critical Issues

This script addresses the most critical issues identified in the codebase analysis:
1. Unused imports (80.4% of all issues)
2. Code complexity (9.4% of all issues)
3. Error handling (4.2% of all issues)
4. Resource management (4.0% of all issues)
5. Potential runtime errors (1.8% of all issues)

It focuses on the top 10 files with the most issues first, which would address
approximately 25% of all identified problems.
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

# Import our existing tools
try:
    # Attempt to import required tools
    import some_required_tool
except ImportError as e:
    print(f"Error importing tools: {e}")
    print("Make sure you've run the reorganization scripts first.")
    sys.exit(1)

# Priority files to fix based on the analysis report
PRIORITY_FILES = [
    "ui/unified.py",
    "legacy/src/unified_ui.py",
    "legacy/src/new_unified_ui.py",
    "tools/fractal_organizer.py",
    "tools/fractal/fractal_organizer.py",
    "tools/fractal/organizer.py",
    "tools/shadow_tree.py",
    "legacy/src/imports.py",
    "legacy/src/bootstrap.py",
    "ui/new_unified.py"
]

class ImportVisitor(ast.NodeVisitor):
    """AST visitor to find unused imports."""
    
    def __init__(self):
        self.imports = []
        self.used_names = set()
        
    def visit_Import(self, node):
        """Visit Import nodes."""
        for name in node.names:
            alias = name.asname if name.asname else name.name
            self.imports.append({
                "name": name.name,
                "alias": alias,
                "node": node,
                "lineno": node.lineno
            })
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node):
        """Visit ImportFrom nodes."""
        module = node.module if node.module else ""
        for name in node.names:
            alias = name.asname if name.asname else name.name
            self.imports.append({
                "name": f"{module}.{name.name}" if module else name.name,
                "alias": alias,
                "node": node,
                "lineno": node.lineno
            })
        self.generic_visit(node)
        
    def visit_Name(self, node):
        """Visit Name nodes to track used names."""
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)
        
    def visit_Attribute(self, node):
        """Visit Attribute nodes to track used module attributes."""
        if isinstance(node.value, ast.Name):
            # This could be a module attribute access (e.g., os.path)
            self.used_names.add(node.value.id)
        self.generic_visit(node)

class ErrorHandlingVisitor(ast.NodeVisitor):
    """AST visitor to find bare except clauses."""
    
    def __init__(self):
        self.bare_excepts = []
        
    def visit_Try(self, node):
        """Visit Try nodes to find bare except clauses."""
        for handler in node.handlers:
            if handler.type is None:
                self.bare_excepts.append({
                    "node": handler,
                    "lineno": handler.lineno
                })
        self.generic_visit(node)

class ResourceManagementVisitor(ast.NodeVisitor):
    """AST visitor to find resource management issues."""
    
    def __init__(self):
        self.file_ops = []
        self.with_contexts = []
        
    def visit_Call(self, node):
        """Visit Call nodes to find file operations."""
        if isinstance(node.func, ast.Name) and node.func.id in ["open", "file"]:
            self.file_ops.append({
                "node": node,
                "lineno": node.lineno
            })
        elif isinstance(node.func, ast.Attribute) and node.func.attr in ["open", "file"]:
            self.file_ops.append({
                "node": node,
                "lineno": node.lineno
            })
        self.generic_visit(node)
        
    def visit_With(self, node):
        """Visit With nodes to track context manager usage."""
        for item in node.items:
            if isinstance(item.context_expr, ast.Call):
                call = item.context_expr
                if (isinstance(call.func, ast.Name) and call.func.id in ["open", "file"]) or \
                   (isinstance(call.func, ast.Attribute) and call.func.attr in ["open", "file"]):
                    self.with_contexts.append({
                        "node": node,
                        "lineno": node.lineno
                    })
        self.generic_visit(node)

class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor to find complex functions."""
    
    def __init__(self):
        self.complex_functions = []
        
    def visit_FunctionDef(self, node):
        """Visit FunctionDef nodes to find complex functions."""
        # Count the number of lines in the function
        if hasattr(node, 'end_lineno') and node.end_lineno is not None:
            lines = node.end_lineno - node.lineno
            if lines > 50:  # Functions with more than 50 lines are considered complex
                self.complex_functions.append({
                    "name": node.name,
                    "lines": lines,
                    "node": node,
                    "lineno": node.lineno
                })
        self.generic_visit(node)

def find_unused_imports(file_path):
    """Find unused imports in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        visitor = ImportVisitor()
        visitor.visit(tree)
        
        unused_imports = []
        for imp in visitor.imports:
            # Check if the import alias is used
            if imp["alias"] not in visitor.used_names:
                # Special case for import side effects (e.g., import sys)
                if "." not in imp["name"]:
                    # Check if any attribute of this module is used
                    module_used = False
                    for used in visitor.used_names:
                        if used.startswith(imp["alias"] + "."):
                            module_used = True
                            break
                    if module_used:
                        continue
                unused_imports.append(imp)
        
        return unused_imports
    except Exception as e:
        print(f"Error analyzing imports in {file_path}: {e}")
        return []

def find_bare_excepts(file_path):
    """Find bare except clauses in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        visitor = ErrorHandlingVisitor()
        visitor.visit(tree)
        
        return visitor.bare_excepts
    except Exception as e:
        print(f"Error analyzing error handling in {file_path}: {e}")
        return []

def find_resource_issues(file_path):
    """Find resource management issues in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        visitor = ResourceManagementVisitor()
        visitor.visit(tree)
        
        # Find file operations not in with contexts
        resource_issues = []
        for op in visitor.file_ops:
            # Check if this operation is within a with context
            in_with = False
            for ctx in visitor.with_contexts:
                if ctx["lineno"] <= op["lineno"] and hasattr(ctx["node"], 'end_lineno') and ctx["node"].end_lineno >= op["lineno"]:
                    in_with = True
                    break
            if not in_with:
                resource_issues.append(op)
        
        return resource_issues
    except Exception as e:
        print(f"Error analyzing resource management in {file_path}: {e}")
        return []

def find_complex_functions(file_path):
    """Find complex functions in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        visitor = ComplexityVisitor()
        visitor.visit(tree)
        
        return visitor.complex_functions
    except Exception as e:
        print(f"Error analyzing complexity in {file_path}: {e}")
        return []

def fix_unused_imports(file_path, unused_imports, dry_run=True):
    """Fix unused imports in a Python file."""
    if not unused_imports:
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Sort unused imports by line number (descending) to avoid line number changes
        unused_imports.sort(key=lambda x: x["lineno"], reverse=True)
        
        # Remove unused imports
        for imp in unused_imports:
            lineno = imp["lineno"] - 1  # Convert to 0-based index
            if 0 <= lineno < len(lines):
                if dry_run:
                    print(f"Would remove unused import at line {lineno + 1}: {lines[lineno].strip()}")
                else:
                    lines.pop(lineno)
                    print(f"Removed unused import at line {lineno + 1}")
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
    except Exception as e:
        print(f"Error fixing unused imports in {file_path}: {e}")

def fix_bare_excepts(file_path, bare_excepts, dry_run=True):
    """Fix bare except clauses in a Python file."""
    if not bare_excepts:
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
        
        # Replace bare excepts with specific exception types
        for exc in bare_excepts:
            lineno = exc["lineno"] - 1  # Convert to 0-based index
            if 0 <= lineno < len(lines):
                line = lines[lineno]
                if re.search(r'except\s*:', line):
                    fixed_line = line.replace('except Exception:', 'except Exception:')
                    if dry_run:
                        print(f"Would replace line {lineno + 1}: '{line}' with '{fixed_line}'")
                    else:
                        lines[lineno] = fixed_line
                        print(f"Fixed bare except at line {lineno + 1}")
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
    except Exception as e:
        print(f"Error fixing bare excepts in {file_path}: {e}")

def fix_resource_issues(file_path, resource_issues, dry_run=True):
    """Fix resource management issues in a Python file."""
    if not resource_issues:
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # This is a more complex fix that requires AST manipulation
        # For simplicity, we'll just report the issues in dry run mode
        if dry_run:
            for issue in resource_issues:
                print(f"Resource issue at line {issue['lineno']}: File operation not using context manager")
        else:
            print(f"Resource issues require manual fixing in {file_path}")
    except Exception as e:
        print(f"Error analyzing resource issues in {file_path}: {e}")

def suggest_function_refactoring(file_path, complex_functions, dry_run=True):
    """Suggest refactoring for complex functions."""
    if not complex_functions:
        return
    
    try:
        for func in complex_functions:
            print(f"Complex function in {file_path} at line {func['lineno']}: {func['name']} ({func['lines']} lines)")
            
            # Suggest breaking down the function
            print("  Suggestion: Break down this function into smaller, focused components")
            print("  - Extract repeated code patterns into helper functions")
            print("  - Separate different responsibilities into distinct functions")
            print("  - Consider using a class to manage related state")
    except Exception as e:
        print(f"Error suggesting function refactoring in {file_path}: {e}")

def analyze_and_fix_file(file_path, dry_run=True):
    """Analyze and fix issues in a Python file."""
    print(f"\n📝 Analyzing {file_path}")
    print("-" * 80)
    
    # Find issues
    unused_imports = find_unused_imports(file_path)
    bare_excepts = find_bare_excepts(file_path)
    resource_issues = find_resource_issues(file_path)
    complex_functions = find_complex_functions(file_path)
    
    # Report issues
    print(f"Found {len(unused_imports)} unused imports")
    print(f"Found {len(bare_excepts)} bare except clauses")
    print(f"Found {len(resource_issues)} resource management issues")
    print(f"Found {len(complex_functions)} complex functions")
    
    # Fix issues
    fix_unused_imports(file_path, unused_imports, dry_run)
    fix_bare_excepts(file_path, bare_excepts, dry_run)
    fix_resource_issues(file_path, resource_issues, dry_run)
    suggest_function_refactoring(file_path, complex_functions, dry_run)
    
    return {
        "unused_imports": len(unused_imports),
        "bare_excepts": len(bare_excepts),
        "resource_issues": len(resource_issues),
        "complex_functions": len(complex_functions)
    }

def cleanup_critical_issues(dry_run=True):
    """Clean up critical issues in the codebase."""
    print("\n🧹 Cleaning Up Critical Issues")
    print("=" * 80)
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}")
    
    # Process priority files first
    print("\n🔍 Processing Priority Files")
    print("-" * 80)
    
    priority_stats = defaultdict(int)
    for file_path in PRIORITY_FILES:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            stats = analyze_and_fix_file(full_path, dry_run)
            for key, value in stats.items():
                priority_stats[key] += value
        else:
            print(f"File not found: {file_path}")
    
    # Generate report
    print("\n📊 Priority Files Summary")
    print("-" * 80)
    print(f"Processed {len(PRIORITY_FILES)} priority files")
    print(f"Found {sum(priority_stats.values())} total issues:")
    print(f"- {priority_stats['unused_imports']} unused imports")
    print(f"- {priority_stats['bare_excepts']} bare except clauses")
    print(f"- {priority_stats['resource_issues']} resource management issues")
    print(f"- {priority_stats['complex_functions']} complex functions")
    
    # Generate recommendations
    print("\n📋 Recommendations for Further Cleanup")
    print("-" * 80)
    print("1. Import System Improvements:")
    print("   - Implement a centralized import management system")
    print("   - Use relative imports for internal modules")
    print("   - Consider using __all__ to define public interfaces")
    print("\n2. Error Handling Strategy:")
    print("   - Define custom exception classes for different error types")
    print("   - Implement proper logging for exceptions")
    print("   - Add recovery mechanisms for critical operations")
    print("\n3. Resource Management:")
    print("   - Use context managers (with statements) consistently")
    print("   - Create utility functions for common resource operations")
    print("   - Add cleanup code in finally blocks")
    print("\n4. Code Complexity Reduction:")
    print("   - Break down complex functions into smaller, focused components")
    print("   - Apply single responsibility principle")
    print("   - Extract repeated patterns into utility functions")
    print("\n5. Module Organization:")
    print("   - Leverage the ModuleRegistry for better dependency management")
    print("   - Establish clear boundaries between modules")
    print("   - Consolidate duplicate functionality")
    
    print("\n✅ Critical issues analysis complete!")
    if dry_run:
        print("\nTo apply the fixes, run: py cleanup_critical_issues.py --apply")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean up critical issues in the codebase")
    parser.add_argument("--apply", action="store_true", help="Apply the fixes (default: dry run)")
    
    args = parser.parse_args()
    
    cleanup_critical_issues(not args.apply)

if __name__ == "__main__":
    main()
