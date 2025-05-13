#!/usr/bin/env python3
"""
Test script for the refactoring system.
This script tests the basic functionality of the refactoring system after reorganization.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase


import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def test_analyze():
    """Test the analyze functionality."""
    print("Testing analyze functionality...")

    # Create a simple test file
    test_file = os.path.join(project_root, "test_file.py")
    with open(test_file, "w") as f:
        f.write(
            """
def complex_function():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    
    if a > b:
        if c > d:
            if e > f:
                if g > h:
                    return i
                else:
                    return j
            else:
                return g
        else:
            return e
    else:
        return a
"""
        )

    try:
        # Run the analyze command
        cmd = f"python {os.path.join(project_root, 'refactor_codebase.py')} analyze --file {test_file}"
        print(f"Running: {cmd}")
        result = os.system(cmd)

        if result == 0:
            print("✓ Analyze test passed")
        else:
            print("✗ Analyze test failed")
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)


def test_split():
    """Test the split functionality."""
    print("\nTesting split functionality...")

    # Create a simple test file
    test_file = os.path.join(project_root, "test_file.py")
    with open(test_file, "w") as f:
        f.write(
            """
def function1():
    return "Function 1"

def function2():
    return "Function 2"

def function3():
    return "Function 3"
"""
        )

    try:
        # Run the split command
        output_dir = os.path.join(project_root, "test_output")
        cmd = f"python {os.path.join(project_root, 'refactor_codebase.py')} split --file {test_file} --output {output_dir} --apply"
        print(f"Running: {cmd}")
        result = os.system(cmd)

        if result == 0 and os.path.exists(output_dir):
            print("✓ Split test passed")
        else:
            print("✗ Split test failed")
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(output_dir):
            import shutil

            shutil.rmtree(output_dir)


def test_fix():
    """Test the fix functionality."""
    print("\nTesting fix functionality...")

    # Create a simple test file with unused imports
    test_file = os.path.join(project_root, "test_file.py")
    with open(test_file, "w") as f:
        f.write(
            """
import os
import sys
import json
import time
import random

def simple_function():
    return os.path.join("a", "b")
"""
        )

    try:
        # Run the fix command
        cmd = f"python {os.path.join(project_root, 'refactor_codebase.py')} fix --file {test_file} --apply"
        print(f"Running: {cmd}")
        result = os.system(cmd)

        if result == 0:
            print("✓ Fix test passed")
        else:
            print("✗ Fix test failed")
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)


def test_report():
    """Test the report functionality."""
    print("\nTesting report functionality...")

    # Run the report command
    output_file = os.path.join(project_root, "test_report.json")
    cmd = f"python {os.path.join(project_root, 'refactor_codebase.py')} report --output {output_file}"
    print(f"Running: {cmd}")
    result = os.system(cmd)

    try:
        if result == 0 and os.path.exists(output_file):
            print("✓ Report test passed")
        else:
            print("✗ Report test failed")
    finally:
        # Clean up
        if os.path.exists(output_file):
            os.remove(output_file)


def main():
    """Run all tests."""
    print("Running refactoring system tests...\n")

    # Run the tests
    test_analyze()
    test_split()
    test_fix()
    test_report()

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()
