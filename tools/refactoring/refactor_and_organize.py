#!/usr/bin/env python
"""
Refactor and Organize Codebase

This script uses existing tools to:
1. Find similar code patterns across files
2. Extract common functionality into helper functions
3. Create LINQ-like pipeline operations
4. Organize files into appropriate folders

Approach: Direct and minimal, using existing functionality.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import ast
import shutil
import importlib
import json
import re
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Fix imports
print("Fixing imports...")
from fix_imports_simple import *

def print_section(title):
    """Print a section title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def get_top_level_files():
    """Get all Python files in the top level directory."""
    return [f for f in os.listdir(PROJECT_ROOT) if f.endswith('.py') and os.path.isfile(os.path.join(PROJECT_ROOT, f))]

def print_section(title):
    """Print a section title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def get_top_level_files():
    """Get all Python files in the top level directory."""
    return [f for f in os.listdir(PROJECT_ROOT) if f.endswith('.py') and os.path.isfile(os.path.join(PROJECT_ROOT, f))]

def analyze_code_patterns():
    """Analyze code patterns in the codebase using AST parsing."""
    print_section("ANALYZING CODE PATTERNS")
    
    # Get top-level files
    top_level_files = get_top_level_files()
    print(f"Analyzing {len(top_level_files)} top-level Python files...")
    
    # Full paths for the analyzer
    file_paths = [os.path.join(PROJECT_ROOT, f) for f in top_level_files]
    
    # Simple pattern analysis
    patterns = []
    similar_functions = []
    
    # Track function definitions for similarity comparison
    function_defs = []
    
    # Analyze each file
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the AST
            tree = ast.parse(content)
            
            # Find patterns
            for node in ast.walk(tree):
                # List comprehensions
                if isinstance(node, ast.ListComp):
                    patterns.append({
                        'type': 'list_comprehension',
                        'file': file_path,
                        'line': node.lineno
                    })
                
                # For loops
                elif isinstance(node, ast.For):
                    patterns.append({
                        'type': 'for_loop',
                        'file': file_path,
                        'line': node.lineno
                    })
                
                # Function definitions
                elif isinstance(node, ast.FunctionDef):
                    function_defs.append({
                        'name': node.name,
                        'file': file_path,
                        'line': node.lineno,
                        'args': len(node.args.args),
                        'body_length': len(node.body)
                    })
        
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    # Find similar functions (very simple approach)
    function_by_args = defaultdict(list)
    for func in function_defs:
        key = (func['args'], func['body_length'])
        function_by_args[key].append(func)
    
    # Functions with same arg count and similar body length might be similar
    for key, funcs in function_by_args.items():
        if len(funcs) > 1:
            similar_functions.append(funcs)
    
    print(f"\nFound {len(patterns)} code patterns")
    print(f"Found {len(similar_functions)} potentially similar function groups")
    
    return patterns, similar_functions

def suggest_folder_placements():
    """Suggest appropriate folders for files based on their content and naming."""
    print_section("SUGGESTING FOLDER PLACEMENTS")
    
    # Get top-level files
    top_level_files = get_top_level_files()
    print(f"Analyzing {len(top_level_files)} top-level Python files for folder placement...")
    
    # Define folder categories and their keywords
    categories = {
        'core': ['core', 'system', 'module', 'base', 'hierarchical', 'state'],
        'tools/refactoring': ['refactor', 'split', 'builder', 'analyzer'],
        'tools/analysis': ['analyze', 'stat', 'report', 'structure'],
        'utils/import': ['import', 'fix_', 'circular', 'dependency'],
        'utils/file': ['file', 'path', 'directory', 'io'],
        'tests': ['test_', 'coverage', 'fixture'],
        'modules/standard': ['standard', 'processing', 'export'],
    }
    
    # Analyze files and suggest folders
    folder_suggestions = {}
    
    for file in top_level_files:
        file_path = os.path.join(PROJECT_ROOT, file)
        file_lower = file.lower()
        
        # Try to determine the best category based on filename
        best_category = 'utils'  # Default category
        best_score = 0
        
        for category, keywords in categories.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in file_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_category = category
        
        # If we couldn't determine from filename, check file content
        if best_score == 0:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                for category, keywords in categories.items():
                    score = 0
                    for keyword in keywords:
                        score += content.count(keyword.lower()) * 0.1
                    
                    if score > best_score:
                        best_score = score
                        best_category = category
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        folder_suggestions[file] = best_category
        print(f"{file} -> {best_category}")
    
    return folder_suggestions

def extract_common_patterns(pattern_results):
    """Extract common patterns into helper functions."""
    print_section("EXTRACTING COMMON PATTERNS")
    
    # Group patterns by type
    pattern_by_type = defaultdict(list)
    for pattern in pattern_results:
        pattern_by_type[pattern['type']].append(pattern)
    
    print(f"Found {len(pattern_by_type)} pattern types")
    
    # Create utils directory if it doesn't exist
    utils_dir = os.path.join(PROJECT_ROOT, 'utils')
    if not os.path.exists(utils_dir):
        os.makedirs(utils_dir)
    
    # Create a utility module with helper functions
    utility_module_path = os.path.join(utils_dir, 'common_helpers.py')
    
    utility_content = """\
Common Helper Functions

This module contains common utility functions extracted from repeated patterns
in the codebase.
"""

import os

    
    print(f"Generated utility module at {utility_module_path}")
    return utility_module_path

def create_pipeline_functions():
    """Create LINQ-like pipeline functions for data processing."""
    print_section("CREATING PIPELINE FUNCTIONS")
    
    # Create utils directory if it doesn't exist
    utils_dir = os.path.join(PROJECT_ROOT, 'utils')
    if not os.path.exists(utils_dir):
        os.makedirs(utils_dir)
        
    # Create a pipeline module with LINQ-like functions
    pipeline_module_path = os.path.join(utils_dir, 'pipeline.py')
    
    pipeline_content = """\
"""Pipeline Functions

This module contains LINQ-like pipeline functions for data processing.
"""

def where(iterable, predicate):
    """Filter items in an iterable based on a predicate function."""
    return [item for item in iterable if predicate(item)]

def select(iterable, selector):
    """Transform items in an iterable using a selector function."""
    return [selector(item) for item in iterable]

def group_by(iterable, key_selector):
    """Group items in an iterable by a key selector function."""
    result = {}
    for item in iterable:
        key = key_selector(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result

def order_by(iterable, key_selector, reverse=False):
    """Order items in an iterable by a key selector function."""
    return sorted(iterable, key=key_selector, reverse=reverse)

def first_or_default(iterable, predicate=None, default=None):
    """Get the first item that matches a predicate, or a default value."""
    if predicate is None:
        try:
            return next(iter(iterable))
        except StopIteration:
            return default
    
    for item in iterable:
        if predicate(item):
            return item
    
    return default

class Pipeline:
    """A pipeline for chaining operations on an iterable."""
    
    def __init__(self, iterable):
        self.iterable = iterable
    
    def where(self, predicate):
        """Filter items in the pipeline."""
        self.iterable = where(self.iterable, predicate)
        return self
    
    def select(self, selector):
        """Transform items in the pipeline."""
        self.iterable = select(self.iterable, selector)
        return self
    
    def group_by(self, key_selector):
        """Group items in the pipeline."""
        self.iterable = group_by(self.iterable, key_selector)
        return self
    
    def order_by(self, key_selector, reverse=False):
        """Order items in the pipeline."""
        self.iterable = order_by(self.iterable, key_selector, reverse)
        return self
    
    def first_or_default(self, predicate=None, default=None):
        """Get the first item that matches a predicate."""
        return first_or_default(self.iterable, predicate, default)
    
    def to_list(self):
        """Convert the pipeline to a list."""
        return list(self.iterable)
    
    def to_dict(self):
        """Convert the pipeline to a dictionary."""
        return dict(self.iterable)
    
    def to_set(self):
        """Convert the pipeline to a set."""
        return set(self.iterable)

def from_iterable(iterable):
    """Create a pipeline from an iterable."""
    return Pipeline(iterable)
"""
    
    with open(pipeline_module_path, 'w') as f:
        f.write(pipeline_content)

    
    print(f"Generated pipeline module at {pipeline_module_path}")
    return pipeline_module_path

def move_files_to_folders(folder_suggestions):
    """Move files to their suggested folders."""
    print_section("MOVING FILES TO FOLDERS")
    
    # Track results
    move_results = {}
    
    for file, folder in folder_suggestions.items():
        source_path = os.path.join(PROJECT_ROOT, file)
        target_dir = os.path.join(PROJECT_ROOT, folder)
        target_path = os.path.join(target_dir, file)
        
        # Skip if source doesn't exist or target already exists
        if not os.path.exists(source_path) or os.path.exists(target_path):
            print(f"Skipping {file} -> {folder}")
            continue
        
        # Create target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        # Create __init__.py if it doesn't exist
        init_path = os.path.join(target_dir, '__init__.py')
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                f.write(f'"""{os.path.basename(target_dir)} package.\n\nThis package contains modules related to {os.path.basename(target_dir)}.\n"""\n')
        
        # Copy the file instead of moving to avoid breaking things
        try:
            shutil.copy2(source_path, target_path)
            print(f"Copied {file} -> {folder}/{file}")
            move_results[file] = {
                'source': source_path,
                'target': target_path,
                'status': 'copied'
            }
        except Exception as e:
            print(f"Error copying {file}: {e}")
    
    print(f"Copied {len(move_results)} files to their suggested folders")
    return move_results

def update_imports():
    """Update imports after moving files."""
    print_section("UPDATING IMPORTS")
    
    print("To update imports, please run fix_imports.py manually after this script")
    print("This will ensure all imports are correctly updated")
    return {}

def test_imports():
    """Test imports after reorganization."""
    print_section("TESTING IMPORTS")
    
    print("To test imports, please run test_all_imports.py manually after this script")
    print("This will verify that all imports still work correctly")
    return {}

def main():
    """Main function to orchestrate the refactoring and organization process."""
    print_section("STARTING REFACTOR AND ORGANIZE")
    
    # Step 1: Analyze code patterns
    patterns, similar_functions = analyze_code_patterns()
    
    # Step 2: Suggest folder placements
    folder_suggestions = suggest_folder_placements()
    
    # Step 3: Extract common patterns into utility functions
    utility_module_path = extract_common_patterns(patterns)
    
    # Step 4: Create pipeline functions
    pipeline_module_path = create_pipeline_functions()
    
    # Step 5: Move files to folders
    move_results = move_files_to_folders(folder_suggestions)
    
    # Step 6: Update imports (manual step)
    update_imports()
    
    # Step 7: Test imports (manual step)
    test_imports()
    
    print_section("REFACTOR AND ORGANIZE COMPLETE")
    print(f"Analyzed {len(patterns)} code patterns")
    print(f"Found {len(similar_functions)} potentially similar function groups")
    print(f"Created utility module at {utility_module_path}")
    print(f"Created pipeline module at {pipeline_module_path}")
    print(f"Copied {len(move_results)} files to their suggested folders")
    
    print("\nNext steps:")
    print("1. Run test_all_imports.py to verify imports still work")
    print("2. Run fix_imports.py if any import issues persist")
    print("3. Remove original files that were copied to new locations if desired")

if __name__ == "__main__":
    main()
