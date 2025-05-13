#!/usr/bin/env python
"""
Complexity Validator

This module integrates the complexity analyzer with the Shadow validation system
to provide complexity analysis and optimization suggestions as part of the validation process.
"""

import os
import sys
import ast
import time
import logging
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="validator.log",
)
logger = logging.getLogger("complexity_validator")

# Import the complexity analyzer
try:
    from tools.profiling.complexity_analyzer import (
        ComplexityAnalyzer,
        analyze_code_complexity,
        analyze_file_complexity,
        suggest_optimizations,
        format_analysis_results,
    )

    COMPLEXITY_ANALYZER_AVAILABLE = True
except ImportError:
    logger.warning(
        "Complexity analyzer not available. Install the module for complexity analysis."
    )
    COMPLEXITY_ANALYZER_AVAILABLE = False


class ComplexityValidator:
    """
    Validates code complexity and suggests optimizations.
    """

    def __init__(self):
        """Initialize the complexity validator."""
        self.analyzer = ComplexityAnalyzer() if COMPLEXITY_ANALYZER_AVAILABLE else None

    def is_available(self) -> bool:
        """
        Check if complexity validation is available.

        Returns:
            True if complexity validation is available, False otherwise
        """
        return COMPLEXITY_ANALYZER_AVAILABLE and self.analyzer is not None

    def validate(self, code: str) -> Dict[str, Any]:
        """
        Validate code complexity.

        Args:
            code: The code to validate

        Returns:
            A dictionary with validation results
        """
        if not self.is_available():
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Complexity analyzer not available.",
                "suggestions": ["Install the complexity analyzer module."],
                "source": "complexity_validator",
            }

        try:
            # Analyze code complexity
            start_time = time.time()
            analysis = self.analyzer.analyze_code(code)

            # Determine validation status based on complexity
            status = "VALID"
            confidence = 0.7
            explanation = (
                f"Code complexity is {analysis.get('overall_complexity', 'Unknown')}."
            )

            if analysis.get("has_high_complexity", False):
                status = "MOSTLY_VALID"
                confidence = 0.6
                explanation = f"Code has high complexity ({analysis.get('overall_complexity', 'Unknown')})."

            # Get optimization suggestions
            suggestions = []
            for func_info in analysis.get("functions", []):
                func_name = func_info.get("name", "unknown")
                complexity = func_info.get("complexity", "O(1)")

                if self._is_high_complexity(complexity):
                    suggestions.append(
                        f"Function '{func_name}' has high complexity: {complexity}"
                    )

                # Add specific optimization suggestions
                for opt in func_info.get("optimizations", []):
                    suggestions.append(f"[{func_name}] {opt}")

            # Prepare the result
            result = {
                "status": status,
                "confidence": confidence,
                "explanation": explanation,
                "suggestions": suggestions,
                "source": "complexity_validator",
                "complexity_analysis": analysis,
                "execution_time": time.time() - start_time,
            }

            return result
        except Exception as e:
            logger.error(f"Error in complexity validation: {str(e)}")
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error in complexity validation: {str(e)}",
                "suggestions": ["Try again with simpler code."],
                "source": "complexity_validator",
            }

    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate the complexity of a Python file.

        Args:
            file_path: Path to the file to validate

        Returns:
            A dictionary with validation results
        """
        if not self.is_available():
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "Complexity analyzer not available.",
                "suggestions": ["Install the complexity analyzer module."],
                "source": "complexity_validator",
                "file_path": file_path,
            }

        try:
            # Analyze file complexity
            start_time = time.time()
            analysis = self.analyzer.analyze_file(file_path)

            # Determine validation status based on complexity
            status = "VALID"
            confidence = 0.7
            explanation = (
                f"Code complexity is {analysis.get('overall_complexity', 'Unknown')}."
            )

            if analysis.get("has_high_complexity", False):
                status = "MOSTLY_VALID"
                confidence = 0.6
                explanation = f"Code has high complexity ({analysis.get('overall_complexity', 'Unknown')})."

            # Get optimization suggestions
            suggestions = []
            for func_info in analysis.get("functions", []):
                func_name = func_info.get("name", "unknown")
                complexity = func_info.get("complexity", "O(1)")

                if self._is_high_complexity(complexity):
                    suggestions.append(
                        f"Function '{func_name}' has high complexity: {complexity}"
                    )

                # Add specific optimization suggestions
                for opt in func_info.get("optimizations", []):
                    suggestions.append(f"[{func_name}] {opt}")

            # Prepare the result
            result = {
                "status": status,
                "confidence": confidence,
                "explanation": explanation,
                "suggestions": suggestions,
                "source": "complexity_validator",
                "complexity_analysis": analysis,
                "file_path": file_path,
                "execution_time": time.time() - start_time,
            }

            return result
        except Exception as e:
            logger.error(f"Error in complexity validation: {str(e)}")
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error in complexity validation: {str(e)}",
                "suggestions": ["Try again with simpler code."],
                "source": "complexity_validator",
                "file_path": file_path,
            }

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

    def format_complexity_results(self, results: Dict[str, Any]) -> str:
        """
        Format complexity results as a human-readable string.

        Args:
            results: The validation results

        Returns:
            A formatted string with the results
        """
        if not self.is_available():
            return "Complexity analyzer not available."

        if "complexity_analysis" not in results:
            return "No complexity analysis available."

        return self.analyzer.format_analysis_results(results["complexity_analysis"])


def test_complexity_validator():
    """Test the complexity validator."""
    validator = ComplexityValidator()

    if not validator.is_available():
        print(
            "Complexity validator not available. Install the complexity analyzer module."
        )
        return

    # Test with a simple code snippet
    code = """
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
"""

    # Validate the code
    print("Validating code complexity...")
    result = validator.validate(code)

    # Print the results
    print("\n" + "=" * 60)
    print("COMPLEXITY VALIDATION RESULT")
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

    # Print detailed complexity analysis
    print("\n" + "=" * 60)
    print("DETAILED COMPLEXITY ANALYSIS")
    print("=" * 60)
    print(validator.format_complexity_results(result))
    print("=" * 60)


if __name__ == "__main__":
    test_complexity_validator()
