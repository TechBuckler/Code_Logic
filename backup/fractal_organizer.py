"""
Fractal Code Organizer

This module enforces extreme modularity by recursively breaking down code into
smaller and smaller components, while providing mechanisms to navigate and
"bubble up" the structure when needed.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import ast
import json
# Maximum depth of fractal organization
MAX_FRACTAL_DEPTH = 5

# Minimum size to consider splitting (don't split tiny files)
MIN_SPLIT_SIZE = 100  # lines

class FractalNode:
    """Represents a node in the fractal code structure."""
    
    def __init__(self, name, path, parent=None):
        self.name = name
        self.path = path
        self.parent = parent
        self.children = []
        self.functions = {}
        self.imports = []
        self.level = 0 if parent is None else parent.level + 1
        
    def add_child(self, child):
        """Add a child node to this node."""
        self.children.append(child)
        child.parent = self
        
    def add_function(self, name, code, resource_type="cpu"):
        """Add a function to this node."""
        self.functions[name] = {
            "code": code,
            "resource_type": resource_type
        }
        
    def to_dict(self):
        """Convert the node to a dictionary."""
        return {
            "name": self.name,
            "path": str(self.path),
            "level": self.level,
            "functions": list(self.functions.keys()),
            "children": [child.to_dict() for child in self.children]
        }
        
    def __str__(self):
        return f"FractalNode({self.name}, level={self.level}, functions={len(self.functions)}, children={len(self.children)})"


class FractalAnalyzer:
    """Analyzes code to create a fractal structure."""
    
    def __init__(self):
        self.root = None
        
    def analyze_directory(self, directory):
        """Analyze a directory and create a fractal structure."""
        directory = Path(directory)
        self.root = FractalNode(directory.name, directory)
        
        # Find all Python files
        python_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        # Analyze each file
        for file_path in python_files:
            rel_path = os.path.relpath(file_path, directory)
            self._analyze_file(file_path, rel_path)
            
        return self.root
    
    def _analyze_file(self, file_path, rel_path):
        """Analyze a Python file and add it to the fractal structure."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse the file
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # Skip files with syntax errors
            return
            
        # Extract functions
        functions = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get function source
                func_lines = content.splitlines()[node.lineno-1:node.end_lineno]
                func_source = "\n".join(func_lines)
                
                # Add to functions dictionary
                functions[node.name] = func_source
        
        # Create path components
        path_parts = rel_path.split(os.sep)
        
        # Navigate to the correct node
        current = self.root
        for part in path_parts[:-1]:  # All except the file name
            # Find or create child node
            found = False
            for child in current.children:
                if child.name == part:
                    current = child
                    found = True
                    break
                    
            if not found:
                # Create new node
                new_path = current.path / part
                new_node = FractalNode(part, new_path, current)
                current.add_child(new_node)
                current = new_node
        
        # Add file node
        file_name = path_parts[-1]
        file_node = FractalNode(file_name, current.path / file_name, current)
        current.add_child(file_node)
        
        # Add functions to file node
        for func_name, func_source in functions.items():
            file_node.add_function(func_name, func_source)


class FractalSplitter:
    """Splits code into a fractal structure."""
    
    def __init__(self, max_functions=MAX_FUNCTIONS_PER_FILE, 
                 max_lines=MAX_LINES_PER_FUNCTION,
                 max_depth=MAX_FRACTAL_DEPTH):
        self.max_functions = max_functions
        self.max_lines = max_lines
        self.max_depth = max_depth
        
    def split_directory(self, src_dir, dest_dir):
        """Split a directory into a fractal structure."""
        src_dir = Path(src_dir)
        dest_dir = Path(dest_dir)
        
        # Create destination directory
        os.makedirs(dest_dir, exist_ok=True)
        
        # Find all Python files
        python_files = []
        for root, _, files in os.walk(src_dir):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        # Process each file
        for file_path in python_files:
            rel_path = os.path.relpath(file_path, src_dir)
            dest_path = dest_dir / rel_path
            
            # Create parent directories
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Split the file
            self.split_file(file_path, dest_path)
    
    def split_file(self, src_file, dest_file):
        """Split a file into a fractal structure."""
        with open(src_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Skip small files
        if len(content.splitlines()) < MIN_SPLIT_SIZE:
            # Just copy the file
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            with open(dest_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return
            
        # Parse the file
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # Just copy files with syntax errors
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            with open(dest_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return
            
        # Extract imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    import_str = f"import {name.name}"
                    if name.asname:
                        import_str += f" as {name.asname}"
                    imports.append(import_str)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for name in node.names:
                    import_str = f"from {module} import {name.name}"
                    if name.asname:
                        import_str += f" as {name.asname}"
                    imports.append(import_str)
        
        # Extract functions and classes
        functions = {}
        classes = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get function source
                func_lines = content.splitlines()[node.lineno-1:node.end_lineno]
                func_source = "\n".join(func_lines)
                
                # Add to functions dictionary
                functions[node.name] = {
                    "source": func_source,
                    "lines": node.end_lineno - node.lineno + 1
                }
            elif isinstance(node, ast.ClassDef):
                # Get class source
                class_lines = content.splitlines()[node.lineno-1:node.end_lineno]
                class_source = "\n".join(class_lines)
                
                # Add to classes dictionary
                classes[node.name] = {
                    "source": class_source,
                    "lines": node.end_lineno - node.lineno + 1
                }
        
        # Check if we need to split
        if len(functions) + len(classes) <= self.max_functions:
            # No need to split, just copy the file
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            with open(dest_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return
            
        # Create fractal structure
        base_name = os.path.splitext(os.path.basename(dest_file))[0]
        fractal_dir = os.path.join(os.path.dirname(dest_file), f"{base_name}_fractal")
        os.makedirs(fractal_dir, exist_ok=True)
        
        # Create __init__.py to make it a package
        init_path = os.path.join(fractal_dir, "__init__.py")
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write(f'"""\nFractal package for {base_name}\n"""\n\n')
            
            # Add imports
            for imp in imports:
                f.write(f"{imp}\n")
            
            f.write("\n")
            
            # Add imports for all functions and classes
            for func_name in functions:
                f.write(f"from .{func_name} import {func_name}\n")
            
            for class_name in classes:
                f.write(f"from .{class_name} import {class_name}\n")
        
        # Create a file for each function
        for func_name, func_info in functions.items():
            func_path = os.path.join(fractal_dir, f"{func_name}.py")
            
            with open(func_path, 'w', encoding='utf-8') as f:
                f.write(f'"""\nFunction {func_name} from {base_name}\n"""\n\n')
                
                # Add imports
                for imp in imports:
                    f.write(f"{imp}\n")
                
                # Add imports for all other functions and classes
                for other_func in functions:
                    if other_func != func_name:
                        f.write(f"from .{other_func} import {other_func}\n")
                
                for class_name in classes:
                    f.write(f"from .{class_name} import {class_name}\n")
                
                f.write("\n")
                f.write(func_info["source"])
        
        # Create a file for each class
        for class_name, class_info in classes.items():
            class_path = os.path.join(fractal_dir, f"{class_name}.py")
            
            with open(class_path, 'w', encoding='utf-8') as f:
                f.write(f'"""\nClass {class_name} from {base_name}\n"""\n\n')
                
                # Add imports
                for imp in imports:
                    f.write(f"{imp}\n")
                
                # Add imports for all functions
                for func_name in functions:
                    f.write(f"from .{func_name} import {func_name}\n")
                
                # Add imports for all other classes
                for other_class in classes:
                    if other_class != class_name:
                        f.write(f"from .{other_class} import {other_class}\n")
                
                f.write("\n")
                f.write(class_info["source"])
        
        # Create a proxy file that imports everything from the fractal package
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(f'"""\nProxy module for {base_name}\n"""\n\n')
            f.write(f"from {base_name}_fractal import *\n")


class FractalNavigator:
    """Navigates a fractal code structure."""
    
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.current_dir = self.root_dir
        self.history = [self.root_dir]
        
    def go_up(self):
        """Go up one level in the fractal structure."""
        if len(self.history) > 1:
            self.history.pop()
            self.current_dir = self.history[-1]
            return True
        return False
        
    def go_down(self, name):
        """Go down into a child directory."""
        child_dir = self.current_dir / name
        if child_dir.is_dir():
            self.current_dir = child_dir
            self.history.append(child_dir)
            return True
        return False
        
    def list_current(self):
        """List the contents of the current directory."""
        result = {
            "path": str(self.current_dir),
            "directories": [],
            "files": [],
            "functions": []
        }
        
        # List directories
        for item in self.current_dir.iterdir():
            if item.is_dir() and not item.name.startswith('__'):
                result["directories"].append(item.name)
        
        # List Python files
        for item in self.current_dir.iterdir():
            if item.is_file() and item.name.endswith('.py') and not item.name.startswith('__'):
                result["files"].append(item.name)
                
                # Extract functions from the file
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        content = f.read()
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            result["functions"].append({
                                "name": node.name,
                                "file": item.name
                            })
                except Exception:
                    pass
        
        return result
    
    def find_function(self, name):
        """Find a function in the fractal structure."""
        results = []
        
        def search_dir(directory):
            # Search Python files in this directory
            for item in directory.iterdir():
                if item.is_file() and item.name.endswith('.py'):
                    try:
                        with open(item, 'r', encoding='utf-8') as f:
                            content = f.read()
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef) and node.name == name:
                                results.append({
                                    "path": str(item),
                                    "line": node.lineno
                                })
                    except Exception:
                        pass
                        
            # Recursively search subdirectories
            for item in directory.iterdir():
                if item.is_dir() and not item.name.startswith('__'):
                    search_dir(item)
        
        search_dir(self.root_dir)
        return results


class FractalBubbler:
    """Bubbles up code from a fractal structure."""
    
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        
    def bubble_up(self, target_dir, max_depth=2):
        """Bubble up code from deeper levels to a maximum depth."""
        target_dir = Path(target_dir)
        
        # Find all Python files deeper than max_depth
        deep_files = []
        for root, dirs, files in os.walk(target_dir):
            path = Path(root)
            # Calculate depth relative to target_dir
            depth = len(path.relative_to(target_dir).parts)
            
            if depth > max_depth:
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        deep_files.append(os.path.join(root, file))
        
        # Process each deep file
        for file_path in deep_files:
            # Calculate the new path at max_depth
            rel_path = os.path.relpath(file_path, target_dir)
            parts = rel_path.split(os.sep)
            
            if len(parts) <= max_depth + 1:
                continue  # Already at or above max_depth
                
            # Create new path at max_depth
            new_parts = parts[:max_depth] + ['bubbled_' + '_'.join(parts[max_depth:-1]) + '_' + parts[-1]]
            new_path = os.path.join(target_dir, *new_parts)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            
            # Copy the file
            with open(file_path, 'r', encoding='utf-8') as src:
                content = src.read()
                
            with open(new_path, 'w', encoding='utf-8') as dest:
                # Add a comment about the original location
                dest.write(f'"""\nBubbled up from {rel_path}\n"""\n\n')
                dest.write(content)
            
            # Remove the original file
            os.remove(file_path)
            
            # Check if the directory is now empty and remove it if so
            dir_path = os.path.dirname(file_path)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
    
    def create_index(self, target_dir):
        """Create an index of all functions in the fractal structure."""
        target_dir = Path(target_dir)
        index = {}
        
        # Find all Python files
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, target_dir)
                    
                    # Extract functions
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                if node.name not in index:
                                    index[node.name] = []
                                index[node.name].append({
                                    "path": rel_path,
                                    "line": node.lineno
                                })
                    except Exception:
                        pass
        
        # Write index to file
        index_path = target_dir / "fractal_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
            
        return index


def main():
    """Main function for the fractal organizer."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fractal Code Organizer')
    parser.add_argument('--analyze', action='store_true', help='Analyze a directory')
    parser.add_argument('--split', action='store_true', help='Split a directory into a fractal structure')
    parser.add_argument('--bubble', action='store_true', help='Bubble up code from a fractal structure')
    parser.add_argument('--index', action='store_true', help='Create an index of functions')
    parser.add_argument('--src', type=str, default='.', help='Source directory')
    parser.add_argument('--dest', type=str, default='fractal_output', help='Destination directory')
    parser.add_argument('--max-functions', type=int, default=MAX_FUNCTIONS_PER_FILE, help='Maximum functions per file')
    parser.add_argument('--max-lines', type=int, default=MAX_LINES_PER_FUNCTION, help='Maximum lines per function')
    parser.add_argument('--max-depth', type=int, default=MAX_FRACTAL_DEPTH, help='Maximum fractal depth')
    
    args = parser.parse_args()
    
    if args.analyze:
        analyzer = FractalAnalyzer()
        root = analyzer.analyze_directory(args.src)
        print(f"Analyzed {args.src}")
        print(f"Root: {root}")
        print(f"Total nodes: {len(list(root.children))}")
        
    if args.split:
        splitter = FractalSplitter(args.max_functions, args.max_lines, args.max_depth)
        splitter.split_directory(args.src, args.dest)
        print(f"Split {args.src} into {args.dest}")
        
    if args.bubble:
        bubbler = FractalBubbler(args.dest)
        bubbler.bubble_up(args.dest, args.max_depth)
        print(f"Bubbled up code in {args.dest} to maximum depth {args.max_depth}")
        
    if args.index:
        bubbler = FractalBubbler(args.dest)
        index = bubbler.create_index(args.dest)
        print(f"Created index with {len(index)} functions")


if __name__ == "__main__":
    main()