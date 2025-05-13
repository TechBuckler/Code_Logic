#!/usr/bin/env python
"""
Module Refactoring Script

This script refactors all modules according to the reorganization plan,
moving files to their new locations and updating imports.
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

# Import utility functions

# Module mapping definitions
MODULE_MAPPINGS = [
    # Core components
    {"old_path": "src/ast_explorer.py", "new_path": "core/ast/explorer.py", "module_type": "core"},
    {"old_path": "src/ir_model.py", "new_path": "core/ir/model.py", "module_type": "core"},
    {"old_path": "src/proof_engine.py", "new_path": "core/proof/engine.py", "module_type": "core"},
    {"old_path": "src/optimizer.py", "new_path": "core/optimization/optimizer.py", "module_type": "core"},
    {"old_path": "src/exporter.py", "new_path": "core/export/exporter.py", "module_type": "core"},
    {"old_path": "src/runtime_optimization.py", "new_path": "core/optimization/runtime.py", "module_type": "core"},
    
    # Module system
    {"old_path": "src/module_system.py", "new_path": "modules/system.py", "module_type": "module_system"},
    {"old_path": "src/background_system.py", "new_path": "modules/background.py", "module_type": "module_system"},
    {"old_path": "src/modules/ast_parser_module.py", "new_path": "modules/standard/ast_parser_module.py", "module_type": "module"},
    {"old_path": "src/modules/exporter_module.py", "new_path": "modules/standard/exporter_module.py", "module_type": "module"},
    {"old_path": "src/modules/graph_builder_module.py", "new_path": "modules/standard/graph_builder_module.py", "module_type": "module"},
    {"old_path": "src/modules/ir_generator_module.py", "new_path": "modules/standard/ir_generator_module.py", "module_type": "module"},
    {"old_path": "src/modules/module_explorer_module.py", "new_path": "modules/standard/module_explorer_module.py", "module_type": "module"},
    {"old_path": "src/modules/optimization_testbed_module.py", "new_path": "modules/standard/optimization_testbed_module.py", "module_type": "module"},
    {"old_path": "src/modules/optimizer_module.py", "new_path": "modules/standard/optimizer_module.py", "module_type": "module"},
    {"old_path": "src/modules/project_organizer_module.py", "new_path": "modules/standard/project_organizer_module.py", "module_type": "module"},
    {"old_path": "src/modules/proof_engine_module.py", "new_path": "modules/standard/proof_engine_module.py", "module_type": "module"},
    {"old_path": "src/modules/shadow_tree_module.py", "new_path": "modules/standard/shadow_tree_module.py", "module_type": "module"},
    
    # UI components
    {"old_path": "src/unified_ui.py", "new_path": "ui/unified.py", "module_type": "ui"},
    {"old_path": "src/ui_renderers.py", "new_path": "ui/renderers/base.py", "module_type": "ui"},
    {"old_path": "src/ui_renderers_part2.py", "new_path": "ui/renderers/advanced.py", "module_type": "ui"},
    {"old_path": "src/ui_renderers_part3.py", "new_path": "ui/renderers/specialized.py", "module_type": "ui"},
    {"old_path": "src/ui_utils.py", "new_path": "ui/components/utils.py", "module_type": "ui"},
    {"old_path": "src/new_unified_ui.py", "new_path": "ui/new_unified.py", "module_type": "ui"},
    
    # Utilities
    {"old_path": "src/file_utils.py", "new_path": "utils/file/operations.py", "module_type": "utils"},
    {"old_path": "src/runtime_utils.py", "new_path": "utils/runtime/operations.py", "module_type": "utils"},
    {"old_path": "src/utils.py", "new_path": "utils/general.py", "module_type": "utils"},
    
    # Tools
    {"old_path": "shadow_tree.py", "new_path": "tools/shadow_tree/navigator.py", "module_type": "tools"},
    {"old_path": "simple_shadow_tree.py", "new_path": "tools/shadow_tree/simple.py", "module_type": "tools"},
    {"old_path": "fractal_organizer.py", "new_path": "tools/fractal/organizer.py", "module_type": "tools"},
    {"old_path": "resource_splitter.py", "new_path": "tools/resource/splitter.py", "module_type": "tools"},
    {"old_path": "file_splitter.py", "new_path": "tools/resource/file_splitter.py", "module_type": "tools"},
    {"old_path": "smart_splitter.py", "new_path": "tools/resource/smart_splitter.py", "module_type": "tools"},
    {"old_path": "scan_codebase.py", "new_path": "tools/testing/codebase_scanner.py", "module_type": "tools"},
    {"old_path": "scan_files.py", "new_path": "tools/testing/file_scanner.py", "module_type": "tools"},
    
    # Entry points
    {"old_path": "run_app.py", "new_path": "run_ui.py", "module_type": "entry"},
    {"old_path": "logic_tool.py", "new_path": "run_cli.py", "module_type": "entry"},
    {"old_path": "run_bootstrap.py", "new_path": "run_bootstrap.py", "module_type": "entry"},
    {"old_path": "run_complete_system.py", "new_path": "run_complete.py", "module_type": "entry"},
    {"old_path": "run_explorer.py", "new_path": "run_explorer.py", "module_type": "entry"},
    {"old_path": "run_hierarchical.py", "new_path": "run_hierarchical.py", "module_type": "entry"},
]

# Import patterns to update
IMPORT_PATTERNS = [
    # Old absolute imports
    (r'from src\.(\w+) import', r'from core.\1 import'),
    (r'from src\.modules\.(\w+) import', r'from modules.standard.\1 import'),
    (r'from src\.ui_renderers import', r'from ui.renderers.base import'),
    (r'from src\.unified_ui import', r'from ui.unified import'),
    
    # Old relative imports
    (r'from \.(\w+) import', r'from core.\1 import'),
    (r'from \.modules\.(\w+) import', r'from modules.standard.\1 import'),
    
    # Direct imports
    (r'import src\.(\w+)', r'import core.\1'),
    (r'import src\.modules\.(\w+)', r'import modules.standard.\1'),
]

def create_init_files(directory):
    """Create __init__.py files in all subdirectories."""
    for root, dirs, files in os.walk(directory):
        init_file = os.path.join(root, "__init__.py")
        if not os.path.exists(init_file):
            # Get the directory name for the module docstring
            dir_name = os.path.basename(root)
            content = f'"""\n{dir_name} package.\n"""\n'
            write_file(init_file, content)
            print(f"Created: {init_file}")

def update_imports(content, module_type):
    """Update import statements in the content."""
    updated_content = content
    
    # Apply all import patterns
    for pattern, replacement in IMPORT_PATTERNS:
        updated_content = re.sub(pattern, replacement, updated_content)
    
    # Special case for utils
    if module_type == "utils":
        # Update utils imports to use the new utility modules
        updated_content = re.sub(
            r'import os\nimport sys\nimport json',
            'import os\nimport sys\nimport json\n\n# Import utility functions\nfrom utils.path import ensure_dir, join_paths\nfrom utils.file import read_file, write_file\nfrom utils.data import load_json, save_json',
            updated_content
        )
    
    return updated_content

def refactor_module(old_path, new_path, module_type, dry_run=True):
    """Refactor a module by moving it and updating imports."""
    old_full_path = os.path.join(project_root, old_path)
    new_full_path = os.path.join(project_root, new_path)
    
    # Check if the source file exists
    if not os.path.exists(old_full_path):
        print(f"Warning: Source file not found: {old_full_path}")
        return False
    
    print(f"Refactoring: {old_path} -> {new_path}")
    
    # Read the content
    content = read_file(old_full_path)
    
    # Update imports
    updated_content = update_imports(content, module_type)
    
    if not dry_run:
        # Create the target directory
        ensure_dir(os.path.dirname(new_full_path))
        
        # Write the updated content
        write_file(new_full_path, updated_content)
        
        print(f"  ✅ Moved and updated: {new_path}")
    else:
        print(f"  📝 Would move and update: {new_path} (dry run)")
    
    return True

def main():
    """Main function."""
    print("\n🔄 Module Refactoring Script")
    print("=" * 80)
    
    # Check if this is a dry run
    dry_run = "--apply" not in sys.argv
    print(f"Mode: {'DRY RUN (no changes will be made)' if dry_run else 'APPLY (changes will be made)'}")
    
    # Process each module mapping
    successful = 0
    failed = 0
    
    for mapping in MODULE_MAPPINGS:
        result = refactor_module(
            mapping["old_path"], 
            mapping["new_path"], 
            mapping["module_type"],
            dry_run
        )
        if result:
            successful += 1
        else:
            failed += 1
    
    print(f"\nRefactoring summary: {successful} successful, {failed} failed")
    
    # Create __init__.py files
    if not dry_run:
        print("\n📝 Creating __init__.py files")
        for directory in ["core", "modules", "ui", "utils", "tools"]:
            create_init_files(os.path.join(project_root, directory))
    
    print("\n✅ Refactoring complete!")
    if dry_run:
        print("\nTo apply the changes, run: python refactor_modules.py --apply")

if __name__ == "__main__":
    main()
