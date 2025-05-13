#!/usr/bin/env python
"""
Verify Codebase

This script verifies that all major components of the codebase work correctly
after the reorganization.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import importlib
import time
import traceback

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions

class CodebaseVerifier:
    """Verifies the functionality of the codebase."""
    
    def __init__(self):
        """Initialize the verifier."""
        self.results = {
            "passed": [],
            "failed": [],
            "skipped": []
        }
        self.total_time = 0
    
    def verify_all(self):
        """Run all verification tests."""
        print("\n🔍 Verifying Codebase Functionality")
        print("=" * 80)
        
        start_time = time.time()
        
        # Core components
        self.verify_core_ast()
        self.verify_core_ir()
        self.verify_core_proof()
        self.verify_core_optimization()
        self.verify_core_export()
        
        # Modules
        self.verify_standard_modules()
        self.verify_hierarchical_modules()
        self.verify_resource_oriented_modules()
        
        # UI components
        self.verify_ui_components()
        self.verify_ui_renderers()
        
        # Utils
        self.verify_utils()
        
        # Tools
        self.verify_shadow_tree()
        self.verify_fractal_tools()
        
        self.total_time = time.time() - start_time
        
        # Print summary
        self.print_summary()
    
    def run_test(self, name, test_func):
        """Run a single test and record the result."""
        print(f"\n📋 Testing: {name}")
        print("-" * 80)
        
        start_time = time.time()
        
        try:
            result = test_func()
            if result:
                self.results["passed"].append(name)
                print(f"✅ Passed: {name} ({time.time() - start_time:.2f}s)")
            else:
                self.results["failed"].append(name)
                print(f"❌ Failed: {name} ({time.time() - start_time:.2f}s)")
        except Exception as e:
            self.results["failed"].append(name)
            print(f"❌ Error in {name}: {str(e)}")
            traceback.print_exc()
    
    def verify_imports(self, module_path):
        """Verify that a module can be imported."""
        try:
            module = importlib.import_module(module_path)
            return True
        except ImportError as e:
            print(f"Import error: {str(e)}")
            return False
    
    def verify_core_ast(self):
        """Verify the core AST module."""
        def test_func():
            return self.verify_imports("core.ast")
        
        self.run_test("Core AST", test_func)
    
    def verify_core_ir(self):
        """Verify the core IR module."""
        def test_func():
            return self.verify_imports("core.ir")
        
        self.run_test("Core IR", test_func)
    
    def verify_core_proof(self):
        """Verify the core proof module."""
        def test_func():
            return self.verify_imports("core.proof")
        
        self.run_test("Core Proof", test_func)
    
    def verify_core_optimization(self):
        """Verify the core optimization module."""
        def test_func():
            return self.verify_imports("core.optimization")
        
        self.run_test("Core Optimization", test_func)
    
    def verify_core_export(self):
        """Verify the core export module."""
        def test_func():
            return self.verify_imports("core.export")
        
        self.run_test("Core Export", test_func)
    
    def verify_standard_modules(self):
        """Verify the standard modules."""
        def test_func():
            # Test each category of standard modules
            processing = self.verify_imports("modules.standard.processing")
            analysis = self.verify_imports("modules.standard.analysis")
            export = self.verify_imports("modules.standard.export")
            organization = self.verify_imports("modules.standard.organization")
            
            # Check if shadow tree module is importable
            shadow_tree = self.verify_imports("modules.standard.organization.shadow_tree_module")
            
            return processing and analysis and export and organization and shadow_tree
        
        self.run_test("Standard Modules", test_func)
    
    def verify_hierarchical_modules(self):
        """Verify the hierarchical modules."""
        def test_func():
            return self.verify_imports("modules.hierarchical")
        
        self.run_test("Hierarchical Modules", test_func)
    
    def verify_resource_oriented_modules(self):
        """Verify the resource-oriented modules."""
        def test_func():
            return self.verify_imports("modules.resource_oriented")
        
        self.run_test("Resource-Oriented Modules", test_func)
    
    def verify_ui_components(self):
        """Verify the UI components."""
        def test_func():
            return self.verify_imports("ui.components")
        
        self.run_test("UI Components", test_func)
    
    def verify_ui_renderers(self):
        """Verify the UI renderers."""
        def test_func():
            return self.verify_imports("ui.renderers")
        
        self.run_test("UI Renderers", test_func)
    
    def verify_utils(self):
        """Verify the utility modules."""
        def test_func():
            # Test each utility module
            path_utils = self.verify_imports("utils.path_utils")
            file_utils = self.verify_imports("utils.file_utils")
            json_utils = self.verify_imports("utils.json_utils")
            string_utils = self.verify_imports("utils.string_utils")
            import_utils = self.verify_imports("utils.import_utils")
            
            return path_utils and file_utils and json_utils and string_utils and import_utils
        
        self.run_test("Utilities", test_func)
    
    def verify_shadow_tree(self):
        """Verify the Shadow Tree tool."""
        def test_func():
            # Check if shadow tree tool is importable
            return self.verify_imports("tools.shadow_tree")
        
        self.run_test("Shadow Tree Tool", test_func)
    
    def verify_fractal_tools(self):
        """Verify the Fractal tools."""
        def test_func():
            # Check if fractal tools are importable
            return self.verify_imports("tools.fractal")
        
        self.run_test("Fractal Tools", test_func)
    
    def print_summary(self):
        """Print a summary of the verification results."""
        print("\n📊 Verification Summary")
        print("=" * 80)
        
        total_tests = len(self.results["passed"]) + len(self.results["failed"]) + len(self.results["skipped"])
        
        print(f"Total tests: {total_tests}")
        print(f"Passed: {len(self.results['passed'])} ({len(self.results['passed']) / total_tests * 100:.1f}%)")
        print(f"Failed: {len(self.results['failed'])} ({len(self.results['failed']) / total_tests * 100:.1f}%)")
        print(f"Skipped: {len(self.results['skipped'])} ({len(self.results['skipped']) / total_tests * 100:.1f}%)")
        print(f"Total time: {self.total_time:.2f}s")
        
        if self.results["failed"]:
            print("\n❌ Failed tests:")
            for test in self.results["failed"]:
                print(f"  - {test}")
        
        if self.results["passed"] and not self.results["failed"]:
            print("\n🎉 All tests passed!")
        elif self.results["passed"]:
            print("\n⚠️ Some tests passed, but others failed.")
        else:
            print("\n❌ All tests failed.")

def main():
    """Main function."""
    verifier = CodebaseVerifier()
    verifier.verify_all()

if __name__ == "__main__":
    main()
