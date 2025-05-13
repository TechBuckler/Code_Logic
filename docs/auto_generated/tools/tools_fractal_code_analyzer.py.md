# code_analyzer.py

**Path:** `tools\fractal\code_analyzer.py`

## Description

Code Analyzer Module

Provides functions for analyzing Python code files to extract
dependencies, complexity metrics, and semantic information.

## Metrics

- **Lines of Code:** 217
- **Functions:** 8
- **Classes:** 0
- **Imports:** 5
- **Complexity:** 33

## Imports

- `import os`
- `import ast`
- `import re`
- `import importlib`
- `from collections.defaultdict`
- `from collections.Counter`

## Functions

### `analyze_file(file_path)`

Analyze a Python file to extract metrics and semantic information.

Args:
    file_path: Path to the Python file
    
Returns:
    Dictionary with analysis results

**Complexity:** 3

### `extract_dependencies(file_path)`

Extract dependencies from a Python file.

Args:
    file_path: Path to the Python file
    
Returns:
    Set of dependencies

**Complexity:** 10

### `_calculate_complexity(tree)`

Calculate cyclomatic complexity of the code.

**Complexity:** 5

### `_extract_functions(tree)`

Extract function definitions from the AST.

**Complexity:** 3

### `_extract_classes(tree)`

Extract class definitions from the AST.

**Complexity:** 5

### `_extract_imports(tree)`

Extract imports from the AST.

**Complexity:** 6

### `_extract_variables(tree)`

Extract variable assignments from the AST.

**Complexity:** 5

### `_extract_keywords(content)`

Extract keywords from the content.

**Complexity:** 3

## Keywords

`node, ast, tree, name, isinstance, content, file_path, imports, walk, module, functions, classes, complexity, len, append, variables, spec, metrics, semantics, docstring`

