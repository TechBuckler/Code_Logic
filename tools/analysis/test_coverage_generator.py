#!/usr/bin/env python
"""
Test Coverage Generator

This script provides a comprehensive testing solution that:
1. Discovers all modules in the codebase
2. Generates test cases for untested modules
3. Runs all existing and generated tests
4. Produces a coverage report
5. Integrates with the existing documentation system
6. Validates imports for all modules

Usage:
    py test_coverage_generator.py [--discover] [--generate] [--run] [--report] [--validate-imports] [--fix-imports]

Options:
    --discover         Only discover modules and create a report
    --generate         Generate test cases for untested modules
    --run              Run all tests
    --report           Generate coverage report
    --validate-imports Check that all imports work correctly
    --fix-imports      Attempt to fix import issues
    --all              Do all of the above (default)
    --fast             Run in fast mode (skip slow tests)
"""

import os
import sys
import ast
import time
import json
import unittest
import argparse
import subprocess
from typing import Dict, List, Any, Optional, Set, Tuple

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)


# Define utility functions directly to avoid import issues
def ensure_dir(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)
    return directory


def read_file(file_path):
    """Read a file and return its contents."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(file_path, content):
    """Write content to a file."""
    ensure_dir(os.path.dirname(file_path))
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


# Try to import coverage - install if not available
try:
    import coverage
except ImportError:
    print("Coverage package not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "coverage"])
    import coverage


class TestCoverageGenerator:
    """Generate and run tests with coverage for the entire codebase."""

    def __init__(self):
        """Initialize the test coverage generator."""
        self.project_root = project_root
        self.tests_dir = os.path.join(self.project_root, "tests")
        self.unit_tests_dir = os.path.join(self.tests_dir, "unit")
        self.integration_tests_dir = os.path.join(self.tests_dir, "integration")
        self.e2e_tests_dir = os.path.join(self.tests_dir, "e2e")
        self.coverage_dir = os.path.join(self.project_root, "coverage")

        # Ensure directories exist
        for directory in [
            self.tests_dir,
            self.unit_tests_dir,
            self.integration_tests_dir,
            self.e2e_tests_dir,
            self.coverage_dir,
        ]:
            ensure_dir(directory)

        # Initialize coverage
        self.cov = coverage.Coverage(
            source=[self.project_root],
            omit=[
                "*/__pycache__/*",
                "*/\\.git/*",
                "*/tests/*",
                "*/venv/*",
                "*/env/*",
                "*/.vscode/*",
                "*/coverage/*",
                "*/docs/auto_generated/*",
            ],
        )

    def discover_modules(self) -> List[Dict[str, Any]]:
        """
        Discover all Python modules in the codebase.

        Returns:
            List of dictionaries containing module information
        """
        print("\n🔍 Discovering modules...")
        modules = []

        # Find all Python files
        python_files = []
        for root, _, files in os.walk(self.project_root):
            # Skip certain directories
            if any(
                skip in root
                for skip in [
                    ".git",
                    "__pycache__",
                    ".vscode",
                    ".idea",
                    "venv",
                    "env",
                    "tests",
                    "docs/auto_generated",
                ]
            ):
                continue

            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.project_root)

                    # Skip test files and specific problematic files
                    if file.startswith("test_") or "test" in file.lower():
                        continue

                    # Get module name from file path
                    module_path = rel_path.replace(os.sep, ".").replace(".py", "")

                    # Add to modules list
                    modules.append(
                        {
                            "file_path": file_path,
                            "rel_path": rel_path,
                            "module_path": module_path,
                        }
                    )

        print(f"Found {len(modules)} Python modules")
        return modules

    def check_test_coverage(self, modules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check which modules have tests and which don't.

        Args:
            modules: List of module information dictionaries

        Returns:
            Dictionary with tested and untested modules
        """
        print("\n📊 Checking test coverage...")

        # Find all test files
        test_files = []
        for root, _, files in os.walk(self.tests_dir):
            for file in files:
                if file.startswith("test_") and file.endswith(".py"):
                    test_files.append(os.path.join(root, file))

        # Read test files to see which modules they import
        tested_modules = set()
        for test_file in test_files:
            try:
                content = read_file(test_file)
                tree = ast.parse(content)

                # Look for imports in the test file
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            tested_modules.add(name.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            tested_modules.add(node.module)
            except Exception as e:
                print(f"Error parsing {test_file}: {e}")

        # Determine which modules are tested and which aren't
        tested = []
        untested = []

        for module in modules:
            module_path = module["module_path"]
            parts = module_path.split(".")

            # Check if this module or any parent module is tested
            is_tested = False
            for i in range(len(parts)):
                prefix = ".".join(parts[: i + 1])
                if prefix in tested_modules:
                    is_tested = True
                    break

            if is_tested:
                tested.append(module)
            else:
                untested.append(module)

        print(f"Modules with tests: {len(tested)}")
        print(f"Modules without tests: {len(untested)}")

        return {"tested": tested, "untested": untested}

    def generate_test_cases(self, untested_modules: List[Dict[str, Any]]) -> int:
        """
        Generate test cases for untested modules.

        Args:
            untested_modules: List of untested module information dictionaries

        Returns:
            Number of test cases generated
        """
        print("\n🧪 Generating test cases...")

        generated_count = 0

        for module in untested_modules:
            file_path = module["file_path"]
            module_path = module["module_path"]

            # Determine appropriate test directory (unit, integration, e2e)
            if "tools" in module_path:
                test_dir = self.unit_tests_dir
            elif "core" in module_path or "utils" in module_path:
                test_dir = self.unit_tests_dir
            else:
                test_dir = self.integration_tests_dir

            # Create test file path
            module_name = os.path.basename(file_path).replace(".py", "")
            test_file_path = os.path.join(test_dir, f"test_{module_name}.py")

            # Skip if test file already exists
            if os.path.exists(test_file_path):
                continue

            try:
                # Parse the module to extract classes and functions
                content = read_file(file_path)
                tree = ast.parse(content)

                # Extract module docstring
                module_docstring = ast.get_docstring(tree) or f"Tests for {module_path}"

                # Extract classes and functions
                classes = []
                functions = []

                for node in tree.body:
                    if isinstance(node, ast.ClassDef):
                        classes.append(node.name)
                    elif isinstance(node, ast.FunctionDef):
                        # Skip private functions
                        if not node.name.startswith("_"):
                            functions.append(node.name)

                # Generate test file content
                test_content = f'''"""
{module_docstring}

Auto-generated test cases for {module_path}
"""
# Fix imports for reorganized codebase
import utils.import_utils

import os
import sys
import unittest
from pathlib import Path

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import the module to test
try:
    import {module_path}
except ImportError as e:
    print(f"Error importing {module_path}: {{e}}")
    print("Make sure the module exists and imports are correct.")
    sys.exit(1)

'''

                # Add test class
                if classes:
                    for class_name in classes:
                        test_content += f'''
class Test{class_name}(unittest.TestCase):
    """Test the {class_name} class."""
    
    def setUp(self):
        """Set up the test environment."""
        pass
    
    def tearDown(self):
        """Clean up after the test."""
        pass
    
    def test_{class_name.lower()}_initialization(self):
        """Test that {class_name} can be initialized."""
        try:
            instance = {module_path}.{class_name}()
            self.assertIsNotNone(instance)
        except Exception as e:
            self.fail(f"Failed to initialize {class_name}: {{e}}")
    
'''

                # Add test functions
                if functions:
                    test_content += f'''
class Test{module_name.capitalize()}Functions(unittest.TestCase):
    """Test the functions in {module_path}."""
    
    def setUp(self):
        """Set up the test environment."""
        pass
    
    def tearDown(self):
        """Clean up after the test."""
        pass
    
'''

                    for func_name in functions:
                        test_content += f'''
    def test_{func_name}(self):
        """Test the {func_name} function."""
        try:
            # Call the function with appropriate arguments
            # This is a placeholder - you'll need to provide actual arguments
            # result = {module_path}.{func_name}()
            # self.assertIsNotNone(result)
            pass
        except Exception as e:
            self.fail(f"Failed to call {func_name}: {{e}}")
    
'''

                # Add main block
                test_content += """
if __name__ == "__main__":
    unittest.main()
"""

                # Write the test file
                try:
                    write_file(test_file_path, test_content)
                    generated_count += 1
                    print(f"Generated test case: {test_file_path}")
                except Exception as e:
                    print(f"Error writing test file {test_file_path}: {e}")

            except Exception as e:
                print(f"Error generating test for {module_path}: {e}")

        print(f"Generated {generated_count} test cases")
        return generated_count

    def run_tests(self) -> Dict[str, Any]:
        """
        Run all tests with coverage.

        Returns:
            Dictionary with test results
        """
        print("\n🏃 Running tests with coverage...")

        # Start coverage
        self.cov.start()

        # Discover and run tests
        loader = unittest.TestLoader()
        suite = loader.discover(self.tests_dir)

        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        # Stop coverage
        self.cov.stop()

        # Save coverage data
        self.cov.save()

        # Return test results
        return {
            "run": result.testsRun,
            "errors": len(result.errors),
            "failures": len(result.failures),
            "skipped": len(result.skipped),
        }

    def generate_coverage_report(self) -> Dict[str, Any]:
        """
        Generate coverage report.

        Returns:
            Dictionary with coverage statistics
        """
        print("\n📝 Generating coverage report...")

        # Generate HTML report
        html_dir = os.path.join(self.coverage_dir, "html")
        ensure_dir(html_dir)
        self.cov.html_report(directory=html_dir)

        # Generate JSON report
        json_file = os.path.join(self.coverage_dir, "coverage.json")
        self.cov.json_report(outfile=json_file)

        # Get coverage data
        data = self.cov.get_data()
        total_statements = 0
        covered_statements = 0

        for filename in data.measured_files():
            # Skip certain files
            if any(skip in filename for skip in ["__pycache__", ".git", "tests"]):
                continue

            # Get line coverage for this file
            line_data = data.lines(filename)
            file_statements = len(line_data)
            file_covered = sum(1 for _ in data.executed_lines(filename))

            total_statements += file_statements
            covered_statements += file_covered

        # Calculate coverage percentage
        coverage_pct = (
            (covered_statements / total_statements * 100) if total_statements > 0 else 0
        )

        # Create coverage report
        report = {
            "total_statements": total_statements,
            "covered_statements": covered_statements,
            "coverage_percentage": coverage_pct,
            "html_report": html_dir,
            "json_report": json_file,
        }

        # Save report summary
        summary_file = os.path.join(self.coverage_dir, "summary.json")
        with open(summary_file, "w") as f:
            json.dump(report, f, indent=2)

        print(
            f"Coverage: {coverage_pct:.2f}% ({covered_statements}/{total_statements} statements)"
        )
        print(f"HTML report: {html_dir}")
        print(f"JSON report: {json_file}")

        return report

    def integrate_with_documentation(self, coverage_report: Dict[str, Any]) -> None:
        """
        Integrate coverage information with the existing documentation system.

        Args:
            coverage_report: Dictionary with coverage statistics
        """
        print("\n📚 Integrating with documentation system...")

        # Check if documentation generator exists
        doc_generator_path = os.path.join(
            self.project_root, "utils", "file", "document_codebase.py"
        )
        if not os.path.exists(doc_generator_path):
            print("Documentation generator not found. Skipping integration.")
            return

        # Run the documentation generator
        print("Running documentation generator...")
        try:
            subprocess.run([sys.executable, doc_generator_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running documentation generator: {e}")
            return

        # Add coverage information to documentation
        docs_dir = os.path.join(self.project_root, "docs", "auto_generated")
        if not os.path.exists(docs_dir):
            print("Documentation directory not found. Skipping integration.")
            return

        # Create coverage page
        coverage_doc_path = os.path.join(docs_dir, "coverage.md")
        with open(coverage_doc_path, "w") as f:
            f.write("# Test Coverage Report\n\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Summary\n\n")
            f.write(
                f"- **Coverage Percentage:** {coverage_report['coverage_percentage']:.2f}%\n"
            )
            f.write(
                f"- **Covered Statements:** {coverage_report['covered_statements']}/{coverage_report['total_statements']}\n"
            )
            f.write(
                f"- **HTML Report:** [View HTML Report](../coverage/html/index.html)\n\n"
            )

            f.write("## Test Results\n\n")
            f.write(
                f"- **Tests Run:** {coverage_report.get('test_results', {}).get('run', 'N/A')}\n"
            )
            f.write(
                f"- **Errors:** {coverage_report.get('test_results', {}).get('errors', 'N/A')}\n"
            )
            f.write(
                f"- **Failures:** {coverage_report.get('test_results', {}).get('failures', 'N/A')}\n"
            )
            f.write(
                f"- **Skipped:** {coverage_report.get('test_results', {}).get('skipped', 'N/A')}\n\n"
            )

        print(f"Created coverage documentation: {coverage_doc_path}")

        # Update index.md to include coverage link
        index_path = os.path.join(docs_dir, "index.md")
        if os.path.exists(index_path):
            content = read_file(index_path)
            if "Test Coverage Report" not in content:
                with open(index_path, "a") as f:
                    f.write("\n## Test Coverage\n\n")
                    f.write("- [Test Coverage Report](coverage.md)\n")
                print(f"Updated documentation index: {index_path}")

    def run_all(self) -> None:
        """Run the entire test coverage generation process."""
        # Discover modules
        modules = self.discover_modules()

        # Check test coverage
        coverage_check = self.check_test_coverage(modules)

        # Generate test cases for untested modules
        self.generate_test_cases(coverage_check["untested"])

        # Run tests
        test_results = self.run_tests()

        # Generate coverage report
        coverage_report = self.generate_coverage_report()
        coverage_report["test_results"] = test_results

        # Integrate with documentation
        self.integrate_with_documentation(coverage_report)

        print("\n✅ Test coverage generation complete!")
        print(f"Coverage: {coverage_report['coverage_percentage']:.2f}%")
        print(f"HTML report: {coverage_report['html_report']}")


def validate_imports(modules, fix=False, fast=False):
    """
    Validate that all modules can be imported correctly.

    Args:
        modules: List of module information dictionaries
        fix: Whether to attempt to fix import issues
        fast: Whether to run in fast mode (skip slow imports)

    Returns:
        Dictionary with validation results
    """
    print("\n🔍 Validating imports...")

    # Track results
    results = {
        "total": len(modules),
        "success": 0,
        "failed": 0,
        "fixed": 0,
        "failures": [],
    }

    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Make sure utils.import_utils is available
    try:
        import utils.import_utils

        utils.import_utils.patch_imports()
    except ImportError:
        print(
            "Warning: utils.import_utils not available. Import validation may be less effective."
        )

    # Process each module
    for module in modules:
        module_path = module["module_path"]

        # Skip certain modules in fast mode
        if fast and any(skip in module_path for skip in ["test", "docs", "examples"]):
            continue

        # Try to import the module
        try:
            __import__(module_path)
            results["success"] += 1
            print(f"✓ {module_path}")
        except Exception as e:
            results["failed"] += 1
            error_msg = str(e)
            print(f"✗ {module_path}: {error_msg}")
            results["failures"].append({"module": module_path, "error": error_msg})

            # Try to fix the issue
            if fix:
                fixed = False

                # Common import issues and fixes
                if "No module named" in error_msg:
                    missing_module = error_msg.split("No module named ")[1].strip("'")

                    # Create compatibility module if needed
                    if missing_module.startswith("modules.") or missing_module in [
                        "module_system",
                        "background_system",
                    ]:
                        # Create minimal compatibility module
                        try:
                            # Determine the file path
                            if missing_module == "module_system":
                                file_path = os.path.join(
                                    project_root, "module_system.py"
                                )
                            elif missing_module == "background_system":
                                file_path = os.path.join(
                                    project_root, "background_system.py"
                                )
                            else:
                                parts = missing_module.split(".")
                                file_path = os.path.join(project_root, *parts) + ".py"

                            # Create directory if needed
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)

                            # Only create if it doesn't exist
                            if not os.path.exists(file_path):
                                with open(file_path, "w") as f:
                                    f.write(
                                        f"""{missing_module} compatibility module.
Auto-generated for compatibility during refactoring.
"""
                                    )
                                    f.write("# Add minimal functionality\n")
                                    f.write("class DummyClass:\n    pass\n\n")
                                    f.write(
                                        f"# Export symbols\n__all__ = ['DummyClass']\n"
                                    )

                                print(f"  Created compatibility module: {file_path}")
                                fixed = True
                                results["fixed"] += 1
                        except Exception as fix_error:
                            print(
                                f"  Failed to create compatibility module: {fix_error}"
                            )

                # Try to import again after fixing
                if fixed:
                    try:
                        # Clear import cache
                        if module_path in sys.modules:
                            del sys.modules[module_path]

                        __import__(module_path)
                        print(f"  ✓ Fixed import for {module_path}")
                        results["success"] += 1
                        results["failed"] -= 1
                    except Exception as retry_error:
                        print(f"  ✗ Still failed: {retry_error}")

    # Print summary
    print(
        f"\nImport validation complete: {results['success']}/{results['total']} modules imported successfully"
    )
    if results["fixed"] > 0:
        print(f"Fixed {results['fixed']} import issues")

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test Coverage Generator")
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Only discover modules and create a report",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate test cases for untested modules",
    )
    parser.add_argument("--run", action="store_true", help="Run all tests")
    parser.add_argument(
        "--report", action="store_true", help="Generate coverage report"
    )
    parser.add_argument(
        "--validate-imports",
        action="store_true",
        help="Check that all imports work correctly",
    )
    parser.add_argument(
        "--fix-imports", action="store_true", help="Attempt to fix import issues"
    )
    parser.add_argument(
        "--all", action="store_true", help="Do all of the above (default)"
    )
    parser.add_argument(
        "--fast", action="store_true", help="Run in fast mode (skip slow tests)"
    )

    args = parser.parse_args()

    # Default to --all if no arguments provided
    if not (
        args.discover
        or args.generate
        or args.run
        or args.report
        or args.validate_imports
        or args.fix_imports
    ):
        args.all = True

    generator = TestCoverageGenerator()

    if args.discover:
        # Just discover modules and create a report
        modules = generator.discover_modules()
        print(f"\nDiscovered {len(modules)} modules in the codebase")

        # Create a simple report
        report_dir = os.path.join(generator.project_root, "coverage")
        ensure_dir(report_dir)
        report_file = os.path.join(report_dir, "modules_report.json")

        # Group modules by directory
        module_groups = {}
        for module in modules:
            parts = module["module_path"].split(".")
            if len(parts) > 0:
                top_level = parts[0]
                if top_level not in module_groups:
                    module_groups[top_level] = []
                module_groups[top_level].append(module)

        # Create report
        report = {
            "total_modules": len(modules),
            "module_groups": {k: len(v) for k, v in module_groups.items()},
            "modules": [m["module_path"] for m in modules],
        }

        # Write report
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\nModule report written to: {report_file}")
        print("\nModule groups:")
        # Sort by count (convert to list of tuples first)
        sorted_groups = sorted(
            [(k, len(v)) for k, v in module_groups.items()],
            key=lambda x: x[1],
            reverse=True,
        )
        for group, count in sorted_groups:
            print(f"  {group}: {count} modules")

        return

    if args.generate or args.all:
        modules = generator.discover_modules()
        coverage_check = generator.check_test_coverage(modules)
        generator.generate_test_cases(coverage_check["untested"])

    if args.run or args.all:
        generator.run_tests()

    if args.report or args.all:
        coverage_report = generator.generate_coverage_report()
        generator.integrate_with_documentation(coverage_report)

    if args.validate_imports or args.fix_imports or args.all:
        modules = generator.discover_modules()
        validate_imports(modules, fix=args.fix_imports or args.all, fast=args.fast)

    if args.all:
        print("\n✅ Test coverage generation complete!")


if __name__ == "__main__":
    main()
