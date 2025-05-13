# Codebase Refactoring System

This system provides a comprehensive set of tools for analyzing, refactoring, and improving Python codebases. It's designed to help identify complex code, break it down into manageable components, and rebuild optimized versions.

## Components

The refactoring system consists of four main components:

1. **Refactor Analyzer** (`refactor_analyzer.py`): Analyzes code to identify refactoring opportunities, including:
   - Unused imports
   - Complex functions (high cyclomatic complexity or length)
   - Error handling issues
   - Resource management problems
   - Dependency relationships

2. **Refactor Splitter** (`refactor_splitter.py`): Breaks down complex files and functions:
   - Splits large files into logical modules
   - Breaks complex functions into smaller, focused functions
   - Extracts common functionality into utility functions
   - Maintains imports and dependencies during splitting

3. **Refactor Builder** (`refactor_builder.py`): Rebuilds optimized files from components:
   - Combines split files while maintaining functionality
   - Optimizes imports and removes unused code
   - Ensures proper dependency management
   - Generates clean, well-structured code

4. **Refactor Codebase** (`refactor_codebase.py`): Main entry point that provides a unified interface to all tools.

## Usage

### Analyzing Code

To identify refactoring opportunities:

```bash
# Analyze a specific file
python refactor_codebase.py analyze --file path/to/file.py --output analysis.json

# Analyze the entire codebase
python refactor_codebase.py analyze --output codebase_analysis.json
```

### Splitting Complex Code

To break down complex files and functions:

```bash
# Split a specific file
python refactor_codebase.py split --file path/to/file.py --output output_dir --apply

# Split a specific function
python refactor_codebase.py split --file path/to/file.py --function function_name --output output_file.py --apply

# Split the entire codebase
python refactor_codebase.py split --output refactored_codebase --apply
```

### Rebuilding Optimized Code

To rebuild optimized files from components:

```bash
# Rebuild a specific file from its parts
python refactor_codebase.py rebuild --parts path/to/module_parts --output rebuilt_module.py --apply

# Rebuild the entire codebase
python refactor_codebase.py rebuild --parts refactored_codebase --output rebuilt_codebase --apply
```

### Fixing Common Issues

To apply fixes for common issues:

```bash
# Fix a specific file
python refactor_codebase.py fix --file path/to/file.py --apply

# Fix the entire codebase
python refactor_codebase.py fix --apply
```

### Generating Reports

To generate a report on codebase structure and complexity:

```bash
# Generate a report
python refactor_codebase.py report --output codebase_report.json
```

## Workflow Example

A typical workflow might look like this:

1. **Analyze** the codebase to identify issues:
   ```bash
   python refactor_codebase.py analyze --output analysis.json
   ```

2. **Generate a report** to prioritize refactoring efforts:
   ```bash
   python refactor_codebase.py report --output report.json
   ```

3. **Fix** simple issues automatically:
   ```bash
   python refactor_codebase.py fix --apply
   ```

4. **Split** complex files and functions:
   ```bash
   python refactor_codebase.py split --apply
   ```

5. **Rebuild** the codebase with optimized components:
   ```bash
   python refactor_codebase.py rebuild --parts refactored --output rebuilt --apply
   ```

## Features

- **Dynamic Analysis**: Identifies complex code based on metrics like cyclomatic complexity and lines of code
- **Dependency Tracking**: Maintains relationships between functions and classes during refactoring
- **Import Optimization**: Removes unused imports and organizes import statements
- **Error Handling Improvement**: Identifies and fixes bare except clauses and other error handling issues
- **Resource Management**: Detects potential resource leaks and suggests fixes
- **Comprehensive Reporting**: Generates detailed reports on codebase structure and complexity

## Requirements

- Python 3.8+
- AST module (standard library)
- NetworkX (for dependency analysis)

## Notes

- Always run tools with the `--apply` flag to apply changes (otherwise, they run in dry-run mode)
- Back up your codebase before applying extensive refactoring
- The system preserves functionality but may change code structure significantly
