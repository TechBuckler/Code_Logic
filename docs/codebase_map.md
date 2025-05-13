# Codebase Structure Report

## Summary
- Total Python files: 187
- Total functions: 580
- Total classes: 92

## Resource Distribution
### CPU (77 files)
- `cleanup_files.py`
- `code_mapper.py`
- `decide_optimized.py`
- `enhanced_split\cpu\unified_ui_run_ui.py`
- `extract_functions_optimized.py`
- `file_splitter.py`
- `file_splitter_split\cpu\file_splitter_main.py`
- `improved_explorer.py`
- `ir_split\core\ir_model__get_return_value.py`
- `ir_split\memory\ir_model_extract_ir_from_source.py`
- `logic_tool.py`
- `optimizer_split\core\optimizer_find_redundant_conditions.py`
- `optimizer_split\core\optimizer_merge_similar_branches.py`
- `optimizer_split\memory\optimizer_evaluate_logic.py`
- `optimizer_split\memory\optimizer_extract_numeric_bounds.py`
- `optimizer_split\memory\optimizer_extract_thresholds.py`
- `optimizer_split\memory\optimizer_generate_lookup_table.py`
- `optimizer_split\memory\optimizer_simplify_conditions.py`
- `proof_split\core\proof_engine_parse_condition_to_z3.py`
- `proof_split\cpu\proof_engine_run_default_proof.py`
- `proof_split\memory\proof_engine_run_z3_proof.py`
- `resource_split\ui\unified_ui_run_ui.py`
- `resource_split\unified_ui_merged.py`
- `resource_splitter.py`
- `run_app.py`
- `run_complete_system.py`
- `run_explorer.py`
- `run_hierarchical.py`
- `run_new_architecture.py`
- `runtime_opt_split\cpu\runtime_optimization_integrate_with_pipeline.py`
- `runtime_split\core\runtime_utils_condition.py`
- `runtime_split\core\runtime_utils_mine_patterns_from_directory.py`
- `runtime_split\core\runtime_utils_start_runtime_optimization.py`
- `runtime_split\core\runtime_utils_stop_runtime_optimization.py`
- `runtime_split\cpu\runtime_utils_optimize.py`
- `runtime_split\cpu\runtime_utils_optimize_file.py`
- `runtime_split\cpu\runtime_utils_register_runtime_modules.py`
- `safe_runner.py`
- `scan_codebase.py`
- `scan_files.py`
- `smart_splitter.py`
- `split_files\unified_ui_run_ui.py`
- `src\ai_suggester.py`
- `src\ast_explorer.py`
- `src\background_system.py`
- `src\bootstrap.py`
- `src\core\hierarchical_core.py`
- `src\core\hierarchical_module.py`
- `src\core\simple_hierarchical_core.py`
- `src\core\state_manager.py`
- `src\core\unified_core.py`
- `src\exporter.py`
- `src\exporter_optimized.py`
- `src\file_utils.py`
- `src\imports.py`
- `src\ir_model.py`
- `src\module_system.py`
- `src\modules\ast_parser_module.py`
- `src\modules\exporter_module.py`
- `src\modules\hierarchical\ast_parser_module.py`
- `src\modules\hierarchical\ir_generator_module.py`
- `src\modules\hierarchical\optimization_core_module.py`
- `src\modules\hierarchical\optimizer_module.py`
- `src\modules\hierarchical\proof_engine_module.py`
- `src\modules\ir_generator_module.py`
- `src\modules\module_explorer_module.py`
- `src\modules\optimizer_module.py`
- `src\modules\project_organizer_module.py`
- `src\modules\proof_engine_module.py`
- `src\optimizer.py`
- `src\proof_engine.py`
- `src\runtime_optimization.py`
- `src\runtime_utils.py`
- `src\starter_pipeline.py`
- `src\unified_ui.py`
- `src\utils.py`
- `src_new\core\hierarchical_core.py`

### MEMORY (2 files)
- `src\ui_renderers.py`
- `src\ui_renderers_part3.py`

### GPU (1 files)
- `src\modules\optimization_testbed_module.py`

### UI (11 files)
- `src\core\ui_components.py`
- `src\demo_hierarchical.py`
- `src\graph_builder.py`
- `src\hierarchical_app.py`
- `src\hierarchical_main.py`
- `src\modules\graph_builder_module.py`
- `src\modules\hierarchical\analysis_core_module.py`
- `src\new_main.py`
- `src\new_unified_ui.py`
- `src\ui_renderers_part2.py`
- `src\ui_utils.py`

### CORE (96 files)
- `cleanup_final.py`
- `enhanced_split\cpu\__init__.py`
- `enhanced_split\cpu\unified_ui_background_optimization.py`
- `enhanced_split\cpu\unified_ui_cleanup.py`
- `enhanced_split\cpu\unified_ui_initialize_system.py`
- `enhanced_split\unified_ui_merged.py`
- `file_splitter_split\cpu\__init__.py`
- `file_splitter_split\cpu\cpu_module.py`
- `file_splitter_split\cpu\file_splitter_merge_compressed_files.py`
- `file_splitter_split\cpu\file_splitter_merge_files.py`
- `file_splitter_split\cpu\file_splitter_split_by_bytes.py`
- `file_splitter_split\cpu\file_splitter_split_by_lines.py`
- `file_splitter_split\cpu\file_splitter_split_by_python_classes.py`
- `file_splitter_split\cpu\file_splitter_split_by_python_functions.py`
- `file_splitter_split\cpu\file_splitter_split_with_compression.py`
- `ir_split\core\__init__.py`
- `ir_split\core\ir_model__extract_if_conditions.py`
- `ir_split\cpu\__init__.py`
- `ir_split\cpu\ir_model_get_ir_model.py`
- `ir_split\memory\__init__.py`
- `optimization_split\core\__init__.py`
- `optimization_split\core\optimization_testbed_module___init__.py`
- `optimization_split\core\optimization_testbed_module_initialize.py`
- `optimization_split\cpu\__init__.py`
- `optimization_split\cpu\optimization_testbed_module_analyze_code.py`
- `optimization_split\cpu\optimization_testbed_module_benchmark_code.py`
- `optimization_split\cpu\optimization_testbed_module_can_process.py`
- `optimization_split\cpu\optimization_testbed_module_optimize_code.py`
- `optimization_split\cpu\optimization_testbed_module_optimize_for_profile.py`
- `optimization_split\cpu\optimization_testbed_module_process.py`
- `optimization_split\gpu\__init__.py`
- `optimization_split\gpu\optimization_testbed_module__analyze_function.py`
- `optimization_split\gpu\optimization_testbed_module_visit_FunctionDef.py`
- `optimization_split\memory\__init__.py`
- `optimization_split\memory\optimization_testbed_module_visualize_optimization.py`
- `optimization_split\optimization_testbed_module_merged.py`
- `optimization_split\ui\__init__.py`
- `optimization_split\ui\optimization_testbed_module_visit_Call.py`
- `optimization_split\ui\optimization_testbed_module_visit_For.py`
- `optimizer_split\core\__init__.py`
- `optimizer_split\cpu\__init__.py`
- `optimizer_split\cpu\optimizer_optimize_logic.py`
- `optimizer_split\memory\__init__.py`
- `proof_split\core\__init__.py`
- `proof_split\cpu\__init__.py`
- `proof_split\cpu\proof_engine_output.py`
- `proof_split\memory\__init__.py`
- `proof_split\ui\__init__.py`
- `proof_split\ui\proof_engine_build_output_function.py`
- `resource_split\core\unified_ui_background_optimization.py`
- `resource_split\core\unified_ui_cleanup.py`
- `resource_split\runtime\unified_ui_initialize_system.py`
- `resource_split\runtime\unified_ui_run_ui.py`
- `resource_split\ui\unified_ui_initialize_system.py`
- `run_bootstrap.py`
- `run_new_app.py`
- `runtime_opt_split\cpu\__init__.py`
- `runtime_opt_split\cpu\runtime_optimization___init__.py`
- `runtime_opt_split\cpu\runtime_optimization_get_stats.py`
- `runtime_opt_split\cpu\runtime_optimization_initialize.py`
- `runtime_opt_split\cpu\runtime_optimization_optimize_function.py`
- `runtime_opt_split\cpu\runtime_optimization_optimize_module.py`
- `runtime_opt_split\cpu\runtime_optimization_start.py`
- `runtime_opt_split\cpu\runtime_optimization_stop.py`
- `runtime_opt_split\memory\__init__.py`
- `runtime_opt_split\memory\runtime_optimization__background_loop.py`
- `runtime_split\core\__init__.py`
- `runtime_split\core\runtime_utils___init__.py`
- `runtime_split\core\runtime_utils__extract_patterns.py`
- `runtime_split\core\runtime_utils__get_node_type.py`
- `runtime_split\core\runtime_utils__hash_function.py`
- `runtime_split\core\runtime_utils__serialize_condition.py`
- `runtime_split\core\runtime_utils_analyze_directory.py`
- `runtime_split\core\runtime_utils_analyze_file.py`
- `runtime_split\core\runtime_utils_load_patterns.py`
- `runtime_split\core\runtime_utils_start.py`
- `runtime_split\core\runtime_utils_stop.py`
- `runtime_split\core\runtime_utils_visit_If.py`
- `runtime_split\cpu\__init__.py`
- `runtime_split\cpu\runtime_utils__monitor_loop.py`
- `runtime_split\cpu\runtime_utils__optimize_function.py`
- `runtime_split\cpu\runtime_utils_inject_tokens.py`
- `runtime_split\cpu\runtime_utils_process.py`
- `runtime_split\cpu\runtime_utils_register_function.py`
- `runtime_split\cpu\runtime_utils_visit_FunctionDef.py`
- `runtime_split\cpu\runtime_utils_wrapper.py`
- `runtime_split\gpu\__init__.py`
- `runtime_split\gpu\runtime_utils__check_gpu.py`
- `runtime_split\gpu\runtime_utils__is_gpu_candidate.py`
- `runtime_split\gpu\runtime_utils_route.py`
- `runtime_split\memory\__init__.py`
- `runtime_split\memory\runtime_utils_save_patterns.py`
- `safe_eval_optimized.py`
- `split_files\unified_ui_initialize_system.py`
- `src\__init__.py`
- `src\modules\__init__.py`

## File Details

### `cleanup_files.py`
**Description**: Cleanup script to remove redundant documentation files from the Logic Tool project.
**Functions**:
- `main` (CPU)

### `cleanup_final.py`
**Description**: Final cleanup script to remove unnecessary files and combine duplicates.
**Dependencies**: `shutil`

### `code_mapper.py`
**Description**: Code Mapper Module  This module provides tools for analyzing and mapping the codebase structure, dependencies, and resource usage patterns.
**Dependencies**: `argparse`, `importlib`, `inspect`, `pathlib`, `resource_splitter`, `src`
**Classes**:
- `ClassVisitor` (extends ast.NodeVisitor)
- `FunctionCallVisitor` (extends ast.NodeVisitor)
- `FunctionVisitor` (extends ast.NodeVisitor)
- `ImportVisitor` (extends ast.NodeVisitor)
**Functions**:
- `ClassVisitor.__init__` (CORE)
- `ClassVisitor.set_source` (CPU)
- `ClassVisitor.visit_ClassDef` (CPU)
- `FunctionCallVisitor.__init__` (CORE)
- `FunctionCallVisitor.visit_Call` (CPU)
- `FunctionVisitor.__init__` (CORE)
- `FunctionVisitor.set_source` (CPU)
- `FunctionVisitor.visit_ClassDef` (CPU)
- `FunctionVisitor.visit_FunctionDef` (CPU)
- `ImportVisitor.__init__` (CORE)
- `ImportVisitor.visit_Import` (CPU)
- `ImportVisitor.visit_ImportFrom` (CPU)
- `analyze_file` (CPU)
- `analyze_resource_focus` (CPU)
- `analyze_resource_profile` (GPU)
- `find_python_files` (CPU)
- `generate_codebase_report` (CPU)
- `main` (NETWORK)
- `map_codebase` (GPU)
- `split_codebase` (CPU)

### `decide_optimized.py`
**Functions**:
- `decide` (CPU)

### `enhanced_split\cpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `enhanced_split\cpu\unified_ui_background_optimization.py` (Error: Syntax error: unexpected indent (<unknown>, line 34))

### `enhanced_split\cpu\unified_ui_cleanup.py` (Error: Syntax error: unexpected indent (<unknown>, line 34))

### `enhanced_split\cpu\unified_ui_initialize_system.py`
**Dependencies**: `atexit`, `base64`, `io`, `matplotlib`, `numpy`, `src`, `streamlit`
**Functions**:
- `initialize_system` (CORE)

### `enhanced_split\cpu\unified_ui_run_ui.py`
**Dependencies**: `atexit`, `base64`, `io`, `matplotlib`, `numpy`, `src`, `streamlit`
**Functions**:
- `background_optimization` (CPU)
- `cleanup` (CPU)
- `run_ui` (UI)

### `enhanced_split\unified_ui_merged.py` (Error: Syntax error: unexpected indent (<unknown>, line 66))

### `extract_functions_optimized.py`
**Functions**:
- `extract_functions` (CPU)

### `file_splitter.py`
**Description**: File Splitter and Merger Utility  This module provides utilities for splitting and merging files using various methods: - Line-based splitting - Byte-based splitting - Token-based splitting (for Python code) - Logical block splitting (for Python code) - Compression-based splitting.
**Dependencies**: `base64`, `io`, `tokenize`, `zlib`
**Classes**:
- `FileSplitter`
**Functions**:
- `FileSplitter.merge_compressed_files` (CPU)
- `FileSplitter.merge_files` (CPU)
- `FileSplitter.split_by_bytes` (CPU)
- `FileSplitter.split_by_lines` (CPU)
- `FileSplitter.split_by_python_classes` (CPU)
- `FileSplitter.split_by_python_functions` (CPU)
- `FileSplitter.split_with_compression` (CPU)
- `main` (CPU)

### `file_splitter_split\cpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `file_splitter_split\cpu\cpu_module.py`
**Dependencies**: `src`
**Classes**:
- `CpuModule` (extends Module)
**Functions**:
- `CpuModule.__init__` (CORE)

### `file_splitter_split\cpu\file_splitter_main.py`
**Dependencies**: `base64`, `io`, `tokenize`, `zlib`
**Functions**:
- `main` (CPU)

### `file_splitter_split\cpu\file_splitter_merge_compressed_files.py` (Error: Syntax error: unexpected indent (<unknown>, line 13))

### `file_splitter_split\cpu\file_splitter_merge_files.py` (Error: Syntax error: unexpected indent (<unknown>, line 13))

### `file_splitter_split\cpu\file_splitter_split_by_bytes.py` (Error: Syntax error: unexpected indent (<unknown>, line 13))

### `file_splitter_split\cpu\file_splitter_split_by_lines.py` (Error: Syntax error: unexpected indent (<unknown>, line 13))

### `file_splitter_split\cpu\file_splitter_split_by_python_classes.py` (Error: Syntax error: unexpected indent (<unknown>, line 13))

### `file_splitter_split\cpu\file_splitter_split_by_python_functions.py` (Error: Syntax error: unexpected indent (<unknown>, line 13))

### `file_splitter_split\cpu\file_splitter_split_with_compression.py` (Error: Syntax error: unexpected indent (<unknown>, line 13))

### `improved_explorer.py`
**Description**: Improved Module Explorer Script  This script provides a cleaner view of all modules in the project.
**Dependencies**: `pprint`
**Functions**:
- `explore_modules` (CPU)

### `ir_split\core\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `ir_split\core\ir_model__extract_if_conditions.py` (Error: Syntax error: '{' was never closed (<unknown>, line 48))

### `ir_split\core\ir_model__get_return_value.py`
**Dependencies**: `asttokens`
**Functions**:
- `_get_return_value` (CPU)

### `ir_split\cpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `ir_split\cpu\ir_model_get_ir_model.py` (Error: Syntax error: '[' was never closed (<unknown>, line 18))

### `ir_split\memory\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `ir_split\memory\ir_model_extract_ir_from_source.py`
**Dependencies**: `asttokens`, `core`
**Functions**:
- `extract_ir_from_source` (CPU)

### `logic_tool.py`
**Dependencies**: `argparse`, `importlib`, `src`
**Functions**:
- `main` (UI)
- `mine_task` (CPU)
- `optimize_task` (CPU)

### `optimization_split\core\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `optimization_split\core\optimization_testbed_module___init__.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\core\optimization_testbed_module_initialize.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\cpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `optimization_split\cpu\optimization_testbed_module_analyze_code.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\cpu\optimization_testbed_module_benchmark_code.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\cpu\optimization_testbed_module_can_process.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\cpu\optimization_testbed_module_optimize_code.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\cpu\optimization_testbed_module_optimize_for_profile.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\cpu\optimization_testbed_module_process.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\gpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `optimization_split\gpu\optimization_testbed_module__analyze_function.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\gpu\optimization_testbed_module_visit_FunctionDef.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\memory\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `optimization_split\memory\optimization_testbed_module_visualize_optimization.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\optimization_testbed_module_merged.py` (Error: Syntax error: unexpected indent (<unknown>, line 52))

### `optimization_split\ui\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `optimization_split\ui\optimization_testbed_module_visit_Call.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimization_split\ui\optimization_testbed_module_visit_For.py` (Error: Syntax error: unexpected indent (<unknown>, line 27))

### `optimizer_split\core\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `optimizer_split\core\optimizer_find_redundant_conditions.py`
**Dependencies**: `src`, `sympy`
**Functions**:
- `find_redundant_conditions` (CPU)

### `optimizer_split\core\optimizer_merge_similar_branches.py`
**Dependencies**: `src`, `sympy`
**Functions**:
- `merge_similar_branches` (CPU)

### `optimizer_split\cpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `optimizer_split\cpu\optimizer_optimize_logic.py` (Error: Syntax error: '{' was never closed (<unknown>, line 36))

### `optimizer_split\memory\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `optimizer_split\memory\optimizer_evaluate_logic.py`
**Dependencies**: `src`, `sympy`
**Functions**:
- `evaluate_logic` (CPU)

### `optimizer_split\memory\optimizer_extract_numeric_bounds.py`
**Dependencies**: `src`, `sympy`
**Functions**:
- `extract_numeric_bounds` (CPU)

### `optimizer_split\memory\optimizer_extract_thresholds.py`
**Dependencies**: `src`, `sympy`
**Functions**:
- `extract_thresholds` (CPU)

### `optimizer_split\memory\optimizer_generate_lookup_table.py`
**Dependencies**: `src`, `sympy`
**Functions**:
- `generate_lookup_table` (CPU)

### `optimizer_split\memory\optimizer_simplify_conditions.py`
**Dependencies**: `src`, `sympy`
**Functions**:
- `simplify_conditions` (CPU)

### `proof_split\core\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `proof_split\core\proof_engine_parse_condition_to_z3.py`
**Dependencies**: `z3`
**Functions**:
- `parse_condition_to_z3` (CPU)

### `proof_split\cpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `proof_split\cpu\proof_engine_output.py` (Error: Syntax error: unexpected indent (<unknown>, line 6))

### `proof_split\cpu\proof_engine_run_default_proof.py`
**Dependencies**: `z3`
**Functions**:
- `output` (CPU)
- `run_default_proof` (CPU)

### `proof_split\memory\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `proof_split\memory\proof_engine_run_z3_proof.py`
**Dependencies**: `core`, `cpu`, `ui`, `z3`
**Functions**:
- `build_output_function` (UI)
- `run_z3_proof` (CPU)

### `proof_split\ui\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `proof_split\ui\proof_engine_build_output_function.py` (Error: Syntax error: unexpected indent (<unknown>, line 7))

### `resource_split\core\unified_ui_background_optimization.py` (Error: Syntax error: unexpected indent (<unknown>, line 1))

### `resource_split\core\unified_ui_cleanup.py` (Error: Syntax error: unexpected indent (<unknown>, line 1))

### `resource_split\runtime\unified_ui_initialize_system.py`
**Dependencies**: `src`, `streamlit`
**Functions**:
- `initialize_system` (CORE)

### `resource_split\runtime\unified_ui_run_ui.py`

### `resource_split\ui\unified_ui_initialize_system.py`
**Dependencies**: `src`
**Functions**:
- `initialize_system` (CORE)

### `resource_split\ui\unified_ui_run_ui.py`
**Dependencies**: `atexit`, `base64`, `io`, `matplotlib`, `numpy`, `src`
**Functions**:
- `background_optimization` (CPU)
- `cleanup` (CPU)
- `run_ui` (UI)

### `resource_split\unified_ui_merged.py`
**Dependencies**: `atexit`, `base64`, `io`, `matplotlib`, `numpy`, `src`
**Functions**:
- `background_optimization` (CPU)
- `cleanup` (CPU)
- `initialize_system` (UI)
- `run_ui` (GPU)

### `resource_splitter.py`
**Description**: Resource-Oriented File Splitter  This script splits Python files into resource-oriented components and organizes them in a logical directory structure.
**Dependencies**: `importlib`, `pathlib`, `src`
**Functions**:
- `analyze_resource_focus` (GPU)
- `analyze_resource_profile` (GPU)
- `categorize_by_resource` (GPU)
- `extract_functions` (CPU)
- `get_dependency_order` (CPU)
- `main` (CPU)
- `merge_from_manifest` (CPU)
- `split_file_by_resource` (GPU)
- `visit` (CPU)

### `run_app.py`
**Description**: Run the Logic Tool UI with safe execution.
**Dependencies**: `psutil`, `streamlit`, `subprocess`
**Functions**:
- `kill_process_tree` (CPU)
- `main` (UI)

### `run_bootstrap.py`
**Description**: Run the bootstrap process to generate the new hierarchical architecture.
**Dependencies**: `src`

### `run_complete_system.py`
**Description**: Run the Complete Logic Tool System with Hierarchical Architecture  This script runs the complete Logic Tool system with the hierarchical architecture, including analysis, optimization, and verification modules.
**Dependencies**: `asttokens`, `matplotlib`, `streamlit`, `subprocess`, `sympy`, `z3`
**Functions**:
- `check_dependencies` (UI)
- `run_streamlit_app` (CPU)

### `run_explorer.py`
**Description**: Module Explorer Script  This script runs the module explorer to list all modules in the project.
**Dependencies**: `src`
**Functions**:
- `main` (CPU)

### `run_hierarchical.py`
**Description**: Run the Logic Tool with the new hierarchical architecture.
**Dependencies**: `subprocess`
**Functions**:
- `run_streamlit_app` (CPU)

### `run_new_app.py`
**Description**: Run the new Logic Tool UI with improved architecture.
**Dependencies**: `src`

### `run_new_architecture.py`
**Description**: Run the new hierarchical architecture for the Logic Tool.
**Dependencies**: `subprocess`
**Functions**:
- `run_streamlit_app` (CPU)

### `runtime_opt_split\cpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `runtime_opt_split\cpu\runtime_optimization___init__.py` (Error: Syntax error: unexpected indent (<unknown>, line 11))

### `runtime_opt_split\cpu\runtime_optimization_get_stats.py` (Error: Syntax error: unexpected indent (<unknown>, line 11))

### `runtime_opt_split\cpu\runtime_optimization_initialize.py`
**Dependencies**: `src`, `threading`
**Functions**:
- `initialize` (CORE)

### `runtime_opt_split\cpu\runtime_optimization_integrate_with_pipeline.py`
**Dependencies**: `src`, `threading`
**Functions**:
- `integrate_with_pipeline` (CPU)

### `runtime_opt_split\cpu\runtime_optimization_optimize_function.py` (Error: Syntax error: unexpected indent (<unknown>, line 11))

### `runtime_opt_split\cpu\runtime_optimization_optimize_module.py` (Error: Syntax error: unexpected indent (<unknown>, line 11))

### `runtime_opt_split\cpu\runtime_optimization_start.py` (Error: Syntax error: unexpected indent (<unknown>, line 11))

### `runtime_opt_split\cpu\runtime_optimization_stop.py` (Error: Syntax error: unexpected indent (<unknown>, line 11))

### `runtime_opt_split\memory\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `runtime_opt_split\memory\runtime_optimization__background_loop.py` (Error: Syntax error: unexpected indent (<unknown>, line 11))

### `runtime_split\core\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `runtime_split\core\runtime_utils___init__.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils__extract_patterns.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils__get_node_type.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils__hash_function.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils__serialize_condition.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils_analyze_directory.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils_analyze_file.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils_condition.py`
**Dependencies**: `hashlib`, `inspect`, `src`, `threading`
**Functions**:
- `condition` (CPU)

### `runtime_split\core\runtime_utils_load_patterns.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils_mine_patterns_from_directory.py`
**Dependencies**: `hashlib`, `inspect`, `src`, `threading`
**Functions**:
- `mine_patterns_from_directory` (CPU)

### `runtime_split\core\runtime_utils_start.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils_start_runtime_optimization.py`
**Dependencies**: `hashlib`, `inspect`, `src`, `threading`
**Functions**:
- `start_runtime_optimization` (CPU)

### `runtime_split\core\runtime_utils_stop.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\core\runtime_utils_stop_runtime_optimization.py`
**Dependencies**: `hashlib`, `inspect`, `src`, `threading`
**Functions**:
- `stop_runtime_optimization` (CPU)

### `runtime_split\core\runtime_utils_visit_If.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\cpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `runtime_split\cpu\runtime_utils__monitor_loop.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\cpu\runtime_utils__optimize_function.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\cpu\runtime_utils_inject_tokens.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\cpu\runtime_utils_optimize.py`
**Dependencies**: `hashlib`, `inspect`, `src`, `threading`
**Functions**:
- `optimize` (CPU)
- `wrapper` (CPU)

### `runtime_split\cpu\runtime_utils_optimize_file.py`
**Dependencies**: `hashlib`, `inspect`, `src`, `threading`
**Functions**:
- `optimize_file` (CPU)

### `runtime_split\cpu\runtime_utils_process.py` (Error: Syntax error: unexpected indent (<unknown>, line 15))

### `runtime_split\cpu\runtime_utils_register_function.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\cpu\runtime_utils_register_runtime_modules.py`
**Dependencies**: `core`, `hashlib`, `inspect`, `src`, `threading`
**Classes**:
- `JitRoutingModule` (extends Module)
- `PatternMiningModule` (extends Module)
- `TokenInjectionModule` (extends Module)
**Functions**:
- `JitRoutingModule.__init__` (CORE)
- `JitRoutingModule.process` (CPU)
- `PatternMiningModule.__init__` (CORE)
- `PatternMiningModule.process` (CPU)
- `TokenInjectionModule.__init__` (CORE)
- `TokenInjectionModule.process` (CPU)
- `register_runtime_modules` (CPU)

### `runtime_split\cpu\runtime_utils_visit_FunctionDef.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\cpu\runtime_utils_wrapper.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\gpu\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `runtime_split\gpu\runtime_utils__check_gpu.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\gpu\runtime_utils__is_gpu_candidate.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\gpu\runtime_utils_route.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `runtime_split\memory\__init__.py` (Error: Syntax error: invalid syntax (<unknown>, line 2))

### `runtime_split\memory\runtime_utils_save_patterns.py` (Error: Syntax error: unexpected indent (<unknown>, line 14))

### `safe_eval_optimized.py` (Error: Syntax error: expected an indented block after function definition on line 1 (<unknown>, line 2))

### `safe_runner.py`
**Description**: Safe Run Wrapper for Logic Tool  This script provides a robust wrapper around the Logic Tool CLI commands, ensuring proper process termination and error handling.
**Dependencies**: `psutil`, `subprocess`
**Functions**:
- `kill_process_tree` (CPU)
- `main` (UI)

### `scan_codebase.py`
**Description**: Codebase Scanner  This script scans the entire codebase and provides a comprehensive report of the directory structure, file types, and code organization.
**Classes**:
- `CodebaseScanner`
**Functions**:
- `CodebaseScanner.__init__` (CORE)
- `CodebaseScanner._format_size` (CPU)
- `CodebaseScanner._scan_directory` (CPU)
- `CodebaseScanner.analyze_code_organization` (CORE)
- `CodebaseScanner.export_to_json` (CPU)
- `CodebaseScanner.find_files_by_extension` (CPU)
- `CodebaseScanner.print_structure` (CPU)
- `CodebaseScanner.print_summary` (CPU)
- `CodebaseScanner.scan` (MEMORY)
- `CodebaseScanner.search_in_structure` (CPU)
- `main` (CPU)

### `scan_files.py`
**Description**: Simple File Scanner  This script scans the codebase and prints each file as it's found, without storing everything in memory.
**Functions**:
- `main` (CPU)
- `scan_directory` (MEMORY)

### `smart_splitter.py`
**Description**: Smart File Splitter  This script provides enhanced file splitting capabilities with a focus on: 1.
**Dependencies**: `file_splitter`, `shutil`
**Classes**:
- `SmartSplitter`
**Functions**:
- `SmartSplitter.__init__` (CORE)
- `SmartSplitter._analyze_dependencies` (CPU)
- `SmartSplitter._categorize_by_resource` (GPU)
- `SmartSplitter._get_dependency_order` (CPU)
- `SmartSplitter._split_by_functions` (CPU)
- `SmartSplitter._write_resource_files` (CPU)
- `SmartSplitter.merge_from_manifest` (CPU)
- `SmartSplitter.split_file_by_resource` (CPU)
- `SmartSplitter.visit` (CPU)
- `main` (CPU)

### `split_files\unified_ui_initialize_system.py`
**Dependencies**: `src`, `streamlit`
**Functions**:
- `initialize_system` (CORE)

### `split_files\unified_ui_run_ui.py`
**Dependencies**: `atexit`, `base64`, `io`, `matplotlib`, `numpy`, `src`, `streamlit`
**Functions**:
- `background_optimization` (CPU)
- `cleanup` (CPU)
- `run_ui` (UI)

### `src\__init__.py`

### `src\ai_suggester.py`
**Dependencies**: `openai`, `subprocess`
**Functions**:
- `ask_llama` (CPU)
- `ask_openai` (CPU)
- `compare_ai` (CPU)

### `src\ast_explorer.py`
**Classes**:
- `FunctionVisitor` (extends ast.NodeVisitor)
**Functions**:
- `FunctionVisitor.visit_FunctionDef` (CPU)
- `extract_functions` (CPU)

### `src\background_system.py`
**Dependencies**: `psutil`, `queue`, `threading`
**Classes**:
- `BackgroundSystem`
**Functions**:
- `BackgroundSystem.__init__` (CORE)
- `BackgroundSystem._is_idle` (CPU)
- `BackgroundSystem._worker` (CPU)
- `BackgroundSystem.add_task` (CPU)
- `BackgroundSystem.get_log` (CPU)
- `BackgroundSystem.start` (CPU)
- `BackgroundSystem.stop` (CPU)

### `src\bootstrap.py`
**Description**: Bootstrap - Self-generating architecture system  This module analyzes the existing codebase and transforms it into the new hierarchical architecture.
**Dependencies**: `importlib`, `shutil`, `src`
**Classes**:
- `BootstrapModule` (extends HierarchicalModule)
**Functions**:
- `BootstrapModule.__init__` (CORE)
- `BootstrapModule._generate_entry_point` (UI)
- `BootstrapModule._generate_module_file` (UI)
- `BootstrapModule._generate_module_hierarchy` (UI)
- `BootstrapModule._generate_registry` (UI)
- `BootstrapModule._identify_module_relationships` (CPU)
- `BootstrapModule._on_analysis_complete` (CPU)
- `BootstrapModule._on_generation_complete` (CPU)
- `BootstrapModule._on_transformation_complete` (CPU)
- `BootstrapModule._transform_module` (UI)
- `BootstrapModule.analyze_codebase` (CPU)
- `BootstrapModule.generate_architecture` (UI)
- `BootstrapModule.initialize` (CORE)
- `BootstrapModule.process` (CPU)
- `BootstrapModule.transform_codebase` (CPU)
- `run_bootstrap` (CORE)

### `src\core\hierarchical_core.py`
**Description**: Hierarchical Core - Foundation for the self-bootstrapping architecture  This module provides the core components for a hierarchical, modular system that can dynamically organize, load, and manage modules at multiple levels of abstraction.
**Dependencies**: `abc`, `asyncio`, `concurrent`, `enum`, `importlib`, `inspect`, `threading`, `uuid`, `weakref`
**Classes**:
- `CodeAnalyzer`
- `Event`
- `EventBus`
- `EventPriority` (extends Enum)
- `FileSplitter`
- `HierarchicalModule` (extends ABC)
- `ModuleGenerator`
- `ModuleLoader`
- `ModuleRegistry`
- `ModuleStatus` (extends Enum)
- `StateChangeEvent` (extends Event)
- `StateStore`
**Functions**:
- `CodeAnalyzer.analyze_directory` (CPU)
- `CodeAnalyzer.analyze_file` (CPU)
- `Event.__init__` (UI)
- `Event.__str__` (CPU)
- `EventBus.__init__` (CORE)
- `EventBus.publish` (CPU)
- `EventBus.subscribe` (CPU)
- `EventBus.unsubscribe` (CPU)
- `FileSplitter.split_by_class` (CPU)
- `FileSplitter.split_by_size` (CPU)
- `HierarchicalModule.__init__` (CORE)
- `HierarchicalModule.add_child` (CPU)
- `HierarchicalModule.get_child` (CPU)
- `HierarchicalModule.get_descendant` (CPU)
- `HierarchicalModule.get_full_id` (CPU)
- `HierarchicalModule.get_path` (CPU)
- `HierarchicalModule.initialize` (CORE)
- `HierarchicalModule.process` (CPU)
- `HierarchicalModule.remove_child` (CPU)
- `HierarchicalModule.shutdown` (CPU)
- `HierarchicalModule.to_dict` (CPU)
- `ModuleGenerator.generate_module_class` (CORE)
- `ModuleGenerator.generate_module_file` (CPU)
- `ModuleLoader._load_module_from_config` (CORE)
- `ModuleLoader.load_from_config` (CORE)
- `ModuleLoader.load_module_class` (CPU)
- `ModuleLoader.load_module_instance` (CPU)
- `ModuleRegistry.__init__` (MEMORY)
- `ModuleRegistry._initialize_module` (CORE)
- `ModuleRegistry._remove_from_cache` (MEMORY)
- `ModuleRegistry._update_cache` (MEMORY)
- `ModuleRegistry.get_module` (MEMORY)
- `ModuleRegistry.initialize_all` (CORE)
- `ModuleRegistry.register_module` (MEMORY)
- `ModuleRegistry.shutdown_all` (CPU)
- `ModuleRegistry.to_dict` (CPU)
- `ModuleRegistry.unregister_module` (MEMORY)
- `StateChangeEvent.__init__` (CORE)
- `StateStore.__init__` (CORE)
- `StateStore.get` (CPU)
- `StateStore.get_all` (CPU)
- `StateStore.set` (CPU)
- `StateStore.unwatch` (CPU)
- `StateStore.watch` (CPU)

### `src\core\hierarchical_module.py`
**Description**: Hierarchical Module System - Extends the base module system with hierarchical capabilities  This module provides a hierarchical extension to the base module system, allowing modules to be organized in a tree structure with parent-child relationships.
**Dependencies**: `src`
**Classes**:
- `HierarchicalModule` (extends Module)
- `ModuleHierarchy`
**Functions**:
- `HierarchicalModule.__init__` (CORE)
- `HierarchicalModule.add_child` (CPU)
- `HierarchicalModule.can_process` (CPU)
- `HierarchicalModule.find_module` (CPU)
- `HierarchicalModule.get_all_children` (CPU)
- `HierarchicalModule.get_child` (CPU)
- `HierarchicalModule.get_full_name` (CPU)
- `HierarchicalModule.get_path` (CPU)
- `HierarchicalModule.initialize` (CORE)
- `HierarchicalModule.process` (CPU)
- `HierarchicalModule.remove_child` (CPU)
- `HierarchicalModule.render_ui` (UI)
- `HierarchicalModule.shutdown` (CPU)
- `ModuleHierarchy.__init__` (CORE)
- `ModuleHierarchy.add_root_module` (CPU)
- `ModuleHierarchy.find_module` (CPU)
- `ModuleHierarchy.get_all_modules` (CPU)
- `ModuleHierarchy.get_root_module` (CPU)
- `ModuleHierarchy.initialize_all` (CORE)
- `ModuleHierarchy.remove_root_module` (CPU)
- `ModuleHierarchy.shutdown_all` (CPU)

### `src\core\simple_hierarchical_core.py`
**Description**: Simple Hierarchical Core - A lightweight foundation for hierarchical modules  This module provides a simplified hierarchical module system with event-based communication and state management.
**Dependencies**: `uuid`, `weakref`
**Classes**:
- `Event`
- `EventBus`
- `HierarchicalModule`
- `ModuleRegistry`
- `StateStore`
- `UIKeyManager`
**Functions**:
- `Event.__init__` (UI)
- `EventBus.__init__` (CORE)
- `EventBus.publish` (CPU)
- `EventBus.subscribe` (CPU)
- `EventBus.unsubscribe` (CPU)
- `HierarchicalModule.__init__` (CORE)
- `HierarchicalModule.add_child` (CPU)
- `HierarchicalModule.get_child` (CPU)
- `HierarchicalModule.get_full_id` (CPU)
- `HierarchicalModule.get_path` (CPU)
- `HierarchicalModule.initialize` (CORE)
- `HierarchicalModule.process` (CPU)
- `HierarchicalModule.remove_child` (CPU)
- `HierarchicalModule.shutdown` (CPU)
- `ModuleRegistry.__init__` (CORE)
- `ModuleRegistry.get_module` (CPU)
- `ModuleRegistry.initialize_all` (CORE)
- `ModuleRegistry.register_module` (CPU)
- `ModuleRegistry.shutdown_all` (CPU)
- `ModuleRegistry.unregister_module` (CPU)
- `StateStore.__init__` (CORE)
- `StateStore.get` (CPU)
- `StateStore.set` (CPU)
- `StateStore.unwatch` (CPU)
- `StateStore.watch` (CPU)
- `UIKeyManager.__new__` (CPU)
- `UIKeyManager.clear_keys` (CPU)
- `UIKeyManager.get_unique_key` (CPU)

### `src\core\state_manager.py`
**Description**: State Manager - Core component for managing shared state and event communication.
**Classes**:
- `EventBus`
- `SharedState`
- `StateManager`
**Functions**:
- `EventBus.__init__` (CORE)
- `EventBus.publish` (CPU)
- `EventBus.subscribe` (CPU)
- `EventBus.unsubscribe` (CPU)
- `SharedState.__init__` (CORE)
- `SharedState.clear` (CPU)
- `SharedState.get` (CPU)
- `SharedState.get_all` (CPU)
- `SharedState.set` (CPU)
- `SharedState.unwatch` (CPU)
- `SharedState.watch` (CPU)
- `StateManager.__new__` (UI)
- `StateManager.get_event_bus` (CPU)
- `StateManager.get_shared_state` (CPU)
- `StateManager.load_state` (CPU)
- `StateManager.register_ui_key` (UI)
- `StateManager.release_ui_key` (UI)
- `StateManager.save_state` (CPU)

### `src\core\ui_components.py`
**Description**: UI Components - Core components for the unified UI.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `ContentComponent`
- `NavigationComponent`
- `ResultsComponent`
- `UIManager`
**Functions**:
- `ContentComponent.__init__` (UI)
- `ContentComponent.register_renderer` (UI)
- `ContentComponent.render_content` (UI)
- `NavigationComponent.__init__` (CORE)
- `NavigationComponent.render_sidebar` (UI)
- `ResultsComponent.__init__` (UI)
- `ResultsComponent.register_renderer` (UI)
- `ResultsComponent.render_results` (UI)
- `UIManager.__new__` (CPU)
- `UIManager.register_results_renderer` (UI)
- `UIManager.register_tool` (UI)
- `UIManager.render` (UI)

### `src\core\unified_core.py`
**Description**: Unified Core Architecture  This module provides a unified core architecture that integrates all existing modules while maintaining a clean hierarchical structure.
**Dependencies**: `importlib`, `src`
**Classes**:
- `UnifiedCore`
**Functions**:
- `UnifiedCore.__init__` (CORE)
- `UnifiedCore._build_hierarchy` (UI)
- `UnifiedCore._connect_modules` (UI)
- `UnifiedCore._register_modules` (UI)
- `UnifiedCore.get_module` (CPU)
- `UnifiedCore.get_modules_in_category` (CPU)
- `UnifiedCore.handle_event` (CPU)
- `UnifiedCore.initialize` (UI)
- `UnifiedCore.process_with_module` (CPU)
- `UnifiedCore.register_event_handler` (CPU)
- `UnifiedCore.shutdown` (CPU)

### `src\demo_hierarchical.py`
**Description**: Demo of the Hierarchical Module System  This script demonstrates the hierarchical module system by creating a simple hierarchy of modules and showing how they interact.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `AnalysisModule` (extends HierarchicalModule)
- `OptimizationModule` (extends HierarchicalModule)
- `ParserModule` (extends HierarchicalModule)
- `PerformanceTestModule` (extends HierarchicalModule)
**Functions**:
- `AnalysisModule.__init__` (CORE)
- `AnalysisModule.render_ui` (UI)
- `OptimizationModule.__init__` (CORE)
- `OptimizationModule.handle_parsed_code` (CPU)
- `OptimizationModule.render_ui` (UI)
- `ParserModule.__init__` (CORE)
- `ParserModule.render_ui` (UI)
- `PerformanceTestModule.__init__` (CORE)
- `PerformanceTestModule.render_ui` (UI)
- `log_event` (CPU)
- `main` (UI)

### `src\exporter.py`
**Dependencies**: `jinja2`
**Functions**:
- `export_to_python` (CPU)

### `src\exporter_optimized.py`
**Dependencies**: `jinja2`, `runtime_optimization`
**Functions**:
- `export_to_python` (CPU)

### `src\file_utils.py`
**Description**: File Utilities for the Logic Tool  This module provides utility functions for working with files, including copying, transforming, and loading Python modules.
**Dependencies**: `importlib`, `shutil`
**Functions**:
- `copy_file` (CPU)
- `load_module_from_file` (CPU)
- `scan_directory_for_modules` (CPU)
- `transform_file` (CPU)

### `src\graph_builder.py`
**Dependencies**: `matplotlib`, `networkx`
**Functions**:
- `build_function_graph` (UI)

### `src\hierarchical_app.py`
**Description**: Hierarchical Logic Tool Application  This is the main entry point for the Logic Tool using the hierarchical module system.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `LogicToolApp` (extends HierarchicalModule)
**Functions**:
- `LogicToolApp.__init__` (CORE)
- `LogicToolApp.handle_navigation` (CPU)
- `LogicToolApp.load_core_modules` (CPU)
- `LogicToolApp.render_home` (UI)
- `LogicToolApp.render_sidebar` (UI)
- `LogicToolApp.render_ui` (UI)
- `log_event` (CPU)
- `main` (UI)

### `src\hierarchical_main.py`
**Description**: Hierarchical Logic Tool - Main Application  This is the main entry point for the Logic Tool using the hierarchical module architecture.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `LogicToolApp` (extends HierarchicalModule)
**Functions**:
- `LogicToolApp.__init__` (CORE)
- `LogicToolApp.handle_navigation` (CPU)
- `LogicToolApp.load_core_modules` (CPU)
- `LogicToolApp.log_event` (CPU)
- `LogicToolApp.render_home` (UI)
- `LogicToolApp.render_sidebar` (UI)
- `LogicToolApp.render_ui` (UI)
- `main` (UI)

### `src\imports.py`
**Description**: Centralized imports for the Logic Tool system.
**Dependencies**: `ast_explorer`, `background_system`, `exporter`, `graph_builder`, `importlib`, `inspect`, `ir_model`, `module_system`, `optimizer`, `proof_engine`, `src`
**Functions**:
- `decide` (CPU)
- `determine_notification` (CPU)
- `get_function_source` (CPU)
- `load_module_from_file` (CPU)

### `src\ir_model.py`
**Dependencies**: `asttokens`
**Functions**:
- `_extract_if_conditions` (CPU)
- `_get_return_value` (CPU)
- `extract_ir_from_source` (CPU)
- `get_ir_model` (CPU)

### `src\module_system.py`
**Classes**:
- `Module`
- `ModuleRegistry`
**Functions**:
- `Module.__init__` (GPU)
- `Module.can_process` (CPU)
- `Module.get_resource_profile` (CPU)
- `Module.initialize` (CORE)
- `Module.process` (CPU)
- `Module.set_resource_profile` (CPU)
- `Module.shutdown` (CPU)
- `ModuleRegistry.__init__` (GPU)
- `ModuleRegistry.calculate_score` (CPU)
- `ModuleRegistry.get_module` (CPU)
- `ModuleRegistry.get_modules_by_resource_type` (CPU)
- `ModuleRegistry.get_resource_constraints` (CPU)
- `ModuleRegistry.initialize_all` (CORE)
- `ModuleRegistry.optimize_module_chain` (CPU)
- `ModuleRegistry.process_chain` (CPU)
- `ModuleRegistry.register` (CPU)
- `ModuleRegistry.set_resource_constraints` (CPU)
- `ModuleRegistry.shutdown_all` (CPU)

### `src\modules\__init__.py`

### `src\modules\ast_parser_module.py`
**Dependencies**: `src`
**Classes**:
- `AstParserModule` (extends Module)
**Functions**:
- `AstParserModule.__init__` (CORE)
- `AstParserModule.can_process` (CPU)
- `AstParserModule.process` (CPU)

### `src\modules\exporter_module.py`
**Dependencies**: `src`
**Classes**:
- `ExporterModule` (extends Module)
**Functions**:
- `ExporterModule.__init__` (CORE)
- `ExporterModule.can_process` (CPU)
- `ExporterModule.process` (CPU)

### `src\modules\graph_builder_module.py`
**Dependencies**: `src`
**Classes**:
- `GraphBuilderModule` (extends Module)
**Functions**:
- `GraphBuilderModule.__init__` (UI)
- `GraphBuilderModule.can_process` (CPU)
- `GraphBuilderModule.process` (UI)

### `src\modules\hierarchical\analysis_core_module.py`
**Description**: Analysis Core Module - Hierarchical version  This module serves as the core for all analysis-related functionality, including code parsing, AST exploration, and logic analysis.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `AnalysisCoreModule` (extends HierarchicalModule)
**Functions**:
- `AnalysisCoreModule.__init__` (CORE)
- `AnalysisCoreModule.load_child_modules` (CPU)
- `AnalysisCoreModule.process` (CPU)
- `AnalysisCoreModule.render_code_input` (UI)
- `AnalysisCoreModule.render_results` (UI)
- `AnalysisCoreModule.render_ui` (UI)

### `src\modules\hierarchical\ast_parser_module.py`
**Description**: Hierarchical AST Parser Module  This module extends the base AST parser module with hierarchical capabilities.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `ASTParserModule` (extends HierarchicalModule)
**Functions**:
- `ASTParserModule.__init__` (CORE)
- `ASTParserModule.can_process` (CPU)
- `ASTParserModule.process` (CPU)
- `ASTParserModule.render_ui` (UI)

### `src\modules\hierarchical\ir_generator_module.py`
**Description**: Hierarchical IR Generator Module  This module extends the base IR generator module with hierarchical capabilities.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `IRGeneratorModule` (extends HierarchicalModule)
**Functions**:
- `IRGeneratorModule.__init__` (CORE)
- `IRGeneratorModule.can_process` (CPU)
- `IRGeneratorModule.handle_ast_parsing_complete` (CPU)
- `IRGeneratorModule.process` (CPU)
- `IRGeneratorModule.render_ui` (UI)

### `src\modules\hierarchical\optimization_core_module.py`
**Description**: Optimization Core Module - Hierarchical version  This module serves as the core for all optimization-related functionality, including logic optimization, formal verification, and performance analysis.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `OptimizationCoreModule` (extends HierarchicalModule)
**Functions**:
- `OptimizationCoreModule.__init__` (CORE)
- `OptimizationCoreModule.load_child_modules` (CPU)
- `OptimizationCoreModule.process` (CPU)
- `OptimizationCoreModule.render_results` (UI)
- `OptimizationCoreModule.render_ui` (UI)

### `src\modules\hierarchical\optimizer_module.py`
**Dependencies**: `src`, `streamlit`
**Classes**:
- `OptimizerModule` (extends HierarchicalModule)
**Functions**:
- `OptimizerModule.__init__` (CORE)
- `OptimizerModule.can_process` (CPU)
- `OptimizerModule.handle_ir_generation_complete` (CPU)
- `OptimizerModule.process` (CPU)
- `OptimizerModule.render_ui` (UI)

### `src\modules\hierarchical\proof_engine_module.py`
**Description**: Hierarchical Proof Engine Module  This module extends the base proof engine module with hierarchical capabilities.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `ProofEngineModule` (extends HierarchicalModule)
**Functions**:
- `ProofEngineModule.__init__` (CORE)
- `ProofEngineModule.can_process` (CPU)
- `ProofEngineModule.handle_ir_generation_complete` (CPU)
- `ProofEngineModule.process` (CPU)
- `ProofEngineModule.render_ui` (UI)

### `src\modules\ir_generator_module.py`
**Dependencies**: `src`
**Classes**:
- `IrGeneratorModule` (extends Module)
**Functions**:
- `IrGeneratorModule.__init__` (CORE)
- `IrGeneratorModule.can_process` (CPU)
- `IrGeneratorModule.process` (CPU)

### `src\modules\module_explorer_module.py`
**Description**: Module Explorer Module  This module allows exploring, editing, and running other modules in the system.
**Dependencies**: `importlib`, `inspect`, `pathlib`, `starter_pipeline`, `subprocess`
**Classes**:
- `ModuleExplorerModule`
**Functions**:
- `ModuleExplorerModule.__init__` (MEMORY)
- `ModuleExplorerModule._find_module_path` (CPU)
- `ModuleExplorerModule._find_project_root` (CPU)
- `ModuleExplorerModule._get_module_info` (CPU)
- `ModuleExplorerModule._import_module` (MEMORY)
- `ModuleExplorerModule.can_process` (CPU)
- `ModuleExplorerModule.edit_module` (UI)
- `ModuleExplorerModule.initialize` (CORE)
- `ModuleExplorerModule.list_modules` (CPU)
- `ModuleExplorerModule.process` (CPU)
- `ModuleExplorerModule.run_module` (UI)
- `ModuleExplorerModule.run_pipeline` (CPU)
- `ModuleExplorerModule.view_module` (UI)

### `src\modules\optimization_testbed_module.py`
**Description**: Optimization Testbed Module  This module provides a comprehensive testing environment for analyzing code and finding optimal tradeoffs between memory usage, CPU performance, GPU utilization, and other factors based on the target environment and use case.
**Dependencies**: `astunparse`, `base64`, `concurrent`, `importlib`, `inspect`, `io`, `matplotlib`, `numpy`, `psutil`, `threading`, `traceback`
**Classes**:
- `CodeOptimizer` (extends ast.NodeTransformer)
- `OptimizationTestbedModule`
**Functions**:
- `CodeOptimizer.__init__` (CORE)
- `CodeOptimizer.visit_Call` (CPU)
- `CodeOptimizer.visit_For` (CPU)
- `CodeOptimizer.visit_FunctionDef` (GPU)
- `OptimizationTestbedModule.__init__` (GPU)
- `OptimizationTestbedModule._analyze_function` (GPU)
- `OptimizationTestbedModule.analyze_code` (GPU)
- `OptimizationTestbedModule.benchmark_code` (MEMORY)
- `OptimizationTestbedModule.can_process` (CPU)
- `OptimizationTestbedModule.initialize` (CORE)
- `OptimizationTestbedModule.optimize_code` (GPU)
- `OptimizationTestbedModule.optimize_for_profile` (GPU)
- `OptimizationTestbedModule.process` (CPU)
- `OptimizationTestbedModule.visualize_optimization` (GPU)

### `src\modules\optimizer_module.py`
**Dependencies**: `src`
**Classes**:
- `OptimizerModule` (extends Module)
**Functions**:
- `OptimizerModule.__init__` (CORE)
- `OptimizerModule.can_process` (CPU)
- `OptimizerModule.process` (CPU)

### `src\modules\project_organizer_module.py`
**Description**: Project Organizer Module  This module handles project organization, file naming conventions, and project structure.
**Dependencies**: `pathlib`, `shutil`
**Classes**:
- `ProjectOrganizerModule`
**Functions**:
- `ProjectOrganizerModule.__init__` (CORE)
- `ProjectOrganizerModule._move_files` (CPU)
- `ProjectOrganizerModule._rename_files` (UI)
- `ProjectOrganizerModule._suggest_better_name` (CPU)
- `ProjectOrganizerModule.analyze_project` (CPU)
- `ProjectOrganizerModule.can_process` (CPU)
- `ProjectOrganizerModule.initialize` (MEMORY)
- `ProjectOrganizerModule.process` (CPU)
- `ProjectOrganizerModule.reorganize_project` (CPU)

### `src\modules\proof_engine_module.py`
**Dependencies**: `src`
**Classes**:
- `ProofEngineModule` (extends Module)
**Functions**:
- `ProofEngineModule.__init__` (CORE)
- `ProofEngineModule.can_process` (CPU)
- `ProofEngineModule.process` (CPU)

### `src\new_main.py`
**Description**: New Main Application - Entry point for the Logic Tool with hierarchical architecture  This module serves as the main entry point for the Logic Tool, using the new hierarchical architecture based on simple_hierarchical_core.
**Dependencies**: `src`, `streamlit`
**Classes**:
- `AnalysisCoreModule` (extends HierarchicalModule)
- `LogicToolApp` (extends HierarchicalModule)
- `OptimizationCoreModule` (extends HierarchicalModule)
- `ProjectCoreModule` (extends HierarchicalModule)
- `UICoreModule` (extends HierarchicalModule)
**Functions**:
- `AnalysisCoreModule.__init__` (CORE)
- `AnalysisCoreModule.analyze_code` (CPU)
- `AnalysisCoreModule.render` (UI)
- `LogicToolApp.__init__` (CORE)
- `LogicToolApp.handle_navigation` (CPU)
- `LogicToolApp.load_core_modules` (UI)
- `LogicToolApp.render` (UI)
- `LogicToolApp.render_home` (UI)
- `LogicToolApp.render_sidebar` (UI)
- `OptimizationCoreModule.__init__` (CORE)
- `OptimizationCoreModule.optimize_code` (CPU)
- `OptimizationCoreModule.render` (MEMORY)
- `ProjectCoreModule.__init__` (CORE)
- `ProjectCoreModule.create_project` (CPU)
- `ProjectCoreModule.open_project` (CPU)
- `ProjectCoreModule.render` (UI)
- `UICoreModule.__init__` (CORE)
- `UICoreModule.render` (UI)
- `main` (UI)

### `src\new_unified_ui.py`
**Description**: New Unified UI - Redesigned UI with improved architecture.
**Dependencies**: `importlib`, `src`, `streamlit`
**Functions**:
- `initialize_modules` (CORE)
- `initialize_session_state` (CORE)
- `register_ui_components` (UI)
- `render_code_analysis` (UI)
- `render_code_analysis_results` (UI)
- `run_ui` (UI)

### `src\optimizer.py`
**Dependencies**: `src`, `sympy`
**Functions**:
- `evaluate_logic` (CPU)
- `extract_numeric_bounds` (CPU)
- `extract_thresholds` (CPU)
- `find_redundant_conditions` (CPU)
- `generate_lookup_table` (CPU)
- `merge_similar_branches` (CPU)
- `optimize_logic` (CPU)
- `simplify_conditions` (CPU)

### `src\proof_engine.py`
**Dependencies**: `z3`
**Functions**:
- `build_output_function` (UI)
- `output` (CPU)
- `parse_condition_to_z3` (CPU)
- `run_default_proof` (CPU)
- `run_z3_proof` (UI)

### `src\runtime_optimization.py`
**Description**: Runtime Optimization Module This module provides the runtime optimization components that integrate with the logic analysis system.
**Dependencies**: `src`, `threading`
**Classes**:
- `RuntimeOptimizer`
**Functions**:
- `RuntimeOptimizer.__init__` (GPU)
- `RuntimeOptimizer._background_loop` (MEMORY)
- `RuntimeOptimizer.get_stats` (CPU)
- `RuntimeOptimizer.optimize_function` (CPU)
- `RuntimeOptimizer.optimize_module` (CPU)
- `RuntimeOptimizer.start` (CPU)
- `RuntimeOptimizer.stop` (CPU)
- `initialize` (CORE)
- `integrate_with_pipeline` (CPU)

### `src\runtime_utils.py`
**Description**: Runtime Utilities for the Logic Tool System.
**Dependencies**: `hashlib`, `inspect`, `src`, `threading`
**Classes**:
- `AdaptiveAgent`
- `JitRouter`
- `JitRoutingModule` (extends Module)
- `PatternMiner`
- `PatternMiningModule` (extends Module)
- `TokenInjectionModule` (extends Module)
- `TokenInjector`
- `_OptimizationTransformer` (extends ast.NodeTransformer)
**Functions**:
- `AdaptiveAgent.__init__` (CORE)
- `AdaptiveAgent._hash_function` (CPU)
- `AdaptiveAgent._monitor_loop` (CPU)
- `AdaptiveAgent._optimize_function` (CPU)
- `AdaptiveAgent.register_function` (CPU)
- `AdaptiveAgent.start` (CPU)
- `AdaptiveAgent.stop` (CPU)
- `JitRouter.__init__` (GPU)
- `JitRouter._check_gpu` (GPU)
- `JitRouter._is_gpu_candidate` (GPU)
- `JitRouter.route` (GPU)
- `JitRoutingModule.__init__` (CORE)
- `JitRoutingModule.process` (CPU)
- `PatternMiner.__init__` (MEMORY)
- `PatternMiner._extract_patterns` (CPU)
- `PatternMiner._get_node_type` (CPU)
- `PatternMiner._serialize_condition` (CPU)
- `PatternMiner.analyze_directory` (CPU)
- `PatternMiner.analyze_file` (CPU)
- `PatternMiner.load_patterns` (CPU)
- `PatternMiner.save_patterns` (MEMORY)
- `PatternMiningModule.__init__` (CORE)
- `PatternMiningModule.process` (CPU)
- `TokenInjectionModule.__init__` (CORE)
- `TokenInjectionModule.process` (CPU)
- `TokenInjector.__init__` (CORE)
- `TokenInjector.inject_tokens` (CPU)
- `TokenInjector.load_patterns` (CPU)
- `_OptimizationTransformer.__init__` (CORE)
- `_OptimizationTransformer.visit_FunctionDef` (CPU)
- `_OptimizationTransformer.visit_If` (CPU)
- `condition` (CPU)
- `mine_patterns_from_directory` (CPU)
- `optimize` (CPU)
- `optimize_file` (CPU)
- `register_runtime_modules` (CPU)
- `start_runtime_optimization` (CPU)
- `stop_runtime_optimization` (CPU)
- `wrapper` (CPU)

### `src\starter_pipeline.py`
**Dependencies**: `argparse`, `src`
**Functions**:
- `parse_arguments` (CPU)
- `run_pipeline` (UI)

### `src\ui_renderers.py`
**Description**: UI Renderers - Module-specific UI rendering functions.
**Dependencies**: `base64`, `io`, `matplotlib`, `numpy`, `src`, `streamlit`
**Functions**:
- `render_custom_function` (UI)
- `render_optimization_results` (MEMORY)
- `render_runtime_optimization` (GPU)

### `src\ui_renderers_part2.py`
**Description**: UI Renderers Part 2 - Additional module-specific UI rendering functions.
**Dependencies**: `base64`, `io`, `matplotlib`, `numpy`, `src`, `streamlit`
**Functions**:
- `render_module_explorer` (UI)
- `render_optimization_testbed` (UI)
- `render_project_organizer` (UI)

### `src\ui_renderers_part3.py`
**Description**: UI Renderers Part 3 - Final module-specific UI rendering functions.
**Dependencies**: `base64`, `io`, `matplotlib`, `numpy`, `src`, `streamlit`
**Functions**:
- `complete_unified_ui` (UI)
- `render_benchmark_results` (MEMORY)

### `src\ui_utils.py`
**Description**: UI Utilities for the Logic Tool.
**Dependencies**: `streamlit`
**Functions**:
- `clear_keys` (UI)
- `get_unique_key` (UI)
- `is_key_used` (CPU)
- `register_keys` (UI)

### `src\unified_ui.py`
**Dependencies**: `atexit`, `base64`, `io`, `matplotlib`, `numpy`, `src`, `streamlit`
**Functions**:
- `background_optimization` (CPU)
- `cleanup` (CPU)
- `initialize_system` (UI)
- `run_ui` (GPU)

### `src\utils.py`
**Functions**:
- `safe_eval` (CPU)

### `src_new\core\hierarchical_core.py`
**Description**: Hierarchical Core - Foundation for the self-bootstrapping architecture  This module provides the core components for a hierarchical, modular system that can dynamically organize, load, and manage modules at multiple levels of abstraction.
**Dependencies**: `abc`, `asyncio`, `concurrent`, `enum`, `importlib`, `inspect`, `threading`, `uuid`, `weakref`
**Classes**:
- `CodeAnalyzer`
- `Event`
- `EventBus`
- `EventPriority` (extends Enum)
- `FileSplitter`
- `HierarchicalModule` (extends ABC)
- `ModuleGenerator`
- `ModuleLoader`
- `ModuleRegistry`
- `ModuleStatus` (extends Enum)
- `StateChangeEvent` (extends Event)
- `StateStore`
**Functions**:
- `CodeAnalyzer.analyze_directory` (CPU)
- `CodeAnalyzer.analyze_file` (CPU)
- `Event.__init__` (UI)
- `Event.__str__` (CPU)
- `EventBus.__init__` (CORE)
- `EventBus.publish` (CPU)
- `EventBus.subscribe` (CPU)
- `EventBus.unsubscribe` (CPU)
- `FileSplitter.split_by_class` (CPU)
- `FileSplitter.split_by_size` (CPU)
- `HierarchicalModule.__init__` (CORE)
- `HierarchicalModule.add_child` (CPU)
- `HierarchicalModule.get_child` (CPU)
- `HierarchicalModule.get_descendant` (CPU)
- `HierarchicalModule.get_full_id` (CPU)
- `HierarchicalModule.get_path` (CPU)
- `HierarchicalModule.initialize` (CORE)
- `HierarchicalModule.process` (CPU)
- `HierarchicalModule.remove_child` (CPU)
- `HierarchicalModule.shutdown` (CPU)
- `HierarchicalModule.to_dict` (CPU)
- `ModuleGenerator.generate_module_class` (CORE)
- `ModuleGenerator.generate_module_file` (CPU)
- `ModuleLoader._load_module_from_config` (CORE)
- `ModuleLoader.load_from_config` (CORE)
- `ModuleLoader.load_module_class` (CPU)
- `ModuleLoader.load_module_instance` (CPU)
- `ModuleRegistry.__init__` (MEMORY)
- `ModuleRegistry._initialize_module` (CORE)
- `ModuleRegistry._remove_from_cache` (MEMORY)
- `ModuleRegistry._update_cache` (MEMORY)
- `ModuleRegistry.get_module` (MEMORY)
- `ModuleRegistry.initialize_all` (CORE)
- `ModuleRegistry.register_module` (MEMORY)
- `ModuleRegistry.shutdown_all` (CPU)
- `ModuleRegistry.to_dict` (CPU)
- `ModuleRegistry.unregister_module` (MEMORY)
- `StateChangeEvent.__init__` (CORE)
- `StateStore.__init__` (CORE)
- `StateStore.get` (CPU)
- `StateStore.get_all` (CPU)
- `StateStore.set` (CPU)
- `StateStore.unwatch` (CPU)
- `StateStore.watch` (CPU)
