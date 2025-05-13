#!/usr/bin/env python
"""
Test Full Validation Pipeline

This script tests the complete validation pipeline, including complexity analysis,
to verify that all components are working together correctly.
"""

import os
import sys
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='pipeline_test.log'
)
logger = logging.getLogger('pipeline_test')

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Run the import fixer first to ensure all modules are available
print("Running import fixer...")

# Import the fix_imports_simple module directly
exec(open(os.path.join(project_root, 'fix_imports_simple.py')).read())
print("Import fixer executed successfully.")

# Import validation components
try:
    from tools.validation.enhanced_shadow_validator import EnhancedShadowValidator, format_validation_result
    ENHANCED_VALIDATOR_AVAILABLE = True
except ImportError:
    logger.error("Enhanced Shadow Validator not available")
    ENHANCED_VALIDATOR_AVAILABLE = False

try:
    from tools.profiling.complexity_analyzer import ComplexityAnalyzer, format_analysis_results
    COMPLEXITY_ANALYZER_AVAILABLE = True
except ImportError:
    logger.error("Complexity Analyzer not available")
    COMPLEXITY_ANALYZER_AVAILABLE = False

def test_sample_code():
    """Test the pipeline with sample code."""
    print("\n=== Testing Pipeline with Sample Code ===\n")
    
    # Sample code with various complexity patterns
    code = """
def constant_time(n):
    \"\"\"O(1) function.\"\"\"
    return n * 2

def linear_search(arr, target):
    \"\"\"O(n) function.\"\"\"
    for item in arr:
        if item == target:
            return True
    return False

def bubble_sort(arr):
    \"\"\"O(n²) function.\"\"\"
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def binary_search(arr, target):
    \"\"\"O(log n) function.\"\"\"
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def fibonacci(n):
    \"\"\"O(2^n) function.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def triple_nested(arr):
    \"\"\"O(n³) function.\"\"\"
    n = len(arr)
    result = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result += arr[i] * arr[j] * arr[k]
    return result
"""
    
    # Test with enhanced validator
    if ENHANCED_VALIDATOR_AVAILABLE:
        print("Testing with Enhanced Shadow Validator...")
        validator = EnhancedShadowValidator()
        result = validator.validate_code(code)
        format_validation_result(result)
        
        # Print stats
        stats = validator.get_stats()
        print("\n=== Validation Stats ===")
        print(f"Total validations: {stats['total_validations']}")
        print(f"Free validations: {stats['free_validations']}")
        print(f"Paid validations: {stats['paid_validations']}")
        
        # Check if complexity analysis was included
        if 'complexity_analysis' in result:
            print("\n=== Complexity Analysis Included in Validation ===")
            print(f"Overall complexity: {result['complexity_analysis'].get('overall_complexity', 'Unknown')}")
            print(f"High complexity detected: {result['complexity_analysis'].get('has_high_complexity', False)}")
            print(f"Optimization opportunities: {result['complexity_analysis'].get('optimization_opportunities', 0)}")
        else:
            print("\n❌ Complexity analysis not included in validation result")
    else:
        print("❌ Enhanced Shadow Validator not available")
    
    # Test with standalone complexity analyzer
    if COMPLEXITY_ANALYZER_AVAILABLE:
        print("\n=== Testing Standalone Complexity Analyzer ===")
        analyzer = ComplexityAnalyzer()
        analysis = analyzer.analyze_code(code)
        print(format_analysis_results(analysis))
    else:
        print("\n❌ Complexity Analyzer not available")

def test_file(file_path):
    """Test the pipeline with a Python file."""
    print(f"\n=== Testing Pipeline with File: {file_path} ===\n")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    # Test with enhanced validator
    if ENHANCED_VALIDATOR_AVAILABLE:
        print("Testing with Enhanced Shadow Validator...")
        validator = EnhancedShadowValidator()
        result = validator.validate_file(file_path)
        format_validation_result(result)
    else:
        print("❌ Enhanced Shadow Validator not available")
    
    # Test with standalone complexity analyzer
    if COMPLEXITY_ANALYZER_AVAILABLE:
        print("\n=== Testing Standalone Complexity Analyzer ===")
        analyzer = ComplexityAnalyzer()
        analysis = analyzer.analyze_file(file_path)
        print(format_analysis_results(analysis))
    else:
        print("\n❌ Complexity Analyzer not available")

def list_available_components():
    """List all available components in the validation pipeline."""
    print("\n=== Available Components ===\n")
    
    components = {
        "Enhanced Shadow Validator": ENHANCED_VALIDATOR_AVAILABLE,
        "Complexity Analyzer": COMPLEXITY_ANALYZER_AVAILABLE
    }
    
    # Try to import other components
    try:
        from tools.validation.shadow_validator import RuleBasedValidator
        components["Rule-Based Validator"] = True
    except ImportError:
        components["Rule-Based Validator"] = False
    
    try:
        from tools.validation.shadow_embeddings import LocalEmbeddings
        components["Local Embeddings"] = True
    except ImportError:
        components["Local Embeddings"] = False
    
    try:
        from tools.validation.shadow_ai_validator import AIValidatorSync
        components["AI Validator"] = True
    except ImportError:
        components["AI Validator"] = False
    
    try:
        from tools.validation.complexity_validator import ComplexityValidator
        components["Complexity Validator"] = True
    except ImportError:
        components["Complexity Validator"] = False
    
    # Print component status
    for name, available in components.items():
        status = "✅ Available" if available else "❌ Not Available"
        print(f"{name}: {status}")
    
    return components

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test the full validation pipeline.')
    parser.add_argument('--file', '-f', help='Path to a Python file to test')
    parser.add_argument('--components', '-c', action='store_true', help='List available components')
    parser.add_argument('--sample', '-s', action='store_true', help='Test with sample code')
    
    args = parser.parse_args()
    
    if args.components:
        list_available_components()
    
    if args.sample:
        test_sample_code()
    
    if args.file:
        test_file(args.file)
    
    if not (args.components or args.sample or args.file):
        # Default: run all tests
        list_available_components()
        test_sample_code()
        # Test with a few files from the codebase
        test_files = [
            os.path.join(project_root, "tools", "profiling", "complexity_analyzer.py"),
            os.path.join(project_root, "tools", "validation", "enhanced_shadow_validator.py"),
            os.path.join(project_root, "validate_with_shadow_enhanced.py")
        ]
        for file_path in test_files:
            if os.path.exists(file_path):
                test_file(file_path)

if __name__ == "__main__":
    main()
