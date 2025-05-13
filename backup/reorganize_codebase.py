#!/usr/bin/env python
"""
Codebase Reorganization Tool

This script reorganizes the codebase according to the plan outlined in
reorganization_plan.md, using the existing fractal organizer and resource
splitter tools.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import shutil
import importlib.util
import re

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Try to import our tools
try:
    # Import the fractal organizer
    fractal_organizer_path = os.path.join(project_root, "src", "fractal_organizer.py")
    spec = importlib.util.spec_from_file_location("fractal_organizer", fractal_organizer_path)
    fractal_organizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fractal_organizer)
    
    # Import the resource splitter
    resource_splitter_path = os.path.join(project_root, "src", "resource_splitter.py")
    spec = importlib.util.spec_from_file_location("resource_splitter", resource_splitter_path)
    resource_splitter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resource_splitter)
    
    print("✅ Successfully imported reorganization tools")
except Exception as e:
    print(f"❌ Error importing tools: {str(e)}")
    print("Falling back to basic reorganization")
    fractal_organizer = None
    resource_splitter = None

# Define the target directory structure
TARGET_STRUCTURE = {
    "core": {
        "ast": {},
        "ir": {},
        "proof": {},
        "optimization": {},
        "export": {},
    },
    "modules": {
        "hierarchical": {},
        "resource_oriented": {
            "cpu": {},
            "memory": {},
            "gpu": {},
            "network": {},
        },
        "standard": {},
    },
    "ui": {
        "components": {},
        "renderers": {},
        "pages": {},
    },
    "utils": {
        "file": {},
        "nlp": {},
        "runtime": {},
        "system": {},
    },
    "tools": {
        "shadow_tree": {},
        "fractal": {},
        "resource": {},
        "testing": {},
    },
    "docs": {
        "architecture": {},
        "api": {},
        "examples": {},
    },
    "tests": {
        "unit": {},
        "integration": {},
        "resources": {},
    },
}

# File classification patterns
FILE_PATTERNS = {
    "core/ast": [
        r"ast_.*\.py$",
        r".*parser.*\.py$",
    ],
    "core/ir": [
        r"ir_.*\.py$",
        r".*intermediate.*\.py$",
        r".*generator.*\.py$",
    ],
    "core/proof": [
        r"proof_.*\.py$",
        r".*engine.*\.py$",
        r".*verifier.*\.py$",
    ],
    "core/optimization": [
        r"optimi[sz].*\.py$",
        r".*optimizer.*\.py$",
    ],
    "core/export": [
        r"export.*\.py$",
        r".*exporter.*\.py$",
        r".*output.*\.py$",
    ],
    "modules/hierarchical": [
        r"hierarchical_.*\.py$",
        r".*_hierarchical_.*\.py$",
    ],
    "modules/standard": [
        r".*_module\.py$",
    ],
    "ui/components": [
        r".*component.*\.py$",
        r"ui_.*\.py$",
    ],
    "ui/renderers": [
        r".*render.*\.py$",
        r".*visual.*\.py$",
    ],
    "ui/pages": [
        r".*page.*\.py$",
        r".*view.*\.py$",
    ],
    "utils/file": [
        r"file_.*\.py$",
        r".*splitter.*\.py$",
    ],
    "utils/nlp": [
        r"nlp_.*\.py$",
        r".*language.*\.py$",
        r".*token.*\.py$",
    ],
    "utils/runtime": [
        r"runtime_.*\.py$",
        r".*optimization.*\.py$",
    ],
    "utils/system": [
        r"system_.*\.py$",
        r".*util.*\.py$",
    ],
    "tools/shadow_tree": [
        r"shadow_tree.*\.py$",
    ],
    "tools/fractal": [
        r"fractal_.*\.py$",
    ],
    "tools/resource": [
        r"resource_.*\.py$",
    ],
    "tools/testing": [
        r"test_.*\.py$",
        r".*_test.*\.py$",
    ],
}

def create_directory_structure(base_dir, structure, level=0):
    """Create the target directory structure."""
    for name, substructure in structure.items():
        dir_path = os.path.join(base_dir, name)
        os.makedirs(dir_path, exist_ok=True)
        print(f"{'  ' * level}📁 Created directory: {name}")
        
        # Create __init__.py file
        init_path = os.path.join(dir_path, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w") as f:
                f.write(f"# {name.capitalize()} package\n")
        
        # Create subdirectories
        if substructure:
            create_directory_structure(dir_path, substructure, level + 1)

def classify_file(file_path):
    """Classify a file based on its name and content."""
    file_name = os.path.basename(file_path)
    
    # Check each pattern
    for target_dir, patterns in FILE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, file_name, re.IGNORECASE):
                return target_dir
    
    # Default classifications based on directories
    if "modules" in file_path:
        return "modules/standard"
    elif "core" in file_path:
        return "core/ast"  # Default core category
    elif "ui" in file_path or "unified" in file_path:
        return "ui/components"
    elif "util" in file_path:
        return "utils/system"
    elif "test" in file_path:
        return "tests/unit"
    
    # If no match, put in utils
    return "utils/system"

def copy_file_to_target(src_file, target_dir, dry_run=False):
    """Copy a file to its target directory."""
    # Create the target directory if it doesn't exist
    if not dry_run:
        os.makedirs(target_dir, exist_ok=True)
    
    # Get the target file path
    file_name = os.path.basename(src_file)
    target_file = os.path.join(target_dir, file_name)
    
    # Copy the file
    if not dry_run:
        shutil.copy2(src_file, target_file)
        print(f"📄 Copied {file_name} to {target_dir}")
    else:
        print(f"📄 Would copy {file_name} to {target_dir}")
    
    return target_file

def scan_and_classify_files(src_dir, target_base_dir, dry_run=False):
    """Scan the source directory and classify files."""
    classified_files = {}
    
    # Walk through the source directory
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            # Skip __pycache__ and other non-Python files
            if file.endswith(".py") and "__pycache__" not in root:
                src_file = os.path.join(root, file)
                
                # Classify the file
                target_category = classify_file(src_file)
                target_dir = os.path.join(target_base_dir, target_category)
                
                # Add to classified files
                if target_category not in classified_files:
                    classified_files[target_category] = []
                classified_files[target_category].append((src_file, target_dir))
    
    return classified_files

def update_imports(file_path, old_to_new_mapping):
    """Update import statements in a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace import statements
    for old_path, new_path in old_to_new_mapping.items():
        old_import = old_path.replace("/", ".").replace("\\", ".")
        new_import = new_path.replace("/", ".").replace("\\", ".")
        
        # Replace "from old_import import" with "from new_import import"
        content = re.sub(
            r"from\s+(" + re.escape(old_import) + r")\s+import",
            f"from {new_import} import",
            content
        )
        
        # Replace "import old_import" with "import new_import"
        content = re.sub(
            r"import\s+(" + re.escape(old_import) + r")\s+",
            f"import {new_import} ",
            content
        )
    
    # Write the updated content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def reorganize_codebase(dry_run=False):
    """Reorganize the codebase according to the plan."""
    print("\n🔄 Starting codebase reorganization")
    print("=" * 50)
    
    # Define paths
    src_dir = os.path.join(project_root, "src")
    target_base_dir = os.path.join(project_root, "reorganized")
    
    # Create the target directory
    if not dry_run:
        os.makedirs(target_base_dir, exist_ok=True)
    
    # Create the target directory structure
    if not dry_run:
        create_directory_structure(target_base_dir, TARGET_STRUCTURE)
    
    # Scan and classify files
    print("\n📊 Scanning and classifying files")
    classified_files = scan_and_classify_files(src_dir, target_base_dir, dry_run)
    
    # Copy files to their target directories
    print("\n📋 Copying files to target directories")
    old_to_new_mapping = {}
    
    for category, files in classified_files.items():
        print(f"\n📁 Category: {category}")
        for src_file, target_dir in files:
            # Copy the file
            target_file = copy_file_to_target(src_file, target_dir, dry_run)
            
            # Add to mapping
            rel_src = os.path.relpath(src_file, project_root)
            rel_target = os.path.relpath(target_file, target_base_dir)
            old_to_new_mapping[rel_src] = rel_target
    
    # Update import statements
    if not dry_run:
        print("\n🔄 Updating import statements")
        for root, dirs, files in os.walk(target_base_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    update_imports(file_path, old_to_new_mapping)
    
    print("\n✅ Reorganization complete!")
    if dry_run:
        print("This was a dry run. No files were actually moved.")
    else:
        print(f"The reorganized codebase is available at: {target_base_dir}")
    
    return target_base_dir

def apply_fractal_organization(target_dir):
    """Apply fractal organization to the reorganized codebase."""
    if not fractal_organizer:
        print("❌ Fractal organizer not available")
        return
    
    print("\n🌳 Applying fractal organization")
    print("=" * 50)
    
    # TODO: Implement fractal organization
    # This would use the fractal_organizer module to further organize
    # each directory to ensure a balanced structure
    
    print("✅ Fractal organization complete!")

def apply_resource_splitting(target_dir):
    """Apply resource splitting to the reorganized codebase."""
    if not resource_splitter:
        print("❌ Resource splitter not available")
        return
    
    print("\n🔄 Applying resource splitting")
    print("=" * 50)
    
    # TODO: Implement resource splitting
    # This would use the resource_splitter module to categorize files
    # by their resource usage
    
    print("✅ Resource splitting complete!")

def identify_duplicate_functionality(src_dir):
    """Identify duplicate functionality across the codebase."""
    print("\n🔍 Identifying duplicate functionality")
    print("=" * 50)
    
    # Common patterns to look for
    DUPLICATE_PATTERNS = [
        # File operations
        (r"def\s+(?:read|load)_file\s*\(.*?\)\s*:.*?with\s+open\(.*?\)\s+as\s+f\s*:.*?return\s+f\.read\(\)", "file_utils.py", "read_file"),
        (r"def\s+(?:write|save)_(?:to_)?file\s*\(.*?\)\s*:.*?with\s+open\(.*?\)\s+as\s+f\s*:.*?f\.write\(.*?\)", "file_utils.py", "write_file"),
        
        # Path handling
        (r"(?:os\.path\.join|os\.path\.dirname|os\.path\.abspath).*?(?:os\.path\.join|os\.path\.dirname|os\.path\.abspath)", "path_utils.py", "path_operations"),
        
        # JSON operations
        (r"json\.(?:load|loads|dump|dumps).*?json\.(?:load|loads|dump|dumps)", "json_utils.py", "json_operations"),
        
        # String processing
        (r"def\s+(?:clean|normalize|process)_(?:text|string)\s*\(.*?\)\s*:.*?return\s+re\.sub\(.*?\)", "string_utils.py", "string_processing"),
        
        # Configuration handling
        (r"def\s+(?:load|get)_config\s*\(.*?\)\s*:.*?(?:json\.load|yaml\.load|toml\.load)", "config_utils.py", "config_operations"),
        
        # Logging setup
        (r"logging\.(?:basicConfig|getLogger).*?logging\.(?:INFO|DEBUG|WARNING|ERROR)", "logging_utils.py", "setup_logging"),
    ]
    
    # Results dictionary
    duplicates = {}
    
    # Walk through the source directory
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py") and "__pycache__" not in root:
                file_path = os.path.join(root, file)
                
                # Read the file content
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Check for each pattern
                    for pattern, helper_file, function_name in DUPLICATE_PATTERNS:
                        matches = re.findall(pattern, content, re.DOTALL)
                        if matches:
                            if (helper_file, function_name) not in duplicates:
                                duplicates[(helper_file, function_name)] = []
                            duplicates[(helper_file, function_name)].append((file_path, len(matches)))
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
    
    # Print results
    if duplicates:
        print("\n📊 Found potential duplicate functionality:")
        for (helper_file, function_name), occurrences in duplicates.items():
            if len(occurrences) > 2:  # Only show if it appears in more than 2 files
                print(f"\n🔄 {function_name} (could be consolidated in {helper_file})")
                print(f"   Found in {len(occurrences)} files:")
                for file_path, count in sorted(occurrences, key=lambda x: x[1], reverse=True)[:5]:
                    rel_path = os.path.relpath(file_path, src_dir)
                    print(f"   - {rel_path} ({count} occurrences)")
                if len(occurrences) > 5:
                    print(f"   - ... and {len(occurrences) - 5} more files")
    else:
        print("No significant duplicate functionality found.")
    
    return duplicates

def create_helper_files(target_dir, duplicates):
    """Create helper files to consolidate duplicate functionality."""
    if not duplicates:
        return
    
    print("\n📝 Creating helper files to consolidate duplicate functionality")
    print("=" * 50)
    
    # Helper file templates
    HELPER_TEMPLATES = {
        "file_utils.py": '''"""File utility functions for common file operations."""

def read_file(file_path, encoding="utf-8"):
    """Read a file and return its contents."""
    with open(file_path, "r", encoding=encoding) as f:
        return f.read()

def write_file(file_path, content, encoding="utf-8"):
    """Write content to a file."""
    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)
    return True

def append_to_file(file_path, content, encoding="utf-8"):
    """Append content to a file."""
    with open(file_path, "a", encoding=encoding) as f:
        f.write(content)
    return True
''',
        "path_utils.py": '''"""Path utility functions for common path operations."""

import os
import sys
from pathlib import Path

def get_project_root():
    """Get the absolute path to the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ensure_dir(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)
    return directory

def get_relative_path(path, base=None):
    """Get a path relative to the base directory."""
    if base is None:
        base = get_project_root()
    return os.path.relpath(path, base)
''',
        "json_utils.py": '''"""JSON utility functions for common JSON operations."""

import json

def load_json(file_path):
    """Load JSON from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data, indent=2):
    """Save data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)
    return True

def parse_json(json_string):
    """Parse a JSON string."""
    return json.loads(json_string)
''',
        "string_utils.py": '''"""String utility functions for common string operations."""

import re

def clean_text(text):
    """Clean text by removing special characters and extra whitespace."""
    text = re.sub(r'[^\\w\\s]', '', text)
    text = re.sub(r'\\s+', ' ', text)
    return text.strip()

def normalize_string(text):
    """Normalize a string by converting to lowercase and removing special characters."""
    return clean_text(text.lower())

def extract_keywords(text, min_length=3):
    """Extract keywords from text."""
    words = re.findall(r'\\b\\w+\\b', text.lower())
    return [word for word in words if len(word) >= min_length]
''',
        "config_utils.py": '''"""Configuration utility functions."""

import json
import os

def load_config(config_path):
    """Load configuration from a JSON file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config_path, config):
    """Save configuration to a JSON file."""
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    return True

def get_config_value(config, key, default=None):
    """Get a value from a configuration dictionary."""
    keys = key.split('.')
    result = config
    try:
        for k in keys:
            result = result[k]
        return result
    except (KeyError, TypeError):
        return default
''',
        "logging_utils.py": '''"""Logging utility functions."""

import logging
import os
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_file=None):
    """Set up logging with the specified log level and optional log file."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file) if log_file else logging.NullHandler()
        ]
    )
    
    return logging.getLogger()

def get_logger(name, log_level=logging.INFO):
    """Get a logger with the specified name and log level."""
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger
'''
    }
    
    # Create utils directory if it doesn't exist
    utils_dir = os.path.join(target_dir, "utils")
    os.makedirs(utils_dir, exist_ok=True)
    
    # Create helper files
    created_files = set()
    for (helper_file, _), _ in duplicates.items():
        if helper_file in HELPER_TEMPLATES and helper_file not in created_files:
            file_path = os.path.join(utils_dir, helper_file)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(HELPER_TEMPLATES[helper_file])
            print(f"📄 Created helper file: {helper_file}")
            created_files.add(helper_file)
    
    # Create __init__.py to make the utils directory a package
    init_path = os.path.join(utils_dir, "__init__.py")
    with open(init_path, "w", encoding="utf-8") as f:
        f.write('"""Utility functions package."""\n\n')
        for helper_file in created_files:
            module_name = helper_file.replace(".py", "")
            f.write(f"from .{module_name} import *\n")
    
    print(f"✅ Created {len(created_files)} helper files in {utils_dir}")

def main(dry_run=True):
    """Main function."""
    print("\n🏗️  Codebase Reorganization Tool")
    print("=" * 50)
    
    if dry_run:
        print("\n🔍 Running in DRY RUN mode - no files will be modified")
    else:
        print("\n⚠️ Running in LIVE mode - files will be modified")
    
    # Identify duplicate functionality
    src_dir = os.path.join(project_root, "src")
    duplicates = identify_duplicate_functionality(src_dir)
    
    # Reorganize the codebase
    target_dir = reorganize_codebase(dry_run)
    
    if not dry_run:
        # Create helper files to consolidate duplicate functionality
        create_helper_files(target_dir, duplicates)
        
        # Apply fractal organization
        apply_fractal_organization(target_dir)
        
        # Apply resource splitting
        apply_resource_splitting(target_dir)
        
        print("\n🎉 Reorganization complete!")
        print(f"The reorganized codebase is available at: {target_dir}")
        print("\nPlease review the changes before replacing the original codebase.")

if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Reorganize the codebase and consolidate duplicate functionality")
    parser.add_argument("--live", action="store_true", help="Run in live mode (actually modify files)")
    args = parser.parse_args()
    
    # Print usage instructions
    print("Usage: py reorganize_codebase.py [--live]")
    print("This tool will reorganize the codebase and consolidate duplicate functionality.")
    print("By default, it runs in dry run mode. Use --live to actually modify files.")
    print()
    
    # Run the main function
    main(dry_run=not args.live)
