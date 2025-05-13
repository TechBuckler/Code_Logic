#!/usr/bin/env python
"""
Compare Code Versions

This script compares the validation results of original and optimized code
to see if code transformations affect AI processing.
"""

import os
import sys
import ast
import difflib
from typing import Dict, Any

# Add the project root to the path if needed
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import our validation system
from validate_with_shadow import ShadowValidator

class CodeOptimizer:
    """Simple code optimizer using AST transformations."""
    
    def optimize(self, code: str) -> str:
        """
        Optimize the given code.
        
        Args:
            code: The code to optimize
            
        Returns:
            The optimized code
        """
        try:
            # Parse the code into an AST
            tree = ast.parse(code)
            
            # Apply transformations
            transformer = ASTOptimizer()
            optimized_tree = transformer.visit(tree)
            ast.fix_missing_locations(optimized_tree)
            
            # Generate the optimized code
            return ast.unparse(optimized_tree)
        except Exception as e:
            print(f"Error optimizing code: {str(e)}")
            return code

class ASTOptimizer(ast.NodeTransformer):
    """AST transformer that applies optimizations."""
    
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
                if len(node.body) == 1:
                    return node.body[0]
                else:
                    return ast.Module(body=node.body, type_ignores=[])
            # If the condition is False and there's an else clause, return the else clause
            elif node.orelse:
                if len(node.orelse) == 1:
                    return node.orelse[0]
                else:
                    return ast.Module(body=node.orelse, type_ignores=[])
            # If the condition is False and there's no else clause, return a pass statement
            else:
                return ast.Pass()
        
        return node

def compare_code_versions(code: str) -> Dict[str, Any]:
    """
    Compare original and optimized code versions.
    
    Args:
        code: The original code
        
    Returns:
        A dictionary with comparison results
    """
    validator = ShadowValidator()
    optimizer = CodeOptimizer()
    
    # Validate the original code
    original_result = validator.validate_code(code)
    
    # Optimize the code
    optimized_code = optimizer.optimize(code)
    
    # Validate the optimized code
    optimized_result = validator.validate_code(optimized_code)
    
    # Generate a diff between the original and optimized code
    diff = list(difflib.unified_diff(
        code.splitlines(),
        optimized_code.splitlines(),
        fromfile='original',
        tofile='optimized',
        lineterm=''
    ))
    
    # Check if the validation result changed
    validation_changed = original_result['status'] != optimized_result['status']
    
    # Check if suggestions changed
    original_suggestions = set(original_result.get('suggestions', []))
    optimized_suggestions = set(optimized_result.get('suggestions', []))
    suggestions_changed = original_suggestions != optimized_suggestions
    
    return {
        'original_code': code,
        'optimized_code': optimized_code,
        'original_result': original_result,
        'optimized_result': optimized_result,
        'diff': diff,
        'validation_changed': validation_changed,
        'suggestions_changed': suggestions_changed,
        'added_suggestions': optimized_suggestions - original_suggestions,
        'removed_suggestions': original_suggestions - optimized_suggestions
    }

def print_comparison_results(results: Dict[str, Any]) -> None:
    """
    Print the comparison results.
    
    Args:
        results: The comparison results
    """
    print("\n" + "=" * 80)
    print("CODE COMPARISON RESULTS")
    print("=" * 80)
    
    print(f"Validation status changed: {results['validation_changed']}")
    print(f"Suggestions changed: {results['suggestions_changed']}")
    
    print("\nORIGINAL CODE:")
    print("-" * 40)
    print(results['original_code'])
    
    print("\nOPTIMIZED CODE:")
    print("-" * 40)
    print(results['optimized_code'])
    
    if results['diff']:
        print("\nDIFF:")
        print("-" * 40)
        for line in results['diff']:
            print(line)
    
    print("\nORIGINAL VALIDATION:")
    print("-" * 40)
    print(f"Status: {results['original_result']['status']}")
    print(f"Confidence: {results['original_result']['confidence']:.2f}")
    
    if results['original_result'].get('suggestions'):
        print("\nOriginal Suggestions:")
        for i, suggestion in enumerate(results['original_result']['suggestions'], 1):
            print(f"{i}. {suggestion}")
    
    print("\nOPTIMIZED VALIDATION:")
    print("-" * 40)
    print(f"Status: {results['optimized_result']['status']}")
    print(f"Confidence: {results['optimized_result']['confidence']:.2f}")
    
    if results['optimized_result'].get('suggestions'):
        print("\nOptimized Suggestions:")
        for i, suggestion in enumerate(results['optimized_result']['suggestions'], 1):
            print(f"{i}. {suggestion}")
    
    if results['added_suggestions']:
        print("\nADDED SUGGESTIONS:")
        for suggestion in results['added_suggestions']:
            print(f"+ {suggestion}")
    
    if results['removed_suggestions']:
        print("\nREMOVED SUGGESTIONS:")
        for suggestion in results['removed_suggestions']:
            print(f"- {suggestion}")
    
    print("=" * 80)

def test_samples():
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
    result = 10 + 20 + 30
    
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
    
    # Test with code that has issues
    problematic_code = """
def badFunction():
    # Missing docstring
    x = 10
    y = 20
    return x+y

class badClass:
    # Missing docstring and wrong naming convention
    def __init__(self):
        self.value = 42
    
    def getValue(self):
        # Wrong naming convention
        return self.value
"""
    
    # Test each code snippet
    print("\nTesting simple code...")
    simple_results = compare_code_versions(simple_code)
    print_comparison_results(simple_results)
    
    print("\nTesting optimizable code...")
    optimizable_results = compare_code_versions(optimizable_code)
    print_comparison_results(optimizable_results)
    
    print("\nTesting problematic code...")
    problematic_results = compare_code_versions(problematic_code)
    print_comparison_results(problematic_results)

def test_file(file_path: str):
    """
    Test with a file.
    
    Args:
        file_path: Path to the file to test
    """
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        print(f"\nTesting file: {file_path}")
        results = compare_code_versions(code)
        print_comparison_results(results)
    except Exception as e:
        print(f"Error testing file {file_path}: {str(e)}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare Code Versions')
    parser.add_argument('--file', help='Path to a file to test')
    parser.add_argument('--code', help='Code snippet to test')
    parser.add_argument('--sample', action='store_true', help='Run tests with sample code snippets')
    
    args = parser.parse_args()
    
    if args.file:
        test_file(args.file)
    elif args.code:
        results = compare_code_versions(args.code)
        print_comparison_results(results)
    elif args.sample:
        test_samples()
    else:
        # Default to sample code if no arguments are provided
        test_samples()

if __name__ == "__main__":
    main()
