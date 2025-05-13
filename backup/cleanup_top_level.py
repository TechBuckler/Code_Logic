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
]

# Files to move to tools/refactoring
REFACTORING_TOOLS = [
    "refactor_splitter.py",
    "refactor_analyzer.py",
    "refactor_builder.py",
    "refactor_codebase.py",
    "refactor_organize_simple.py",
    "refactor_and_organize.py",
    "organize_codebase.py",
]

# Files to move to utils/import
IMPORT_UTILS = [
    "fix_hierarchical_module.py",
    "fix_imports_simple.py",
    "universal_import_fixer.py",
    "dynamic_import_resolver.py",
    "debug_import.py",
]

# Files to move to tools/analysis
ANALYSIS_TOOLS = [
    "analyze_directory_structure.py",
    "code_stats_analyzer.py",
    "test_coverage_generator.py",
    "test_new_structure.py",
    "test_refactoring.py",
    "test_all_imports.py",
    "test_imports.py",
    "test_core_functionality.py",
]

# Additional categorization
SYSTEM_UTILS = [
    "background_system.py",
    "module_system.py",
]

CLEANUP_TOOLS = [
    "cleanup_after_reorganize.py",
    "simple_cleanup.py",
    "cleanup_top_level.py",
]

REFACTORING_UTILS = [
    "circular_dependency_breaker.py",
    "balance_codebase.py",
]

# Data files
DATA_FILES = [
    "directory_structure_data.json",
    "directory_structure_report.md",
]

# Core files
CORE_FILES = [
    "run_with_fixes.py",
    "requirements.txt",
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
    
    # 4. Move system utilities
    system_dir = "utils/system"
    for file_name in SYSTEM_UTILS:
        move_file(file_name, system_dir)

    # 5. Move cleanup tools
    cleanup_dir = "tools/cleanup"
    for file_name in CLEANUP_TOOLS:
        move_file(file_name, cleanup_dir)

    # 6. Move refactoring utilities
    refactoring_utils_dir = "utils/refactoring"
    for file_name in REFACTORING_UTILS:
        move_file(file_name, refactoring_utils_dir)

    # 7. Move data files
    data_dir = "data"
    for file_name in DATA_FILES:
        move_file(file_name, data_dir)
        
    # 8. Move core files
    core_dir = "core"
    for file_name in CORE_FILES:
        move_file(file_name, core_dir)
        
    # 9. Remove redundant files
    removed_count = 0
    for file_name in os.listdir(PROJECT_ROOT):
        if os.path.isfile(os.path.join(PROJECT_ROOT, file_name)) and file_name != "__init__.py":
            if file_name not in KEEP_FILES and not any(file_name in files for files in 
                                                    [REFACTORING_TOOLS, IMPORT_UTILS, ANALYSIS_TOOLS, 
                                                     SYSTEM_UTILS, CLEANUP_TOOLS, REFACTORING_UTILS,
                                                     DATA_FILES, CORE_FILES]):
                # Move any remaining files to backup
                backup_dir = "backup"
                move_file(file_name, backup_dir)
                removed_count += 1
    
    print(f"\nMoved {removed_count} redundant files to the backup directory")
    
    # 5. Report results
    remaining_files = [f for f in os.listdir(PROJECT_ROOT) 
                      if os.path.isfile(os.path.join(PROJECT_ROOT, f)) and f.endswith(".py")]
    
    print(f"\nRemaining Python files at top level: {len(remaining_files)}")
    for file_name in sorted(remaining_files):
        print(f"  - {file_name}")
    
    print("\n" + "=" * 80)
    print("CLEANUP COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    cleanup_top_level()
