"""
Code Mapper Module

This module provides tools for analyzing and mapping the codebase structure,
dependencies, and resource usage patterns. It uses AST (Abstract Syntax Tree)
to parse Python files and extract detailed information about their structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import ast
import importlib

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Try to import the module system and resource splitter
try:
    HAS_MODULE_SYSTEM = True
except ImportError:
    HAS_MODULE_SYSTEM = False

# Import resource analysis functions
try:
    from resource_splitter import analyze_resource_focus, analyze_resource_profile
    HAS_RESOURCE_SPLITTER = True
except ImportError:
    HAS_RESOURCE_SPLITTER = False
    
    # Define fallback functions if resource_splitter is not available
    def analyze_resource_focus(func_code):
        """Analyze the resource focus of a function."""
        return "cpu"  # Default to CPU focus
        
    def analyze_resource_profile(func_code):
        """Analyze the resource profile of a function."""
        return {
            'cpu': 0.5, 'memory': 0.5, 'gpu': 0.0, 
            'network': 0.0, 'startup': 0.3, 'runtime': 0.5
        }


class ImportVisitor(ast.NodeVisitor):
    """AST visitor that collects all imports in a Python file."""
    
    def __init__(self):
        self.imports = []
        self.from_imports = []
        
    def visit_Import(self, node):
        for name in node.names:
            self.imports.append({
                'module': name.name,
                'alias': name.asname,
                'line': node.lineno
            })
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node):
        module = node.module
        for name in node.names:
            self.from_imports.append({
                'module': module,
                'name': name.name,
                'alias': name.asname,
                'line': node.lineno
            })
        self.generic_visit(node)


class FunctionVisitor(ast.NodeVisitor):
    """AST visitor that collects all functions in a Python file."""
    
    def __init__(self):
        self.functions = {}
        self.current_class = None
        self.source_lines = []
        
    def set_source(self, source):
        """Set the source code for extracting function definitions."""
        self.source_lines = source.splitlines()
        
    def visit_ClassDef(self, node):
        old_class = self.current_class
        self.current_class = node.name
        
        # Process the class body
        self.generic_visit(node)
        
        # Restore the previous class context
        self.current_class = old_class
        
    def visit_FunctionDef(self, node):
        # Get the function name with class prefix if applicable
        func_name = f"{self.current_class}.{node.name}" if self.current_class else node.name
        
        # Extract the function source code
        start_line = node.lineno - 1  # Convert to 0-based index
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
        
        # Extract the function source code
        if start_line < len(self.source_lines) and end_line < len(self.source_lines):
            func_source = "\n".join(self.source_lines[start_line:end_line+1])
        else:
            func_source = f"# Could not extract source for {func_name}"
        
        # Extract function arguments
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        
        # Extract docstring if present
        docstring = ast.get_docstring(node)
        
        # Extract function calls within this function
        call_visitor = FunctionCallVisitor()
        call_visitor.visit(node)
        
        # Store the function information
        self.functions[func_name] = {
            'name': node.name,
            'qualified_name': func_name,
            'class': self.current_class,
            'args': args,
            'docstring': docstring,
            'source': func_source,
            'start_line': start_line + 1,  # Convert back to 1-based index
            'end_line': end_line + 1,
            'calls': call_visitor.calls
        }
        
        # Continue visiting the function body
        self.generic_visit(node)


class FunctionCallVisitor(ast.NodeVisitor):
    """AST visitor that collects all function calls within a function."""
    
    def __init__(self):
        self.calls = []
        
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            # Direct function call: func()
            self.calls.append({
                'name': node.func.id,
                'line': node.lineno if hasattr(node, 'lineno') else 0
            })
        elif isinstance(node.func, ast.Attribute):
            # Method call: obj.method()
            if isinstance(node.func.value, ast.Name):
                self.calls.append({
                    'name': f"{node.func.value.id}.{node.func.attr}",
                    'line': node.lineno if hasattr(node, 'lineno') else 0
                })
        
        # Continue visiting the call arguments
        self.generic_visit(node)


class ClassVisitor(ast.NodeVisitor):
    """AST visitor that collects all classes in a Python file."""
    
    def __init__(self):
        self.classes = {}
        self.source_lines = []
        
    def set_source(self, source):
        """Set the source code for extracting class definitions."""
        self.source_lines = source.splitlines()
        
    def visit_ClassDef(self, node):
        # Extract the class source code
        start_line = node.lineno - 1  # Convert to 0-based index
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
        
        # Extract the class source code
        if start_line < len(self.source_lines) and end_line < len(self.source_lines):
            class_source = "\n".join(self.source_lines[start_line:end_line+1])
        else:
            class_source = f"# Could not extract source for {node.name}"
        
        # Extract base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{base.value.id}.{base.attr}" if isinstance(base.value, ast.Name) else base.attr)
        
        # Extract docstring if present
        docstring = ast.get_docstring(node)
        
        # Store the class information
        self.classes[node.name] = {
            'name': node.name,
            'bases': bases,
            'docstring': docstring,
            'source': class_source,
            'start_line': start_line + 1,  # Convert back to 1-based index
            'end_line': end_line + 1
        }
        
        # Continue visiting the class body
        self.generic_visit(node)


def analyze_file(file_path):
    """Analyze a Python file and extract its structure."""
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    try:
        tree = ast.parse(source)
        
        # Extract imports
        import_visitor = ImportVisitor()
        import_visitor.visit(tree)
        
        # Extract functions
        function_visitor = FunctionVisitor()
        function_visitor.set_source(source)
        function_visitor.visit(tree)
        
        # Extract classes
        class_visitor = ClassVisitor()
        class_visitor.set_source(source)
        class_visitor.visit(tree)
        
        # Extract module docstring
        module_docstring = ast.get_docstring(tree)
        
        # Analyze resource usage for each function
        for func_name, func_info in function_visitor.functions.items():
            func_code = func_info['source']
            func_info['resource_focus'] = analyze_resource_focus(func_code)
            func_info['resource_profile'] = analyze_resource_profile(func_code)
        
        return {
            'file_path': file_path,
            'module_name': os.path.basename(file_path).replace('.py', ''),
            'docstring': module_docstring,
            'imports': import_visitor.imports,
            'from_imports': import_visitor.from_imports,
            'functions': function_visitor.functions,
            'classes': class_visitor.classes
        }
    except SyntaxError as e:
        return {
            'file_path': file_path,
            'error': f"Syntax error: {str(e)}",
            'imports': [],
            'from_imports': [],
            'functions': {},
            'classes': {}
        }


def find_python_files(directory):
    """Find all Python files in a directory and its subdirectories."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def map_codebase(directory):
    """Map the entire codebase structure."""
    python_files = find_python_files(directory)
    
    # Analyze each file
    file_analyses = {}
    for file_path in python_files:
        rel_path = os.path.relpath(file_path, directory)
        file_analyses[rel_path] = analyze_file(file_path)
    
    # Build dependency graph
    dependency_graph = {}
    for rel_path, analysis in file_analyses.items():
        dependencies = set()
        
        # Add dependencies from imports
        for imp in analysis['imports']:
            dependencies.add(imp['module'].split('.')[0])
        
        for imp in analysis['from_imports']:
            if imp['module']:
                dependencies.add(imp['module'].split('.')[0])
        
        # Remove standard library modules
        std_libs = {'os', 'sys', 'ast', 'json', 'time', 'math', 're', 'random', 
                   'datetime', 'collections', 'itertools', 'functools', 'typing'}
        dependencies = {dep for dep in dependencies if dep not in std_libs}
        
        dependency_graph[rel_path] = list(dependencies)
    
    # Build resource usage map
    resource_map = {
        'cpu': [],
        'memory': [],
        'gpu': [],
        'network': [],
        'ui': [],
        'core': []
    }
    
    for rel_path, analysis in file_analyses.items():
        # Count functions by resource focus
        resource_counts = {
            'cpu': 0, 'memory': 0, 'gpu': 0, 'network': 0, 'ui': 0, 'core': 0
        }
        
        for func_name, func_info in analysis['functions'].items():
            resource = func_info.get('resource_focus', 'cpu')
            resource_counts[resource] += 1
        
        # Determine the primary resource focus of the file
        if sum(resource_counts.values()) > 0:
            primary_resource = max(resource_counts, key=resource_counts.get)
            resource_map[primary_resource].append(rel_path)
        else:
            # Default to core if no functions
            resource_map['core'].append(rel_path)
    
    return {
        'files': file_analyses,
        'dependencies': dependency_graph,
        'resource_map': resource_map
    }


def generate_codebase_report(map_data, output_file=None):
    """Generate a human-readable report of the codebase structure."""
    report = []
    
    # Add header
    report.append("# Codebase Structure Report")
    report.append("")
    
    # Add summary
    file_count = len(map_data['files'])
    function_count = sum(len(analysis['functions']) for analysis in map_data['files'].values())
    class_count = sum(len(analysis['classes']) for analysis in map_data['files'].values())
    
    report.append(f"## Summary")
    report.append(f"- Total Python files: {file_count}")
    report.append(f"- Total functions: {function_count}")
    report.append(f"- Total classes: {class_count}")
    report.append("")
    
    # Add resource distribution
    report.append(f"## Resource Distribution")
    for resource, files in map_data['resource_map'].items():
        if not files:
            continue
        report.append(f"### {resource.upper()} ({len(files)} files)")
        for file in sorted(files):
            report.append(f"- `{file}`")
        report.append("")
    
    # Add file details section header
    report.append(f"## File Details")
    report.append("")
    
    # Add file details - one file at a time
    for rel_path, analysis in sorted(map_data['files'].items()):
        # Skip files with errors
        if 'error' in analysis:
            report.append(f"### `{rel_path}` (Error: {analysis['error']})")
            report.append("")
            continue
            
        report.append(f"### `{rel_path}`")
        
        # Add docstring if available
        if analysis.get('docstring'):
            docstring = analysis['docstring'].split('.')[0].replace('\n', ' ')
            report.append(f"**Description**: {docstring}.")
        
        # Add dependencies
        deps = map_data['dependencies'].get(rel_path, [])
        if deps:
            report.append(f"**Dependencies**: {', '.join(f'`{dep}`' for dep in sorted(deps))}")
        
        # Add classes
        if analysis['classes']:
            report.append(f"**Classes**:")
            for class_name, class_info in sorted(analysis['classes'].items()):
                bases = f" (extends {', '.join(class_info['bases'])})" if class_info['bases'] else ""
                report.append(f"- `{class_name}`{bases}")
        
        # Add functions
        if analysis['functions']:
            report.append(f"**Functions**:")
            for func_name, func_info in sorted(analysis['functions'].items()):
                resource = func_info.get('resource_focus', 'cpu')
                report.append(f"- `{func_name}` ({resource.upper()})")
        
        report.append("")
    
    # Write to file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
    
    return '\n'.join(report)


def split_codebase(directory, output_dir):
    """Split the entire codebase into resource-oriented components."""
    import importlib.util
    
    # Dynamically import resource_splitter
    spec = importlib.util.spec_from_file_location(
        "resource_splitter", 
        os.path.join(os.path.abspath(directory), "resource_splitter.py")
    )
    resource_splitter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resource_splitter)
    
    python_files = find_python_files(directory)
    results = {}
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for file_path in python_files:
        rel_path = os.path.relpath(file_path, directory)
        output_subdir = os.path.join(output_dir, rel_path.replace('.py', '_split'))
        
        try:
            # Skip files that are already in a split directory
            if '_split' in file_path or 'split_output' in file_path:
                continue
                
            # Skip the resource_splitter.py file itself to avoid recursion
            if os.path.basename(file_path) == 'resource_splitter.py':
                continue
                
            # Skip files that are too large or complex
            file_size = os.path.getsize(file_path)
            if file_size > 1000000:  # Skip files larger than 1MB
                results[rel_path] = {
                    'status': 'skipped',
                    'reason': f'File too large ({file_size} bytes)'
                }
                print(f"Skipping {rel_path}: File too large ({file_size} bytes)")
                continue
            
            # Split the file using the split_file_by_resource function
            print(f"Splitting {rel_path}...")
            manifest = resource_splitter.split_file_by_resource(file_path, output_subdir)
            
            if manifest and 'split_files' in manifest:
                component_count = len(manifest['split_files'])
                results[rel_path] = {
                    'status': 'success',
                    'components': component_count,
                    'output_dir': output_subdir
                }
                print(f"Split {rel_path} into {component_count} resource-oriented components")
            else:
                results[rel_path] = {
                    'status': 'error',
                    'error': 'Manifest not created properly'
                }
        except Exception as e:
            results[rel_path] = {
                'status': 'error',
                'error': str(e)
            }
            print(f"Error splitting {rel_path}: {str(e)}")
    
    return results


def main():
    """Main function for the code mapper."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Code Mapper Tool')
    parser.add_argument('--dir', type=str, default='.', help='Directory to analyze')
    parser.add_argument('--output', type=str, default='codebase_map.md', help='Output report file')
    parser.add_argument('--split', action='store_true', help='Split files into resource-oriented components')
    parser.add_argument('--split-dir', type=str, default='split_output', help='Output directory for split files')
    
    args = parser.parse_args()
    
    # Map the codebase
    print(f"Mapping codebase in {args.dir}...")
    map_data = map_codebase(args.dir)
    
    # Generate report
    print(f"Generating report to {args.output}...")
    generate_codebase_report(map_data, args.output)
    
    # Split files if requested
    if args.split:
        print(f"Splitting files into {args.split_dir}...")
        split_results = split_codebase(args.dir, args.split_dir)
        
        # Add split results to the report
        with open(args.output, 'a', encoding='utf-8') as f:
            f.write("\n\n## Split Results\n")
            for file, result in split_results.items():
                if result['status'] == 'success':
                    f.write(f"- `{file}`: Split into {result['components']} components in `{result['output_dir']}`\n")
                else:
                    f.write(f"- `{file}`: Error - {result['error']}\n")
    
    print("Done!")


if __name__ == "__main__":
    main()
