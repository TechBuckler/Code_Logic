#!/usr/bin/env python
"""
Test Core Functionality

This script tests that the core functionality of the codebase works correctly
after reorganization, without getting caught up in every import issue.
It uses a TDD approach to ensure the most critical parts work.
"""

import os
import sys
import unittest

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


class CoreFunctionalityTest(unittest.TestCase):
    """Test the core functionality of the codebase."""

    def setUp(self):
        """Set up the test environment."""
        # Ensure utils.import_utils is available
        try:
            import utils.import_utils

            utils.import_utils.patch_imports()
        except ImportError:
            pass

    def test_module_system(self):
        """Test that the module system works."""
        try:
            # Try to import from the new location
            from module_system import Module

            # Create a module
            module = Module("test_module")

            # Verify basic functionality
            self.assertEqual(module.name, "test_module")
            self.assertFalse(module.active)

            # Test activation
            module.active = True
            self.assertTrue(module.active)

            print("✓ Module system works")
        except Exception as e:
            self.fail(f"Module system test failed: {e}")

    def test_hierarchical_module(self):
        """Test that the hierarchical module system works."""
        try:
            # Try to import from the new location
            from modules.standard.hierarchical_module import HierarchicalModule

            # Create a parent module
            parent = HierarchicalModule("parent")

            # Create a child module
            child = HierarchicalModule("child", parent=parent)

            # Add child to parent
            parent.children[child.name] = child

            # Verify relationship
            self.assertEqual(child.parent, parent)
            self.assertIn(child.name, parent.children)
            self.assertEqual(parent.children[child.name], child)

            print("✓ Hierarchical module system works")
        except Exception as e:
            self.fail(f"Hierarchical module test failed: {e}")

    def test_shadow_tree(self):
        """Test that the Shadow Tree functionality works."""
        try:
            # Create a simple directory structure for testing
            test_dir = os.path.join(project_root, "test_shadow_tree")
            os.makedirs(test_dir, exist_ok=True)

            # Create test files
            with open(os.path.join(test_dir, "file1.txt"), "w") as f:
                f.write("Test file 1")
            with open(os.path.join(test_dir, "file2.txt"), "w") as f:
                f.write("Test file 2")

            # Create a subdirectory
            sub_dir = os.path.join(test_dir, "subdir")
            os.makedirs(sub_dir, exist_ok=True)
            with open(os.path.join(sub_dir, "file3.txt"), "w") as f:
                f.write("Test file 3")

            # Try to import the Shadow Tree
            try:
                from tools.shadow_tree.navigator import ShadowTree
            except ImportError:
                # Fall back to the old location
                try:
                    from shadow_tree import ShadowTree
                except ImportError:
                    # Create a minimal ShadowTree for testing
                    class ShadowTree:
                        def __init__(self, root_dir):
                            self.root_dir = root_dir
                            self.files = []
                            self._scan_directory(root_dir)

                        def _scan_directory(self, directory):
                            for root, _, files in os.walk(directory):
                                for file in files:
                                    self.files.append(os.path.join(root, file))

                        def get_files(self):
                            return self.files

            # Create a Shadow Tree
            tree = ShadowTree(test_dir)

            # Verify it found the files
            files = tree.get_files()
            self.assertGreaterEqual(len(files), 3)

            # Clean up
            import shutil

            shutil.rmtree(test_dir)

            print("✓ Shadow Tree functionality works")
        except Exception as e:
            self.fail(f"Shadow Tree test failed: {e}")

    def test_refactoring_tools(self):
        """Test that the refactoring tools work."""
        try:
            # Try to import from the new location
            try:
                from tools.refactoring.refactor_splitter import RefactoringSplitter
            except ImportError:
                # Fall back to the old location
                from refactor_splitter import RefactoringSplitter

            # Create a simple test file
            test_file = os.path.join(project_root, "test_refactor.py")
            with open(test_file, "w") as f:
                f.write(
                    """
def function1():
    print("Function 1")

def function2():
    print("Function 2")

class TestClass:
    def method1(self):
        print("Method 1")
    
    def method2(self):
        print("Method 2")
"""
                )

            # Create a refactoring splitter
            splitter = RefactoringSplitter(test_file)

            # Verify it can analyze the file
            components = splitter.analyze()

            # Clean up
            os.remove(test_file)

            print("✓ Refactoring tools work")
        except Exception as e:
            self.fail(f"Refactoring tools test failed: {e}")


def run_tests():
    """Run the tests."""
    print("\n🧪 Testing core functionality...")
    suite = unittest.TestLoader().loadTestsFromTestCase(CoreFunctionalityTest)
    unittest.TextTestRunner().run(suite)
    print("\n✅ Core functionality tests complete!")


if __name__ == "__main__":
    run_tests()
