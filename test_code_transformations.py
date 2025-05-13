#!/usr/bin/env python
"""
Test Code Transformations

This script tests how different code transformations affect validation results
using the Enhanced Shadow validation system.
"""

import os
import sys
import ast
import time
import json
import hashlib
import logging
from typing import Dict, List, Any, Optional, Tuple

# Fix imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.import_utils import fix_imports
fix_imports()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='transformation_test.log'
)
logger = logging.getLogger('code_transformations')

# Import the enhanced shadow validator
try:
    from tools.validation.enhanced_shadow_validator import EnhancedShadowValidator, format_validation_result
except ImportError:
    logger.error("Failed to import EnhancedShadowValidator. Make sure the module is available.")
    sys.exit(1)

class CodeTransformer:
    """
    Applies various code transformations to Python code.
    """
    def __init__(self):
        """Initialize the code transformer."""
        self.transformations = {
            "original": self.original,
            "remove_comments": self.remove_comments,
            "rename_variables": self.rename_variables,
            "constant_folding": self.constant_folding,
            "minify": self.minify,
            "optimize_imports": self.optimize_imports,
            "all": self.apply_all_transformations
        }
    
    def original(self, code: str) -> str:
        """Return the original code unchanged."""
        return code
    
    def remove_comments(self, code: str) -> str:
        """Remove comments from the code."""
        try:
            # Parse the code to an AST
            tree = ast.parse(code)
            
            # Create a new code string without comments
            lines = code.split('\n')
            result_lines = []
            
            for i, line in enumerate(lines):
                # Remove inline comments
                comment_pos = line.find('#')
                if comment_pos >= 0:
                    line = line[:comment_pos].rstrip()
                
                # Skip empty lines
                if line.strip():
                    result_lines.append(line)
            
            return '\n'.join(result_lines)
        except Exception as e:
            logger.error(f"Error removing comments: {str(e)}")
            return code
    
    def rename_variables(self, code: str) -> str:
        """Rename variables to shorter names."""
        try:
            class VariableRenamer(ast.NodeTransformer):
                def __init__(self):
                    self.var_map = {}
                    self.counter = 0
                
                def visit_Name(self, node):
                    if isinstance(node.ctx, ast.Store):
                        if node.id not in self.var_map and not node.id.startswith('__'):
                            self.var_map[node.id] = f"v{self.counter}"
                            self.counter += 1
                    
                    if node.id in self.var_map:
                        node.id = self.var_map[node.id]
                    
                    return node
            
            # Parse the code to an AST
            tree = ast.parse(code)
            
            # Apply the transformer
            transformer = VariableRenamer()
            new_tree = transformer.visit(tree)
            
            # Generate new code
            return ast.unparse(new_tree)
        except Exception as e:
            logger.error(f"Error renaming variables: {str(e)}")
            return code
    
    def constant_folding(self, code: str) -> str:
        """Fold constant expressions."""
        try:
            class ConstantFolder(ast.NodeTransformer):
                def visit_BinOp(self, node):
                    # Recursively visit children
                    self.generic_visit(node)
                    
                    # Check if both operands are constants
                    if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                        try:
                            # Evaluate the expression
                            if isinstance(node.op, ast.Add):
                                result = node.left.value + node.right.value
                            elif isinstance(node.op, ast.Sub):
                                result = node.left.value - node.right.value
                            elif isinstance(node.op, ast.Mult):
                                result = node.left.value * node.right.value
                            elif isinstance(node.op, ast.Div):
                                result = node.left.value / node.right.value
                            elif isinstance(node.op, ast.FloorDiv):
                                result = node.left.value // node.right.value
                            elif isinstance(node.op, ast.Mod):
                                result = node.left.value % node.right.value
                            elif isinstance(node.op, ast.Pow):
                                result = node.left.value ** node.right.value
                            else:
                                return node
                            
                            # Replace with a constant node
                            return ast.Constant(value=result)
                        except Exception:
                            return node
                    
                    return node
            
            # Parse the code to an AST
            tree = ast.parse(code)
            
            # Apply the transformer
            transformer = ConstantFolder()
            new_tree = transformer.visit(tree)
            
            # Generate new code
            return ast.unparse(new_tree)
        except Exception as e:
            logger.error(f"Error folding constants: {str(e)}")
            return code
    
    def minify(self, code: str) -> str:
        """Minify the code by removing whitespace."""
        try:
            # Remove comments first
            code = self.remove_comments(code)
            
            # Parse the code to an AST
            tree = ast.parse(code)
            
            # Generate minified code
            return ast.unparse(tree)
        except Exception as e:
            logger.error(f"Error minifying code: {str(e)}")
            return code
    
    def optimize_imports(self, code: str) -> str:
        """Optimize imports by removing unused ones."""
        try:
            class ImportOptimizer(ast.NodeTransformer):
                def __init__(self):
                    self.used_names = set()
                    self.imports = []
                
                def visit_Name(self, node):
                    self.used_names.add(node.id)
                    return node
                
                def visit_Import(self, node):
                    for name in node.names:
                        if name.asname:
                            if name.asname in self.used_names:
                                self.imports.append(node)
                                break
                        elif name.name.split('.')[0] in self.used_names:
                            self.imports.append(node)
                            break
                    return None
                
                def visit_ImportFrom(self, node):
                    for name in node.names:
                        if name.asname:
                            if name.asname in self.used_names:
                                self.imports.append(node)
                                break
                        elif name.name in self.used_names:
                            self.imports.append(node)
                            break
                    return None
                
                def get_optimized_tree(self, tree):
                    # First pass: collect used names
                    self.visit(tree)
                    
                    # Second pass: create a new tree with only used imports
                    new_tree = ast.Module(body=[], type_ignores=[])
                    
                    # Add imports first
                    for imp in self.imports:
                        new_tree.body.append(imp)
                    
                    # Add the rest of the code
                    for node in tree.body:
                        if not isinstance(node, (ast.Import, ast.ImportFrom)):
                            new_tree.body.append(node)
                    
                    return new_tree
            
            # Parse the code to an AST
            tree = ast.parse(code)
            
            # Apply the optimizer
            optimizer = ImportOptimizer()
            new_tree = optimizer.get_optimized_tree(tree)
            
            # Generate new code
            return ast.unparse(new_tree)
        except Exception as e:
            logger.error(f"Error optimizing imports: {str(e)}")
            return code
    
    def apply_all_transformations(self, code: str) -> str:
        """Apply all transformations in sequence."""
        code = self.remove_comments(code)
        code = self.optimize_imports(code)
        code = self.constant_folding(code)
        code = self.rename_variables(code)
        code = self.minify(code)
        return code
    
    def transform(self, code: str, transformation: str) -> str:
        """
        Apply a transformation to the code.
        
        Args:
            code: The code to transform
            transformation: The name of the transformation to apply
            
        Returns:
            The transformed code
        """
        if transformation not in self.transformations:
            logger.warning(f"Unknown transformation: {transformation}")
            return code
        
        return self.transformations[transformation](code)

def test_transformations(file_path: str, output_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Test how different code transformations affect validation results.
    
    Args:
        file_path: Path to the file to test
        output_file: Optional path to save the results
        
    Returns:
        A dictionary with test results
    """
    try:
        # Read the file
        with open(file_path, 'r') as f:
            code = f.read()
        
        # Create transformer and validator
        transformer = CodeTransformer()
        validator = EnhancedShadowValidator()
        
        # Test each transformation
        results = {
            "file_path": file_path,
            "transformations": {}
        }
        
        for name in transformer.transformations:
            # Transform the code
            transformed_code = transformer.transform(code, name)
            
            # Calculate hash for the transformed code
            code_hash = hashlib.md5(transformed_code.encode()).hexdigest()
            
            # Validate the transformed code
            validation_result = validator.validate_code(transformed_code)
            
            # Add to results
            results["transformations"][name] = {
                "code_hash": code_hash,
                "validation_result": validation_result,
                "code_size": len(transformed_code),
                "lines_of_code": len(transformed_code.split('\n'))
            }
            
            # Print results
            print(f"\nTransformation: {name}")
            print(f"Code size: {len(transformed_code)} bytes")
            print(f"Lines of code: {len(transformed_code.split('\n'))}")
            format_validation_result(validation_result)
        
        # Save results if requested
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {output_file}")
        
        return results
    except Exception as e:
        logger.error(f"Error testing transformations: {str(e)}")
        return {
            "error": str(e),
            "file_path": file_path
        }

def compare_transformations(results: Dict[str, Any]) -> None:
    """
    Compare the results of different transformations.
    
    Args:
        results: The test results
    """
    print("\n" + "=" * 80)
    print("TRANSFORMATION COMPARISON")
    print("=" * 80)
    
    # Extract transformations
    transformations = results.get("transformations", {})
    if not transformations:
        print("No transformation results available.")
        return
    
    # Compare validation results
    print("\nVALIDATION STATUS COMPARISON:")
    for name, result in transformations.items():
        validation = result.get("validation_result", {})
        status = validation.get("status", "UNKNOWN")
        confidence = validation.get("confidence", 0.0)
        source = validation.get("source", "unknown")
        cost = validation.get("cost", 0.0)
        
        print(f"{name:20} | Status: {status:10} | Confidence: {confidence:.2f} | Source: {source:15} | Cost: ${cost:.6f}")
    
    # Compare code metrics
    print("\nCODE METRICS COMPARISON:")
    original_size = transformations.get("original", {}).get("code_size", 0)
    original_lines = transformations.get("original", {}).get("lines_of_code", 0)
    
    for name, result in transformations.items():
        size = result.get("code_size", 0)
        lines = result.get("lines_of_code", 0)
        
        if original_size > 0:
            size_diff = ((size - original_size) / original_size) * 100
        else:
            size_diff = 0.0
        
        if original_lines > 0:
            lines_diff = ((lines - original_lines) / original_lines) * 100
        else:
            lines_diff = 0.0
        
        print(f"{name:20} | Size: {size:6} bytes ({size_diff:+.1f}%) | Lines: {lines:4} ({lines_diff:+.1f}%)")
    
    # Compare validation suggestions
    print("\nVALIDATION SUGGESTIONS COMPARISON:")
    for name, result in transformations.items():
        validation = result.get("validation_result", {})
        suggestions = validation.get("suggestions", [])
        
        print(f"\n{name} ({len(suggestions)} suggestions):")
        for i, suggestion in enumerate(suggestions[:5], 1):
            print(f"{i}. {suggestion}")
        
        if len(suggestions) > 5:
            print(f"... and {len(suggestions) - 5} more suggestions.")
    
    print("=" * 80)

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test code transformations with the Enhanced Shadow validation system.')
    parser.add_argument('file', help='Path to the Python file to test')
    parser.add_argument('--output', '-o', help='Output file for test results (JSON format)')
    parser.add_argument('--compare', '-c', action='store_true', help='Compare transformation results')
    
    args = parser.parse_args()
    
    # Test transformations
    results = test_transformations(args.file, args.output)
    
    # Compare transformations if requested
    if args.compare:
        compare_transformations(results)

if __name__ == "__main__":
    main()
