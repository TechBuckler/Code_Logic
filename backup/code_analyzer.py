"""
Code Analyzer Module

Provides functions for analyzing Python code files to extract
dependencies, complexity metrics, and semantic information.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import ast
import re
import importlib

def analyze_file(file_path):
    """
    Analyze a Python file to extract metrics and semantic information.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Dictionary with analysis results
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse the AST
        tree = ast.parse(content)
        
        # Extract basic metrics
        metrics = {
            "loc": len(content.splitlines()),
            "functions": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
            "classes": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
            "imports": len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]),
            "complexity": _calculate_complexity(tree)
        }
        
        # Extract semantic information
        semantics = {
            "docstring": ast.get_docstring(tree),
            "functions": _extract_functions(tree),
            "classes": _extract_classes(tree),
            "imports": _extract_imports(tree),
            "variables": _extract_variables(tree),
            "keywords": _extract_keywords(content)
        }
        
        return {
            "metrics": metrics,
            "semantics": semantics,
            "path": file_path,
            "filename": os.path.basename(file_path)
        }
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return {
            "metrics": {"loc": 0, "functions": 0, "classes": 0, "imports": 0, "complexity": 0},
            "semantics": {"docstring": "", "functions": [], "classes": [], "imports": [], "variables": [], "keywords": []},
            "path": file_path,
            "filename": os.path.basename(file_path),
            "error": str(e)
        }

def extract_dependencies(file_path):
    """
    Extract dependencies from a Python file.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Set of dependencies
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse the AST
        tree = ast.parse(content)
        
        # Extract imports
        imports = _extract_imports(tree)
        
        # Convert imports to file paths
        dependencies = set()
        for imp in imports:
            if imp["module"].startswith("."):
                # Relative import
                continue
                
            try:
                # Try to find the module
                spec = importlib.util.find_spec(imp["module"])
                if spec and spec.origin and spec.origin.endswith(".py"):
                    dependencies.add(spec.origin)
            except (ImportError, AttributeError):
                pass
                
        return dependencies
    except Exception as e:
        print(f"Error extracting dependencies from {file_path}: {e}")
        return set()

def _calculate_complexity(tree):
    """Calculate cyclomatic complexity of the code."""
    complexity = 1  # Base complexity
    
    # Count branches
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
            complexity += len(node.values) - 1
            
    return complexity

def _extract_functions(tree):
    """Extract function definitions from the AST."""
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "docstring": ast.get_docstring(node) or "",
                "complexity": _calculate_complexity(node)
            })
            
    return functions

def _extract_classes(tree):
    """Extract class definitions from the AST."""
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = []
            
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    methods.append(child.name)
                    
            classes.append({
                "name": node.name,
                "methods": methods,
                "docstring": ast.get_docstring(node) or "",
                "bases": [base.id if isinstance(base, ast.Name) else "" for base in node.bases]
            })
            
    return classes

def _extract_imports(tree):
    """Extract imports from the AST."""
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append({
                    "module": name.name,
                    "alias": name.asname,
                    "type": "import"
                })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for name in node.names:
                imports.append({
                    "module": f"{module}.{name.name}" if module else name.name,
                    "alias": name.asname,
                    "type": "from"
                })
                
    return imports

def _extract_variables(tree):
    """Extract variable assignments from the AST."""
    variables = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables.append(target.id)
                    
    return variables

def _extract_keywords(content):
    """Extract keywords from the content."""
    # Remove comments and strings
    content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)
    content = re.sub(r"'''.*?'''", '', content, flags=re.DOTALL)
    
    # Tokenize
    words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', content)
    
    # Remove Python keywords and common words
    python_keywords = set([
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
        'try', 'while', 'with', 'yield'
    ])
    
    common_words = set(['self', 'cls', 'args', 'kwargs', 'data', 'result', 'value', 'item'])
    
    filtered_words = [w for w in words if w not in python_keywords and w not in common_words and len(w) > 2]
    
    # Count frequencies
    counter = Counter(filtered_words)
    
    # Return top keywords
    return [word for word, _ in counter.most_common(20)]
