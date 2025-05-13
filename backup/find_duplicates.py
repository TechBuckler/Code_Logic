#!/usr/bin/env python
"""
Duplicate Functionality Finder

This script identifies duplicate functionality across the codebase
and suggests helper files to consolidate them.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import re

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def identify_duplicate_functionality(src_dir):
    """Identify duplicate functionality across the codebase."""
    print("\n🔍 Identifying duplicate functionality")
    print("=" * 80)
    
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
        print("=" * 80)
        
        for (helper_file, function_name), occurrences in duplicates.items():
            if len(occurrences) > 2:  # Only show if it appears in more than 2 files
                print(f"\n🔄 {function_name} (could be consolidated in {helper_file})")
                print(f"   Found in {len(occurrences)} files:")
                
                # Sort by number of occurrences
                sorted_occurrences = sorted(occurrences, key=lambda x: x[1], reverse=True)
                
                # Show top occurrences
                for file_path, count in sorted_occurrences[:10]:
                    rel_path = os.path.relpath(file_path, src_dir)
                    print(f"   - {rel_path} ({count} occurrences)")
                
                if len(occurrences) > 10:
                    print(f"   - ... and {len(occurrences) - 10} more files")
    else:
        print("No significant duplicate functionality found.")
    
    return duplicates

def suggest_helper_files(duplicates):
    """Suggest helper files to consolidate duplicate functionality."""
    if not duplicates:
        return
    
    print("\n📝 Suggested helper files to consolidate duplicate functionality:")
    print("=" * 80)
    
    # Group by helper file
    helper_files = {}
    for (helper_file, function_name), occurrences in duplicates.items():
        if helper_file not in helper_files:
            helper_files[helper_file] = []
        helper_files[helper_file].append((function_name, len(occurrences)))
    
    # Print suggestions
    for helper_file, functions in helper_files.items():
        print(f"\n📄 {helper_file}")
        print(f"   Functions to include:")
        for function_name, count in sorted(functions, key=lambda x: x[1], reverse=True):
            print(f"   - {function_name} (used in {count} places)")

def main():
    """Main function."""
    print("\n🔍 Duplicate Functionality Finder")
    print("=" * 80)
    
    # Define source directory
    src_dir = os.path.join(project_root, "src")
    if not os.path.exists(src_dir):
        print(f"Error: Source directory not found: {src_dir}")
        return
    
    print(f"Scanning directory: {src_dir}")
    
    # Identify duplicate functionality
    duplicates = identify_duplicate_functionality(src_dir)
    
    # Suggest helper files
    suggest_helper_files(duplicates)
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
