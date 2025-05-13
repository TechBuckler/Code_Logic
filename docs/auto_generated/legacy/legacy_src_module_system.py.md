# module_system.py

**Path:** `legacy\src\module_system.py`

## Metrics

- **Lines of Code:** 171
- **Functions:** 18
- **Classes:** 2
- **Imports:** 10
- **Complexity:** 22

## Imports

- `import sys`
- `import os`
- `from modules.ast_parser_module.AstParserModule`
- `from modules.exporter_module.ExporterModule`
- `from modules.graph_builder_module.GraphBuilderModule`
- `from modules.ir_generator_module.IRGeneratorModule`
- `from modules.optimizer_module.OptimizerModule`
- `from modules.proof_engine_module.ProofEngineModule`
- `from modules.module_explorer_module.ModuleExplorerModule`
- `from modules.shadow_tree_module.ShadowTreeModule`

## Classes

### Module

#### Methods

- `__init__`
- `initialize`
- `shutdown`
- `can_process`
- `process`
- `get_resource_profile`
- `set_resource_profile`

### ModuleRegistry

#### Methods

- `__init__`
- `register`
- `initialize_all`
- `shutdown_all`
- `get_module`
- `process_chain`
- `get_modules_by_resource_type`
- `set_resource_constraints`
- `get_resource_constraints`
- `optimize_module_chain`

## Functions

### `__init__(self, name)`

**Complexity:** 1

### `initialize(self)`

**Complexity:** 1

### `shutdown(self)`

**Complexity:** 1

### `can_process(self, data)`

**Complexity:** 1

### `process(self, data, context)`

**Complexity:** 1

### `get_resource_profile(self)`

Return the resource profile for this module.

**Complexity:** 1

### `set_resource_profile(self, profile)`

Set the resource profile for this module.

**Complexity:** 1

### `__init__(self)`

**Complexity:** 1

### `register(self, module)`

**Complexity:** 1

### `initialize_all(self)`

**Complexity:** 2

### `shutdown_all(self)`

**Complexity:** 2

### `get_module(self, name)`

**Complexity:** 1

### `process_chain(self, data, module_names, context)`

**Complexity:** 4

### `get_modules_by_resource_type(self, resource_type)`

Get all modules of a specific resource type.

**Complexity:** 1

### `set_resource_constraints(self, constraints)`

Set resource constraints for the module registry.

**Complexity:** 1

### `get_resource_constraints(self)`

Get current resource constraints.

**Complexity:** 1

### `optimize_module_chain(self, module_names, optimization_profile)`

Optimize a module chain based on resource constraints.
Returns an optimized list of module names that satisfy the constraints.

**Complexity:** 16

### `calculate_score(module)`

**Complexity:** 3

## Keywords

`resource, module, modules, name, profile, resource_constraints, module_names, usage, path, get_module, get, optimized_chain, exceeded_resources, active, resource_type, get_resource_profile, total_usage, items, score, current_usage`

