# analysis_core_module.py

**Path:** `legacy\src\modules\hierarchical\analysis_core_module.py`

## Description

Analysis Core Module - Hierarchical version

This module serves as the core for all analysis-related functionality,
including code parsing, AST exploration, and logic analysis.

## Metrics

- **Lines of Code:** 154
- **Functions:** 6
- **Classes:** 1
- **Imports:** 8
- **Complexity:** 13

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
- `from src.modules.hierarchical.ast_parser_module.ASTParserModule`
- `from src.modules.hierarchical.ir_generator_module.IRGeneratorModule`

## Classes

### AnalysisCoreModule

Core module for all analysis functionality

#### Methods

- `__init__`
- `load_child_modules`
- `render_ui`
- `render_code_input`
- `render_results`
- `process`

#### Inherits From

- `HierarchicalModule`

## Functions

### `__init__(self, parent)`

**Complexity:** 1

### `load_child_modules(self)`

Load all analysis-related child modules

**Complexity:** 1

### `render_ui(self)`

Render the analysis UI

**Complexity:** 1

### `render_code_input(self)`

Render the code input section

**Complexity:** 7

### `render_results(self)`

Render the analysis results

**Complexity:** 4

### `process(self, data, context)`

Process data through the analysis pipeline

**Complexity:** 3

## Keywords

`code, path, state_manager, Code, tabs, Input, ast_result, analysis, key, register_ui_key, uploaded_file, ir_model, dirname, src, ast_parser, ir_generator, File, shared_state, sys, project_root`

