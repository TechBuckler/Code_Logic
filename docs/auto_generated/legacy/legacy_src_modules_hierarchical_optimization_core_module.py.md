# optimization_core_module.py

**Path:** `legacy\src\modules\hierarchical\optimization_core_module.py`

## Description

Optimization Core Module - Hierarchical version

This module serves as the core for all optimization-related functionality,
including logic optimization, formal verification, and performance analysis.

## Metrics

- **Lines of Code:** 156
- **Functions:** 5
- **Classes:** 1
- **Imports:** 9
- **Complexity:** 15

## Imports

- `import os`
- `import sys`
- `import streamlit as st`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from src.core.hierarchical_module.HierarchicalModule`
- `from src.core.state_manager.state_manager`
- `from src.modules.hierarchical.optimizer_module.OptimizerModule`
- `from src.modules.hierarchical.proof_engine_module.ProofEngineModule`
- `from src.imports.export_to_python`

## Classes

### OptimizationCoreModule

Core module for all optimization functionality

#### Methods

- `__init__`
- `load_child_modules`
- `render_ui`
- `render_results`
- `process`

#### Inherits From

- `HierarchicalModule`

## Functions

### `__init__(self, parent)`

**Complexity:** 1

### `load_child_modules(self)`

Load all optimization-related child modules

**Complexity:** 1

### `render_ui(self)`

Render the optimization UI

**Complexity:** 1

### `render_results(self)`

Render the combined optimization results

**Complexity:** 12

### `process(self, data, context)`

Process data through the optimization pipeline

**Complexity:** 3

## Keywords

`optimization_results, get, proof_result, path, ir_model, tabs, merged, src, optimization, original_count, dirname, state_manager, optimizer, proof_engine, Verification, function_name, markdown, error, logic, merged_count`

