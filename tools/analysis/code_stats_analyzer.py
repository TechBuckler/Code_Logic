#!/usr/bin/env python
"""
Code Statistics Analyzer

This script analyzes all Python files in the codebase and provides statistics on:
- Commands (statements)
- Branches (if/else, loops)
- Variables
- Functions/methods
- Classes
- Lines of code
- Comments
"""
# Fix imports for reorganized codebase
import utils.import_utils


import os
import sys
import ast
import re
from collections import defaultdict, Counter

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import our fix for RuntimeOptimizationModule
from fix_imports_simple import *


class CodeVisitor(ast.NodeVisitor):
    """AST visitor to collect code statistics."""

    def __init__(self):
        self.stats = {
            "commands": 0,  # All statements
            "branches": 0,  # if/else, loops
            "variables": set(),  # Variable names
            "functions": 0,  # Function definitions
            "classes": 0,  # Class definitions
            "imports": 0,  # Import statements
            "lines": 0,  # Lines of code
            "comments": 0,  # Comments
            "docstrings": 0,  # Docstrings
            "assignments": 0,  # Assignment statements
            "calls": 0,  # Function/method calls
            "returns": 0,  # Return statements
        }
        self.current_function = None
        self.current_class = None

    def visit_FunctionDef(self, node):
        """Count function definitions."""
        self.stats["functions"] += 1
        self.stats["commands"] += 1
        old_function = self.current_function
        self.current_function = node.name

        # Check for docstring
        if (
            len(node.body) > 0
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Str)
        ):
            self.stats["docstrings"] += 1

        # Visit function body
        for child in node.body:
            self.visit(child)

        self.current_function = old_function

    def visit_ClassDef(self, node):
        """Count class definitions."""
        self.stats["classes"] += 1
        self.stats["commands"] += 1
        old_class = self.current_class
        self.current_class = node.name

        # Check for docstring
        if (
            len(node.body) > 0
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Str)
        ):
            self.stats["docstrings"] += 1

        # Visit class body
        for child in node.body:
            self.visit(child)

        self.current_class = old_class

    def visit_If(self, node):
        """Count if statements."""
        self.stats["branches"] += 1
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_For(self, node):
        """Count for loops."""
        self.stats["branches"] += 1
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_While(self, node):
        """Count while loops."""
        self.stats["branches"] += 1
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_Import(self, node):
        """Count import statements."""
        self.stats["imports"] += len(node.names)
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Count import from statements."""
        self.stats["imports"] += len(node.names)
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        """Count assignments and track variables."""
        self.stats["assignments"] += 1
        self.stats["commands"] += 1

        # Extract variable names
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.stats["variables"].add(target.id)
            elif isinstance(target, ast.Tuple) or isinstance(target, ast.List):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.stats["variables"].add(elt.id)

        self.generic_visit(node)

    def visit_Call(self, node):
        """Count function/method calls."""
        self.stats["calls"] += 1
        self.generic_visit(node)

    def visit_Return(self, node):
        """Count return statements."""
        self.stats["returns"] += 1
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_Expr(self, node):
        """Count expressions."""
        if not (
            isinstance(node.value, ast.Str)
            and (
                self.current_function is None or node.value == node.parent.body[0].value
            )
        ):
            self.stats["commands"] += 1
        self.generic_visit(node)

    # Count other statements as commands
    def visit_Assert(self, node):
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_Delete(self, node):
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_Pass(self, node):
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_Raise(self, node):
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_Break(self, node):
        self.stats["commands"] += 1
        self.generic_visit(node)

    def visit_Continue(self, node):
        self.stats["commands"] += 1
        self.generic_visit(node)


def count_lines_and_comments(file_path):
    """Count lines of code and comments in a file."""
    lines = 0
    comments = 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:  # Non-empty line
                    lines += 1
                    if line.startswith("#"):
                        comments += 1
                    elif "#" in line:
                        comments += 1
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return lines, comments


def analyze_file(file_path):
    """Analyze a Python file and return statistics."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse the AST
        tree = ast.parse(content)

        # Visit the AST to collect statistics
        visitor = CodeVisitor()
        visitor.visit(tree)

        # Count lines and comments
        lines, comments = count_lines_and_comments(file_path)
        visitor.stats["lines"] = lines
        visitor.stats["comments"] = comments

        return visitor.stats
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return None


def find_python_files(directory):
    """Find all Python files in a directory (recursive)."""
    python_files = []

    for root, _, files in os.walk(directory):
        # Skip certain directories
        if any(skip in root for skip in ["__pycache__", ".git", ".vscode", ".idea"]):
            continue

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files


def analyze_codebase():
    """Analyze the entire codebase and return statistics."""
    python_files = find_python_files(PROJECT_ROOT)
    print(f"Found {len(python_files)} Python files to analyze")

    # Initialize statistics
    total_stats = {
        "commands": 0,
        "branches": 0,
        "variables": set(),
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "lines": 0,
        "comments": 0,
        "docstrings": 0,
        "assignments": 0,
        "calls": 0,
        "returns": 0,
    }

    # Statistics by directory
    dir_stats = defaultdict(
        lambda: {
            "files": 0,
            "commands": 0,
            "branches": 0,
            "variables": set(),
            "functions": 0,
            "classes": 0,
            "lines": 0,
        }
    )

    # Analyze each file
    for file_path in python_files:
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        print(f"Analyzing {rel_path}...")

        stats = analyze_file(file_path)
        if stats:
            # Update total statistics
            for key, value in stats.items():
                if key == "variables":
                    total_stats[key].update(value)
                else:
                    total_stats[key] += value

            # Update directory statistics
            dir_name = os.path.dirname(rel_path)
            if not dir_name:
                dir_name = "."  # Root directory

            dir_stats[dir_name]["files"] += 1
            for key, value in stats.items():
                if key in ["commands", "branches", "functions", "classes", "lines"]:
                    dir_stats[dir_name][key] += value
                elif key == "variables":
                    dir_stats[dir_name][key].update(value)

    return total_stats, dir_stats


def print_statistics(total_stats, dir_stats):
    """Print the statistics in a readable format."""
    print("\n" + "=" * 80)
    print("CODEBASE STATISTICS")
    print("=" * 80)

    # Print total statistics
    print("\nTotal Statistics:")
    print(f"Total Python files: {sum(stats['files'] for stats in dir_stats.values())}")
    print(f"Total lines of code: {total_stats['lines']}")
    print(f"Total commands (statements): {total_stats['commands']}")
    print(f"Total branches (if/else, loops): {total_stats['branches']}")
    print(f"Total functions/methods: {total_stats['functions']}")
    print(f"Total classes: {total_stats['classes']}")
    print(f"Total unique variables: {len(total_stats['variables'])}")
    print(f"Total imports: {total_stats['imports']}")
    print(f"Total comments: {total_stats['comments']}")
    print(f"Total docstrings: {total_stats['docstrings']}")
    print(f"Total assignments: {total_stats['assignments']}")
    print(f"Total function calls: {total_stats['calls']}")
    print(f"Total return statements: {total_stats['returns']}")

    # Calculate percentages
    if total_stats["commands"] > 0:
        branch_percent = (total_stats["branches"] / total_stats["commands"]) * 100
        print(f"\nBranches as percentage of commands: {branch_percent:.2f}%")

    if total_stats["lines"] > 0:
        comment_percent = (total_stats["comments"] / total_stats["lines"]) * 100
        print(f"Comments as percentage of lines: {comment_percent:.2f}%")

    # Print statistics by directory
    print("\nStatistics by Directory:")
    print(
        f"{'Directory':<40} {'Files':<6} {'Lines':<8} {'Commands':<10} {'Branches':<10} {'Functions':<10} {'Classes':<8}"
    )
    print("-" * 100)

    # Sort directories by number of files
    sorted_dirs = sorted(dir_stats.items(), key=lambda x: x[1]["files"], reverse=True)

    for dir_name, stats in sorted_dirs:
        if stats["files"] > 0:
            print(
                f"{dir_name:<40} {stats['files']:<6} {stats['lines']:<8} {stats['commands']:<10} {stats['branches']:<10} {stats['functions']:<10} {stats['classes']:<8}"
            )

    # Print top directories by various metrics
    print("\nTop 10 Directories by Lines of Code:")
    top_by_lines = sorted(dir_stats.items(), key=lambda x: x[1]["lines"], reverse=True)[
        :10
    ]
    for dir_name, stats in top_by_lines:
        print(f"{dir_name:<40} {stats['lines']:<8} lines")

    print("\nTop 10 Directories by Command Density (Commands per Line):")
    command_density = [
        (dir_name, stats["commands"] / stats["lines"] if stats["lines"] > 0 else 0)
        for dir_name, stats in dir_stats.items()
        if stats["files"] > 0
    ]
    command_density.sort(key=lambda x: x[1], reverse=True)
    for dir_name, density in command_density[:10]:
        print(f"{dir_name:<40} {density:.2f} commands/line")

    print("\nTop 10 Directories by Branch Density (Branches per Command):")
    branch_density = [
        (
            dir_name,
            stats["branches"] / stats["commands"] if stats["commands"] > 0 else 0,
        )
        for dir_name, stats in dir_stats.items()
        if stats["files"] > 0
    ]
    branch_density.sort(key=lambda x: x[1], reverse=True)
    for dir_name, density in branch_density[:10]:
        print(f"{dir_name:<40} {density:.2f} branches/command")


def main():
    """Main function."""
    print("Analyzing codebase...")
    total_stats, dir_stats = analyze_codebase()
    print_statistics(total_stats, dir_stats)


if __name__ == "__main__":
    main()
