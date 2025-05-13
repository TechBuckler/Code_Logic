# runtime_utils.py

**Path:** `legacy\src\runtime_utils.py`

## Description

Runtime Utilities for the Logic Tool System.
This file provides functions that bridge the logic analysis and runtime optimization components.

## Metrics

- **Lines of Code:** 437
- **Functions:** 39
- **Classes:** 8
- **Imports:** 10
- **Complexity:** 50

## Imports

- `import os`
- `import ast`
- `import inspect`
- `import time`
- `import threading`
- `import json`
- `import hashlib`
- `from collections.defaultdict`
- `from collections.Counter`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Callable`
- `from typing.Union`
- `from typing.Tuple`
- `from src.module_system.Module`

## Classes

### PatternMiner

Mines patterns from Python code for optimization.

#### Methods

- `__init__`
- `analyze_file`
- `analyze_directory`
- `save_patterns`
- `load_patterns`
- `_extract_patterns`
- `_serialize_condition`
- `_get_node_type`

### TokenInjector

Injects optimization tokens into Python code.

#### Methods

- `__init__`
- `load_patterns`
- `inject_tokens`

### AdaptiveAgent

Agent for adaptive runtime optimization.

#### Methods

- `__init__`
- `start`
- `stop`
- `register_function`
- `_monitor_loop`
- `_optimize_function`
- `_hash_function`

### JitRouter

Routes function execution to CPU or GPU.

#### Methods

- `__init__`
- `route`
- `_check_gpu`
- `_is_gpu_candidate`

### _OptimizationTransformer

AST transformer for adding optimization tokens.

#### Methods

- `__init__`
- `visit_FunctionDef`
- `visit_If`

#### Inherits From


### PatternMiningModule

#### Methods

- `__init__`
- `process`

#### Inherits From

- `Module`

### TokenInjectionModule

#### Methods

- `__init__`
- `process`

#### Inherits From

- `Module`

### JitRoutingModule

#### Methods

- `__init__`
- `process`

#### Inherits From

- `Module`

## Functions

### `optimize(func)`

Decorator for runtime optimization.

**Complexity:** 2

### `condition(cond)`

Runtime optimization for conditions.

**Complexity:** 1

### `start_runtime_optimization()`

Start the runtime optimization system.

**Complexity:** 1

### `stop_runtime_optimization()`

Stop the runtime optimization system.

**Complexity:** 1

### `mine_patterns_from_directory(directory, output_file)`

Mine patterns from a directory of Python files.

**Complexity:** 1

### `optimize_file(input_file, output_file, pattern_file)`

Optimize a Python file using mined patterns.

**Complexity:** 2

### `register_runtime_modules(registry)`

Register runtime modules with the module registry.

**Complexity:** 5

### `__init__(self, cache_dir)`

**Complexity:** 1

### `analyze_file(self, file_path)`

Analyze a Python file for patterns.

**Complexity:** 4

### `analyze_directory(self, directory)`

Analyze all Python files in a directory.

**Complexity:** 4

### `save_patterns(self, output_file)`

Save mined patterns to a file.

**Complexity:** 2

### `load_patterns(self, input_file)`

Load patterns from a file.

**Complexity:** 1

### `_extract_patterns(self, tree)`

Extract patterns from an AST.

**Complexity:** 9

### `_serialize_condition(self, node)`

Serialize a condition node to a pattern string.

**Complexity:** 7

### `_get_node_type(self, node)`

Get a type descriptor for a node.

**Complexity:** 6

### `__init__(self, pattern_file)`

**Complexity:** 3

### `load_patterns(self, pattern_file)`

Load patterns from a file.

**Complexity:** 1

### `inject_tokens(self, source_file, output_file)`

Inject optimization tokens into a Python file.

**Complexity:** 2

### `__init__(self)`

**Complexity:** 1

### `start(self, daemon)`

Start the adaptive agent.

**Complexity:** 2

### `stop(self)`

Stop the adaptive agent.

**Complexity:** 2

### `register_function(self, func, metadata)`

Register a function for optimization.

**Complexity:** 1

### `_monitor_loop(self)`

Background monitoring loop.

**Complexity:** 5

### `_optimize_function(self, func_name)`

Optimize a function based on runtime metrics.

**Complexity:** 2

### `_hash_function(self, func)`

Generate a hash for a function.

**Complexity:** 3

### `__init__(self)`

**Complexity:** 1

### `route(self, func)`

Route a function to CPU or GPU.

**Complexity:** 4

### `_check_gpu(self)`

Check if GPU is available.

**Complexity:** 1

### `_is_gpu_candidate(self, func)`

Determine if a function is a good GPU candidate.

**Complexity:** 3

### `wrapper()`

**Complexity:** 2

### `__init__(self, patterns)`

**Complexity:** 1

### `visit_FunctionDef(self, node)`

Add optimization decorators to functions.

**Complexity:** 1

### `visit_If(self, node)`

Add optimization hints to if statements.

**Complexity:** 1

### `__init__(self)`

**Complexity:** 1

### `process(self, data, context)`

**Complexity:** 3

### `__init__(self)`

**Complexity:** 1

### `process(self, data, context)`

**Complexity:** 3

### `__init__(self)`

**Complexity:** 1

### `process(self, data, context)`

**Complexity:** 1

## Keywords

`node, ast, str, func, patterns, func_name, output_file, time, isinstance, __init__, source, pattern, __name__, pattern_file, Callable, Dict, optimized_functions, function_patterns, file_path, open`

