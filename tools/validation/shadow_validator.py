#!/usr/bin/env python
"""
Shadow Validator Integration

This module integrates the core concepts from the Shadow validation system
into the code_logic_tool_full pipeline.
"""

import os
import sys
import ast
import time
import hashlib
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="validator.log",
)
logger = logging.getLogger("shadow_validator")


class RuleBasedValidator:
    """Simple rule-based validator for Python code."""

    def __init__(self):
        """Initialize the rule-based validator."""
        self.rules = [
            self._check_syntax,
            self._check_complexity,
            self._check_naming_conventions,
            self._check_imports,
            self._check_docstrings,
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
            "cost": 0.0,
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
                    statement_count = sum(
                        1 for _ in ast.walk(node) if isinstance(_, (ast.stmt))
                    )
                    if statement_count > 50:
                        issues.append(
                            f"Function '{node.name}' is too complex ({statement_count} statements)"
                        )

                    # Check for deeply nested loops/conditionals
                    nested_depth = self._get_nesting_depth(node)
                    if nested_depth > 4:
                        issues.append(
                            f"Function '{node.name}' has deeply nested blocks (depth {nested_depth})"
                        )
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
                    if (
                        not node.name.islower()
                        and "_" not in node.name
                        and not node.name.startswith("__")
                    ):
                        issues.append(
                            f"Function '{node.name}' should use snake_case naming convention"
                        )

                # Check class names (PascalCase)
                elif isinstance(node, ast.ClassDef):
                    if not node.name[0].isupper() or "_" in node.name:
                        issues.append(
                            f"Class '{node.name}' should use PascalCase naming convention"
                        )

                # Check constant names (UPPER_CASE)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if (
                            isinstance(target, ast.Name)
                            and target.id.isupper()
                            and "_" not in target.id
                        ):
                            # This is likely a constant, check if it's actually assigned a constant value
                            if not isinstance(
                                node.value,
                                (
                                    ast.Num,
                                    ast.Str,
                                    ast.NameConstant,
                                    ast.List,
                                    ast.Dict,
                                    ast.Set,
                                ),
                            ):
                                issues.append(
                                    f"Constant '{target.id}' should be assigned a constant value"
                                )
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
                    if not (
                        node.body
                        and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Str)
                    ):
                        if isinstance(node, ast.FunctionDef):
                            issues.append(
                                f"Function '{node.name}' is missing a docstring"
                            )
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
            "total_validations": 0,
            "rule_based_validations": 0,
            "pattern_validations": 0,
            "execution_time": 0.0,
        }

    def validate_code(self, code: str, scope: str = "all") -> Dict[str, Any]:
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
        self.stats["total_validations"] += 1

        # Generate a unique hash for the code
        code_hash = hashlib.md5(code.encode()).hexdigest()

        # Check cache first
        if code_hash in self.cache:
            logger.info(f"Cache hit for {code_hash}")
            result = self.cache[code_hash]
            # Add execution time to the result
            result["execution_time"] = time.time() - start_time
            return result

        # Rule-based validation
        rule_result = self.rule_validator.validate(code)
        self.stats["rule_based_validations"] += 1

        # Add execution time to the result
        rule_result["execution_time"] = time.time() - start_time

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
                "suggestions": [
                    f"Check if the function '{function_name}' exists in the code"
                ],
                "cost": 0.0,
            }

        # Validate the extracted function
        return self.validate_code(function_code, scope="function")

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
                    func_lines = code.splitlines()[node.lineno - 1 : node.end_lineno]
                    return "\n".join(func_lines)
            return None
        except Exception as e:
            logger.error(f"Error extracting function: {str(e)}")
            return None

    def get_stats(self) -> Dict[str, Any]:
        """Get validation statistics."""
        return self.stats


def test_validator():
    """Test the shadow validator with a sample code."""
    validator = ShadowValidator()

    # Test with a simple code snippet
    code = """
def hello_world():
    print("Hello, World!")
    
class TestClass:
    def __init__(self):
        self.value = 42
        
    def get_value(self):
        return self.value
    """

    result = validator.validate_code(code)
    print("\n" + "=" * 60)
    print("VALIDATION RESULT")
    print("=" * 60)
    print(f"Status: {result.get('status', 'UNKNOWN')}")
    print(f"Confidence: {result.get('confidence', 0.0):.2f}")
    print(f"Source: {result.get('source', 'unknown')}")
    print(f"Execution time: {result.get('execution_time', 0.0):.2f} seconds")

    if "explanation" in result:
        print(f"\nExplanation: {result['explanation']}")

    if "suggestions" in result and result["suggestions"]:
        print("\nSuggestions:")
        for i, suggestion in enumerate(result["suggestions"], 1):
            print(f"{i}. {suggestion}")

    print("\n" + "=" * 60)

    # Test with a function
    result = validator.validate_function(code, "get_value")
    print("\n" + "=" * 60)
    print("FUNCTION VALIDATION RESULT")
    print("=" * 60)
    print(f"Status: {result.get('status', 'UNKNOWN')}")
    print(f"Confidence: {result.get('confidence', 0.0):.2f}")
    print(f"Source: {result.get('source', 'unknown')}")
    print(f"Execution time: {result.get('execution_time', 0.0):.2f} seconds")

    if "explanation" in result:
        print(f"\nExplanation: {result['explanation']}")

    if "suggestions" in result and result["suggestions"]:
        print("\nSuggestions:")
        for i, suggestion in enumerate(result["suggestions"], 1):
            print(f"{i}. {suggestion}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_validator()
