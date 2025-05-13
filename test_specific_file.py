#!/usr/bin/env python
"""
Test Specific File

This script tests how code transformations affect validation results
for a specific file in the codebase.
"""

import os
import sys
import ast
from typing import Dict, Any

# Add the project root to the path if needed
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import our validation system
from validate_with_shadow import ShadowValidator

def optimize_constants(code: str) -> str:
    """
    Optimize constant expressions in the code.
    
    Args:
        code: The code to optimize
        
    Returns:
        The optimized code
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(code)
        
        # Apply constant folding
        transformer = ConstantFolder()
        optimized_tree = transformer.visit(tree)
        ast.fix_missing_locations(optimized_tree)
        
        # Generate the optimized code
        return ast.unparse(optimized_tree)
    except Exception as e:
        print(f"Error optimizing constants: {str(e)}")
        return code

class ConstantFolder(ast.NodeTransformer):
    """AST transformer that folds constant expressions."""
    
    def visit_BinOp(self, node):
        """Fold constant binary operations."""
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

def remove_comments(code: str) -> str:
    """
    Remove comments from the code.
    
    Args:
        code: The code to process
        
    Returns:
        The code without comments
    """
    result = []
    lines = code.splitlines()
    
    for line in lines:
        # Remove inline comments
        comment_pos = line.find('#')
        if comment_pos >= 0:
            line = line[:comment_pos]
        
        # Add the line if it's not empty
        if line.strip():
            result.append(line)
    
    return '\n'.join(result)

def minify_code(code: str) -> str:
    """
    Minify the code by removing whitespace.
    
    Args:
        code: The code to minify
        
    Returns:
        The minified code
    """
    # Remove comments first
    code = remove_comments(code)
    
    # Parse the code into an AST
    try:
        tree = ast.parse(code)
        
        # Generate minified code
        return ast.unparse(tree)
    except Exception as e:
        print(f"Error minifying code: {str(e)}")
        return code

def test_file_transformations(file_path: str) -> None:
    """
    Test how different code transformations affect validation results.
    
    Args:
        file_path: Path to the file to test
    """
    try:
        # Read the file
        with open(file_path, 'r') as f:
            original_code = f.read()
        
        # Create a validator
        validator = ShadowValidator()
        
        # Validate the original code
        print(f"\nValidating original code from {file_path}...")
        original_result = validator.validate_code(original_code)
        print_validation_result("ORIGINAL CODE", original_result)
        
        # Optimize constants and validate
        print("\nOptimizing constants...")
        optimized_code = optimize_constants(original_code)
        optimized_result = validator.validate_code(optimized_code)
        print_validation_result("OPTIMIZED CODE", optimized_result)
        
        # Remove comments and validate
        print("\nRemoving comments...")
        no_comments_code = remove_comments(original_code)
        no_comments_result = validator.validate_code(no_comments_code)
        print_validation_result("CODE WITHOUT COMMENTS", no_comments_result)
        
        # Minify code and validate
        print("\nMinifying code...")
        minified_code = minify_code(original_code)
        minified_result = validator.validate_code(minified_code)
        print_validation_result("MINIFIED CODE", minified_result)
        
        # Compare results
        print("\nCOMPARISON SUMMARY:")
        print("-" * 40)
        print(f"Original status: {original_result['status']}, confidence: {original_result['confidence']:.2f}")
        print(f"Optimized status: {optimized_result['status']}, confidence: {optimized_result['confidence']:.2f}")
        print(f"No comments status: {no_comments_result['status']}, confidence: {no_comments_result['confidence']:.2f}")
        print(f"Minified status: {minified_result['status']}, confidence: {minified_result['confidence']:.2f}")
        
        # Check if validation results changed
        print("\nVALIDATION CHANGES:")
        print("-" * 40)
        print(f"Optimization changed validation: {original_result['status'] != optimized_result['status']}")
        print(f"Comment removal changed validation: {original_result['status'] != no_comments_result['status']}")
        print(f"Minification changed validation: {original_result['status'] != minified_result['status']}")
        
        # Check if suggestions changed
        original_suggestions = set(original_result.get('suggestions', []))
        optimized_suggestions = set(optimized_result.get('suggestions', []))
        no_comments_suggestions = set(no_comments_result.get('suggestions', []))
        minified_suggestions = set(minified_result.get('suggestions', []))
        
        print("\nSUGGESTION CHANGES:")
        print("-" * 40)
        print(f"Optimization changed suggestions: {original_suggestions != optimized_suggestions}")
        print(f"Comment removal changed suggestions: {original_suggestions != no_comments_suggestions}")
        print(f"Minification changed suggestions: {original_suggestions != minified_suggestions}")
        
        # Print added/removed suggestions
        if original_suggestions != optimized_suggestions:
            print("\nOPTIMIZATION SUGGESTION CHANGES:")
            print_suggestion_changes(original_suggestions, optimized_suggestions)
        
        if original_suggestions != no_comments_suggestions:
            print("\nCOMMENT REMOVAL SUGGESTION CHANGES:")
            print_suggestion_changes(original_suggestions, no_comments_suggestions)
        
        if original_suggestions != minified_suggestions:
            print("\nMINIFICATION SUGGESTION CHANGES:")
            print_suggestion_changes(original_suggestions, minified_suggestions)
        
    except Exception as e:
        print(f"Error testing file {file_path}: {str(e)}")

def print_validation_result(title: str, result: Dict[str, Any]) -> None:
    """
    Print a validation result.
    
    Args:
        title: The title for the result
        result: The validation result
    """
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)
    print(f"Status: {result['status']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Source: {result['source']}")
    
    if "explanation" in result:
        print(f"\nExplanation: {result['explanation']}")
    
    if result.get('suggestions'):
        print("\nSuggestions:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"{i}. {suggestion}")

def print_suggestion_changes(original: set, modified: set) -> None:
    """
    Print the changes in suggestions.
    
    Args:
        original: The original suggestions
        modified: The modified suggestions
    """
    added = modified - original
    removed = original - modified
    
    if added:
        print("\nAdded suggestions:")
        for suggestion in added:
            print(f"+ {suggestion}")
    
    if removed:
        print("\nRemoved suggestions:")
        for suggestion in removed:
            print(f"- {suggestion}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Specific File')
    parser.add_argument('file_path', help='Path to the file to test')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"Error: File {args.file_path} does not exist.")
        return 1
    
    test_file_transformations(args.file_path)
    return 0

if __name__ == "__main__":
    sys.exit(main())
