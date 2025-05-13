# unified_core.py

**Path:** `core\unified_core.py`

## Description

Unified Core Architecture

This module provides a unified core architecture that integrates all existing modules
while maintaining a clean hierarchical structure. It serves as the central hub for
all functionality in the Logic Tool.

## Metrics

- **Lines of Code:** 199
- **Functions:** 11
- **Classes:** 1
- **Imports:** 16
- **Complexity:** 14

## Imports

- `import os`
- `import sys`
- `import importlib`
- `from typing.Dict`
- `from typing.List`
- `from typing.Any`
- `from typing.Optional`
- `from typing.Set`
- `from typing.Callable`
- `from src.core.state_manager.state_manager`
- `from src.imports.ModuleRegistry`
- `from src.modules.ast_parser_module.AstParserModule`
- `from src.modules.ir_generator_module.IrGeneratorModule`
- `from src.modules.optimizer_module.OptimizerModule`
- `from src.modules.proof_engine_module.ProofEngineModule`
- `from src.modules.graph_builder_module.GraphBuilderModule`
- `from src.modules.exporter_module.ExporterModule`
- `from src.modules.project_organizer_module.ProjectOrganizerModule`
- `from src.modules.module_explorer_module.ModuleExplorerModule`
- `from src.modules.optimization_testbed_module.OptimizationTestbedModule`
- `from src.runtime_utils.register_runtime_modules`

## Classes

### UnifiedCore

Unified core architecture that integrates all existing modules
while maintaining a clean hierarchical structure.

#### Methods

- `__init__`
- `initialize`
- `_register_modules`
- `_build_hierarchy`
- `_connect_modules`
- `handle_event`
- `register_event_handler`
- `get_module`
- `get_modules_in_category`
- `process_with_module`
- `shutdown`

## Functions

### `__init__(self)`

Initialize the unified core

**Complexity:** 1

### `initialize(self)`

Initialize the unified core and all modules

**Complexity:** 1

### `_register_modules(self)`

Register all modules with the registry

**Complexity:** 1

### `_build_hierarchy(self)`

Build a hierarchical structure of modules

**Complexity:** 1

### `_connect_modules(self)`

Connect modules through events

**Complexity:** 5

### `handle_event(self, event_type, data)`

Handle events from the event bus

**Complexity:** 5

### `register_event_handler(self, event_type, handler)`

Register a handler for an event

**Complexity:** 2

### `get_module(self, name)`

Get a module by name

**Complexity:** 1

### `get_modules_in_category(self, category)`

Get all modules in a category

**Complexity:** 2

### `process_with_module(self, module_name, data, context)`

Process data with a specific module

**Complexity:** 3

### `shutdown(self)`

Shutdown the unified core and all modules

**Complexity:** 1

## Keywords

`module_registry, modules, src, event, register, name, event_type, handler, path, event_handlers, get_module, module, children, module_hierarchy, shared_state, ir_generator, flow, sys, dirname, project_root`

