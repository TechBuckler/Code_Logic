#!/usr/bin/env python
"""
Validate With Shadow

This script integrates the Shadow validation system with the existing module system
and provides a simple command-line interface for validating Python code.
"""

import os
import sys
import ast
import time
import hashlib
import logging
import argparse
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='validator.log'
)
logger = logging.getLogger('shadow_validator')

class RuleBasedValidator:
    """Simple rule-based validator for Python code."""
    
    def __init__(self):
        """Initialize the rule-based validator."""
        self.rules = [
            self._check_syntax,
            self._check_complexity,
            self._check_naming_conventions,
            self._check_imports,
            self._check_docstrings
        ]
    
    def validate(self, code: str) -> Dict[str, Any]:
        """
        Validate code using predefined rules.
        
        Args:
            code: The code to validate
            
        Returns:
            A dictionary with validation results
        """
        issues = []
        confidence = 0.0
        
        # Apply each rule
        for rule in self.rules:
            rule_result = rule(code)
            if rule_result:
                issues.extend(rule_result)
        
        # Calculate confidence based on number of issues
        if issues:
            confidence = min(0.5 + (len(issues) * 0.1), 0.95)
            status = "NOT_VALID"
        else:
            confidence = 0.7
            status = "VALID"
        
        return {
            "status": status,
            "confidence": confidence,
            "source": "rule_based",
            "explanation": "Rule-based validation completed",
            "suggestions": issues,
            "cost": 0.0
        }
    
    def _check_syntax(self, code: str) -> List[str]:
        """Check for syntax errors."""
        issues = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(f"Syntax error at line {e.lineno}: {e.msg}")
        return issues
    
    def _check_complexity(self, code: str) -> List[str]:
        """Check for code complexity issues."""
        issues = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # Check for overly complex functions
                if isinstance(node, ast.FunctionDef):
                    # Count the number of statements
                    statement_count = sum(1 for _ in ast.walk(node) if isinstance(_, (ast.stmt)))
                    if statement_count > 50:
                        issues.append(f"Function '{node.name}' is too complex ({statement_count} statements)")
                    
                    # Check for deeply nested loops/conditionals
                    nested_depth = self._get_nesting_depth(node)
                    if nested_depth > 4:
                        issues.append(f"Function '{node.name}' has deeply nested blocks (depth {nested_depth})")
        except Exception as e:
            issues.append(f"Error checking complexity: {str(e)}")
        return issues
    
    def _get_nesting_depth(self, node, current_depth=0) -> int:
        """Get the maximum nesting depth of a node."""
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While, ast.If, ast.With)):
                child_depth = self._get_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._get_nesting_depth(child, current_depth)
                max_depth = max(max_depth, child_depth)
        return max_depth
    
    def _check_naming_conventions(self, code: str) -> List[str]:
        """Check for naming convention issues."""
        issues = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # Check function names (snake_case)
                if isinstance(node, ast.FunctionDef):
                    if not node.name.islower() and '_' not in node.name and not node.name.startswith('__'):
                        issues.append(f"Function '{node.name}' should use snake_case naming convention")
                
                # Check class names (PascalCase)
                elif isinstance(node, ast.ClassDef):
                    if not node.name[0].isupper() or '_' in node.name:
                        issues.append(f"Class '{node.name}' should use PascalCase naming convention")
                
                # Check constant names (UPPER_CASE)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper() and '_' not in target.id:
                            # This is likely a constant, check if it's actually assigned a constant value
                            if not isinstance(node.value, (ast.Num, ast.Str, ast.NameConstant, ast.List, ast.Dict, ast.Set)):
                                issues.append(f"Constant '{target.id}' should be assigned a constant value")
        except Exception as e:
            issues.append(f"Error checking naming conventions: {str(e)}")
        return issues
    
    def _check_imports(self, code: str) -> List[str]:
        """Check for import issues."""
        issues = []
        try:
            tree = ast.parse(code)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(node.module)
            
            # Check for duplicate imports
            seen = set()
            for imp in imports:
                if imp in seen:
                    issues.append(f"Duplicate import of '{imp}'")
                seen.add(imp)
        except Exception as e:
            issues.append(f"Error checking imports: {str(e)}")
        return issues
    
    def _check_docstrings(self, code: str) -> List[str]:
        """Check for missing docstrings."""
        issues = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    # Check if the first node in the body is a docstring
                    if not (node.body and isinstance(node.body[0], ast.Expr) and 
                           isinstance(node.body[0].value, ast.Str)):
                        if isinstance(node, ast.FunctionDef):
                            issues.append(f"Function '{node.name}' is missing a docstring")
                        elif isinstance(node, ast.ClassDef):
                            issues.append(f"Class '{node.name}' is missing a docstring")
                        elif isinstance(node, ast.Module):
                            issues.append("Module is missing a docstring")
        except Exception as e:
            issues.append(f"Error checking docstrings: {str(e)}")
        return issues

class ShadowValidator:
    """
    Shadow Validator integrates the core concepts from the Shadow validation system.
    """
    def __init__(self):
        """Initialize the shadow validator."""
        self.rule_validator = RuleBasedValidator()
        self.cache = {}
        
        # Initialize statistics
        self.stats = {
            'total_validations': 0,
            'rule_based_validations': 0,
            'pattern_validations': 0,
            'execution_time': 0.0
        }
    
    def validate_code(self, code: str, scope: str = 'all') -> Dict[str, Any]:
        """
        Validate code using a rule-based approach.
        
        Args:
            code: The code to validate
            scope: The scope of validation ('all', 'function', 'class')
            
        Returns:
            A dictionary with validation results
        """
        start_time = time.time()
        
        # Update statistics
        self.stats['total_validations'] += 1
        
        # Generate a unique hash for the code
        code_hash = hashlib.md5(code.encode()).hexdigest()
        
        # Check cache first
        if code_hash in self.cache:
            logger.info(f"Cache hit for {code_hash}")
            result = self.cache[code_hash]
            # Add execution time to the result
            result['execution_time'] = time.time() - start_time
            return result
        
        # Rule-based validation
        rule_result = self.rule_validator.validate(code)
        self.stats['rule_based_validations'] += 1
        
        # Add execution time to the result
        rule_result['execution_time'] = time.time() - start_time
        
        # Cache the result
        self.cache[code_hash] = rule_result
        
        return rule_result
    
    def validate_function(self, code: str, function_name: str) -> Dict[str, Any]:
        """
        Validate a specific function in the code.
        
        Args:
            code: The full code containing the function
            function_name: The name of the function to validate
            
        Returns:
            A dictionary with validation results
        """
        # Extract the function code
        function_code = self._extract_function(code, function_name)
        if not function_code:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "source": "function_extractor",
                "explanation": f"Function '{function_name}' not found in the code",
                "suggestions": [f"Check if the function '{function_name}' exists in the code"],
                "cost": 0.0
            }
        
        # Validate the extracted function
        return self.validate_code(function_code, scope='function')
    
    def _extract_function(self, code: str, function_name: str) -> Optional[str]:
        """
        Extract a function from code by name.
        
        Args:
            code: The full code containing the function
            function_name: The name of the function to extract
            
        Returns:
            The function code or None if not found
        """
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    # Get the source code for the function
                    func_lines = code.splitlines()[node.lineno-1:node.end_lineno]
                    return '\n'.join(func_lines)
            return None
        except Exception as e:
            logger.error(f"Error extracting function: {str(e)}")
            return None
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a Python file.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            A dictionary with validation results
        """
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            result = self.validate_code(code)
            result['file_path'] = file_path
            return result
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error validating file {file_path}: {str(e)}",
                "suggestions": [],
                "file_path": file_path
            }
    
    def validate_directory(self, directory_path: str, recursive: bool = True) -> Dict[str, List[Dict[str, Any]]]:
        """
        Validate all Python files in a directory.
        
        Args:
            directory_path: Path to the directory to validate
            recursive: Whether to recursively validate subdirectories
            
        Returns:
            A dictionary with validation results for each file
        """
        results = {
            "status": "SUCCESS",
            "files": []
        }
        
        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        result = self.validate_file(file_path)
                        results['files'].append(result)
                
                if not recursive:
                    break
            
            return results
        except Exception as e:
            return {
                "status": "ERROR",
                "explanation": f"Error validating directory {directory_path}: {str(e)}",
                "files": []
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get validation statistics."""
        return self.stats

def format_validation_result(result: Dict[str, Any]) -> None:
    """Format and print a validation result."""
    print("\n" + "=" * 60)
    print("VALIDATION RESULT")
    print("=" * 60)
    
    if "file_path" in result:
        print(f"File: {result['file_path']}")
    
    print(f"Status: {result.get('status', 'UNKNOWN')}")
    print(f"Confidence: {result.get('confidence', 0.0):.2f}")
    print(f"Source: {result.get('source', 'unknown')}")
    
    if "execution_time" in result:
        print(f"Execution time: {result['execution_time']:.2f} seconds")
    
    if "explanation" in result:
        print(f"\nExplanation: {result['explanation']}")
    
    if "suggestions" in result and result["suggestions"]:
        print("\nSuggestions:")
        for i, suggestion in enumerate(result["suggestions"], 1):
            print(f"{i}. {suggestion}")
    
    print("=" * 60)

def main():
    """Main function for the validate code tool."""
    parser = argparse.ArgumentParser(description='Shadow Validation Tool')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Validate file command
    validate_file_parser = subparsers.add_parser('file', help='Validate a Python file')
    validate_file_parser.add_argument('file_path', help='Path to the file to validate')
    validate_file_parser.add_argument('--function', help='Name of the function to validate')
    
    # Validate directory command
    validate_dir_parser = subparsers.add_parser('directory', help='Validate all Python files in a directory')
    validate_dir_parser.add_argument('directory_path', help='Path to the directory to validate')
    validate_dir_parser.add_argument('--recursive', action='store_true', help='Recursively validate subdirectories')
    
    # Validate code command
    validate_code_parser = subparsers.add_parser('code', help='Validate a code snippet')
    validate_code_parser.add_argument('code', help='Code snippet to validate')
    
    # Stats command
    subparsers.add_parser('stats', help='Show validation statistics')
    
    args = parser.parse_args()
    
    validator = ShadowValidator()
    
    if args.command == 'file':
        if not os.path.exists(args.file_path):
            print(f"Error: File {args.file_path} does not exist.")
            return 1
        
        if args.function:
            # Read the file
            with open(args.file_path, 'r') as f:
                code = f.read()
            
            # Validate the function
            result = validator.validate_function(code, args.function)
            result['file_path'] = args.file_path
        else:
            # Validate the file
            result = validator.validate_file(args.file_path)
        
        format_validation_result(result)
    
    elif args.command == 'directory':
        if not os.path.exists(args.directory_path):
            print(f"Error: Directory {args.directory_path} does not exist.")
            return 1
        
        results = validator.validate_directory(args.directory_path, args.recursive)
        
        if results['status'] == 'ERROR':
            print(f"Error: {results['explanation']}")
            return 1
        
        print(f"Validated {len(results['files'])} files in {args.directory_path}")
        
        # Count issues by severity
        valid_files = 0
        invalid_files = 0
        error_files = 0
        
        for result in results['files']:
            if result['status'] == 'VALID':
                valid_files += 1
            elif result['status'] == 'NOT_VALID':
                invalid_files += 1
            else:
                error_files += 1
        
        print(f"Valid files: {valid_files}")
        print(f"Invalid files: {invalid_files}")
        print(f"Error files: {error_files}")
        
        # Ask if the user wants to see details for invalid files
        if invalid_files > 0:
            print("\nInvalid files:")
            for result in results['files']:
                if result['status'] == 'NOT_VALID':
                    print(f"- {result['file_path']} (Confidence: {result['confidence']:.2f})")
            
            see_details = input("\nDo you want to see details for invalid files? (y/n): ")
            if see_details.lower() == 'y':
                for result in results['files']:
                    if result['status'] == 'NOT_VALID':
                        format_validation_result(result)
    
    elif args.command == 'code':
        result = validator.validate_code(args.code)
        format_validation_result(result)
    
    elif args.command == 'stats':
        stats = validator.get_stats()
        print("\n" + "=" * 60)
        print("VALIDATION STATS")
        print("=" * 60)
        for key, value in stats.items():
            print(f"{key}: {value}")
        print("=" * 60)
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
