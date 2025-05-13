# bootstrap.py

**Path:** `legacy\src\bootstrap.py`

## Description

Bootstrap - Self-generating architecture system

This module analyzes the existing codebase and transforms it into the new
hierarchical architecture. It serves as the entry point for the self-bootstrapping
process.

## Metrics

- **Lines of Code:** 704
- **Functions:** 16
- **Classes:** 1
- **Imports:** 7
- **Complexity:** 63

## Imports

- `import os`
- `import sys`
- `import json`
- `import importlib`
- `import shutil`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from typing.Set`
- `from typing.Tuple`
- `from src.core.hierarchical_core.HierarchicalModule`
- `from src.core.hierarchical_core.ModuleRegistry`
- `from src.core.hierarchical_core.EventBus`
- `from src.core.hierarchical_core.StateStore`
- `from src.core.hierarchical_core.ModuleLoader`
- `from src.core.hierarchical_core.CodeAnalyzer`
- `from src.core.hierarchical_core.ModuleGenerator`
- `from src.core.hierarchical_core.FileSplitter`

## Classes

### BootstrapModule

Module for bootstrapping the new architecture

#### Methods

- `__init__`
- `initialize`
- `process`
- `analyze_codebase`
- `generate_architecture`
- `transform_codebase`
- `_identify_module_relationships`
- `_generate_module_hierarchy`
- `_generate_module_file`
- `_generate_registry`
- `_transform_module`
- `_generate_entry_point`
- `_on_analysis_complete`
- `_on_generation_complete`
- `_on_transformation_complete`

#### Inherits From

- `HierarchicalModule`

## Functions

### `run_bootstrap()`

Run the bootstrap process

**Complexity:** 1

### `__init__(self, module_id, parent)`

**Complexity:** 1

### `initialize(self)`

Initialize the bootstrap module

**Complexity:** 3

### `process(self, command, context)`

Process bootstrap commands

Args:
    command: The command to process
    context: Additional context
    
Returns:
    Command result

**Complexity:** 8

### `analyze_codebase(self)`

Analyze the existing codebase to identify modules and their relationships

Returns:
    Analysis results

**Complexity:** 7

### `generate_architecture(self)`

Generate the new architecture based on analysis results

Returns:
    Generation results

**Complexity:** 9

### `transform_codebase(self)`

Transform the existing codebase to use the new architecture

Returns:
    Transformation results

**Complexity:** 5

### `_identify_module_relationships(self, modules)`

Identify relationships between modules

Args:
    modules: List of module information
    
Returns:
    Dictionary mapping module names to lists of related module names

**Complexity:** 5

### `_generate_module_hierarchy(self)`

Generate the module hierarchy based on analysis results

Returns:
    List of module information for the new hierarchy

**Complexity:** 23

### `_generate_module_file(self, module_info)`

Generate a module file

Args:
    module_info: Module information
    
Returns:
    Path to the generated file

**Complexity:** 6

### `_generate_registry(self)`

Generate the module registry

Returns:
    Path to the generated registry file

**Complexity:** 1

### `_transform_module(self, old_name, new_info)`

Transform an existing module to use the new architecture

Args:
    old_name: Name of the old module
    new_info: Information about the new module
    
Returns:
    Path to the transformed module file

**Complexity:** 4

### `_generate_entry_point(self)`

Generate the new entry point

Returns:
    Path to the generated entry point file

**Complexity:** 1

### `_on_analysis_complete(self, event)`

Handle analysis complete event

**Complexity:** 1

### `_on_generation_complete(self, event)`

Handle generation complete event

**Complexity:** 1

### `_on_transformation_complete(self, event)`

Handle transformation complete event

**Complexity:** 1

## Keywords

`module, modules, name, class_name, print, parent, path, output_dir, append, child, str, join, get, parent_name, error, file_result, module_info, class_info, hierarchy, lower`

