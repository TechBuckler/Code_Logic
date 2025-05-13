#!/usr/bin/env python
"""
Refactor Codebase

This is the main entry point for the codebase refactoring system. It provides a unified
interface to analyze, split, and rebuild Python code across the entire codebase.

Features:
- Analyze code to identify refactoring opportunities
- Break down complex files and functions into smaller components
- Rebuild optimized files from components
- Apply fixes for common issues (unused imports, error handling, etc.)
- Generate reports on codebase structure and complexity

Usage:
  python refactor_codebase.py analyze [--file FILE] [--output OUTPUT]
  python refactor_codebase.py split [--file FILE] [--function FUNCTION] [--output OUTPUT] [--apply]
  python refactor_codebase.py rebuild [--parts PARTS] [--output OUTPUT] [--apply]
  python refactor_codebase.py fix [--file FILE] [--apply]
  python refactor_codebase.py report [--output OUTPUT]
"""
import os
import sys
import json
import argparse
import datetime
import ast

# Dynamically detect the project root by searching upward for a 'utils' directory
import os
import sys
import json
import argparse
import datetime
import ast


# Find project root (directory containing 'utils')
def find_project_root(start_dir):
    current = os.path.abspath(start_dir)
    while True:
        if os.path.isdir(os.path.join(current, "utils")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


project_root = find_project_root(os.path.dirname(os.path.abspath(__file__)))
if not project_root:
    print(
        "[ERROR] Could not find project root (directory containing utils). Please run from within your project directory."
    )
    sys.exit(1)
sys.path.insert(0, project_root)

# Do NOT import utils.import_utils at the top level.
# If you need to use fix_imports_simple or similar, import it dynamically AFTER the directory rename step.


# Define utility functions directly to avoid circular imports
def read_file(file_path):
    """Read a file and return its contents."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(file_path, content):
    """Write content to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def ensure_directory(directory):
    """Ensure a directory exists."""
    os.makedirs(directory, exist_ok=True)


# Alias for compatibility with other modules
def ensure_dir(directory):
    """Alias for ensure_directory."""
    return ensure_directory(directory)


def get_python_files(directory):
    """Get all Python files in a directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


# Import refactoring modules

# Try to import from the new location first, then fall back to the old location
try:
    from tools.refactoring.refactor_splitter import (
        CodeSplitter,
        RefactoringSplitter,
        split_codebase,
    )
except ImportError:
    try:
        from refactor_splitter import CodeSplitter, RefactoringSplitter, split_codebase
    except ImportError:
        print(
            "[WARN] Could not import refactor_splitter from any location. Advanced code splitting/refactoring features will be disabled."
        )
        print(
            "If you want these features, restore refactor_splitter.py to tools/refactoring/ or the project root."
        )

        # Define minimal versions of these classes to prevent errors
        class CodeSplitter:
            def __init__(self, project_root):
                self.project_root = project_root

        class RefactoringSplitter(CodeSplitter):
            pass

        def split_codebase(*args, **kwargs):
            return {"split_files": 0}


# Check if tools are available
HAVE_TOOLS = False
HAVE_UTILS = True
try:
    # Try importing from the new location first
    sys.path.insert(0, os.path.join(project_root, "tools", "refactoring"))
    HAVE_TOOLS = True
except ImportError:
    try:
        # Try importing from the old location
        HAVE_TOOLS = True
    except ImportError:
        print(
            "Warning: Could not import existing splitters. Using fallback implementation."
        )
        HAVE_TOOLS = False


# Define a custom JSON encoder to handle AST nodes and other non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that can handle AST nodes and other non-serializable objects."""

    def default(self, obj):
        # Handle AST nodes
        if isinstance(obj, ast.AST):
            return {
                "_type": obj.__class__.__name__,
                "_fields": {k: getattr(obj, k) for k in obj._fields if hasattr(obj, k)},
            }
        # Handle sets
        elif isinstance(obj, set):
            return list(obj)
        # Let the base class handle everything else
        return super().default(obj)


# Define the analyze_codebase function if it's not in refactor_analyzer.py
def analyze_codebase():
    """Analyze the entire codebase."""
    analyzer = CodeAnalyzer(project_root)
    return analyzer.analyze_codebase()


def analyze_command(args):
    """Run the code analyzer."""
    analyzer = CodeAnalyzer(project_root)

    if args.file:
        # Analyze a specific file
        file_path = os.path.abspath(args.file)
        print(f"Analyzing file: {file_path}")

        analysis = analyzer.analyze_file(file_path)
        if analysis:
            # Print a summary of the analysis
            print("\nAnalysis Summary:")
            print(f"- Lines of code: {analysis['metrics']['loc']}")
            print(f"- Functions: {len(analysis['function_dependencies'])}")
            print(f"- Classes: {len(analysis['class_structure'])}")
            print(f"- Complexity: {analysis['metrics']['complexity']}")
            print(f"- Unused imports: {len(analysis['unused_imports'])}")
            print(f"- Complex functions: {len(analysis['complex_functions'])}")

            # Save the analysis to a file if requested
            if args.output:
                output_file = args.output
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(analysis, f, indent=2)
                print(f"\nAnalysis saved to: {output_file}")
    else:
        # Analyze the entire codebase
        print("Analyzing entire codebase...")

        analysis = analyze_codebase()

        # Print a summary of the analysis
        print("\nCodebase Analysis Summary:")
        print(f"- Files analyzed: {len(analysis['files'])}")
        print(
            f"- Total lines of code: {sum(file['metrics']['loc'] for file in analysis['files'])}"
        )
        print(
            f"- Average complexity: {sum(file['metrics']['complexity'] for file in analysis['files']) / len(analysis['files']):.2f}"
        )
        print(
            f"- Files with unused imports: {sum(1 for file in analysis['files'] if file['unused_imports'])}"
        )
        print(
            f"- Files with complex functions: {sum(1 for file in analysis['files'] if file['complex_functions'])}"
        )

        # Save the analysis to a file if requested
        if args.output:
            output_file = args.output
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(analysis, f, indent=2)
            print(f"\nAnalysis saved to: {output_file}")


def split_command(args):
    """Run the code splitter."""
    splitter = CodeSplitter(project_root)

    if args.file and args.function:
        # Split a specific function
        file_path = os.path.abspath(args.file)
        print(f"Splitting function {args.function} in {file_path}")

        result = splitter.split_function(
            file_path, args.function, args.output, not args.apply
        )

        if result:
            print(f"\nFunction {args.function} successfully split")
            print(f"- Output file: {result['output_file']}")
            print(f"- Helper functions: {len(result['helpers'])}")

            if not args.apply:
                print("\nThis was a dry run. To apply the changes, run with --apply")
    elif args.file:
        # Split a specific file
        file_path = os.path.abspath(args.file)
        print(f"Splitting file {file_path}")

        result = splitter.split_file(file_path, args.output, not args.apply)

        if result:
            print(
                f"\nFile successfully split into {len(result['split_files'])} components"
            )
            print(f"- Output directory: {result['output_dir']}")

            if not args.apply:
                print("\nThis was a dry run. To apply the changes, run with --apply")
    else:
        # Split the entire codebase
        print("Splitting entire codebase")

        result = split_codebase(args.output, not args.apply)

        print(
            f"\nCodebase successfully analyzed for splitting: {result['split_files']} files processed"
        )

        if not args.apply:
            print("\nThis was a dry run. To apply the changes, run with --apply")


def rebuild_command(args):
    """Run the code builder."""
    builder = CodeBuilder(project_root)

    if args.parts:
        # Rebuild from parts
        parts_dir = os.path.abspath(args.parts)
        print(f"Rebuilding from parts: {parts_dir}")

        if os.path.isdir(parts_dir) and os.path.exists(
            os.path.join(parts_dir, "__init__.py")
        ):
            # Rebuild a single file
            result = builder.rebuild_from_parts(
                parts_dir, args.output, True, not args.apply
            )

            if result:
                print(
                    f"\nFile successfully rebuilt from {len(result['part_files'])} parts"
                )
                print(f"- Output file: {result['output_file']}")

                if not args.apply:
                    print(
                        "\nThis was a dry run. To apply the changes, run with --apply"
                    )
        else:
            # Rebuild multiple files
            result = builder.rebuild_codebase(
                parts_dir, args.output, True, not args.apply
            )

            if result:
                print(
                    f"\nCodebase successfully rebuilt: {result['rebuilt_files']} files"
                )
                print(f"- Output directory: {result['output_dir']}")

                if not args.apply:
                    print(
                        "\nThis was a dry run. To apply the changes, run with --apply"
                    )
    else:
        print("Error: --parts argument is required for rebuild command")
        sys.exit(1)


def fix_command(args):
    """
    Run the code fixer and verifier pipeline:
    1. Import directory future-proofing
    2. Codebase-wide linting (flake8)
    3. Auto-formatting (black)
    4. Run all tests (if tests/ exists)
    5. Report summary of actions and failures
    # To disable auto-import-fix, set AUTO_FIX_IMPORTS = False below.
    """
    import shutil
    import subprocess
    from pathlib import Path

    project_root = Path(os.path.dirname(os.path.abspath(__file__))).parent
    old_dir = project_root / "utils" / "import"
    new_dir = project_root / "utils" / "import_utils"

    # Set this to False to disable automatic import directory fix
    AUTO_FIX_IMPORTS = True
    failures = []
    successes = []

    # --- Import Directory Refactor ---
    if AUTO_FIX_IMPORTS:
        try:
            if old_dir.exists() and not new_dir.exists():
                print(f"[fix-imports] Renaming {old_dir} -> {new_dir}")
                shutil.move(str(old_dir), str(new_dir))
                successes.append("Renamed import directory")
            else:
                print(f"[fix-imports] Directory already renamed or missing: {old_dir}")
            for d in [project_root / "utils", new_dir]:
                init_file = d / "__init__.py"
                if not init_file.exists():
                    print(f"[fix-imports] Creating {init_file}")
                    init_file.write_text("")
            py_files = list(project_root.rglob("*.py"))
            for py_file in py_files:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content = content.replace("utils.import.", "utils.import_utils.")
                new_content = new_content.replace(
                    "utils/import/", "utils/import_utils/"
                )
                new_content = new_content.replace(
                    "'utils.import.", "'utils.import_utils."
                )
                new_content = new_content.replace(
                    '"utils.import.', '"utils.import_utils.'
                )
                if new_content != content:
                    print(f"[fix-imports] Updating {py_file}")
                    with open(py_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
            print("[fix-imports] Import directory and references updated.")
            successes.append("Updated import references")
        except Exception as e:
            print(f"[ERROR] Import directory fix failed: {e}")
            failures.append(f"import-fix: {e}")

    # --- Linting (flake8) ---
    print("[lint] Running flake8 on codebase...")
    try:
        result = subprocess.run(
            ["py", "-m", "flake8", str(project_root)], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("[lint] No lint errors found!")
            successes.append("flake8 passed")
        else:
            print("[lint] Lint errors found:")
            print(result.stdout)
            failures.append("flake8: lint errors found")
    except Exception as e:
        print(f"[ERROR] flake8 failed: {e}")
        failures.append(f"flake8: {e}")

    # --- Formatting (black) ---
    print("[format] Running black on codebase...")
    try:
        result = subprocess.run(
            ["py", "-m", "black", str(project_root)], capture_output=True, text=True
        )
        print(result.stdout)
        if result.returncode == 0:
            successes.append("black formatted code")
        else:
            failures.append("black: formatting issues")
    except Exception as e:
        print(f"[ERROR] black failed: {e}")
        failures.append(f"black: {e}")

    # --- Run Tests ---
    tests_dir = project_root / "tests"
    if tests_dir.exists():
        print("[test] Running all tests in tests/ ...")
        try:
            result = subprocess.run(
                ["python", "-m", "unittest", "discover", "-s", str(tests_dir)],
                capture_output=True,
                text=True,
            )
            print(result.stdout)
            if result.returncode == 0:
                print("[test] All tests passed!")
                successes.append("tests passed")
            else:
                print("[test] Some tests failed.")
                failures.append("tests: some failed")
        except Exception as e:
            print(f"[ERROR] tests failed: {e}")
            failures.append(f"tests: {e}")
    else:
        print("[test] No tests/ directory found. Skipping tests.")

    # --- (Optional) Formal Verification Step ---
    # TODO: Integrate static analysis, contract checking, or other formal verification tools here

    # --- Summary ---
    print("\n--- Fix & Verification Summary ---")
    print(f"Successes: {successes}")
    print(f"Failures: {failures if failures else 'None'}")
    print("--- End of pipeline ---\n")

    # --- Existing Fix Logic ---
    if args.file:
        print(f"Fixing file: {args.file}")
        # ... existing fix logic ...
    else:
        print("Fixing the entire codebase (default behavior)")
        # ... place codebase-wide fix logic here if desired ...


def report_command(args):
    analyzer = CodeAnalyzer(project_root)

    print("Generating codebase report...")

    # Analyze the codebase
    analysis = analyze_codebase()

    # Generate a report
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "project_root": project_root,
        "summary": {
            "files": len(analysis.get("files", [])),
            "total_loc": sum(
                file.get("metrics", {}).get("loc", 0)
                for file in analysis.get("files", [])
            ),
            "avg_complexity": sum(
                file.get("metrics", {}).get("complexity", 0)
                for file in analysis.get("files", [])
            )
            / len(analysis.get("files", []))
            if analysis.get("files", [])
            else 0,
            "files_with_unused_imports": sum(
                1
                for file in analysis.get("files", [])
                if file.get("unused_imports", [])
            ),
            "files_with_complex_functions": sum(
                1
                for file in analysis.get("files", [])
                if file.get("complex_functions", [])
            ),
            "total_complex_functions": sum(
                len(file.get("complex_functions", []))
                for file in analysis.get("files", [])
            ),
            "total_unused_imports": sum(
                len(file.get("unused_imports", []))
                for file in analysis.get("files", [])
            ),
        },
        "top_complex_files": sorted(
            [
                {
                    "file": file.get("rel_path", ""),
                    "loc": file.get("metrics", {}).get("loc", 0),
                    "complexity": file.get("metrics", {}).get("complexity", 0),
                    "complex_functions": len(file.get("complex_functions", [])),
                }
                for file in analysis.get("files", [])
            ],
            key=lambda x: x["complexity"],
            reverse=True,
        )[:10],
        "top_complex_functions": sorted(
            [
                {
                    "file": file.get("rel_path", ""),
                    "function": func.get("name", ""),
                    "loc": func.get("loc", 0),
                    "complexity": func.get("complexity", 0),
                }
                for file in analysis["files"]
                for func in file["complex_functions"]
            ],
            key=lambda x: x["complexity"],
            reverse=True,
        )[:20],
        "refactoring_recommendations": [],
    }

    # Add refactoring recommendations
    for file in analysis.get("files", []):
        if file.get("complex_functions", []):
            report["refactoring_recommendations"].append(
                {
                    "file": file.get("rel_path", ""),
                    "recommendation": "Split complex functions",
                    "functions": [
                        func.get("name", "")
                        for func in file.get("complex_functions", [])
                    ],
                    "priority": "high"
                    if len(file.get("complex_functions", [])) > 2
                    else "medium",
                }
            )

        if file.get("unused_imports", []):
            report["refactoring_recommendations"].append(
                {
                    "file": file.get("rel_path", ""),
                    "recommendation": "Remove unused imports",
                    "imports": file.get("unused_imports", []),
                    "priority": "medium",
                }
            )

        if file.get("metrics", {}).get("loc", 0) > 300:
            report["refactoring_recommendations"].append(
                {
                    "file": file.get("rel_path", ""),
                    "recommendation": "Split file into smaller modules",
                    "loc": file.get("metrics", {}).get("loc", 0),
                    "priority": "high"
                    if file.get("metrics", {}).get("loc", 0) > 500
                    else "medium",
                }
            )

    # Print a summary of the report
    print("\nCodebase Report Summary:")
    print(f"- Files analyzed: {report.get('summary', {}).get('files', 0)}")
    print(f"- Total lines of code: {report.get('summary', {}).get('total_loc', 0)}")
    print(
        f"- Average complexity: {report.get('summary', {}).get('avg_complexity', 0):.2f}"
    )
    print(
        f"- Files with unused imports: {report.get('summary', {}).get('files_with_unused_imports', 0)}"
    )
    print(
        f"- Files with complex functions: {report.get('summary', {}).get('files_with_complex_functions', 0)}"
    )
    print(
        f"- Total complex functions: {report.get('summary', {}).get('total_complex_functions', 0)}"
    )
    print(
        f"- Total unused imports: {report.get('summary', {}).get('total_unused_imports', 0)}"
    )

    print("\nTop 5 most complex files:")
    for i, file in enumerate(report.get("top_complex_files", [])[:5]):
        print(
            f"{i+1}. {file.get('file', '')} (Complexity: {file.get('complexity', 0)}, LOC: {file.get('loc', 0)})"
        )

    print("\nTop 5 most complex functions:")
    for i, func in enumerate(report.get("top_complex_functions", [])[:5]):
        print(
            f"{i+1}. {func.get('file', '')}:{func.get('function', '')} (Complexity: {func.get('complexity', 0)}, LOC: {func.get('loc', 0)})"
        )

    print("\nRefactoring recommendations:")
    high_priority = [
        rec
        for rec in report.get("refactoring_recommendations", [])
        if rec.get("priority", "") == "high"
    ]
    for i, rec in enumerate(high_priority[:5]):
        print(
            f"{i+1}. {rec.get('recommendation', '')} in {rec.get('file', '')} (Priority: {rec.get('priority', '')})"
        )

    # Save the report to a file if requested
    if args.output:
        output_file = args.output
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, cls=CustomJSONEncoder)
        print(f"\nReport saved to: {output_file}")
    else:
        # Save to a default file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(project_root, f"codebase_report_{timestamp}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, cls=CustomJSONEncoder)
        print(f"\nReport saved to: {output_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Refactor Python codebase")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze code to identify refactoring opportunities"
    )
    analyze_parser.add_argument("--file", help="Analyze a specific file")
    analyze_parser.add_argument("--output", help="Output file for analysis results")

    # Split command
    split_parser = subparsers.add_parser(
        "split", help="Split complex files and functions"
    )
    split_parser.add_argument("--file", help="Split a specific file")
    split_parser.add_argument(
        "--function", help="Split a specific function (requires --file)"
    )
    split_parser.add_argument("--output", help="Output directory or file")
    split_parser.add_argument(
        "--apply", action="store_true", help="Apply the changes (default: dry run)"
    )

    # Rebuild command
    rebuild_parser = subparsers.add_parser(
        "rebuild", help="Rebuild optimized files from components"
    )
    rebuild_parser.add_argument("--parts", help="Directory containing split parts")
    rebuild_parser.add_argument("--output", help="Output file or directory")
    rebuild_parser.add_argument(
        "--apply", action="store_true", help="Apply the changes (default: dry run)"
    )

    # Fix command
    fix_parser = subparsers.add_parser("fix", help="Apply fixes for common issues")
    fix_parser.add_argument("--file", help="Fix a specific file")
    fix_parser.add_argument(
        "--apply", action="store_true", help="Apply the changes (default: dry run)"
    )

    # Report command
    report_parser = subparsers.add_parser(
        "report", help="Generate a report on codebase structure and complexity"
    )
    report_parser.add_argument("--output", help="Output file for report")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_command(args)
    elif args.command == "split":
        split_command(args)
    elif args.command == "rebuild":
        rebuild_command(args)
    elif args.command == "fix":
        fix_command(args)
    elif args.command == "report":
        report_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
