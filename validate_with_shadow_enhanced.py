#!/usr/bin/env python
"""
Enhanced Shadow Validation System Integration

This script provides a command-line interface to the enhanced Shadow validation system,
integrating rule-based validation, embeddings, and AI models for comprehensive code validation.
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='validator.log'
)
logger = logging.getLogger('shadow_validation')

# Fix imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.import_utils import fix_imports
fix_imports()

# Import the enhanced shadow validator
try:
    from tools.validation.enhanced_shadow_validator import EnhancedShadowValidator, format_validation_result
except ImportError:
    logger.error("Failed to import EnhancedShadowValidator. Make sure the module is available.")
    sys.exit(1)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Validate Python code using the Enhanced Shadow validation system.')
    
    # Input sources
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file', '-f', help='Path to a Python file to validate')
    input_group.add_argument('--directory', '-d', help='Path to a directory containing Python files to validate')
    input_group.add_argument('--code', '-c', help='Python code string to validate')
    input_group.add_argument('--function', help='Function to validate (requires --file)')
    
    # Validation options
    parser.add_argument('--recursive', '-r', action='store_true', help='Recursively validate directories')
    parser.add_argument('--output', '-o', help='Output file for validation results (JSON format)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--stats', '-s', action='store_true', help='Show validation statistics')
    parser.add_argument('--ai-only', action='store_true', help='Use only AI validation (skips rule-based and embeddings)')
    parser.add_argument('--model', '-m', choices=['gpt-3.5-turbo', 'gpt-4-turbo', 'gpt-4o-mini', 'gpt-4o'], 
                        help='Specify AI model to use (only with --ai-only)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate argument combinations
    if args.function and not args.file:
        parser.error("--function requires --file")
    
    if args.model and not args.ai_only:
        parser.error("--model requires --ai-only")
    
    return args

def validate_file(validator, file_path: str, function_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate a Python file.
    
    Args:
        validator: The validator instance
        file_path: Path to the file to validate
        function_name: Optional name of a function to validate
        
    Returns:
        A dictionary with validation results
    """
    try:
        if function_name:
            with open(file_path, 'r') as f:
                code = f.read()
            return validator.validate_function(code, function_name)
        else:
            return validator.validate_file(file_path)
    except Exception as e:
        logger.error(f"Error validating file {file_path}: {str(e)}")
        return {
            "status": "ERROR",
            "confidence": 0.0,
            "explanation": f"Error validating file {file_path}: {str(e)}",
            "suggestions": [],
            "file_path": file_path
        }

def validate_directory(validator, directory_path: str, recursive: bool = True) -> Dict[str, List[Dict[str, Any]]]:
    """
    Validate all Python files in a directory.
    
    Args:
        validator: The validator instance
        directory_path: Path to the directory to validate
        recursive: Whether to recursively validate subdirectories
        
    Returns:
        A dictionary with validation results for each file
    """
    return validator.validate_directory(directory_path, recursive)

def validate_code(validator, code: str) -> Dict[str, Any]:
    """
    Validate a Python code string.
    
    Args:
        validator: The validator instance
        code: The code to validate
        
    Returns:
        A dictionary with validation results
    """
    return validator.validate_code(code)

def save_results(results: Dict[str, Any], output_file: str) -> None:
    """
    Save validation results to a file.
    
    Args:
        results: The validation results
        output_file: Path to the output file
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving results to {output_file}: {str(e)}")

def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Create validator
    validator = EnhancedShadowValidator()
    
    # Validate based on input source
    if args.file:
        if args.function:
            logger.info(f"Validating function {args.function} in file {args.file}")
            results = validate_file(validator, args.file, args.function)
        else:
            logger.info(f"Validating file {args.file}")
            results = validate_file(validator, args.file)
    elif args.directory:
        logger.info(f"Validating directory {args.directory} (recursive: {args.recursive})")
        results = validate_directory(validator, args.directory, args.recursive)
    elif args.code:
        logger.info("Validating code string")
        results = validate_code(validator, args.code)
    
    # Save results if requested
    if args.output:
        save_results(results, args.output)
    
    # Display results
    if isinstance(results, dict) and 'files' in results:
        # Directory validation results
        print(f"Validated {len(results['files'])} files")
        for result in results['files']:
            if args.verbose:
                format_validation_result(result)
            else:
                status = result.get('status', 'UNKNOWN')
                file_path = result.get('file_path', 'unknown')
                print(f"{file_path}: {status}")
    else:
        # Single file or code validation results
        format_validation_result(results)
    
    # Show statistics if requested
    if args.stats:
        stats = validator.get_stats()
        print("\n" + "=" * 60)
        print("VALIDATION STATS")
        print("=" * 60)
        print(f"Total validations: {stats['total_validations']}")
        print(f"Free validations: {stats['free_validations']} ({stats['free_percentage']:.1f}%)")
        print(f"Paid validations: {stats['paid_validations']} ({stats['paid_percentage']:.1f}%)")
        print(f"Total cost: ${stats['total_cost']:.6f}")
        print(f"Cost per 1,000 validations: ${stats['cost_per_1000']:.2f}")
        
        print("\nVALIDATION MODES:")
        for mode, count in stats['validation_modes'].items():
            print(f"{mode}: {count}")
        
        print("\nMODEL USAGE:")
        for model, count in stats['model_usage'].items():
            if count > 0:
                print(f"{model}: {count}")
        
        print("=" * 60)

if __name__ == "__main__":
    main()
