#!/usr/bin/env python
"""
Finalize Reorganization

This script finalizes the codebase reorganization by:
1. Removing redundant *_split directories
2. Moving any remaining important files to the new structure
3. Cleaning up duplicate files
4. Verifying the integrity of the new structure
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import shutil
import re

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions

# Directories to remove (redundant split directories)
REDUNDANT_DIRS = [
    "enhanced_split",
    "file_splitter_split",
    "ir_split",
    "optimization_split",
    "optimizer_split",
    "proof_split",
    "resource_oriented_codebase",
    "resource_split",
    "runtime_opt_split",
    "runtime_split",
    "split_files",
    "src_new"
]

# Old directories that should be preserved but not in root
MOVE_DIRS = {
    "nltk_data": "data/nltk_data",
    "pdict-cache": "data/cache",
    "shadow_tree_output": "tools/shadow_tree/output"
}

# Files to check and potentially move to the new structure
CHECK_FILES = [
    # Python files
    "*.py",
    # Documentation
    "*.md",
    # Configuration
    "*.json",
    "*.yaml",
    "*.toml",
    # Data files
    "*.csv",
    "*.txt"
]

def remove_redundant_directories(dry_run=True):
    """Remove redundant split directories."""
    print("\n🗑️ Removing redundant directories")
    print("=" * 80)
    
    for dir_name in REDUNDANT_DIRS:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            if dry_run:
                print(f"Would remove: {dir_name}/")
            else:
                try:
                    shutil.rmtree(dir_path)
                    print(f"Removed: {dir_name}/")
                except Exception as e:
                    print(f"Error removing {dir_name}/: {e}")
        else:
            print(f"Directory not found: {dir_name}/")
    
    print(f"\n{'Would remove' if dry_run else 'Removed'} {len(REDUNDANT_DIRS)} redundant directories")

def move_directories(dry_run=True):
    """Move directories to their new locations."""
    print("\n📦 Moving directories to new locations")
    print("=" * 80)
    
    for old_dir, new_dir in MOVE_DIRS.items():
        old_path = os.path.join(project_root, old_dir)
        new_path = os.path.join(project_root, new_dir)
        
        if os.path.exists(old_path) and os.path.isdir(old_path):
            if dry_run:
                print(f"Would move: {old_dir}/ -> {new_dir}/")
            else:
                try:
                    # Create destination directory
                    ensure_dir(os.path.dirname(new_path))
                    
                    # Move directory
                    if os.path.exists(new_path):
                        # Merge directories
                        for item in os.listdir(old_path):
                            old_item = os.path.join(old_path, item)
                            new_item = os.path.join(new_path, item)
                            
                            if os.path.isdir(old_item):
                                if not os.path.exists(new_item):
                                    shutil.copytree(old_item, new_item)
                            else:
                                if not os.path.exists(new_item):
                                    shutil.copy2(old_item, new_item)
                        
                        # Remove old directory
                        shutil.rmtree(old_path)
                    else:
                        # Simple move
                        shutil.move(old_path, new_path)
                    
                    print(f"Moved: {old_dir}/ -> {new_dir}/")
                except Exception as e:
                    print(f"Error moving {old_dir}/: {e}")
        else:
            print(f"Directory not found: {old_dir}/")
    
    print(f"\n{'Would move' if dry_run else 'Moved'} {len(MOVE_DIRS)} directories")

def check_remaining_files(dry_run=True):
    """Check for important files in the root directory and move them if needed."""
    print("\n🔍 Checking remaining files")
    print("=" * 80)
    
    # Define target directories for different file types
    file_targets = {
        r".*_module\.py$": "modules/standard",
        r".*_core\.py$": "core",
        r".*_ui\.py$": "ui",
        r".*_utils\.py$": "utils",
        r".*_tool\.py$": "tools",
        r"test_.*\.py$": "tests/unit",
        r".*\.md$": "docs"
    }
    
    # Files to exclude from moving
    exclude_files = [
        "README.md",
        "requirements.txt",
        "setup.py",
        "finalize_reorganization.py",
        "check_structure.py"
    ]
    
    # Get all files in the root directory
    root_files = [f for f in os.listdir(project_root) 
                 if os.path.isfile(os.path.join(project_root, f))]
    
    # Filter to only include files matching our patterns
    check_patterns = [re.compile(pattern.replace("*", ".*")) for pattern in CHECK_FILES]
    filtered_files = [f for f in root_files 
                     if any(pattern.match(f) for pattern in check_patterns)
                     and f not in exclude_files]
    
    # Process each file
    moved_files = 0
    for file in filtered_files:
        # Determine target directory
        target_dir = None
        for pattern, directory in file_targets.items():
            if re.match(pattern, file):
                target_dir = directory
                break
        
        # If no specific target, use a default based on extension
        if target_dir is None:
            if file.endswith(".py"):
                target_dir = "tools"  # Default for Python files
            elif file.endswith(".md"):
                target_dir = "docs"   # Default for Markdown files
            elif file.endswith((".json", ".yaml", ".toml")):
                target_dir = "config" # Default for config files
            elif file.endswith((".csv", ".txt")):
                target_dir = "data"   # Default for data files
        
        if target_dir:
            src_path = os.path.join(project_root, file)
            dest_path = os.path.join(project_root, target_dir, file)
            
            if dry_run:
                print(f"Would move: {file} -> {target_dir}/{file}")
            else:
                try:
                    # Ensure target directory exists
                    ensure_dir(os.path.dirname(dest_path))
                    
                    # Copy the file
                    shutil.copy2(src_path, dest_path)
                    
                    # Remove the original
                    os.remove(src_path)
                    
                    print(f"Moved: {file} -> {target_dir}/{file}")
                    moved_files += 1
                except Exception as e:
                    print(f"Error moving {file}: {e}")
        else:
            print(f"No target directory determined for: {file}")
    
    print(f"\n{'Would move' if dry_run else 'Moved'} {moved_files} files")

def create_data_directory(dry_run=True):
    """Create a data directory for data files."""
    print("\n📁 Creating data directory")
    print("=" * 80)
    
    data_dir = os.path.join(project_root, "data")
    if not os.path.exists(data_dir):
        if dry_run:
            print("Would create: data/")
        else:
            os.makedirs(data_dir)
            
            # Create subdirectories
            for subdir in ["cache", "output", "input"]:
                os.makedirs(os.path.join(data_dir, subdir), exist_ok=True)
            
            # Create __init__.py
            with open(os.path.join(data_dir, "__init__.py"), "w", encoding="utf-8") as f:
                f.write('"""\nData package.\n"""\n')
            
            print("Created: data/ with subdirectories")
    else:
        print("Directory already exists: data/")

def create_config_directory(dry_run=True):
    """Create a config directory for configuration files."""
    print("\n📁 Creating config directory")
    print("=" * 80)
    
    config_dir = os.path.join(project_root, "config")
    if not os.path.exists(config_dir):
        if dry_run:
            print("Would create: config/")
        else:
            os.makedirs(config_dir)
            
            # Create __init__.py
            with open(os.path.join(config_dir, "__init__.py"), "w", encoding="utf-8") as f:
                f.write('"""\nConfiguration package.\n"""\n')
            
            print("Created: config/")
    else:
        print("Directory already exists: config/")

def update_readme(dry_run=True):
    """Update or create a README.md file with the new directory structure."""
    print("\n📝 Updating README.md")
    print("=" * 80)
    
    readme_path = os.path.join(project_root, "README.md")
    
    # Generate README content
    readme_content = """# Code Logic Tool

## Project Structure

This codebase follows a balanced directory structure with 9 top-level folders:

```
code_logic_tool/
├── core/              # Core algorithms and processing
│   ├── ast/           # Abstract Syntax Tree handling
│   ├── ir/            # Intermediate Representation
│   ├── proof/         # Proof generation and validation
│   ├── optimization/  # Optimization algorithms
│   └── export/        # Export functionality
│
├── modules/           # Module implementations
│   ├── standard/      # Standard modules
│   │   ├── processing/    # Processing modules
│   │   ├── analysis/      # Analysis modules
│   │   ├── export/        # Export modules
│   │   └── organization/  # Organization modules
│   ├── hierarchical/  # Hierarchical modules
│   └── resource_oriented/ # Resource-specific implementations
│
├── ui/                # User interface components
│   ├── components/    # Reusable UI components
│   ├── renderers/     # Output renderers
│   └── pages/         # Page definitions
│
├── utils/             # Utility functions and helpers
│   ├── file/          # File operations
│   ├── runtime/       # Runtime utilities
│   ├── system/        # System interaction
│   └── nlp/           # Natural language processing
│
├── tools/             # Standalone tools
│   ├── shadow_tree/   # Shadow Tree navigation
│   ├── fractal/       # Fractal organization tools
│   ├── resource/      # Resource management
│   └── testing/       # Testing tools
│
├── docs/              # Documentation
│   ├── api/           # API documentation
│   ├── guides/        # User guides
│   └── examples/      # Example code
│
├── tests/             # Test suite
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── e2e/           # End-to-end tests
│
├── data/              # Data files
│   ├── cache/         # Cached data
│   ├── input/         # Input data
│   └── output/        # Output data
│
└── config/            # Configuration files
```

## Utility Functions

Common functionality has been consolidated into utility modules:

- `utils.path_utils`: Path manipulation and directory handling
- `utils.file_utils`: File reading, writing, and manipulation
- `utils.json_utils`: JSON parsing and serialization
- `utils.string_utils`: String processing and manipulation

Import these utilities instead of reimplementing common functionality.

## Running the Application

To run the main application:

```bash
py run_ui.py
```

For command-line interface:

```bash
py run_cli.py
```

## Development

This project follows a fractal organization approach, ensuring each directory has a balanced number of items (5-20) and uses resource-based splitting for optimal performance.
"""
    
    if dry_run:
        print("Would update: README.md")
    else:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("Updated: README.md")

def verify_structure():
    """Verify the integrity of the new directory structure."""
    print("\n✅ Verifying directory structure")
    print("=" * 80)
    
    # Expected top-level directories
    expected_dirs = [
        "core",
        "modules",
        "ui",
        "utils",
        "tools",
        "docs",
        "tests",
        "data",
        "config"
    ]
    
    # Check that all expected directories exist
    missing_dirs = []
    for dir_name in expected_dirs:
        dir_path = os.path.join(project_root, dir_name)
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"Missing directories: {', '.join(missing_dirs)}")
    else:
        print("All expected directories are present")
    
    # Check for any remaining redundant directories
    remaining_redundant = []
    for dir_name in REDUNDANT_DIRS:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            remaining_redundant.append(dir_name)
    
    if remaining_redundant:
        print(f"Remaining redundant directories: {', '.join(remaining_redundant)}")
    else:
        print("No redundant directories remaining")
    
    # Overall status
    if not missing_dirs and not remaining_redundant:
        print("\n🎉 Directory structure is complete and clean!")
    else:
        print("\n⚠️ Directory structure needs further attention")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Finalize Reorganization")
    parser.add_argument("--apply", action="store_true", help="Apply the changes")
    
    args = parser.parse_args()
    dry_run = not args.apply
    
    print("\n🚀 Finalizing Codebase Reorganization")
    print("=" * 80)
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}")
    
    # Create new directories
    create_data_directory(dry_run)
    create_config_directory(dry_run)
    
    # Move directories
    move_directories(dry_run)
    
    # Check remaining files
    check_remaining_files(dry_run)
    
    # Remove redundant directories
    remove_redundant_directories(dry_run)
    
    # Update README
    update_readme(dry_run)
    
    # Verify structure
    if not dry_run:
        verify_structure()
    
    print("\n✅ Reorganization finalization complete!")
    if dry_run:
        print("\nTo apply the changes, run: py finalize_reorganization.py --apply")

if __name__ == "__main__":
    main()
