"""
Smart File Splitter

This script provides enhanced file splitting capabilities with a focus on:
1. Resource-oriented splitting
2. Logical directory organization
3. Reversible operations with manifests
4. Dependency management
5. Import resolution
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import ast
import re
import json

# Import the existing FileSplitter

class SmartSplitter:
    """Smart file splitting with resource-oriented organization and reversibility"""
    
    def __init__(self, base_output_dir: str = "smart_split"):
        self.base_output_dir = base_output_dir
        self.manifest = {
            "original_file": "",
            "split_files": [],
            "imports": {},
            "dependencies": {},
            "timestamp": "",
            "version": "1.0"
        }
    
    def split_file_by_resource(self, file_path: str, output_dir: str = None) -> Dict[str, Any]:
        """
        Split a Python file into resource-oriented components
        
        Args:
            file_path: Path to the Python file to split
            output_dir: Base directory for output (will create subdirectories)
            
        Returns:
            Manifest with details of the split operation
        """
        import time
        
        # Set up output directory
        if output_dir:
            self.base_output_dir = output_dir
        
        if not os.path.exists(self.base_output_dir):
            os.makedirs(self.base_output_dir)
        
        # Initialize manifest
        file_name = os.path.basename(file_path)
        base_name, _ = os.path.splitext(file_name)
        
        self.manifest["original_file"] = file_path
        self.manifest["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # First, split by functions to get the basic components
        function_dict = self._split_by_functions(file_path)
        
        # Analyze each function for resource focus
        resource_dict = self._categorize_by_resource(function_dict)
        
        # Create resource directories and write files
        split_files = self._write_resource_files(resource_dict, base_name)
        
        # Update manifest with split files
        self.manifest["split_files"] = split_files
        
        # Analyze and record dependencies
        self._analyze_dependencies(function_dict)
        
        # Write manifest
        manifest_path = os.path.join(self.base_output_dir, f"{base_name}_manifest.json")
        with open(manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
        
        return self.manifest
    
    def merge_from_manifest(self, manifest_path: str) -> str:
        """
        Merge split files back into a single file based on a manifest
        
        Args:
            manifest_path: Path to the manifest JSON file
            
        Returns:
            Path to the merged file
        """
        # Load manifest
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # Get original file path and create merged file path
        original_file = manifest["original_file"]
        file_name = os.path.basename(original_file)
        base_name, ext = os.path.splitext(file_name)
        
        merged_file_path = os.path.join(os.path.dirname(manifest_path), f"{base_name}_merged{ext}")
        
        # Collect all imports
        imports = set()
        for file_info in manifest["split_files"]:
            file_path = file_info["path"]
            with open(file_path, 'r') as f:
                content = f.read()
                
                # Extract imports
                import_lines = re.findall(r'^import .*$|^from .* import .*$', content, re.MULTILINE)
                for imp in import_lines:
                    imports.add(imp)
        
        # Start with imports
        with open(merged_file_path, 'w') as merged_file:
            # Write imports
            for imp in sorted(imports):
                merged_file.write(f"{imp}\n")
            
            merged_file.write("\n\n")
            
            # Write each function in dependency order
            dependency_order = self._get_dependency_order(manifest["dependencies"])
            
            for func_name in dependency_order:
                # Find the file containing this function
                for file_info in manifest["split_files"]:
                    if func_name == file_info["function_name"]:
                        file_path = file_info["path"]
                        with open(file_path, 'r') as f:
                            content = f.read()
                            
                            # Remove imports
                            content = re.sub(r'^import .*$|^from .* import .*$', '', content, flags=re.MULTILINE)
                            
                            # Remove empty lines at the beginning
                            content = re.sub(r'^\s*\n', '', content)
                            
                            merged_file.write(content)
                            merged_file.write("\n\n")
                        break
        
        return merged_file_path
    
    def _split_by_functions(self, file_path: str) -> Dict[str, str]:
        """Split a file by functions and return a dictionary of function name to code"""
        return FileSplitter.split_by_python_functions(file_path)
    
    def _categorize_by_resource(self, function_dict: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        """Categorize functions by resource focus"""
        resource_dict = {
            "cpu": {},
            "memory": {},
            "gpu": {},
            "network": {},
            "startup": {},
            "runtime": {},
            "ui": {},
            "core": {}
        }
        
        # Keywords that indicate resource focus
        resource_keywords = {
            "cpu": ["cpu", "processor", "compute", "calculation", "algorithm"],
            "memory": ["memory", "ram", "allocation", "buffer", "cache"],
            "gpu": ["gpu", "cuda", "graphics", "parallel", "acceleration"],
            "network": ["network", "http", "request", "download", "url", "api"],
            "startup": ["startup", "initialize", "boot", "load", "start"],
            "runtime": ["runtime", "performance", "optimize", "profile", "benchmark"],
            "ui": ["ui", "interface", "display", "render", "view", "button", "input", "widget"]
        }
        
        # Analyze each function
        for func_name, func_code in function_dict.items():
            # Default to core if no specific resource focus is found
            best_resource = "core"
            best_score = 0
            
            # Check for resource keywords
            for resource, keywords in resource_keywords.items():
                score = 0
                for keyword in keywords:
                    score += func_code.lower().count(keyword)
                
                if score > best_score:
                    best_score = score
                    best_resource = resource
            
            # Add to the appropriate resource category
            resource_dict[best_resource][func_name] = func_code
        
        return resource_dict
    
    def _write_resource_files(self, resource_dict: Dict[str, Dict[str, str]], base_name: str) -> List[Dict[str, str]]:
        """Write functions to resource-specific directories"""
        split_files = []
        
        for resource, functions in resource_dict.items():
            if not functions:
                continue
                
            # Create resource directory
            resource_dir = os.path.join(self.base_output_dir, resource)
            if not os.path.exists(resource_dir):
                os.makedirs(resource_dir)
            
            # Write each function to a separate file
            for func_name, func_code in functions.items():
                file_name = f"{base_name}_{func_name}.py"
                file_path = os.path.join(resource_dir, file_name)
                
                with open(file_path, 'w') as f:
                    f.write(func_code)
                
                split_files.append({
                    "path": file_path,
                    "resource": resource,
                    "function_name": func_name,
                    "size": len(func_code)
                })
        
        return split_files
    
    def _analyze_dependencies(self, function_dict: Dict[str, str]) -> None:
        """Analyze function dependencies and update the manifest"""
        dependencies = {}
        imports = {}
        
        # Parse each function to find dependencies
        for func_name, func_code in function_dict.items():
            # Parse the function
            try:
                tree = ast.parse(func_code)
                
                # Find imports
                imports[func_name] = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            imports[func_name].append(name.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ""
                        for name in node.names:
                            imports[func_name].append(f"{module}.{name.name}")
                
                # Find function calls
                dependencies[func_name] = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and hasattr(node.func, 'id'):
                        called_func = node.func.id
                        if called_func in function_dict and called_func != func_name:
                            dependencies[func_name].append(called_func)
            except Exception:
                # If parsing fails, just continue
                dependencies[func_name] = []
        
        self.manifest["dependencies"] = dependencies
        self.manifest["imports"] = imports
    
    def _get_dependency_order(self, dependencies: Dict[str, List[str]]) -> List[str]:
        """Get functions in dependency order (topological sort)"""
        # Create a set of all functions
        all_funcs = set(dependencies.keys())
        for deps in dependencies.values():
            all_funcs.update(deps)
        
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
        for func in all_funcs:
            if func not in visited:
                visit(func)
        
        # Reverse to get the correct order
        return result[::-1]

def main():
    """Main entry point for the script"""
    if len(sys.argv) < 3:
        print("Usage: python smart_splitter.py [split|merge] [file_path] [output_dir]")
        print("\nCommands:")
        print("  split [file_path] [output_dir] - Split a file into resource-oriented components")
        print("  merge [manifest_path] - Merge split files back into a single file")
        return
    
    command = sys.argv[1]
    file_path = sys.argv[2]
    
    splitter = SmartSplitter()
    
    if command == "split":
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "smart_split"
        manifest = splitter.split_file_by_resource(file_path, output_dir)
        print(f"Split {file_path} into {len(manifest['split_files'])} resource-oriented components")
        print(f"Manifest written to {os.path.join(output_dir, os.path.basename(file_path).split('.')[0] + '_manifest.json')}")
    
    elif command == "merge":
        merged_file = splitter.merge_from_manifest(file_path)
        print(f"Merged files into {merged_file}")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
