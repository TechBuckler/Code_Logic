#!/usr/bin/env python
"""
Complexity Analyzer

This module provides tools for analyzing the algorithmic complexity (Big O notation)
of Python code and suggesting optimizations.
"""

import os
import sys
import ast
import time
import inspect
import logging
from typing import Dict, List, Any, Optional, Tuple, Set, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="complexity_analyzer.log",
)
logger = logging.getLogger("complexity_analyzer")


class ComplexityPatterns:
    """Common code patterns and their associated Big O complexity."""

    # Dictionary mapping pattern descriptions to their complexity
    PATTERNS = {
        # Loop patterns
        "single_loop": "O(n)",
        "nested_loop_2": "O(n²)",
        "nested_loop_3": "O(n³)",
        "nested_loop_k": "O(n^k)",
        "logarithmic_loop": "O(log n)",
        "linearithmic_loop": "O(n log n)",
        # Recursion patterns
        "linear_recursion": "O(n)",
        "binary_recursion": "O(2^n)",
        "tail_recursion": "O(n)",
        "divide_conquer": "O(n log n)",
        # Data structure operations
        "list_access": "O(1)",
        "list_search": "O(n)",
        "list_insert_end": "O(1)",
        "list_insert_middle": "O(n)",
        "dict_access": "O(1)",
        "dict_insert": "O(1)",
        "set_access": "O(1)",
        "set_insert": "O(1)",
        # Common algorithms
        "sorting_comparison": "O(n log n)",
        "bubble_sort": "O(n²)",
        "selection_sort": "O(n²)",
        "insertion_sort": "O(n²)",
        "merge_sort": "O(n log n)",
        "quick_sort": "O(n log n)",
        "heap_sort": "O(n log n)",
        "binary_search": "O(log n)",
        "linear_search": "O(n)",
        "dfs_bfs": "O(V + E)",  # V = vertices, E = edges
        "dijkstra": "O((V + E) log V)",
        # Constant time operations
        "constant_time": "O(1)",
    }

    # Optimization suggestions for different complexities
    OPTIMIZATIONS = {
        "O(n²)": [
            "Consider using a hash table (dictionary) for lookups instead of nested loops",
            "Use sorting followed by linear operations instead of nested loops",
            "Consider using sets for membership testing instead of loops",
        ],
        "O(n³)": [
            "Avoid triple nested loops when possible",
            "Consider dynamic programming to reduce repeated calculations",
            "Use matrix operations or libraries optimized for multi-dimensional data",
        ],
        "O(n^k)": [
            "Polynomial time algorithms with k > 3 are usually impractical for large inputs",
            "Consider approximation algorithms or heuristics instead",
            "Break down the problem into smaller subproblems with lower complexity",
        ],
        "O(2^n)": [
            "Exponential algorithms quickly become impractical for n > 20",
            "Consider dynamic programming to cache repeated calculations",
            "Use memoization to avoid redundant recursive calls",
            "Consider approximation algorithms or heuristics",
        ],
        "O(n!)": [
            "Factorial complexity is extremely inefficient for all but the smallest inputs",
            "Consider using heuristics, approximation algorithms, or constraint programming",
            "Break the problem into smaller subproblems or use pruning techniques",
        ],
    }


class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor that analyzes code complexity."""

    def __init__(self):
        """Initialize the complexity visitor."""
        self.complexities = []
        self.loop_depth = 0
        self.function_complexities = {}
        self.current_function = None
        self.recursive_functions = set()
        self.function_calls = {}
        self.variable_types = {}
        self.imported_modules = set()

    def visit_Import(self, node):
        """Record imported modules."""
        for name in node.names:
            self.imported_modules.add(name.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Record imported modules."""
        if node.module:
            self.imported_modules.add(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """Analyze function definitions."""
        old_function = self.current_function
        self.current_function = node.name
        old_loop_depth = self.loop_depth
        self.loop_depth = 0

        # Initialize function complexity data
        self.function_complexities[node.name] = {
            "name": node.name,
            "lineno": node.lineno,
            "complexity": "O(1)",  # Default complexity
            "loop_depth": 0,
            "has_recursion": False,
            "calls": set(),
            "patterns": set(),
            "optimizations": [],
        }

        # Visit function body
        self.generic_visit(node)

        # Check for recursion
        if node.name in self.function_calls.get(node.name, set()):
            self.function_complexities[node.name]["has_recursion"] = True
            self.recursive_functions.add(node.name)

        # Determine function complexity based on patterns
        self._determine_function_complexity(node.name)

        # Restore state
        self.current_function = old_function
        self.loop_depth = old_loop_depth

    def visit_Call(self, node):
        """Record function calls."""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id

            # Record the call
            if self.current_function:
                if self.current_function not in self.function_calls:
                    self.function_calls[self.current_function] = set()
                self.function_calls[self.current_function].add(func_name)

        self.generic_visit(node)

    def visit_For(self, node):
        """Analyze for loops."""
        self.loop_depth += 1

        # Record loop pattern based on depth
        if self.current_function:
            if self.loop_depth == 1:
                self._add_pattern("single_loop")
            elif self.loop_depth == 2:
                self._add_pattern("nested_loop_2")
            elif self.loop_depth == 3:
                self._add_pattern("nested_loop_3")
            else:
                self._add_pattern("nested_loop_k")

            # Check for logarithmic patterns
            if self._is_logarithmic_loop(node):
                self._add_pattern("logarithmic_loop")

            # Update max loop depth
            self.function_complexities[self.current_function]["loop_depth"] = max(
                self.function_complexities[self.current_function]["loop_depth"],
                self.loop_depth,
            )

        # Visit loop body
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        """Analyze while loops."""
        self.loop_depth += 1

        # Record loop pattern based on depth
        if self.current_function:
            if self.loop_depth == 1:
                self._add_pattern("single_loop")
            elif self.loop_depth == 2:
                self._add_pattern("nested_loop_2")
            elif self.loop_depth == 3:
                self._add_pattern("nested_loop_3")
            else:
                self._add_pattern("nested_loop_k")

            # Check for logarithmic patterns
            if self._is_logarithmic_loop(node):
                self._add_pattern("logarithmic_loop")

            # Update max loop depth
            self.function_complexities[self.current_function]["loop_depth"] = max(
                self.function_complexities[self.current_function]["loop_depth"],
                self.loop_depth,
            )

        # Visit loop body
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_ListComp(self, node):
        """Analyze list comprehensions."""
        if self.current_function:
            # Count the number of for clauses
            num_loops = sum(1 for generator in node.generators)

            if num_loops == 1:
                self._add_pattern("single_loop")
            elif num_loops == 2:
                self._add_pattern("nested_loop_2")
            elif num_loops == 3:
                self._add_pattern("nested_loop_3")
            else:
                self._add_pattern("nested_loop_k")

        self.generic_visit(node)

    def visit_Subscript(self, node):
        """Analyze subscript operations (e.g., list[i], dict[key])."""
        if self.current_function and isinstance(node.value, ast.Name):
            var_name = node.value.id

            # If we know the variable type, record the appropriate pattern
            if var_name in self.variable_types:
                var_type = self.variable_types[var_name]

                if var_type == "list":
                    self._add_pattern("list_access")
                elif var_type == "dict":
                    self._add_pattern("dict_access")
                elif var_type == "set":
                    self._add_pattern("set_access")

        self.generic_visit(node)

    def visit_Assign(self, node):
        """Track variable types from assignments."""
        # Try to infer variable types from assignments
        if isinstance(node.value, ast.List):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.variable_types[target.id] = "list"
        elif isinstance(node.value, ast.Dict):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.variable_types[target.id] = "dict"
        elif isinstance(node.value, ast.Set):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.variable_types[target.id] = "set"
        elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            # Track types from constructor calls like list(), dict(), set()
            func_name = node.value.func.id
            if func_name in ("list", "dict", "set"):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.variable_types[target.id] = func_name

        self.generic_visit(node)

    def _add_pattern(self, pattern_name):
        """Add a complexity pattern to the current function."""
        if self.current_function and pattern_name in ComplexityPatterns.PATTERNS:
            self.function_complexities[self.current_function]["patterns"].add(
                pattern_name
            )

    def _is_logarithmic_loop(self, node):
        """
        Check if a loop has logarithmic characteristics.

        Logarithmic loops typically divide the problem size by a constant factor in each iteration.
        Examples: binary search, divide and conquer algorithms.
        """
        # Simple heuristic: look for division or right shift in the loop body
        for child in ast.walk(node):
            if isinstance(child, ast.BinOp) and (
                isinstance(child.op, ast.Div)
                or isinstance(child.op, ast.FloorDiv)
                or isinstance(child.op, ast.RShift)
            ):
                return True

            # Look for multiplication by 0.5 or division by 2
            if (
                isinstance(child, ast.BinOp)
                and isinstance(child.op, ast.Mult)
                and isinstance(child.right, ast.Constant)
                and child.right.value == 0.5
            ):
                return True

            if (
                isinstance(child, ast.BinOp)
                and isinstance(child.op, (ast.Div, ast.FloorDiv))
                and isinstance(child.right, ast.Constant)
                and child.right.value == 2
            ):
                return True

        return False

    def _determine_function_complexity(self, func_name):
        """Determine the overall complexity of a function based on observed patterns."""
        if func_name not in self.function_complexities:
            return

        complexity_info = self.function_complexities[func_name]
        patterns = complexity_info["patterns"]

        # Start with the default complexity
        complexity = "O(1)"

        # Determine complexity based on patterns
        if "nested_loop_k" in patterns:
            k = complexity_info["loop_depth"]
            complexity = f"O(n^{k})"
        elif "nested_loop_3" in patterns:
            complexity = "O(n³)"
        elif "nested_loop_2" in patterns:
            complexity = "O(n²)"
        elif "linearithmic_loop" in patterns or "divide_conquer" in patterns:
            complexity = "O(n log n)"
        elif "single_loop" in patterns:
            complexity = "O(n)"
        elif "logarithmic_loop" in patterns or "binary_search" in patterns:
            complexity = "O(log n)"

        # Check for recursion
        if complexity_info["has_recursion"]:
            # Simple heuristic for recursive complexity
            if self._is_divide_and_conquer(func_name):
                complexity = "O(n log n)"
            elif self._is_binary_recursion(func_name):
                complexity = "O(2^n)"
            else:
                complexity = "O(n)"

        # Set the final complexity
        complexity_info["complexity"] = complexity

        # Add optimization suggestions
        self._add_optimization_suggestions(func_name)

    def _is_divide_and_conquer(self, func_name):
        """Check if a recursive function uses divide and conquer approach."""
        # Simple heuristic: function calls itself multiple times with reduced input
        # and combines results
        return False  # Placeholder for more sophisticated analysis

    def _is_binary_recursion(self, func_name):
        """Check if a function uses binary recursion (calls itself twice)."""
        # Count recursive calls in the function body
        if (
            func_name in self.function_calls
            and func_name in self.function_calls[func_name]
        ):
            # Simplified heuristic
            return True
        return False

    def _add_optimization_suggestions(self, func_name):
        """Add optimization suggestions based on complexity."""
        if func_name not in self.function_complexities:
            return

        complexity_info = self.function_complexities[func_name]
        complexity = complexity_info["complexity"]

        # Add general optimization suggestions based on complexity
        if complexity in ComplexityPatterns.OPTIMIZATIONS:
            complexity_info["optimizations"].extend(
                ComplexityPatterns.OPTIMIZATIONS[complexity]
            )

        # Add specific optimizations based on patterns
        patterns = complexity_info["patterns"]

        if "nested_loop_2" in patterns or "nested_loop_3" in patterns:
            if "dict_access" not in patterns and "set_access" not in patterns:
                complexity_info["optimizations"].append(
                    "Consider using dictionaries or sets for O(1) lookups instead of nested loops"
                )

        if complexity_info["has_recursion"] and "binary_recursion" in patterns:
            complexity_info["optimizations"].append(
                "Use memoization to avoid redundant calculations in recursive calls"
            )


class ComplexityAnalyzer:
    """
    Analyzes the algorithmic complexity of Python code.
    """

    def __init__(self):
        """Initialize the complexity analyzer."""
        pass

    def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analyze the complexity of Python code.

        Args:
            code: The Python code to analyze

        Returns:
            A dictionary with complexity analysis results
        """
        try:
            # Parse the code to an AST
            tree = ast.parse(code)

            # Analyze complexity
            visitor = ComplexityVisitor()
            visitor.visit(tree)

            # Prepare results
            results = {
                "overall_complexity": self._determine_overall_complexity(
                    visitor.function_complexities
                ),
                "functions": list(visitor.function_complexities.values()),
                "imported_modules": list(visitor.imported_modules),
                "has_high_complexity": any(
                    self._is_high_complexity(func["complexity"])
                    for func in visitor.function_complexities.values()
                ),
                "optimization_opportunities": self._count_optimization_opportunities(
                    visitor.function_complexities
                ),
            }

            return results
        except Exception as e:
            logger.error(f"Error analyzing code complexity: {str(e)}")
            return {
                "error": str(e),
                "overall_complexity": "Unknown",
                "functions": [],
                "has_high_complexity": False,
                "optimization_opportunities": 0,
            }

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze the complexity of a Python file.

        Args:
            file_path: Path to the Python file

        Returns:
            A dictionary with complexity analysis results
        """
        try:
            with open(file_path, "r") as f:
                code = f.read()

            results = self.analyze_code(code)
            results["file_path"] = file_path
            return results
        except Exception as e:
            logger.error(f"Error analyzing file complexity: {str(e)}")
            return {
                "error": str(e),
                "file_path": file_path,
                "overall_complexity": "Unknown",
                "functions": [],
                "has_high_complexity": False,
                "optimization_opportunities": 0,
            }

    def _determine_overall_complexity(
        self, function_complexities: Dict[str, Dict[str, Any]]
    ) -> str:
        """
        Determine the overall complexity of the code.

        Args:
            function_complexities: Dictionary of function complexity information

        Returns:
            The overall complexity as a string
        """
        if not function_complexities:
            return "O(1)"

        # Find the highest complexity among all functions
        complexities = []
        for func_info in function_complexities.values():
            complexity = func_info["complexity"]
            complexities.append(complexity)

        # Sort complexities by their order
        complexity_order = {
            "O(1)": 1,
            "O(log n)": 2,
            "O(n)": 3,
            "O(n log n)": 4,
            "O(n²)": 5,
            "O(n³)": 6,
            "O(2^n)": 7,
            "O(n!)": 8,
        }

        # Sort by known complexity order, then alphabetically for unknown complexities
        sorted_complexities = sorted(
            complexities, key=lambda x: complexity_order.get(x, 9)
        )

        # Return the highest complexity
        if sorted_complexities:
            return sorted_complexities[-1]
        else:
            return "O(1)"

    def _is_high_complexity(self, complexity: str) -> bool:
        """
        Check if a complexity is considered high.

        Args:
            complexity: The complexity string

        Returns:
            True if the complexity is high, False otherwise
        """
        high_complexity_patterns = ["O(n²)", "O(n³)", "O(n^", "O(2^n)", "O(n!)"]
        return any(pattern in complexity for pattern in high_complexity_patterns)

    def _count_optimization_opportunities(
        self, function_complexities: Dict[str, Dict[str, Any]]
    ) -> int:
        """
        Count the number of optimization opportunities.

        Args:
            function_complexities: Dictionary of function complexity information

        Returns:
            The number of optimization opportunities
        """
        count = 0
        for func_info in function_complexities.values():
            count += len(func_info.get("optimizations", []))
        return count

    def suggest_optimizations(
        self, analysis_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Suggest optimizations based on complexity analysis.

        Args:
            analysis_results: The results from analyze_code or analyze_file

        Returns:
            A list of optimization suggestions
        """
        suggestions = []

        for func_info in analysis_results.get("functions", []):
            func_name = func_info.get("name", "unknown")
            complexity = func_info.get("complexity", "O(1)")
            optimizations = func_info.get("optimizations", [])

            if optimizations:
                suggestions.append(
                    {
                        "function": func_name,
                        "complexity": complexity,
                        "suggestions": optimizations,
                    }
                )

        return suggestions

    def format_analysis_results(self, results: Dict[str, Any]) -> str:
        """
        Format analysis results as a human-readable string.

        Args:
            results: The analysis results

        Returns:
            A formatted string with the results
        """
        output = []

        # Add file information if available
        if "file_path" in results:
            output.append(f"File: {results['file_path']}")

        # Add overall complexity
        output.append(
            f"Overall Complexity: {results.get('overall_complexity', 'Unknown')}"
        )

        # Add high complexity warning
        if results.get("has_high_complexity", False):
            output.append("\n⚠️ WARNING: High complexity detected!")

        # Add optimization opportunities
        opt_count = results.get("optimization_opportunities", 0)
        if opt_count > 0:
            output.append(f"\nOptimization Opportunities: {opt_count}")

        # Add function details
        output.append("\nFunction Analysis:")
        for func_info in results.get("functions", []):
            name = func_info.get("name", "unknown")
            complexity = func_info.get("complexity", "O(1)")
            line = func_info.get("lineno", 0)

            output.append(f"\n  {name} (line {line}): {complexity}")

            # Add optimization suggestions
            optimizations = func_info.get("optimizations", [])
            if optimizations:
                output.append("    Optimization suggestions:")
                for i, opt in enumerate(optimizations, 1):
                    output.append(f"    {i}. {opt}")

        return "\n".join(output)


def analyze_code_complexity(code: str) -> Dict[str, Any]:
    """
    Analyze the complexity of Python code.

    Args:
        code: The Python code to analyze

    Returns:
        A dictionary with complexity analysis results
    """
    analyzer = ComplexityAnalyzer()
    return analyzer.analyze_code(code)


def analyze_file_complexity(file_path: str) -> Dict[str, Any]:
    """
    Analyze the complexity of a Python file.

    Args:
        file_path: Path to the Python file

    Returns:
        A dictionary with complexity analysis results
    """
    analyzer = ComplexityAnalyzer()
    return analyzer.analyze_file(file_path)


def suggest_optimizations(analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Suggest optimizations based on complexity analysis.

    Args:
        analysis_results: The results from analyze_code or analyze_file

    Returns:
        A list of optimization suggestions
    """
    analyzer = ComplexityAnalyzer()
    return analyzer.suggest_optimizations(analysis_results)


def format_analysis_results(results: Dict[str, Any]) -> str:
    """
    Format analysis results as a human-readable string.

    Args:
        results: The analysis results

    Returns:
        A formatted string with the results
    """
    analyzer = ComplexityAnalyzer()
    return analyzer.format_analysis_results(results)


def test_analyzer():
    """Test the complexity analyzer with sample code."""
    # Sample code with various complexity patterns
    code = """
def constant_time(n):
    return n * 2

def linear_search(arr, target):
    for item in arr:
        if item == target:
            return True
    return False

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def triple_nested(arr):
    n = len(arr)
    result = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result += arr[i] * arr[j] * arr[k]
    return result
"""

    # Analyze the code
    analyzer = ComplexityAnalyzer()
    results = analyzer.analyze_code(code)

    # Print the formatted results
    print(analyzer.format_analysis_results(results))

    # Print optimization suggestions
    suggestions = analyzer.suggest_optimizations(results)
    if suggestions:
        print("\nOptimization Suggestions:")
        for suggestion in suggestions:
            print(f"\nFunction: {suggestion['function']} ({suggestion['complexity']})")
            for i, opt in enumerate(suggestion["suggestions"], 1):
                print(f"  {i}. {opt}")


if __name__ == "__main__":
    test_analyzer()
