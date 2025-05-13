# imports.py

**Path:** `legacy\src\imports.py`

## Description

Centralized imports for the Logic Tool system.
This file ensures all components can find their dependencies.

## Metrics

- **Lines of Code:** 121
- **Functions:** 4
- **Classes:** 0
- **Imports:** 21
- **Complexity:** 28

## Imports

- `import os`
- `import sys`
- `import inspect`
- `import ast`
- `import importlib`
- `from src.ast_explorer.extract_functions`
- `from src.ir_model.extract_ir_from_source`
- `from src.ir_model.get_ir_model`
- `from src.proof_engine.run_z3_proof`
- `from src.graph_builder.build_function_graph`
- `from src.optimizer.optimize_logic`
- `from src.exporter.export_to_python`
- `from src.module_system.Module`
- `from src.module_system.ModuleRegistry`
- `from src.background_system.BackgroundSystem`
- `from ast_explorer.extract_functions`
- `from ir_model.extract_ir_from_source`
- `from ir_model.get_ir_model`
- `from proof_engine.run_z3_proof`
- `from graph_builder.build_function_graph`
- `from optimizer.optimize_logic`
- `from exporter.export_to_python`
- `from module_system.Module`
- `from module_system.ModuleRegistry`
- `from background_system.BackgroundSystem`

## Functions

### `decide(cpu, is_question, is_command)`

Example decision function (previously in original_decision.py)

**Complexity:** 5

### `determine_notification(battery_level, is_weekend, unread_messages, temperature)`

Example notification function (previously in notification_logic.py)

**Complexity:** 13

### `load_module_from_file(file_path, module_name)`

Dynamically load a module from a file path.

**Complexity:** 5

### `get_function_source(func)`

Get the source code of a function.

**Complexity:** 3

## Keywords

`src, path, unread_messages, battery_level, module_name, print, is_weekend, temperature, file_path, spec, module, sys, importlib, project_root, IMPORTS_SUCCESSFUL, imports, is_question, func, inspect, src_dir`

