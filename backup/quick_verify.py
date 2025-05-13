#!/usr/bin/env python
"""
Quick Verification Script

This script performs a quick verification of the codebase by:
1. Testing imports of key modules
2. Running basic functionality tests
3. Verifying file integrity

It's designed to run quickly while providing comprehensive coverage.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import importlib
import time

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Create __init__.py files in all directories to ensure proper imports
def ensure_init_files():
    """Ensure all directories have __init__.py files for proper imports."""
    print("\n📁 Ensuring __init__.py files exist in all directories")
    count = 0
    
    for root, dirs, files in os.walk(project_root):
        # Skip certain directories
        if any(skip in root for skip in ['.git', '__pycache__', '.vscode', '.idea']):
            continue
            
        # Check if directory is a Python package (should have __init__.py)
        if any(f.endswith('.py') for f in files):
            init_path = os.path.join(root, '__init__.py')
            if not os.path.exists(init_path):
                # Create __init__.py file
                dirname = os.path.basename(root)
                with open(init_path, 'w', encoding='utf-8') as f:
                    f.write(f'"""\n{dirname} package.\n"""\n')
                count += 1
                print(f"Created: {os.path.relpath(init_path, project_root)}")
    
    print(f"Created {count} __init__.py files")

# Run quick verification tests
def run_quick_tests():
    """Run quick verification tests on key components."""
    print("\n🔍 Running Quick Verification Tests")
    print("=" * 80)
    
    start_time = time.time()
    results = {"passed": [], "failed": []}
    
    # Test key imports
    import_tests = [
        ("utils.path_utils", "Path Utilities"),
        ("utils.file_utils", "File Utilities"),
        ("utils.string_utils", "String Utilities"),
        ("utils.json_utils", "JSON Utilities"),
        ("utils.import_utils", "Import Utilities"),
        ("core.ast", "Core AST"),
        ("core.ir", "Core IR"),
        ("core.proof", "Core Proof"),
        ("core.optimization", "Core Optimization"),
        ("core.export", "Core Export"),
        ("modules", "Modules Package"),
        ("modules.standard", "Standard Modules"),
        ("modules.hierarchical", "Hierarchical Modules"),
        ("modules.resource_oriented", "Resource Modules"),
        ("ui", "UI Package"),
        ("ui.components", "UI Components"),
        ("ui.renderers", "UI Renderers"),
        ("tools.shadow_tree", "Shadow Tree Tool"),
        ("tools.fractal", "Fractal Tools")
    ]
    
    for module_path, name in import_tests:
        print(f"Testing import: {name}...")
        try:
            importlib.import_module(module_path)
            results["passed"].append(f"Import: {name}")
            print(f"✅ Passed: {name}")
        except Exception as e:
            results["failed"].append(f"Import: {name}")
            print(f"❌ Failed: {name} - {str(e)}")
    
    # Test basic functionality
    try:
        test_path = join_paths(project_root, "test", "path")
        if isinstance(test_path, str) and "test" in test_path and "path" in test_path:
            results["passed"].append("Function: path_utils.join_paths")
            print("✅ Passed: path_utils.join_paths")
        else:
            results["failed"].append("Function: path_utils.join_paths")
            print("❌ Failed: path_utils.join_paths")
    except Exception as e:
        results["failed"].append("Function: path_utils.join_paths")
        print(f"❌ Failed: path_utils.join_paths - {str(e)}")
    
    try:
        test_file = os.path.join(project_root, "test_verify.tmp")
        test_content = "Test content"
        write_file(test_file, test_content)
        read_content = read_file(test_file)
        os.remove(test_file)
        
        if read_content == test_content:
            results["passed"].append("Function: file_utils read/write")
            print("✅ Passed: file_utils read/write")
        else:
            results["failed"].append("Function: file_utils read/write")
            print("❌ Failed: file_utils read/write")
    except Exception as e:
        results["failed"].append("Function: file_utils read/write")
        print(f"❌ Failed: file_utils read/write - {str(e)}")
    
    # Print summary
    total_time = time.time() - start_time
    total_tests = len(results["passed"]) + len(results["failed"])
    
    print("\n📊 Verification Summary")
    print("=" * 80)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {len(results['passed'])} ({len(results['passed']) / total_tests * 100:.1f}%)")
    print(f"Failed: {len(results['failed'])} ({len(results['failed']) / total_tests * 100:.1f}%)")
    print(f"Total time: {total_time:.2f}s")
    
    if results["failed"]:
        print("\n❌ Failed tests:")
        for test in results["failed"]:
            print(f"  - {test}")
    
    if not results["failed"]:
        print("\n🎉 All tests passed! The codebase is working correctly after reorganization.")
    else:
        print("\n⚠️ Some tests failed. The codebase may need additional fixes.")
        print("\nRecommended fixes:")
        for failed in results["failed"]:
            if "Import:" in failed:
                module = failed.split("Import: ")[1]
                print(f"  - Check that {module} has proper __init__.py files and correct imports")
            elif "Function:" in failed:
                func = failed.split("Function: ")[1]
                print(f"  - Fix the implementation of {func}")

def main():
    """Main function."""
    print("\n🚀 Quick Codebase Verification")
    print("=" * 80)
    
    # Ensure all directories have __init__.py files
    ensure_init_files()
    
    # Run quick verification tests
    run_quick_tests()

if __name__ == "__main__":
    main()
