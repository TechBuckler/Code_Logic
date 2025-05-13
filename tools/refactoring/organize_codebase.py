#!/usr/bin/env python3
"""
Organize the codebase according to the established directory structure.
This script will move files to their appropriate locations based on their purpose and functionality.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase


import os
import shutil
import re

# Define the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Define the directory structure
DIRECTORIES = {
    "core": [
        "algorithms",
        "processing",
        "ast",
        "ir",
        "proof",
        "optimization",
        "export",
    ],
    "modules": ["standard", "hierarchical", "resource"],
    "ui": ["components", "renderers", "pages"],
    "utils": ["path", "file", "json", "string", "import"],
    "tools": ["shadow_tree", "fractal", "resource", "testing", "refactoring"],
    "docs": ["api", "user", "developer"],
    "tests": ["unit", "integration", "e2e"],
}

# Define file mappings based on patterns and purpose
FILE_MAPPINGS = {
    # Core files
    r".*analyzer\.py$": "core/processing",
    r".*builder\.py$": "core/processing",
    # Module files
    r".*_module\.py$": "modules/standard",
    r".*_resource\.py$": "modules/resource",
    # Tool files
    r".*splitter\.py$": "tools/refactoring",
    r".*_tool\.py$": "tools",
    r"smart_splitter\.py$": "tools/refactoring",
    r"file_splitter\.py$": "tools/refactoring",
    # Utility files
    r".*_utils\.py$": "utils",
    r"path_utils\.py$": "utils/path",
    r"file_utils\.py$": "utils/file",
    r"json_utils\.py$": "utils/json",
    r"string_utils\.py$": "utils/string",
    r"import_utils\.py$": "utils/import",
    # Documentation files
    r".*\.md$": "docs",
    r"README\.md$": ".",  # Keep README at the root
    r"README_REFACTORING\.md$": "docs/developer",
    # Report files (keep in a reports directory)
    r"codebase_report_.*\.json$": "reports",
    r"codebase_summary\.md$": "reports",
    # Main entry point files (keep at root)
    r"refactor_codebase\.py$": ".",
    r"organize_codebase\.py$": ".",
    r"requirements\.txt$": ".",
    r"__init__\.py$": ".",
    # Test files
    r"test_.*\.py$": "tests/unit",
    r".*_test\.py$": "tests/unit",
    # Split files from refactoring
    r".*_parts/.*\.py$": "modules/resource",
}

# Files to ignore (temporary files, cache, etc.)
IGNORE_PATTERNS = [
    r"__pycache__",
    r"\.git",
    r"\.vscode",
    r"\.idea",
    r"\.DS_Store",
    r".*\.pyc$",
    r".*\.pyo$",
    r".*\.pyd$",
    r".*\.so$",
    r".*\.dll$",
    r".*\.exe$",
]


def should_ignore(path):
    """Check if a path should be ignored."""
    for pattern in IGNORE_PATTERNS:
        if re.match(pattern, os.path.basename(path)):
            return True
    return False


def create_directory_structure():
    """Create the directory structure if it doesn't exist."""
    for directory, subdirectories in DIRECTORIES.items():
        dir_path = os.path.join(PROJECT_ROOT, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")

        # Create subdirectories
        for subdir in subdirectories:
            subdir_path = os.path.join(dir_path, subdir)
            if not os.path.exists(subdir_path):
                os.makedirs(subdir_path)
                print(f"Created subdirectory: {subdir_path}")

    # Create a reports directory for report files
    reports_dir = os.path.join(PROJECT_ROOT, "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        print(f"Created directory: {reports_dir}")


def get_destination_directory(file_path):
    """Determine the destination directory for a file based on its name and purpose."""
    file_name = os.path.basename(file_path)

    for pattern, destination in FILE_MAPPINGS.items():
        if re.match(pattern, file_path):
            return destination

    # Default to utils for Python files not matched elsewhere
    if file_name.endswith(".py"):
        return "utils"

    # Default to docs for other files
    return "docs"


def organize_files():
    """Organize files according to the defined structure."""
    moved_files = []

    # Walk through the project directory
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip directories that should be ignored
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d))]

        for file in files:
            file_path = os.path.join(root, file)

            # Skip files that should be ignored
            if should_ignore(file_path):
                continue

            # Get the relative path from the project root
            rel_path = os.path.relpath(file_path, PROJECT_ROOT)

            # Skip files that are already in the correct directory structure
            if rel_path.startswith(tuple(DIRECTORIES.keys()) + ("reports",)):
                # But check if they need to be moved to a subdirectory
                parts = rel_path.split(os.sep)
                if len(parts) == 2 and parts[0] in DIRECTORIES:
                    # File is in a top-level directory but might need to go in a subdirectory
                    destination = get_destination_directory(rel_path)
                    if destination != parts[0] and "/" in destination:
                        new_path = os.path.join(PROJECT_ROOT, destination, parts[1])
                        if os.path.normpath(file_path) != os.path.normpath(new_path):
                            # Create the destination directory if it doesn't exist
                            os.makedirs(os.path.dirname(new_path), exist_ok=True)
                            shutil.move(file_path, new_path)
                            moved_files.append(
                                (rel_path, os.path.join(destination, parts[1]))
                            )
                continue

            # Determine the destination directory
            destination = get_destination_directory(rel_path)

            # Create the full destination path
            if destination == ".":
                # Keep at root
                continue

            dest_path = os.path.join(PROJECT_ROOT, destination, file)

            # Create the destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Move the file
            if os.path.normpath(file_path) != os.path.normpath(dest_path):
                shutil.move(file_path, dest_path)
                moved_files.append((rel_path, os.path.join(destination, file)))

    return moved_files


def handle_split_files():
    """Handle files that were split by the refactoring tool."""
    # Look for directories ending with _parts
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for dir_name in dirs:
            if dir_name.endswith("_parts"):
                parts_dir = os.path.join(root, dir_name)
                base_name = dir_name[:-6]  # Remove _parts suffix

                # Create a module directory for the split files
                module_dir = os.path.join(
                    PROJECT_ROOT, "modules", "resource", base_name
                )
                os.makedirs(module_dir, exist_ok=True)

                # Move all files from the parts directory to the module directory
                for file in os.listdir(parts_dir):
                    if file.endswith(".py"):
                        src_path = os.path.join(parts_dir, file)
                        dest_path = os.path.join(module_dir, file)
                        shutil.move(src_path, dest_path)
                        print(f"Moved split file: {src_path} -> {dest_path}")

                # Create an __init__.py file to make it a proper package
                init_path = os.path.join(module_dir, "__init__.py")
                if not os.path.exists(init_path):
                    with open(init_path, "w") as f:
                        f.write(
                            f'"""\n{base_name} module.\n\nThis module was automatically split from {base_name}.py.\n"""\n\n'
                        )

                        # Import all the split files
                        for file in os.listdir(module_dir):
                            if file.endswith(".py") and file != "__init__.py":
                                module_name = file[:-3]  # Remove .py extension
                                f.write(f"from .{module_name} import *\n")

                # Remove the now-empty parts directory
                if not os.listdir(parts_dir):
                    os.rmdir(parts_dir)
                    print(f"Removed empty directory: {parts_dir}")


def main():
    """Main function to organize the codebase."""
    print("Organizing codebase...")

    # Create the directory structure
    create_directory_structure()

    # Handle split files first
    handle_split_files()

    # Organize the files
    moved_files = organize_files()

    # Print summary
    print(f"\nMoved {len(moved_files)} files to their appropriate locations.")
    for src, dest in moved_files:
        print(f"  {src} -> {dest}")

    print("\nCodebase organization complete!")


if __name__ == "__main__":
    main()
