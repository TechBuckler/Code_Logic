#!/usr/bin/env python
"""
Codebase Reorganization Implementation

This script implements the reorganization plan for the codebase,
creating the directory structure and moving files to their appropriate locations.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions

def create_directory_structure():
    """Create the balanced directory structure."""
    print("\n🏗️ Creating directory structure")
    print("=" * 80)
    print("This will create the following top-level directories:")
    print("  - core/     (Core algorithms and processing)")
    print("  - modules/  (Module implementations)")
    print("  - ui/       (User interface components)")
    print("  - utils/    (Utility functions and helpers)")
    print("  - tools/    (Standalone tools)")
    print("  - docs/     (Documentation)")
    print("  - tests/    (Test suite)")
    print("\nCreating directories...")
    
    # Define the directory structure
    structure = {
        "core": ["ast", "ir", "proof", "optimization", "export"],
        "modules": ["hierarchical", "resource_oriented", "standard"],
        "ui": ["components", "renderers", "pages"],
        "utils": ["file", "nlp", "runtime", "system"],
        "tools": ["shadow_tree", "fractal", "resource", "testing"],
        "docs": ["api", "guides", "examples"],
        "tests": ["unit", "integration", "e2e"]
    }
    
    # Create directories
    for top_dir, sub_dirs in structure.items():
        top_path = os.path.join(project_root, top_dir)
        if not os.path.exists(top_path):
            os.makedirs(top_path)
            print(f"Created: {top_dir}/")
        
        # Create subdirectories
        for sub_dir in sub_dirs:
            sub_path = os.path.join(top_path, sub_dir)
            if not os.path.exists(sub_path):
                os.makedirs(sub_path)
                print(f"Created: {top_dir}/{sub_dir}/")
    
    # Create special resource-oriented subdirectories
    resource_types = ["cpu", "memory", "gpu", "network"]
    for res_type in resource_types:
        res_path = os.path.join(project_root, "modules", "resource_oriented", res_type)
        if not os.path.exists(res_path):
            os.makedirs(res_path)
            print(f"Created: modules/resource_oriented/{res_type}/")
    
    print("\n✅ Directory structure created successfully!")

def identify_files_to_move():
    """Identify files that should be moved to the new structure."""
    print("\n🔍 Identifying files to move")
    print("=" * 80)
    
    moves = []
    file_count = 0
    
    # Define file patterns and their destinations
    patterns = [
        # Core algorithms
        {"pattern": "_core.py", "destination": "core/"},
        {"pattern": "_ast.py", "destination": "core/ast/"},
        {"pattern": "_ir.py", "destination": "core/ir/"},
        {"pattern": "_proof.py", "destination": "core/proof/"},
        {"pattern": "_optimizer.py", "destination": "core/optimization/"},
        {"pattern": "_export.py", "destination": "core/export/"},
        
        # Modules
        {"pattern": "_module.py", "destination": "modules/standard/"},
        {"pattern": "hierarchical_", "destination": "modules/hierarchical/"},
        
        # UI components
        {"pattern": "_ui.py", "destination": "ui/"},
        {"pattern": "_component.py", "destination": "ui/components/"},
        {"pattern": "_renderer.py", "destination": "ui/renderers/"},
        {"pattern": "_page.py", "destination": "ui/pages/"},
        
        # Tools
        {"pattern": "shadow_tree", "destination": "tools/shadow_tree/"},
        {"pattern": "fractal_", "destination": "tools/fractal/"},
        {"pattern": "resource_", "destination": "tools/resource/"},
        {"pattern": "_test_", "destination": "tools/testing/"},
        
        # Docs
        {"pattern": ".md", "destination": "docs/"},
        {"pattern": "README", "destination": "docs/"},
        {"pattern": "implementation_plan", "destination": "docs/guides/"},
        
        # Tests
        {"pattern": "test_", "destination": "tests/unit/"},
        {"pattern": "integration_test", "destination": "tests/integration/"},
        {"pattern": "e2e_", "destination": "tests/e2e/"},
    ]
    
    # Walk through the source directory
    print("Scanning directories...")
    for root, dirs, files in os.walk(project_root):
        # Skip directories that are part of the new structure
        if any(d in root for d in ["core/", "modules/", "ui/", "utils/", "tools/", "docs/", "tests/"]):
            continue
            
        # Print current directory being scanned
        rel_path = os.path.relpath(root, project_root)
        if rel_path != ".":
            print(f"Scanning: {rel_path}/")
        
        for file in files:
            file_count += 1
            if file_count % 10 == 0:
                print(f"Processed {file_count} files so far...")
                
            if file.endswith(".py") or file.endswith(".md"):
                src_path = os.path.join(root, file)
                
                # Find matching pattern
                dest_dir = None
                for pattern in patterns:
                    if pattern["pattern"] in file:
                        dest_dir = pattern["destination"]
                        break
                
                # If no specific pattern, use default based on file type
                if not dest_dir:
                    if file.endswith(".py"):
                        if "test" in file.lower():
                            dest_dir = "tests/unit/"
                        else:
                            dest_dir = "modules/standard/"
                    elif file.endswith(".md"):
                        dest_dir = "docs/"
                
                if dest_dir:
                    dest_path = os.path.join(project_root, dest_dir, file)
                    moves.append((src_path, dest_path))
    
    print(f"Found {len(moves)} files to move out of {file_count} total files")
    
    # Print some examples of files to be moved
    if moves:
        print("\nExample moves (showing up to 5):")
        for i, (src_path, dest_path) in enumerate(moves[:5]):
            rel_src = os.path.relpath(src_path, project_root)
            rel_dest = os.path.relpath(dest_path, project_root)
            print(f"  {rel_src} -> {rel_dest}")
        
        if len(moves) > 5:
            print(f"  ... and {len(moves) - 5} more")
    
    return moves

def move_files(moves, dry_run=True):
    """Move files to their new locations."""
    print("\n📦 Moving files to new locations")
    print("=" * 80)
    print(f"Mode: {'DRY RUN (showing what would happen)' if dry_run else 'ACTUAL MOVE (files will be copied)'}")
    
    if not moves:
        print("No files to move.")
        return
        
    print(f"Preparing to move {len(moves)} files...")
    
    # Group moves by destination directory for cleaner output
    moves_by_dest = {}
    for src_path, dest_path in moves:
        dest_dir = os.path.dirname(dest_path)
        if dest_dir not in moves_by_dest:
            moves_by_dest[dest_dir] = []
        moves_by_dest[dest_dir].append((src_path, dest_path))
    
    # Process moves by destination
    for dest_dir, dir_moves in moves_by_dest.items():
        rel_dest_dir = os.path.relpath(dest_dir, project_root)
        print(f"\nMoving {len(dir_moves)} files to {rel_dest_dir}/")
        
        # Show up to 3 examples per directory
        for i, (src_path, dest_path) in enumerate(dir_moves[:3]):
            rel_src = os.path.relpath(src_path, project_root)
            rel_dest = os.path.relpath(dest_path, project_root)
            print(f"  {rel_src} -> {rel_dest}")
            
        if len(dir_moves) > 3:
            print(f"  ... and {len(dir_moves) - 3} more files to this directory")
        
        if not dry_run:
            # Ensure destination directory exists
            ensure_dir(os.path.dirname(dest_path))
            
            # Copy the file (safer than moving)
            copy_file(src_path, dest_path)
    
    if dry_run:
        print("\n⚠️ This was a dry run. No files were actually moved.")
        print("Run with --apply to perform the actual file moves.")
    else:
        print("\n✅ Files moved successfully!")

def create_init_files():
    """Create __init__.py files in all Python package directories."""
    print("\n📝 Creating __init__.py files")
    print("=" * 80)
    
    count = 0
    for root, dirs, files in os.walk(project_root):
        # Skip directories that are not part of our structure
        if not any(d in root for d in ["core", "modules", "ui", "utils", "tools", "tests"]):
            continue
        
        # Skip non-Python directories
        if not any(f.endswith(".py") for f in files) and not root.endswith(("core", "modules", "ui", "utils", "tools")):
            continue
        
        # Create __init__.py if it doesn't exist
        init_path = os.path.join(root, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w") as f:
                package_name = os.path.basename(root)
                f.write(f'"""{package_name} package.\n\n"""\n')
            print(f"Created: {os.path.relpath(init_path, project_root)}")
            count += 1
    
    print(f"\n✅ Created {count} __init__.py files")

def create_readme():
    """Create a README.md file explaining the new structure."""
    print("\n📄 Creating README.md")
    print("=" * 80)
    
    readme_path = os.path.join(project_root, "README.md")
    readme_content = """# Code Logic Tool

## Project Structure

This codebase follows a balanced directory structure with 5-7 top-level folders, each containing 5-20 subdirectories:

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
│   ├── hierarchical/  # Hierarchical modules
│   ├── resource_oriented/ # Resource-specific implementations
│   │   ├── cpu/       # CPU-intensive modules
│   │   ├── memory/    # Memory-intensive modules
│   │   ├── gpu/       # GPU-intensive modules
│   │   └── network/   # Network-intensive modules
│   └── standard/      # Standard modules
│
├── ui/                # User interface components
│   ├── components/    # Reusable UI components
│   ├── renderers/     # Output renderers
│   └── pages/         # Page definitions
│
├── utils/             # Utility functions and helpers
│   ├── file/          # File operations
│   ├── nlp/           # Natural language processing
│   ├── runtime/       # Runtime utilities
│   └── system/        # System interaction
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
└── tests/             # Test suite
    ├── unit/          # Unit tests
    ├── integration/   # Integration tests
    └── e2e/           # End-to-end tests
```

## Utility Functions

Common functionality has been consolidated into utility modules:

- `utils.path_utils`: Path manipulation and directory handling
- `utils.file_utils`: File reading, writing, and manipulation
- `utils.json_utils`: JSON parsing and serialization
- `utils.string_utils`: String processing and manipulation

Import these utilities instead of reimplementing common functionality.
"""
    
    with open(readme_path, "w") as f:
        f.write(readme_content)
    
    print(f"Created: README.md")

def main():
    """Main function."""
    print("\n🚀 Codebase Reorganization Implementation")
    print("=" * 80)
    
    # Check if this is a dry run
    dry_run = "--apply" not in sys.argv
    print(f"Mode: {'DRY RUN (no changes will be made)' if dry_run else 'APPLY (changes will be made)'}")
    print("Starting reorganization process...")
    
    # Create directory structure
    create_directory_structure()
    
    # Identify files to move
    moves = identify_files_to_move()
    
    # Move files
    move_files(moves, dry_run=dry_run)
    
    if not dry_run:
        # Create __init__.py files
        create_init_files()
        
        # Create README
        create_readme()
    
    print("\n🎉 Reorganization plan implementation complete!")
    if dry_run:
        print("\nTo apply the changes, run: python implement_reorganization.py --apply")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nReorganization canceled by user.")
    except Exception as e:
        print(f"\n\nError during reorganization: {str(e)}")
    finally:
        print("\nTo apply the changes, run: python implement_reorganization.py --apply")
