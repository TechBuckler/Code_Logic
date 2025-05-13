"""
Resource-Oriented File Splitter

This script splits Python files into resource-oriented components and
organizes them in a logical directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import ast
import json

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Try to import the module system
try:
    HAS_MODULE_SYSTEM = True
except ImportError:
    HAS_MODULE_SYSTEM = False

def analyze_resource_focus(func_code):
    """Analyze the resource focus of a function."""
    # Default to CPU focus
    resource = "cpu"
    
    # Check for GPU operations
    if any(keyword in func_code for keyword in ["cuda", "gpu", "tensor", "parallel"]):
        resource = "gpu"
    
    # Check for memory-intensive operations
    elif any(keyword in func_code for keyword in ["allocate", "buffer", "memory", "cache"]):
        resource = "memory"
    
    # Check for UI operations
    elif any(keyword in func_code for keyword in ["render", "display", "ui", "interface", "widget"]):
        resource = "ui"
    
    # Check for core operations
    elif any(keyword in func_code for keyword in ["initialize", "setup", "config", "__init__"]):
        resource = "core"
    
    # Check for network operations
    elif any(keyword in func_code for keyword in ["http", "request", "download", "upload", "socket"]):
        resource = "network"
    
    return resource

def analyze_resource_profile(func_code):
    """Analyze the resource profile of a function.
    Returns a dictionary with resource usage estimates.
    """
    # Default profile (moderate CPU and memory usage)
    profile = {
        'cpu': 0.5,     # Default CPU usage (0.0-1.0)
        'memory': 0.5,  # Default memory usage (0.0-1.0)
        'gpu': 0.0,     # Default GPU usage (0.0-1.0)
        'network': 0.0, # Default network usage (0.0-1.0)
        'startup': 0.3, # Default startup time impact (0.0-1.0)
        'runtime': 0.5  # Default runtime impact (0.0-1.0)
    }
    
    # Check for CPU-intensive operations
    if any(keyword in func_code for keyword in ["for", "while", "recursion", "sort", "search"]):
        profile['cpu'] = 0.8
        profile['runtime'] = 0.7
    
    # Check for memory-intensive operations
    if any(keyword in func_code for keyword in ["list", "dict", "set", "array", "dataframe"]):
        profile['memory'] = 0.8
    
    # Check for GPU operations
    if any(keyword in func_code for keyword in ["cuda", "gpu", "tensor", "parallel"]):
        profile['gpu'] = 0.9
        profile['cpu'] = 0.3  # GPU offloads CPU
    
    # Check for network operations
    if any(keyword in func_code for keyword in ["http", "request", "download", "upload", "socket"]):
        profile['network'] = 0.8
        profile['runtime'] = 0.8  # Network operations affect runtime
    
    # Check for startup impact
    if any(keyword in func_code for keyword in ["import", "load", "initialize", "setup"]):
        profile['startup'] = 0.7
    
    return profile

def extract_functions(file_path):
    """Extract all functions from a Python file"""
    # Ensure file_path is an absolute path
    file_path = os.path.abspath(file_path)
    
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        return {"imports": [], "functions": {}}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
        functions = {}
        imports = []
        
        # Extract imports first
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    import_str = f"import {name.name}"
                    if name.asname:
                        import_str += f" as {name.asname}"
                    imports.append(import_str)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names_str = ", ".join([n.name + (f" as {n.asname}" if n.asname else "") for n in node.names])
                imports.append(f"from {module} import {names_str}")
        
        # Extract functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get function name
                func_name = node.name
                
                # Get function source lines
                start_line = node.lineno
                end_line = max(node.body[-1].lineno if node.body else start_line,
                              max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')], default=start_line))
                
                # Extract function source
                func_lines = content.splitlines()[start_line-1:end_line]
                func_source = '\n'.join(func_lines)
                
                # Add to functions dict
                functions[func_name] = {
                    "source": func_source,
                    "lineno": start_line,
                    "end_lineno": end_line,
                    "dependencies": []
                }
        
        # Analyze function dependencies
        for func_name, func_info in functions.items():
            func_node = None
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func_name:
                    func_node = node
                    break
            
            if func_node:
                # Find function calls
                for node in ast.walk(func_node):
                    if isinstance(node, ast.Call) and hasattr(node.func, 'id'):
                        called_func = node.func.id
                        if called_func in functions and called_func != func_name:
                            if called_func not in func_info["dependencies"]:
                                func_info["dependencies"].append(called_func)
        
        return {"functions": functions, "imports": imports}
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return {"functions": {}, "imports": []}

def categorize_by_resource(functions_data):
    """Categorize functions by resource focus"""
    resource_categories = {
        "cpu": {},
        "memory": {},
        "gpu": {},
        "network": {},
        "ui": {},
        "core": {}
    }
    
    # Keywords that indicate resource focus
    resource_keywords = {
        "cpu": ["cpu", "processor", "compute", "calculation", "algorithm", "optimize", "performance"],
        "memory": ["memory", "ram", "allocation", "buffer", "cache", "heap", "stack"],
        "gpu": ["gpu", "cuda", "graphics", "parallel", "acceleration", "shader", "render"],
        "network": ["network", "http", "request", "download", "url", "api", "socket", "fetch"],
        "ui": ["ui", "interface", "display", "render", "view", "button", "input", "widget", "form", "click"]
    }
    

        
    # Analyze each function
    for func_name, func_info in functions_data["functions"].items():
        func_code = func_info["source"]
        
        # Determine resource focus
        resource = analyze_resource_focus(func_code)
        
        # Add to the appropriate resource category
        resource_categories[resource][func_name] = func_info
        
        # Add resource profile information
        func_info["resource_profile"] = analyze_resource_profile(func_code)
    
    return resource_categories

def get_dependency_order(functions_data):
    """Get functions in dependency order (topological sort)"""
    # Create a dictionary of function dependencies
    dependencies = {}
    for func_name, func_info in functions_data["functions"].items():
        dependencies[func_name] = func_info["dependencies"]
    
    # Initialize result and visited sets
    result = []
    visited = set()
    temp_visited = set()
    
    def visit(func):
        if func in temp_visited:
            # Cyclic dependency, break it
            return
        if func in visited:
            return
        
        temp_visited.add(func)
        
        # Visit dependencies
        if func in dependencies:
            for dep in dependencies[func]:
                visit(dep)
        
        temp_visited.remove(func)
        visited.add(func)
        result.append(func)
    
    # Visit all functions
    for func in dependencies.keys():
        if func not in visited:
            visit(func)
    
    # Reverse to get the correct order
    return result[::-1]

def split_file_by_resource(file_path, output_dir):
    """Split a Python file into resource-oriented components"""
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract functions and imports
    extracted_data = extract_functions(file_path)
    
    # Categorize by resource
    resource_categories = categorize_by_resource(extracted_data)
    
    # Create resource directories and write files
    file_name = os.path.basename(file_path)
    base_name, _ = os.path.splitext(file_name)
    
    manifest = {
        "original_file": file_path,
        "imports": extracted_data["imports"],
        "split_files": [],
        "dependencies": {},
        "resource_profiles": {func_name: func_info.get("resource_profile", {}) for func_name, func_info in extracted_data["functions"].items()}
    }
    
    # Add dependencies to manifest
    for func_name, func_info in extracted_data["functions"].items():
        manifest["dependencies"][func_name] = func_info["dependencies"]
    
    for resource, funcs in resource_categories.items():
        if not funcs:
            continue
        
        # Create resource directory
        resource_dir = os.path.join(output_dir, resource)
        if not os.path.exists(resource_dir):
            os.makedirs(resource_dir)
        
        # Create an __init__.py file to make the directory a package
        init_path = os.path.join(resource_dir, "__init__.py")
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write(f"""
{resource.upper()} Resource Module

This module contains functions focused on {resource} resource optimization.
""")
        
        # If module system is available, create a Module class for this resource
        if HAS_MODULE_SYSTEM:
            module_path = os.path.join(resource_dir, f"{resource}_module.py")
            with open(module_path, 'w', encoding='utf-8') as f:
                f.write(f"""
from module_system import Module

class {resource.capitalize()}Module(Module):
    def __init__(self, name):
        super().__init__(name)
        self.resource_type = '{resource}'
        self.resource_profile = {{
            'cpu': {0.5 if resource == 'cpu' else 0.3},
            'memory': {0.5 if resource == 'memory' else 0.3},
            'gpu': {0.8 if resource == 'gpu' else 0.0},
            'network': {0.8 if resource == 'network' else 0.0},
            'startup': {0.5 if resource == 'core' else 0.3},
            'runtime': {0.5 if resource in ['cpu', 'gpu'] else 0.3}
        }}
""")
        
        # Write each function to a file
        for func_name, func_info in funcs.items():
            func_code = func_info["source"]
            file_name = f"{base_name}_{func_name}.py"
            file_path = os.path.join(resource_dir, file_name)
            
            # Add imports to the function file
            with open(file_path, 'w', encoding='utf-8') as f:
                # Write imports
                for imp in extracted_data["imports"]:
                    f.write(f"{imp}\n")
                
                f.write("\n\n")
                
                # Write function dependencies if they're in a different resource
                for dep in func_info["dependencies"]:
                    # Find which resource the dependency is in
                    dep_resource = None
                    for res, res_funcs in resource_categories.items():
                        if dep in res_funcs:
                            dep_resource = res
                            break
                    
                    if dep_resource and dep_resource != resource:
                        f.write(f"from {dep_resource}.{base_name}_{dep} import {dep}\n")
                
                f.write("\n")
                
                # Write function code
                f.write(func_code)
            
            manifest["split_files"].append({
                "path": file_path,
                "resource": resource,
                "function": func_name,
                "dependencies": func_info["dependencies"]
            })
    
    # Write manifest
    manifest_path = os.path.join(output_dir, f"{base_name}_manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    return manifest

def merge_from_manifest(manifest_path):
    """Merge split files back into a single file"""
    # Load manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # Create merged file
    original_file = manifest["original_file"]
    file_name = os.path.basename(original_file)
    base_name, ext = os.path.splitext(file_name)
    
    merged_file_path = os.path.join(os.path.dirname(manifest_path), f"{base_name}_merged{ext}")
    
    with open(merged_file_path, 'w', encoding='utf-8') as f:
        # Write imports first
        if "imports" in manifest:
            for imp in manifest["imports"]:
                f.write(f"{imp}\n")
            f.write("\n\n")
        
        # Get dependency order
        if "dependencies" in manifest:
            # Create a dictionary of function dependencies
            dependencies = manifest["dependencies"]
            
            # Initialize result and visited sets
            result = []
            visited = set()
            temp_visited = set()
            
            def visit(func):
                if func in temp_visited:
                    # Cyclic dependency, break it
                    return
                if func in visited:
                    return
                
                temp_visited.add(func)
                
                # Visit dependencies
                if func in dependencies:
                    for dep in dependencies[func]:
                        visit(dep)
                
                temp_visited.remove(func)
                visited.add(func)
                result.append(func)
            
            # Visit all functions
            for func in dependencies.keys():
                if func not in visited:
                    visit(func)
            
            # Reverse to get the correct order
            ordered_functions = result[::-1]
            
            # Write functions in dependency order
            for func_name in ordered_functions:
                # Find the file containing this function
                for file_info in manifest["split_files"]:
                    if func_name == file_info["function"]:
                        file_path = file_info["path"]
                        with open(file_path, 'r', encoding='utf-8') as source_file:
                            content = source_file.read()
                            
                            # Remove imports and empty lines at the beginning
                            lines = content.split("\n")
                            start_idx = 0
                            for i, line in enumerate(lines):
                                if line.startswith("def "):
                                    start_idx = i
                                    break
                            
                            # Write function content
                            f.write("\n".join(lines[start_idx:]))
                            f.write("\n\n")
                        break
        else:
            # Fall back to simple merging if no dependencies
            for file_info in manifest["split_files"]:
                file_path = file_info["path"]
                
                with open(file_path, 'r', encoding='utf-8') as source_file:
                    content = source_file.read()
                    f.write(content)
                    f.write("\n\n")
    
    return merged_file_path

def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python resource_splitter.py [split|merge] [file_path] [output_dir]")
        return
    
    command = sys.argv[1]
    file_path = sys.argv[2]
    
    if command == "split":
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "resource_split"
        manifest = split_file_by_resource(file_path, output_dir)
        print(f"Split {file_path} into {len(manifest['split_files'])} resource-oriented components")
        
    elif command == "merge":
        merged_file = merge_from_manifest(file_path)
        print(f"Merged files into {merged_file}")
        
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
