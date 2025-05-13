"""
File Splitter and Merger Utility

This module provides utilities for splitting and merging files using various methods:
- Line-based splitting
- Byte-based splitting
- Token-based splitting (for Python code)
- Logical block splitting (for Python code)
- Compression-based splitting
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import ast
import zlib

class FileSplitter:
    """Utility for splitting and merging files using various methods"""
    
    @staticmethod
    def split_by_lines(file_path: str, lines_per_chunk: int, output_dir: str = None) -> List[str]:
        """
        Split a file into chunks based on number of lines
        
        Args:
            file_path: Path to the file to split
            lines_per_chunk: Number of lines per chunk
            output_dir: Directory to write the chunks to (None to return without writing)
            
        Returns:
            List of chunk contents or file paths if output_dir is provided
        """
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Split into chunks
        chunks = []
        for i in range(0, len(lines), lines_per_chunk):
            chunk = ''.join(lines[i:i+lines_per_chunk])
            chunks.append(chunk)
        
        # Write chunks to files if output_dir is provided
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            file_name = os.path.basename(file_path)
            base_name, ext = os.path.splitext(file_name)
            
            chunk_paths = []
            for i, chunk in enumerate(chunks):
                chunk_path = os.path.join(output_dir, f"{base_name}_part{i+1}{ext}")
                with open(chunk_path, 'w', encoding='utf-8') as f:
                    f.write(chunk)
                chunk_paths.append(chunk_path)
                
            return chunk_paths
        
        return chunks
    
    @staticmethod
    def split_by_bytes(file_path: str, bytes_per_chunk: int, output_dir: str = None) -> List[bytes]:
        """
        Split a file into chunks based on number of bytes
        
        Args:
            file_path: Path to the file to split
            bytes_per_chunk: Number of bytes per chunk
            output_dir: Directory to write the chunks to (None to return without writing)
            
        Returns:
            List of chunk contents or file paths if output_dir is provided
        """
        # Read the file
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Split into chunks
        chunks = []
        for i in range(0, len(content), bytes_per_chunk):
            chunk = content[i:i+bytes_per_chunk]
            chunks.append(chunk)
        
        # Write chunks to files if output_dir is provided
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            file_name = os.path.basename(file_path)
            base_name, ext = os.path.splitext(file_name)
            
            chunk_paths = []
            for i, chunk in enumerate(chunks):
                chunk_path = os.path.join(output_dir, f"{base_name}_part{i+1}{ext}")
                with open(chunk_path, 'wb') as f:
                    f.write(chunk)
                chunk_paths.append(chunk_path)
                
            return chunk_paths
        
        return chunks
    
    @staticmethod
    def split_by_python_classes(file_path: str, output_dir: str = None) -> Dict[str, str]:
        """
        Split a Python file into chunks based on class definitions
        
        Args:
            file_path: Path to the Python file to split
            output_dir: Directory to write the chunks to (None to return without writing)
            
        Returns:
            Dictionary mapping class names to their code or file paths if output_dir is provided
        """
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the Python code
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
            return {}
        
        # Extract imports and other top-level code
        imports = []
        top_level = []
        
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Extract import statements
                imports.append(ast.get_source_segment(content, node))
            elif not isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                # Extract other top-level code (not classes or functions)
                top_level.append(ast.get_source_segment(content, node))
        
        # Combine imports and top-level code
        header = '\n'.join(imports + [''] + top_level + [''])
        
        # Extract classes
        classes = {}
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                class_code = ast.get_source_segment(content, node)
                classes[class_name] = header + class_code
        
        # Write chunks to files if output_dir is provided
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            file_name = os.path.basename(file_path)
            base_name, ext = os.path.splitext(file_name)
            
            class_paths = {}
            for class_name, class_code in classes.items():
                class_path = os.path.join(output_dir, f"{base_name}_{class_name}{ext}")
                with open(class_path, 'w', encoding='utf-8') as f:
                    f.write(class_code)
                class_paths[class_name] = class_path
                
            return class_paths
        
        return classes
    
    @staticmethod
    def split_by_python_functions(file_path: str, output_dir: str = None) -> Dict[str, str]:
        """
        Split a Python file into chunks based on function definitions
        
        Args:
            file_path: Path to the Python file to split
            output_dir: Directory to write the chunks to (None to return without writing)
            
        Returns:
            Dictionary mapping function names to their code or file paths if output_dir is provided
        """
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the Python code
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
            return {}
        
        # Extract imports and other top-level code
        imports = []
        top_level = []
        
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Extract import statements
                imports.append(ast.get_source_segment(content, node))
            elif not isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                # Extract other top-level code (not classes or functions)
                top_level.append(ast.get_source_segment(content, node))
        
        # Combine imports and top-level code
        header = '\n'.join(imports + [''] + top_level + [''])
        
        # Extract functions
        functions = {}
        
        # Top-level functions
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                func_code = ast.get_source_segment(content, node)
                functions[func_name] = header + func_code
        
        # Class methods
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                
                for subnode in node.body:
                    if isinstance(subnode, ast.FunctionDef):
                        method_name = subnode.name
                        full_name = f"{class_name}.{method_name}"
                        
                        # Get the class definition
                        class_code = ast.get_source_segment(content, node)
                        
                        # Split the class code to extract just the method
                        method_code = ast.get_source_segment(content, subnode)
                        
                        # Create a minimal class with just this method
                        minimal_class = f"{header}\nclass {class_name}:\n"
                        # Indent the method code
                        method_lines = method_code.split('\n')
                        indented_method = '\n'.join(['    ' + line for line in method_lines])
                        minimal_class += indented_method
                        
                        functions[full_name] = minimal_class
        
        # Write chunks to files if output_dir is provided
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            file_name = os.path.basename(file_path)
            base_name, ext = os.path.splitext(file_name)
            
            func_paths = {}
            for func_name, func_code in functions.items():
                safe_name = func_name.replace('.', '_')
                func_path = os.path.join(output_dir, f"{base_name}_{safe_name}{ext}")
                with open(func_path, 'w', encoding='utf-8') as f:
                    f.write(func_code)
                func_paths[func_name] = func_path
                
            return func_paths
        
        return functions
    
    @staticmethod
    def split_with_compression(file_path: str, bytes_per_chunk: int, output_dir: str = None) -> List[bytes]:
        """
        Split a file into compressed chunks
        
        Args:
            file_path: Path to the file to split
            bytes_per_chunk: Number of bytes per chunk before compression
            output_dir: Directory to write the chunks to (None to return without writing)
            
        Returns:
            List of compressed chunk contents or file paths if output_dir is provided
        """
        # Read the file
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Split into chunks and compress
        chunks = []
        for i in range(0, len(content), bytes_per_chunk):
            chunk = content[i:i+bytes_per_chunk]
            compressed = zlib.compress(chunk)
            chunks.append(compressed)
        
        # Write chunks to files if output_dir is provided
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            file_name = os.path.basename(file_path)
            base_name, ext = os.path.splitext(file_name)
            
            chunk_paths = []
            for i, chunk in enumerate(chunks):
                chunk_path = os.path.join(output_dir, f"{base_name}_part{i+1}.z{ext}")
                with open(chunk_path, 'wb') as f:
                    f.write(chunk)
                chunk_paths.append(chunk_path)
                
            return chunk_paths
        
        return chunks
    
    @staticmethod
    def merge_files(file_paths: List[str], output_path: str, is_binary: bool = False) -> bool:
        """
        Merge multiple files into a single file
        
        Args:
            file_paths: List of paths to the files to merge
            output_path: Path to the output file
            is_binary: Whether the files are binary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            mode = 'wb' if is_binary else 'w'
            read_mode = 'rb' if is_binary else 'r'
            
            with open(output_path, mode) as out_file:
                for file_path in file_paths:
                    with open(file_path, read_mode) as in_file:
                        out_file.write(in_file.read())
            
            return True
        except Exception as e:
            print(f"Error merging files: {e}")
            return False
    
    @staticmethod
    def merge_compressed_files(file_paths: List[str], output_path: str) -> bool:
        """
        Merge multiple compressed files into a single file
        
        Args:
            file_paths: List of paths to the compressed files to merge
            output_path: Path to the output file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, 'wb') as out_file:
                for file_path in file_paths:
                    with open(file_path, 'rb') as in_file:
                        compressed = in_file.read()
                        decompressed = zlib.decompress(compressed)
                        out_file.write(decompressed)
            
            return True
        except Exception as e:
            print(f"Error merging compressed files: {e}")
            return False

def main():
    """Main entry point for the script"""
    if len(sys.argv) < 3:
        print("Usage: python file_splitter.py [split|merge] [method] [file_path] [options]")
        print("\nSplit Methods:")
        print("  lines [lines_per_chunk] [output_dir]")
        print("  bytes [bytes_per_chunk] [output_dir]")
        print("  classes [output_dir]")
        print("  functions [output_dir]")
        print("  compress [bytes_per_chunk] [output_dir]")
        print("\nMerge Methods:")
        print("  text [output_path] [file1] [file2] ...")
        print("  binary [output_path] [file1] [file2] ...")
        print("  decompress [output_path] [file1] [file2] ...")
        return
    
    command = sys.argv[1]
    method = sys.argv[2]
    
    if command == "split":
        file_path = sys.argv[3]
        
        if method == "lines":
            lines_per_chunk = int(sys.argv[4])
            output_dir = sys.argv[5] if len(sys.argv) > 5 else None
            result = FileSplitter.split_by_lines(file_path, lines_per_chunk, output_dir)
            print(f"Split {file_path} into {len(result)} chunks")
            
        elif method == "bytes":
            bytes_per_chunk = int(sys.argv[4])
            output_dir = sys.argv[5] if len(sys.argv) > 5 else None
            result = FileSplitter.split_by_bytes(file_path, bytes_per_chunk, output_dir)
            print(f"Split {file_path} into {len(result)} chunks")
            
        elif method == "classes":
            output_dir = sys.argv[4] if len(sys.argv) > 4 else None
            result = FileSplitter.split_by_python_classes(file_path, output_dir)
            print(f"Split {file_path} into {len(result)} classes")
            
        elif method == "functions":
            output_dir = sys.argv[4] if len(sys.argv) > 4 else None
            result = FileSplitter.split_by_python_functions(file_path, output_dir)
            print(f"Split {file_path} into {len(result)} functions")
            
        elif method == "compress":
            bytes_per_chunk = int(sys.argv[4])
            output_dir = sys.argv[5] if len(sys.argv) > 5 else None
            result = FileSplitter.split_with_compression(file_path, bytes_per_chunk, output_dir)
            print(f"Split {file_path} into {len(result)} compressed chunks")
            
        else:
            print(f"Unknown split method: {method}")
    
    elif command == "merge":
        output_path = sys.argv[3]
        file_paths = sys.argv[4:]
        
        if method == "text":
            result = FileSplitter.merge_files(file_paths, output_path, False)
            print(f"Merged {len(file_paths)} files into {output_path}: {'Success' if result else 'Failed'}")
            
        elif method == "binary":
            result = FileSplitter.merge_files(file_paths, output_path, True)
            print(f"Merged {len(file_paths)} binary files into {output_path}: {'Success' if result else 'Failed'}")
            
        elif method == "decompress":
            result = FileSplitter.merge_compressed_files(file_paths, output_path)
            print(f"Merged {len(file_paths)} compressed files into {output_path}: {'Success' if result else 'Failed'}")
            
        else:
            print(f"Unknown merge method: {method}")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
