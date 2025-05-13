#!/usr/bin/env python
"""
Test AI Code Validation

This script tests how code transformations affect AI processing by validating
code before and after optimization using the Shadow validation system.
"""

import os
import sys
import ast
import time
import hashlib
import argparse
from typing import Dict, List, Any, Optional, Tuple

# Add the project root to the path if needed
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import our validation system
from validate_with_shadow import ShadowValidator

# Try to import optimization modules
try:
    from tools.optimization.ast_optimizer import optimize_ast
    AST_OPTIMIZER_AVAILABLE = True
except ImportError:
    AST_OPTIMIZER_AVAILABLE = False
    print("AST optimizer not available. Will use basic optimization.")

# Define a simple AST optimizer if the main one is not available
def basic_optimize_ast(code: str) -> str:
    """
    Basic AST-based code optimizer.
    
    Args:
        code: The code to optimize
        
    Returns:
        The optimized code
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(code)
        
        # Apply transformations
        transformer = BasicASTOptimizer()
        optimized_tree = transformer.visit(tree)
        
        # Generate the optimized code
        return ast.unparse(optimized_tree)
    except Exception as e:
        print(f"Error optimizing code: {str(e)}")
        return code

class BasicASTOptimizer(ast.NodeTransformer):
    """Basic AST optimizer that applies simple transformations."""
    
    def visit_BinOp(self, node):
        """Optimize binary operations with constants."""
        self.generic_visit(node)
        
        # Try to evaluate constant expressions
        if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            try:
                # Get the operation
                if isinstance(node.op, ast.Add):
                    result = node.left.value + node.right.value
                elif isinstance(node.op, ast.Sub):
                    result = node.left.value - node.right.value
                elif isinstance(node.op, ast.Mult):
                    result = node.left.value * node.right.value
                elif isinstance(node.op, ast.Div):
                    result = node.left.value / node.right.value
                else:
                    return node
                
                # Return a constant node with the result
                return ast.Constant(value=result)
            except:
                pass
        
        return node
    
    def visit_If(self, node):
        """Optimize if statements with constant conditions."""
        self.generic_visit(node)
        
        # Check if the condition is a constant
        if isinstance(node.test, ast.Constant):
            # If the condition is True, return the body
            if node.test.value:
                return node.body
            # If the condition is False and there's an else clause, return the else clause
            elif node.orelse:
                return node.orelse
            # If the condition is False and there's no else clause, return an empty list
            else:
                return []
        
        return node

def get_code_hash(code: str) -> str:
    """
    Get a hash of the code.
    
    Args:
        code: The code to hash
        
    Returns:
        A hash of the code
    """
    return hashlib.md5(code.encode()).hexdigest()

def optimize_code(code: str) -> str:
    """
    Optimize code using available optimizers.
    
    Args:
        code: The code to optimize
        
    Returns:
        The optimized code
    """
    if AST_OPTIMIZER_AVAILABLE:
        return optimize_ast(code)
    else:
        return basic_optimize_ast(code)

def validate_code_transformations(code: str) -> Dict[str, Any]:
    """
    Validate code before and after transformations.
    
    Args:
        code: The code to validate
        
    Returns:
        A dictionary with validation results
    """
    validator = ShadowValidator()
    
    # Validate the original code
    original_result = validator.validate_code(code)
    original_hash = get_code_hash(code)
    
    # Optimize the code
    optimized_code = optimize_code(code)
    optimized_hash = get_code_hash(optimized_code)
    
    # Validate the optimized code
    optimized_result = validator.validate_code(optimized_code)
    
    # Check if the code changed
    code_changed = original_hash != optimized_hash
    
    # Check if the validation result changed
    validation_changed = original_result['status'] != optimized_result['status']
    
    return {
        'original_code': code,
        'original_hash': original_hash,
        'original_result': original_result,
        'optimized_code': optimized_code,
        'optimized_hash': optimized_hash,
        'optimized_result': optimized_result,
        'code_changed': code_changed,
        'validation_changed': validation_changed
    }

def format_validation_comparison(results: Dict[str, Any]) -> None:
    """
    Format and print a validation comparison.
    
    Args:
        results: The validation comparison results
    """
    print("\n" + "=" * 80)
    print("CODE TRANSFORMATION VALIDATION COMPARISON")
    print("=" * 80)
    
    print(f"Code changed: {results['code_changed']}")
    print(f"Validation changed: {results['validation_changed']}")
    
    print("\nORIGINAL CODE:")
    print("-" * 40)
    print(results['original_code'])
    print("-" * 40)
    print(f"Hash: {results['original_hash']}")
    print(f"Status: {results['original_result']['status']}")
    print(f"Confidence: {results['original_result']['confidence']:.2f}")
    print(f"Source: {results['original_result']['source']}")
    
    if results['original_result']['suggestions']:
        print("\nSuggestions:")
        for i, suggestion in enumerate(results['original_result']['suggestions'], 1):
            print(f"{i}. {suggestion}")
    
    print("\nOPTIMIZED CODE:")
    print("-" * 40)
    print(results['optimized_code'])
    print("-" * 40)
    print(f"Hash: {results['optimized_hash']}")
    print(f"Status: {results['optimized_result']['status']}")
    print(f"Confidence: {results['optimized_result']['confidence']:.2f}")
    print(f"Source: {results['optimized_result']['source']}")
    
    if results['optimized_result']['suggestions']:
        print("\nSuggestions:")
        for i, suggestion in enumerate(results['optimized_result']['suggestions'], 1):
            print(f"{i}. {suggestion}")
    
    print("=" * 80)

def test_with_sample_code():
    """Test with sample code snippets."""
    # Test with a simple code snippet
    simple_code = """
def calculate_sum(a, b):
    # This function calculates the sum of two numbers
    result = a + b
    return result

# Test the function
x = 10
y = 20
z = calculate_sum(x, y)
print(f"The sum of {x} and {y} is {z}")
"""
    
    # Test with code that can be optimized
    optimizable_code = """
def calculate_expression():
    # This function calculates a complex expression
    a = 10
    b = 20
    c = 30
    
    # This can be optimized
    result = a + b + c
    
    # This can be optimized
    if True:
        print("Always executed")
    
    # This can be optimized
    if False:
        print("Never executed")
    
    return result

# Test the function
result = calculate_expression()
print(f"The result is {result}")
"""
    
    # Test with code that has syntax errors
    error_code = """
def broken_function():
    # This function has syntax errors
    a = 10
    b = 20
    return a +  # Missing operand
"""
    
    # Test each code snippet
    print("\nTesting simple code...")
    simple_results = validate_code_transformations(simple_code)
    format_validation_comparison(simple_results)
    
    print("\nTesting optimizable code...")
    optimizable_results = validate_code_transformations(optimizable_code)
    format_validation_comparison(optimizable_results)
    
    print("\nTesting code with errors...")
    error_results = validate_code_transformations(error_code)
    format_validation_comparison(error_results)

def test_with_file(file_path: str):
    """
    Test with a file.
    
    Args:
        file_path: Path to the file to test
    """
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        print(f"\nTesting file: {file_path}")
        results = validate_code_transformations(code)
        format_validation_comparison(results)
    except Exception as e:
        print(f"Error testing file {file_path}: {str(e)}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Test AI Code Validation')
    parser.add_argument('--file', help='Path to a file to test')
    parser.add_argument('--code', help='Code snippet to test')
    parser.add_argument('--sample', action='store_true', help='Run tests with sample code snippets')
    
    args = parser.parse_args()
    
    if args.file:
        test_with_file(args.file)
    elif args.code:
        results = validate_code_transformations(args.code)
        format_validation_comparison(results)
    elif args.sample:
        test_with_sample_code()
    else:
        # Default to sample code if no arguments are provided
        test_with_sample_code()

if __name__ == "__main__":
    main()
