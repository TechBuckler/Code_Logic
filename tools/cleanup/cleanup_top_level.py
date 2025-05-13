#!/usr/bin/env python
"""
Cleanup Top Level

This script cleans up the top-level directory by:
1. Moving working scripts to appropriate directories
2. Removing redundant or failed scripts
3. Keeping only the essential files at the top level
"""

import os
import sys
import shutil

# Define the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Files to keep at the top level
KEEP_FILES = [
    "__init__.py",
    "requirements.txt",
    "run_with_fixes.py",  # Our working script
    "test_core_functionality.py",  # Core tests
    "cleanup_top_level.py",  # This script
]

# Files to move to tools/refactoring
REFACTORING_TOOLS = [
    "refactor_splitter.py",
    "refactor_analyzer.py",
    "refactor_builder.py",
    "refactor_codebase.py",
    "refactor_organize_simple.py",
]

# Files to move to utils/import
IMPORT_UTILS = [
    "fix_hierarchical_module.py",
    "fix_imports_simple.py",
    "universal_import_fixer.py",
]

# Files to move to tools/analysis
ANALYSIS_TOOLS = [
    "analyze_directory_structure.py",
    "code_stats_analyzer.py",
    "test_coverage_generator.py",
]


def ensure_dir(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    return path


def move_file(file_name, target_dir):
    """Move a file to the target directory if it exists."""
    source_path = os.path.join(PROJECT_ROOT, file_name)
    if not os.path.exists(source_path):
        print(f"Skipping {file_name} - file not found")
        return False

    target_path = os.path.join(PROJECT_ROOT, target_dir, file_name)
    ensure_dir(os.path.dirname(target_path))

    try:
        shutil.move(source_path, target_path)
        print(f"Moved {file_name} -> {target_dir}")
        return True
    except Exception as e:
        print(f"Error moving {file_name}: {e}")
        return False


def cleanup_top_level():
    """Clean up the top-level directory."""
    print("\n" + "=" * 80)
    print("CLEANING UP TOP-LEVEL DIRECTORY")
    print("=" * 80)

    # 1. Move refactoring tools
    refactoring_dir = "tools/refactoring"
    for file_name in REFACTORING_TOOLS:
        move_file(file_name, refactoring_dir)

    # 2. Move import utilities
    import_dir = "utils/import"
    for file_name in IMPORT_UTILS:
        move_file(file_name, import_dir)

    # 3. Move analysis tools
    analysis_dir = "tools/analysis"
    for file_name in ANALYSIS_TOOLS:
        move_file(file_name, analysis_dir)

    # 4. Remove redundant files
    removed_count = 0
    for file_name in os.listdir(PROJECT_ROOT):
        if os.path.isfile(os.path.join(PROJECT_ROOT, file_name)) and file_name.endswith(
            ".py"
        ):
            if file_name not in KEEP_FILES and not any(
                file_name in files
                for files in [REFACTORING_TOOLS, IMPORT_UTILS, ANALYSIS_TOOLS]
            ):
                # Check if this is a redundant fix_* or minimal_* file
                if (
                    file_name.startswith("fix_")
                    or file_name.startswith("minimal_")
                    or file_name.startswith("run_")
                ):
                    backup_dir = "backup"
                    move_file(file_name, backup_dir)
                    removed_count += 1

    print(f"\nMoved {removed_count} redundant files to the backup directory")

    # 5. Report results
    remaining_files = [
        f
        for f in os.listdir(PROJECT_ROOT)
        if os.path.isfile(os.path.join(PROJECT_ROOT, f)) and f.endswith(".py")
    ]

    print(f"\nRemaining Python files at top level: {len(remaining_files)}")
    for file_name in sorted(remaining_files):
        print(f"  - {file_name}")

    print("\n" + "=" * 80)
    print("CLEANUP COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    cleanup_top_level()
