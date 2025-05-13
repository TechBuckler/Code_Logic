#!/usr/bin/env python
"""
Validation Pipeline

This script integrates the Shadow validator into the code_logic_tool_full pipeline,
allowing for automated validation of Python code during the refactoring process.
"""

import os
import sys
import json
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


def validate_pipeline(
    input_dir: str, output_file: Optional[str] = None, recursive: bool = True
) -> Dict[str, Any]:
    """
    Validate all Python files in a directory as part of a pipeline.

    Args:
        input_dir: Path to the directory to validate
        output_file: Path to the output file for the validation report
        recursive: Whether to recursively validate subdirectories

    Returns:
        A dictionary with validation results
    """
    if not VALIDATION_MODULE_AVAILABLE:
        return {
            "status": "ERROR",
            "explanation": "Validation module not available",
            "files": [],
        }

    validation_module = ValidationModule()
    results = validation_module.validate_directory(input_dir, recursive)

    # Generate a summary
    summary = {
        "total_files": len(results["files"]),
        "valid_files": 0,
        "invalid_files": 0,
        "error_files": 0,
        "issues_by_type": {},
    }

    for result in results["files"]:
        if result["status"] == "VALID":
            summary["valid_files"] += 1
        elif result["status"] == "NOT_VALID":
            summary["invalid_files"] += 1

            # Count issues by type
            for suggestion in result.get("suggestions", []):
                issue_type = (
                    suggestion.split(":")[0] if ":" in suggestion else suggestion
                )
                if issue_type in summary["issues_by_type"]:
                    summary["issues_by_type"][issue_type] += 1
                else:
                    summary["issues_by_type"][issue_type] = 1
        else:
            summary["error_files"] += 1

    # Add the summary to the results
    results["summary"] = summary

    # Write the results to a file if specified
    if output_file:
        try:
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
            print(f"Validation report written to {output_file}")
        except Exception as e:
            print(f"Error writing validation report: {str(e)}")

    return results


def main():
    """Main function for the validation pipeline."""
    parser = argparse.ArgumentParser(description="Validation Pipeline")
    parser.add_argument("input_dir", help="Path to the directory to validate")
    parser.add_argument(
        "--output", help="Path to the output file for the validation report"
    )
    parser.add_argument(
        "--recursive", action="store_true", help="Recursively validate subdirectories"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print(f"Error: Directory {args.input_dir} does not exist.")
        return 1

    results = validate_pipeline(args.input_dir, args.output, args.recursive)

    if results["status"] == "ERROR":
        print(f"Error: {results['explanation']}")
        return 1

    # Print the summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total files: {results['summary']['total_files']}")
    print(f"Valid files: {results['summary']['valid_files']}")
    print(f"Invalid files: {results['summary']['invalid_files']}")
    print(f"Error files: {results['summary']['error_files']}")

    if results["summary"]["issues_by_type"]:
        print("\nIssues by type:")
        for issue_type, count in results["summary"]["issues_by_type"].items():
            print(f"- {issue_type}: {count}")

    print("=" * 60)

    # Return success if all files are valid, otherwise return an error code
    if (
        results["summary"]["invalid_files"] == 0
        and results["summary"]["error_files"] == 0
    ):
        print("\nAll files passed validation!")
        return 0
    else:
        print("\nSome files failed validation. See the report for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
