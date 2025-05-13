#!/usr/bin/env python
"""
Complete Cleanup

This script handles the final remaining items that need to be cleaned up.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import shutil

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions

def cleanup_pycache(dry_run=True):
    """Remove __pycache__ directories."""
    print("\n🗑️ Removing __pycache__ directories")
    print("=" * 80)
    
    pycache_dirs = []
    for root, dirs, _ in os.walk(project_root):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_dirs.append(os.path.join(root, dir_name))
    
    for pycache_dir in pycache_dirs:
        if dry_run:
            print(f"Would remove: {os.path.relpath(pycache_dir, project_root)}")
        else:
            try:
                shutil.rmtree(pycache_dir)
                print(f"Removed: {os.path.relpath(pycache_dir, project_root)}")
            except Exception as e:
                print(f"Error removing {os.path.relpath(pycache_dir, project_root)}: {e}")
    
    print(f"\n{'Would remove' if dry_run else 'Removed'} {len(pycache_dirs)} __pycache__ directories")

def handle_templates_dir(dry_run=True):
    """Move templates directory to appropriate location."""
    print("\n📁 Handling templates directory")
    print("=" * 80)
    
    templates_dir = os.path.join(project_root, "templates")
    if os.path.exists(templates_dir) and os.path.isdir(templates_dir):
        # Determine if it should go to ui/templates or docs/templates
        # Check if it contains UI-related templates or documentation templates
        ui_related = False
        doc_related = False
        
        for root, _, files in os.walk(templates_dir):
            for file in files:
                if file.endswith((".html", ".css", ".js")):
                    ui_related = True
                elif file.endswith((".md", ".rst", ".txt")):
                    doc_related = True
        
        if ui_related and not doc_related:
            dest_dir = "ui/templates"
        elif doc_related and not ui_related:
            dest_dir = "docs/templates"
        else:
            # If mixed or neither, default to ui/templates
            dest_dir = "ui/templates"
        
        dest_path = os.path.join(project_root, dest_dir)
        
        if dry_run:
            print(f"Would move: templates/ -> {dest_dir}/")
        else:
            try:
                # Create destination directory
                ensure_dir(dest_path)
                
                # Move contents to destination
                for item in os.listdir(templates_dir):
                    src_item = os.path.join(templates_dir, item)
                    dest_item = os.path.join(dest_path, item)
                    
                    if os.path.isdir(src_item):
                        if not os.path.exists(dest_item):
                            shutil.copytree(src_item, dest_item)
                        else:
                            # Merge directories
                            for subitem in os.listdir(src_item):
                                src_subitem = os.path.join(src_item, subitem)
                                dest_subitem = os.path.join(dest_item, subitem)
                                
                                if os.path.isdir(src_subitem):
                                    if not os.path.exists(dest_subitem):
                                        shutil.copytree(src_subitem, dest_subitem)
                                else:
                                    if not os.path.exists(dest_subitem):
                                        shutil.copy2(src_subitem, dest_subitem)
                    else:
                        if not os.path.exists(dest_item):
                            shutil.copy2(src_item, dest_item)
                
                # Remove original directory
                shutil.rmtree(templates_dir)
                
                print(f"Moved: templates/ -> {dest_dir}/")
            except Exception as e:
                print(f"Error moving templates/: {e}")
    else:
        print("Templates directory not found")

def move_cleanup_scripts(dry_run=True):
    """Move cleanup scripts to tools/reorganization/."""
    print("\n📄 Moving cleanup scripts")
    print("=" * 80)
    
    cleanup_scripts = [
        "final_cleanup.py",
        "complete_cleanup.py"
    ]
    
    dest_dir = os.path.join(project_root, "tools", "reorganization")
    
    for script in cleanup_scripts:
        src_path = os.path.join(project_root, script)
        dest_path = os.path.join(dest_dir, script)
        
        if os.path.exists(src_path):
            if dry_run:
                print(f"Would move: {script} -> tools/reorganization/{script}")
            else:
                try:
                    # Ensure destination directory exists
                    ensure_dir(dest_dir)
                    
                    # Copy the file
                    shutil.copy2(src_path, dest_path)
                    
                    # Remove the original (except for the currently running script)
                    if script != os.path.basename(__file__):
                        os.remove(src_path)
                        print(f"Moved: {script} -> tools/reorganization/{script}")
                    else:
                        print(f"Copied: {script} -> tools/reorganization/{script}")
                        print(f"Note: The original {script} will be removed when the script completes")
                except Exception as e:
                    print(f"Error moving {script}: {e}")
        else:
            print(f"File not found: {script}")
    
    print(f"\n{'Would move' if dry_run else 'Moved'} cleanup scripts to tools/reorganization/")

def self_destruct(dry_run=True):
    """Remove this script after execution."""
    if not dry_run:
        script_path = os.path.abspath(__file__)
        
        # Use a batch file to delete the script after execution
        bat_path = os.path.join(project_root, "_cleanup_temp.bat")
        with open(bat_path, "w") as f:
            f.write(f"@echo off\n")
            f.write(f"timeout /t 1 /nobreak > nul\n")
            f.write(f"del \"{script_path}\"\n")
            f.write(f"del \"%~f0\"\n")
        
        # Execute the batch file
        os.system(f"start /b \"\" \"{bat_path}\"")
        
        print(f"Script will self-destruct after execution")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Complete Cleanup")
    parser.add_argument("--apply", action="store_true", help="Apply the changes")
    
    args = parser.parse_args()
    dry_run = not args.apply
    
    print("\n🧹 Complete Cleanup")
    print("=" * 80)
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}")
    
    # Clean up __pycache__ directories
    cleanup_pycache(dry_run)
    
    # Handle templates directory
    handle_templates_dir(dry_run)
    
    # Move cleanup scripts
    move_cleanup_scripts(dry_run)
    
    # Self-destruct
    if not dry_run:
        self_destruct(dry_run)
    
    print("\n✅ Complete cleanup complete!")
    if dry_run:
        print("\nTo apply the changes, run: py complete_cleanup.py --apply")

if __name__ == "__main__":
    main()
