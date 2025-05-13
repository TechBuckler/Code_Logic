#!/usr/bin/env python
"""
Refactor Analyzer

This module analyzes Python files to identify issues and opportunities for refactoring:
- Identifies complex functions that should be broken down
- Detects unused imports and other code quality issues
- Analyzes dependencies between functions and classes
- Maps code structure for intelligent refactoring

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

class CodeAnalyzer:
    """Analyzes Python code for refactoring opportunities."""
    
    def __init__(self, project_root):
        """Initialize the analyzer."""
        self.project_root = project_root
        self.file_cache = {}
        self.ast_cache = {}
        self.dependency_graph = nx.DiGraph()
    
    def find_all_python_files(self, exclude_dirs=None):
        """Find all Python files in the project."""
        if exclude_dirs is None:
            exclude_dirs = ['.git', '__pycache__', '.vscode', '.idea']
            
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        return python_files
    
    def get_file_content(self, file_path):
        """Get the content of a file, using cache if available."""
        if file_path in self.file_cache:
            return self.file_cache[file_path]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.file_cache[file_path] = content
            return content
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    def get_ast(self, file_path):
        """Get the AST for a file, using cache if available."""
        if file_path in self.ast_cache:
            return self.ast_cache[file_path]
        
        content = self.get_file_content(file_path)
        if content is None:
            return None
        
        try:
            tree = ast.parse(content)
            self.ast_cache[file_path] = tree
            return tree
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def analyze_file(self, file_path):
        """Analyze a file for refactoring opportunities."""
        tree = self.get_ast(file_path)
        if tree is None:
            return None
        
        # Collect basic metrics
        metrics = self._collect_metrics(tree)
        
        # Find complex functions
        complex_functions = self._find_complex_functions(tree)
        
        # Find unused imports
        unused_imports = self._find_unused_imports(tree)
        
        # Find resource management issues
        resource_issues = self._find_resource_issues(tree)
        
        # Find error handling issues
        error_handling_issues = self._find_error_handling_issues(tree)
        
        # Extract function dependencies
        function_dependencies = self._extract_function_dependencies(tree)
        
        # Extract class structure
        class_structure = self._extract_class_structure(tree)
        
        return {
            "file_path": file_path,
            "rel_path": os.path.relpath(file_path, self.project_root),
            "metrics": metrics,
            "complex_functions": complex_functions,
            "unused_imports": unused_imports,
            "resource_issues": resource_issues,
            "error_handling_issues": error_handling_issues,
            "function_dependencies": function_dependencies,
            "class_structure": class_structure
        }
    
    def analyze_codebase(self):
        """Analyze the entire codebase."""
        python_files = self.find_all_python_files()
        print(f"Found {len(python_files)} Python files to analyze")
        
        results = []
        for i, file_path in enumerate(python_files):
            if (i + 1) % 20 == 0 or i == len(python_files) - 1:
                print(f"Analyzing file {i + 1}/{len(python_files)}: {os.path.relpath(file_path, self.project_root)}")
            
            result = self.analyze_file(file_path)
            if result:
                results.append(result)
                
                # Build dependency graph
                self._update_dependency_graph(result)
        
        # Analyze module dependencies
        module_dependencies = self._analyze_module_dependencies()
        
        return {
            "files": results,
            "module_dependencies": module_dependencies,
            "summary": self._generate_summary(results)
        }
    
    def _collect_metrics(self, tree):
        """Collect basic metrics from an AST."""
        # Count lines of code
        if hasattr(tree, 'end_lineno'):
            loc = tree.end_lineno
        else:
            loc = len(ast.unparse(tree).splitlines())
        
        # Count functions, classes, and imports
        functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        imports = len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])
        
        # Calculate complexity
        complexity = self._calculate_complexity(tree)
        
        return {
            "loc": loc,
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "complexity": complexity
        }
    
    def _calculate_complexity(self, node):
        """Calculate cyclomatic complexity of an AST node."""
        complexity = 1  # Base complexity
        
        # Count branches
        for subnode in ast.walk(node):
            if isinstance(subnode, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(subnode, ast.BoolOp) and isinstance(subnode.op, ast.And):
                complexity += len(subnode.values) - 1
        
        return complexity
    
    def _find_complex_functions(self, tree):
        """Find complex functions in an AST."""
        complex_functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Calculate function size
                if hasattr(node, 'end_lineno') and node.end_lineno is not None:
                    lines = node.end_lineno - node.lineno
                else:
                    lines = len(ast.unparse(node).splitlines())
                
                # Calculate function complexity
                complexity = self._calculate_complexity(node)
                
                # Check if function is complex
                is_complex = False
                complex_reasons = []
                
                if lines > 50:
                    is_complex = True
                    complex_reasons.append(f"long function ({lines} lines)")
                
                if complexity > 10:
                    is_complex = True
                    complex_reasons.append(f"high complexity ({complexity})")
                
                # Count parameters
                params = len(node.args.args)
                if params > 5:
                    is_complex = True
                    complex_reasons.append(f"many parameters ({params})")
                
                # Check for nested functions or classes
                has_nested = False
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                        has_nested = True
                        break
                
                if has_nested:
                    is_complex = True
                    complex_reasons.append("contains nested functions/classes")
                
                if is_complex:
                    complex_functions.append({
                        "name": node.name,
                        "lineno": node.lineno,
                        "end_lineno": getattr(node, 'end_lineno', node.lineno + lines),
                        "lines": lines,
                        "complexity": complexity,
                        "params": params,
                        "has_nested": has_nested,
                        "reasons": complex_reasons,
                        "docstring": ast.get_docstring(node) or "",
                        "code": ast.unparse(node)
                    })
        
        return complex_functions
    
    def _find_unused_imports(self, tree):
        """Find unused imports in an AST."""
        # Collect all imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append({
                        "name": name.name,
                        "alias": name.asname or name.name,
                        "lineno": node.lineno,
                        "node": node
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for name in node.names:
                    imports.append({
                        "name": f"{module}.{name.name}" if module else name.name,
                        "alias": name.asname or name.name,
                        "lineno": node.lineno,
                        "node": node
                    })
        
        # Collect all used names
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                # This could be a module attribute access (e.g., os.path)
                used_names.add(node.value.id)
        
        # Find unused imports
        unused_imports = []
        for imp in imports:
            # Check if the import alias is used
            if imp["alias"] not in used_names:
                # Special case for import side effects (e.g., import sys)
                if "." not in imp["name"]:
                    # Check if any attribute of this module is used
                    module_used = False
                    for used in used_names:
                        if used.startswith(imp["alias"] + "."):
                            module_used = True
                            break
                    if module_used:
                        continue
                unused_imports.append(imp)
        
        return unused_imports
    
    def _find_resource_issues(self, tree):
        """Find resource management issues in an AST."""
        # Find file operations
        file_ops = []
        with_contexts = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (isinstance(node.func, ast.Name) and node.func.id in ["open", "file"]) or \
                   (isinstance(node.func, ast.Attribute) and node.func.attr in ["open", "file"]):
                    file_ops.append({
                        "lineno": node.lineno,
                        "node": node
                    })
            elif isinstance(node, ast.With):
                for item in node.items:
                    if isinstance(item.context_expr, ast.Call):
                        call = item.context_expr
                        if (isinstance(call.func, ast.Name) and call.func.id in ["open", "file"]) or \
                           (isinstance(call.func, ast.Attribute) and call.func.attr in ["open", "file"]):
                            with_contexts.append({
                                "lineno": node.lineno,
                                "end_lineno": getattr(node, 'end_lineno', node.lineno),
                                "node": node
                            })
        
        # Find file operations not in with contexts
        resource_issues = []
        for op in file_ops:
            # Check if this operation is within a with context
            in_with = False
            for ctx in with_contexts:
                if ctx["lineno"] <= op["lineno"] and ctx["end_lineno"] >= op["lineno"]:
                    in_with = True
                    break
            if not in_with:
                resource_issues.append(op)
        
        return resource_issues
    
    def _find_error_handling_issues(self, tree):
        """Find error handling issues in an AST."""
        error_handling_issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    if handler.type is None:
                        # Bare except clause
                        error_handling_issues.append({
                            "type": "bare_except",
                            "lineno": handler.lineno,
                            "node": handler
                        })
        
        return error_handling_issues
    
    def _extract_function_dependencies(self, tree):
        """Extract function dependencies from an AST."""
        # Collect all function definitions
        functions = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = {
                    "node": node,
                    "calls": set(),
                    "lineno": node.lineno
                }
        
        # Collect function calls
        for func_name, func_info in functions.items():
            for node in ast.walk(func_info["node"]):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    called_func = node.func.id
                    if called_func in functions and called_func != func_name:
                        func_info["calls"].add(called_func)
        
        # Convert to serializable format
        result = {}
        for func_name, func_info in functions.items():
            result[func_name] = {
                "lineno": func_info["lineno"],
                "calls": list(func_info["calls"])
            }
        
        return result
    
    def _extract_class_structure(self, tree):
        """Extract class structure from an AST."""
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                attributes = []
                
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        methods.append({
                            "name": child.name,
                            "lineno": child.lineno,
                            "is_property": any(isinstance(d, ast.Name) and d.id == 'property' 
                                              for d in child.decorator_list),
                            "is_staticmethod": any(isinstance(d, ast.Name) and d.id == 'staticmethod' 
                                                  for d in child.decorator_list),
                            "is_classmethod": any(isinstance(d, ast.Name) and d.id == 'classmethod' 
                                                 for d in child.decorator_list)
                        })
                    elif isinstance(child, ast.Assign):
                        for target in child.targets:
                            if isinstance(target, ast.Name):
                                attributes.append({
                                    "name": target.id,
                                    "lineno": child.lineno
                                })
                
                classes.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "bases": [base.id if isinstance(base, ast.Name) else ast.unparse(base) 
                             for base in node.bases],
                    "methods": methods,
                    "attributes": attributes,
                    "docstring": ast.get_docstring(node) or ""
                })
        
        return classes
    
    def _update_dependency_graph(self, file_analysis):
        """Update the dependency graph with file analysis results."""
        file_node = file_analysis["rel_path"]
        
        # Add file node
        if not self.dependency_graph.has_node(file_node):
            self.dependency_graph.add_node(file_node, type="file")
        
        # Add function nodes and dependencies
        for func_name, func_info in file_analysis["function_dependencies"].items():
            func_node = f"{file_node}::{func_name}"
            if not self.dependency_graph.has_node(func_node):
                self.dependency_graph.add_node(func_node, type="function")
            
            # Add edge from file to function
            self.dependency_graph.add_edge(file_node, func_node)
            
            # Add function call dependencies
            for called_func in func_info["calls"]:
                called_node = f"{file_node}::{called_func}"
                if not self.dependency_graph.has_node(called_node):
                    self.dependency_graph.add_node(called_node, type="function")
                
                self.dependency_graph.add_edge(func_node, called_node)
    
    def _analyze_module_dependencies(self):
        """Analyze module dependencies."""
        # Group files by module
        modules = defaultdict(list)
        for node in self.dependency_graph.nodes():
            if self.dependency_graph.nodes[node].get("type") == "file":
                module_path = os.path.dirname(node)
                if not module_path:
                    module_path = "root"
                modules[module_path].append(node)
        
        # Calculate module dependencies
        module_dependencies = defaultdict(set)
        for module, files in modules.items():
            for file in files:
                for successor in self.dependency_graph.successors(file):
                    if self.dependency_graph.nodes[successor].get("type") == "file":
                        successor_module = os.path.dirname(successor)
                        if not successor_module:
                            successor_module = "root"
                        
                        if successor_module != module:
                            module_dependencies[module].add(successor_module)
        
        # Convert to serializable format
        result = {}
        for module, deps in module_dependencies.items():
            result[module] = list(deps)
        
        return result
    
    def _generate_summary(self, results):
        """Generate a summary of the analysis results."""
        # Collect statistics
        total_files = len(results)
        total_loc = sum(r["metrics"]["loc"] for r in results)
        total_functions = sum(r["metrics"]["functions"] for r in results)
        total_classes = sum(r["metrics"]["classes"] for r in results)
        total_imports = sum(r["metrics"]["imports"] for r in results)
        avg_complexity = sum(r["metrics"]["complexity"] for r in results) / total_files if total_files > 0 else 0
        
        # Count issues
        total_complex_functions = sum(len(r["complex_functions"]) for r in results)
        total_unused_imports = sum(len(r["unused_imports"]) for r in results)
        total_resource_issues = sum(len(r["resource_issues"]) for r in results)
        total_error_handling_issues = sum(len(r["error_handling_issues"]) for r in results)
        
        # Find notable files
        largest_file = max(results, key=lambda r: r["metrics"]["loc"])
        most_complex_file = max(results, key=lambda r: r["metrics"]["complexity"])
        most_functions_file = max(results, key=lambda r: r["metrics"]["functions"])
        most_classes_file = max(results, key=lambda r: r["metrics"]["classes"])
        
        # Find most complex function
        most_complex_function = None
        most_complex_function_file = None
        most_complex_function_complexity = 0
        
        for r in results:
            for func in r["complex_functions"]:
                if func["complexity"] > most_complex_function_complexity:
                    most_complex_function = func
                    most_complex_function_file = r["rel_path"]
                    most_complex_function_complexity = func["complexity"]
        
        return {
            "total_files": total_files,
            "total_loc": total_loc,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "total_imports": total_imports,
            "avg_complexity": avg_complexity,
            "total_complex_functions": total_complex_functions,
            "total_unused_imports": total_unused_imports,
            "total_resource_issues": total_resource_issues,
            "total_error_handling_issues": total_error_handling_issues,
            "largest_file": {
                "path": largest_file["rel_path"],
                "loc": largest_file["metrics"]["loc"]
            },
            "most_complex_file": {
                "path": most_complex_file["rel_path"],
                "complexity": most_complex_file["metrics"]["complexity"]
            },
            "most_functions_file": {
                "path": most_functions_file["rel_path"],
                "functions": most_functions_file["metrics"]["functions"]
            },
            "most_classes_file": {
                "path": most_classes_file["rel_path"],
                "classes": most_classes_file["metrics"]["classes"]
            },
            "most_complex_function": {
                "name": most_complex_function["name"] if most_complex_function else None,
                "file": most_complex_function_file,
                "complexity": most_complex_function_complexity
            }
        }

# Main function for standalone usage
def main():
    """Main function for standalone usage."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Analyze Python code for refactoring opportunities")
    parser.add_argument("--file", help="Analyze a specific file")
    parser.add_argument("--output", help="Output file for analysis results")
    
    args = parser.parse_args()
    
    analyzer = CodeAnalyzer(project_root)
    
    if args.file:
        # Analyze a specific file
        file_path = os.path.abspath(args.file)
        print(f"Analyzing file: {file_path}")
        result = analyzer.analyze_file(file_path)
        
        if result:
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                print(f"Analysis results written to {args.output}")
            else:
                print(json.dumps(result, indent=2))
        else:
            print("Analysis failed")
    else:
        # Analyze the entire codebase
        print("Analyzing entire codebase...")
        results = analyzer.analyze_codebase()
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"Analysis results written to {args.output}")
        else:
            # Print summary
            summary = results["summary"]
            print("\nCodebase Analysis Summary")
            print("=" * 80)
            print(f"Total Files: {summary['total_files']}")
            print(f"Total Lines of Code: {summary['total_loc']}")
            print(f"Total Functions: {summary['total_functions']}")
            print(f"Total Classes: {summary['total_classes']}")
            print(f"Average Complexity: {summary['avg_complexity']:.2f}")
            print(f"Complex Functions: {summary['total_complex_functions']}")
            print(f"Unused Imports: {summary['total_unused_imports']}")
            print(f"Resource Issues: {summary['total_resource_issues']}")
            print(f"Error Handling Issues: {summary['total_error_handling_issues']}")
            
            print("\nNotable Files:")
            print(f"Largest File: {summary['largest_file']['path']} ({summary['largest_file']['loc']} lines)")
            print(f"Most Complex File: {summary['most_complex_file']['path']} (complexity: {summary['most_complex_file']['complexity']})")
            print(f"Most Functions: {summary['most_functions_file']['path']} ({summary['most_functions_file']['functions']} functions)")
            print(f"Most Classes: {summary['most_classes_file']['path']} ({summary['most_classes_file']['classes']} classes)")
            
            if summary['most_complex_function']['name']:
                print(f"Most Complex Function: {summary['most_complex_function']['name']} in {summary['most_complex_function']['file']} (complexity: {summary['most_complex_function']['complexity']})")

def analyze_codebase():
    """Analyze the entire codebase."""
    analyzer = CodeAnalyzer(project_root)
    return analyzer.analyze_codebase()

if __name__ == "__main__":
    main()
