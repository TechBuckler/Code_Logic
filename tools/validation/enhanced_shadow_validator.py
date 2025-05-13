#!/usr/bin/env python
"""
Enhanced Shadow Validator

This module integrates rule-based validation, embeddings, and AI models
into a comprehensive, cost-effective validation system.
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
logger = logging.getLogger("enhanced_shadow_validator")

# Import our validation components
from tools.validation.shadow_validator import RuleBasedValidator

try:
    from tools.validation.shadow_embeddings import LocalEmbeddings, ResponseCache

    EMBEDDINGS_AVAILABLE = True
except ImportError:
    logger.warning(
        "Embeddings not available. Install sentence-transformers for enhanced validation."
    )
    EMBEDDINGS_AVAILABLE = False

try:
    from tools.validation.shadow_ai_validator import AIValidatorSync

    AI_AVAILABLE = True
except ImportError:
    logger.warning(
        "AI validation not available. Install OpenAI for AI-powered validation."
    )
    AI_AVAILABLE = False


class EnhancedShadowValidator:
    """
    Enhanced Shadow Validator that combines rule-based validation, embeddings, and AI models.
    """

    def __init__(self):
        """Initialize the enhanced shadow validator."""
        # Initialize components
        self.rule_validator = RuleBasedValidator()
        self.embeddings = LocalEmbeddings() if EMBEDDINGS_AVAILABLE else None
        self.cache = ResponseCache() if EMBEDDINGS_AVAILABLE else None
        self.ai_validator = AIValidatorSync() if AI_AVAILABLE else None

        # Initialize statistics
        self.stats = {
            "total_validations": 0,
            "free_validations": 0,
            "paid_validations": 0,
            "total_cost": 0.0,
            "validation_modes": {
                "rule_based": 0,
                "pattern_matching": 0,
                "embeddings": 0,
                "ai_model": 0,
            },
            "model_usage": {
                "gpt-3.5-turbo": 0,
                "gpt-4-turbo": 0,
                "gpt-4o-mini": 0,
                "gpt-4o": 0,
            },
        }

    def validate_code(self, code: str, scope: str = "all") -> Dict[str, Any]:
        """
        Validate code using a multi-layered approach.

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
        if self.cache:
            cached_result = self.cache.get(code_hash)
            if cached_result:
                logger.info(f"Cache hit for {code_hash}")
                # Add execution time to the result
                cached_result["execution_time"] = time.time() - start_time
                return cached_result

        # Layered validation approach
        # 1. Rule-based validation (free)
        rule_result = self.rule_validator.validate(code)

        if rule_result:
            # If rule-based validation found critical issues, return immediately
            if (
                rule_result["status"] == "NOT_VALID"
                and rule_result["confidence"] >= 0.9
            ):
                logger.info(
                    f"Rule-based validation found critical issues for {code_hash}"
                )
                self.stats["free_validations"] += 1
                self.stats["validation_modes"]["rule_based"] += 1

                # Add execution time to the result
                rule_result["execution_time"] = time.time() - start_time

                # Cache the result
                if self.cache:
                    self.cache.set(code_hash, rule_result)

                return rule_result

        # 2. Pattern matching and embeddings (free)
        if self.embeddings and self.cache:
            # Find similar code using embeddings
            similar = self.embeddings.find_similar(code, threshold=0.85)
            if similar:
                logger.info(
                    f"Found similar code with similarity {similar['similarity']:.2f} for {code_hash}"
                )
                self.stats["free_validations"] += 1
                self.stats["validation_modes"]["embeddings"] += 1

                # Get the result for the similar code
                similar_result = similar["result"]

                # Add metadata to the result
                similar_result["similarity"] = similar["similarity"]
                similar_result["execution_time"] = time.time() - start_time
                similar_result["source"] = "embeddings"

                # Cache the result
                self.cache.set(code_hash, similar_result)

                return similar_result

        # 3. AI validation (paid, only if needed)
        if self.ai_validator and self.ai_validator.is_available():
            # Select a model
            model = self.ai_validator.select_model()

            # Validate with the selected model
            logger.info(f"Using AI model {model} for {code_hash}")
            ai_result = self.ai_validator.validate_code(code, model)

            # Update statistics
            self.stats["paid_validations"] += 1
            self.stats["validation_modes"]["ai_model"] += 1
            self.stats["model_usage"][model] += 1
            self.stats["total_cost"] += ai_result.get("cost", 0.0)

            # Add execution time to the result
            ai_result["execution_time"] = time.time() - start_time

            # Cache the result
            if self.cache:
                self.cache.set(code_hash, ai_result)

                # Also save the result with its embedding
                if self.embeddings:
                    self.embeddings.save_result(code, ai_result)

            return ai_result

        # If AI validation is not available, return the rule-based result
        logger.info(f"Using rule-based validation for {code_hash}")
        self.stats["free_validations"] += 1
        self.stats["validation_modes"]["rule_based"] += 1

        # Add execution time to the result
        rule_result["execution_time"] = time.time() - start_time

        # Cache the result
        if self.cache:
            self.cache.set(code_hash, rule_result)

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

    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a Python file.

        Args:
            file_path: Path to the file to validate

        Returns:
            A dictionary with validation results
        """
        try:
            with open(file_path, "r") as f:
                code = f.read()

            result = self.validate_code(code)
            result["file_path"] = file_path
            return result
        except Exception as e:
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error validating file {file_path}: {str(e)}",
                "suggestions": [],
                "file_path": file_path,
            }

    def validate_directory(
        self, directory_path: str, recursive: bool = True
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Validate all Python files in a directory.

        Args:
            directory_path: Path to the directory to validate
            recursive: Whether to recursively validate subdirectories

        Returns:
            A dictionary with validation results for each file
        """
        results = {"status": "SUCCESS", "files": []}

        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        result = self.validate_file(file_path)
                        results["files"].append(result)

                if not recursive:
                    break

            return results
        except Exception as e:
            return {
                "status": "ERROR",
                "explanation": f"Error validating directory {directory_path}: {str(e)}",
                "files": [],
            }

    def get_stats(self) -> Dict[str, Any]:
        """
        Get validation statistics.

        Returns:
            A dictionary with validation statistics
        """
        stats = self.stats.copy()

        # Calculate percentages
        if stats["total_validations"] > 0:
            stats["free_percentage"] = (
                stats["free_validations"] / stats["total_validations"]
            ) * 100
            stats["paid_percentage"] = (
                stats["paid_validations"] / stats["total_validations"]
            ) * 100
        else:
            stats["free_percentage"] = 0.0
            stats["paid_percentage"] = 0.0

        # Calculate cost per 1,000 validations
        if stats["total_validations"] > 0:
            stats["cost_per_1000"] = (
                stats["total_cost"] / stats["total_validations"]
            ) * 1000
        else:
            stats["cost_per_1000"] = 0.0

        return stats

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


def format_validation_result(result: Dict[str, Any]) -> None:
    """
    Format and print a validation result.

    Args:
        result: The validation result to format
    """
    print("\n" + "=" * 60)
    print("VALIDATION RESULT")
    print("=" * 60)

    if "file_path" in result:
        print(f"File: {result['file_path']}")

    print(f"Status: {result.get('status', 'UNKNOWN')}")
    print(f"Confidence: {result.get('confidence', 0.0):.2f}")
    print(f"Source: {result.get('source', 'unknown')}")

    if "cost" in result:
        print(f"Cost: ${result.get('cost', 0.0):.6f}")

    if "similarity" in result:
        print(f"Similarity: {result.get('similarity', 0.0):.2f}")

    if "execution_time" in result:
        print(f"Execution time: {result['execution_time']:.2f} seconds")

    if "explanation" in result:
        print(f"\nExplanation: {result['explanation']}")

    if "suggestions" in result and result["suggestions"]:
        print("\nSuggestions:")
        for i, suggestion in enumerate(result["suggestions"], 1):
            print(f"{i}. {suggestion}")

    print("=" * 60)


def test_validator():
    """Test the enhanced shadow validator."""
    validator = EnhancedShadowValidator()

    # Test with a simple code snippet
    code = """
def hello_world():
    # Missing docstring
    print("Hello, World!")
    
class badClass:
    # Missing docstring and wrong naming convention
    def __init__(self):
        self.value = 42
    
    def getValue(self):
        # Wrong naming convention
        return self.value
    """

    # Validate the code
    print("Validating code...")
    result = validator.validate_code(code)
    format_validation_result(result)

    # Validate the code again (should use cache)
    print("\nValidating code again (should use cache)...")
    result = validator.validate_code(code)
    format_validation_result(result)

    # Validate a function
    print("\nValidating function...")
    result = validator.validate_function(code, "getValue")
    format_validation_result(result)

    # Get stats
    stats = validator.get_stats()
    print("\n" + "=" * 60)
    print("VALIDATION STATS")
    print("=" * 60)
    print(f"Total validations: {stats['total_validations']}")
    print(
        f"Free validations: {stats['free_validations']} ({stats['free_percentage']:.1f}%)"
    )
    print(
        f"Paid validations: {stats['paid_validations']} ({stats['paid_percentage']:.1f}%)"
    )
    print(f"Total cost: ${stats['total_cost']:.6f}")
    print(f"Cost per 1,000 validations: ${stats['cost_per_1000']:.2f}")

    print("\nVALIDATION MODES:")
    for mode, count in stats["validation_modes"].items():
        print(f"{mode}: {count}")

    print("\nMODEL USAGE:")
    for model, count in stats["model_usage"].items():
        if count > 0:
            print(f"{model}: {count}")

    print("=" * 60)


if __name__ == "__main__":
    test_validator()
