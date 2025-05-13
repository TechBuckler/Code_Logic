#!/usr/bin/env python
"""
Validate Code Tool

This script provides a command-line interface for validating Python code
using the Shadow validator integrated with the module system.
"""

import os
import sys
import argparse
from typing import Dict, List, Any, Optional

# Add the project root to the path if needed
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the validation module
try:
    from modules.validation_module import ValidationModule

    VALIDATION_MODULE_AVAILABLE = True
except ImportError:
    VALIDATION_MODULE_AVAILABLE = False
    print("Validation module not available. Make sure it's installed correctly.")


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
    parser = argparse.ArgumentParser(description="Code Validation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Validate file command
    validate_file_parser = subparsers.add_parser("file", help="Validate a Python file")
    validate_file_parser.add_argument("file_path", help="Path to the file to validate")
    validate_file_parser.add_argument(
        "--function", help="Name of the function to validate"
    )

    # Validate directory command
    validate_dir_parser = subparsers.add_parser(
        "directory", help="Validate all Python files in a directory"
    )
    validate_dir_parser.add_argument(
        "directory_path", help="Path to the directory to validate"
    )
    validate_dir_parser.add_argument(
        "--recursive", action="store_true", help="Recursively validate subdirectories"
    )

    # Validate code command
    validate_code_parser = subparsers.add_parser("code", help="Validate a code snippet")
    validate_code_parser.add_argument("code", help="Code snippet to validate")

    # Stats command
    subparsers.add_parser("stats", help="Show validation statistics")

    args = parser.parse_args()

    if not VALIDATION_MODULE_AVAILABLE:
        print(
            "Error: Validation module not available. Make sure it's installed correctly."
        )
        return 1

    validation_module = ValidationModule()

    if args.command == "file":
        if not os.path.exists(args.file_path):
            print(f"Error: File {args.file_path} does not exist.")
            return 1

        if args.function:
            # Read the file
            with open(args.file_path, "r") as f:
                code = f.read()

            # Validate the function
            result = validation_module.validate_function(code, args.function)
            result["file_path"] = args.file_path
        else:
            # Validate the file
            result = validation_module.validate_file(args.file_path)

        format_validation_result(result)

    elif args.command == "directory":
        if not os.path.exists(args.directory_path):
            print(f"Error: Directory {args.directory_path} does not exist.")
            return 1

        results = validation_module.validate_directory(
            args.directory_path, args.recursive
        )

        if results["status"] == "ERROR":
            print(f"Error: {results['explanation']}")
            return 1

        print(f"Validated {len(results['files'])} files in {args.directory_path}")

        # Count issues by severity
        valid_files = 0
        invalid_files = 0
        error_files = 0

        for result in results["files"]:
            if result["status"] == "VALID":
                valid_files += 1
            elif result["status"] == "NOT_VALID":
                invalid_files += 1
            else:
                error_files += 1

        print(f"Valid files: {valid_files}")
        print(f"Invalid files: {invalid_files}")
        print(f"Error files: {error_files}")

        # Ask if the user wants to see details for invalid files
        if invalid_files > 0:
            print("\nInvalid files:")
            for result in results["files"]:
                if result["status"] == "NOT_VALID":
                    print(
                        f"- {result['file_path']} (Confidence: {result['confidence']:.2f})"
                    )

            see_details = input(
                "\nDo you want to see details for invalid files? (y/n): "
            )
            if see_details.lower() == "y":
                for result in results["files"]:
                    if result["status"] == "NOT_VALID":
                        format_validation_result(result)

    elif args.command == "code":
        result = validation_module.validate_code(args.code)
        format_validation_result(result)

    elif args.command == "stats":
        stats = validation_module.get_stats()
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
