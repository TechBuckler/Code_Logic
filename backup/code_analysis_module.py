"""
Code Analysis Module

This module provides code analysis functionality for the refactoring system.
It serves as a compatibility module during the transition to the new directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import ast

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class CodeAnalyzer:
    """Analyzes Python code for complexity and refactoring opportunities."""
    
    def __init__(self, file_path=None):
        """Initialize the code analyzer."""
        self.file_path = file_path
        self.ast_tree = None
        self.metrics = {
            "complexity": 0,
            "lines": 0,
            "functions": 0,
            "classes": 0,
            "imports": 0
        }
    
    def analyze(self, code=None):
        """Analyze the code and return metrics."""
        if code is None and self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        
        if code:
            self.ast_tree = ast.parse(code)
            self._calculate_metrics()
        
        return self.metrics
    
    def _calculate_metrics(self):
        """Calculate code metrics from the AST."""
        if not self.ast_tree:
            return
        
        # Count lines
        self.metrics["lines"] = len(ast.unparse(self.ast_tree).splitlines())
        
        # Count functions, classes, and imports
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                self.metrics["functions"] += 1
                # Simple complexity metric: count branches
                self.metrics["complexity"] += self._count_branches(node)
            elif isinstance(node, ast.ClassDef):
                self.metrics["classes"] += 1
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                self.metrics["imports"] += 1
    
    def _count_branches(self, node):
        """Count branching statements in a node to estimate complexity."""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                count += 1
        return count

def analyze_code(file_path):
    """Analyze a Python file and return metrics."""
    analyzer = CodeAnalyzer(file_path)
    return analyzer.analyze()

def analyze_codebase(directory):
    """Analyze all Python files in a directory and return metrics."""
    results = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                try:
                    results[rel_path] = analyze_code(file_path)
                except Exception as e:
                    results[rel_path] = {"error": str(e)}
    
    return results

# Export symbols
__all__ = ['CodeAnalyzer', 'analyze_code', 'analyze_codebase']
