# Codebase Summary

**Generated on:** 2025-05-12 09:47:44

## Overall Statistics

- **Total Files:** 202
- **Total Lines of Code:** 34492
- **Total Functions:** 1150
- **Total Classes:** 145
- **Total Imports:** 964
- **Average Complexity:** 21.31
- **Maximum Complexity:** 181 (in `legacy\src\unified_ui.py`)

## Notable Files

- **Largest File:** `legacy\src\unified_ui.py` (1647 lines)
- **Most Functions:** `legacy\src\core\hierarchical_core.py` (44 functions)
- **Most Classes:** `legacy\src\core\hierarchical_core.py` (12 classes)
- **Most Complex Function:** `run_ui` in `legacy\src\unified_ui.py` (complexity: 180)

## Module Breakdown

### config/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### core/

- **Files:** 2
- **Lines of Code:** 202
- **Functions:** 11
- **Classes:** 1

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| unified_core.py | 199 | 11 | 1 | 14 |
| __init__.py | 3 | 0 | 0 | 1 |

### core/ast/

- **Files:** 2
- **Lines of Code:** 20
- **Functions:** 2
- **Classes:** 1

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| explorer.py | 17 | 2 | 1 | 1 |
| __init__.py | 3 | 0 | 0 | 1 |

### core/export/

- **Files:** 2
- **Lines of Code:** 9
- **Functions:** 1
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| exporter.py | 6 | 1 | 0 | 1 |
| __init__.py | 3 | 0 | 0 | 1 |

### core/ir/

- **Files:** 2
- **Lines of Code:** 134
- **Functions:** 4
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| model.py | 131 | 4 | 0 | 29 |
| __init__.py | 3 | 0 | 0 | 1 |

### core/optimization/

- **Files:** 3
- **Lines of Code:** 394
- **Functions:** 17
- **Classes:** 1

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| optimizer.py | 236 | 8 | 0 | 49 |
| runtime.py | 155 | 9 | 1 | 11 |
| __init__.py | 3 | 0 | 0 | 1 |

### core/proof/

- **Files:** 3
- **Lines of Code:** 183
- **Functions:** 7
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| engine.py | 153 | 5 | 0 | 22 |
| proof_engine_run_default_proof.py | 27 | 2 | 0 | 1 |
| __init__.py | 3 | 0 | 0 | 1 |

### data/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### docs/diagrams/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### legacy/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### legacy/src/

- **Files:** 28
- **Lines of Code:** 7062
- **Functions:** 195
- **Classes:** 25

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| unified_ui.py | 1647 | 6 | 0 | 181 |
| ui_renderers_part2.py | 791 | 3 | 0 | 85 |
| bootstrap.py | 704 | 16 | 1 | 63 |
| ui_renderers.py | 452 | 3 | 0 | 34 |
| runtime_utils.py | 437 | 39 | 8 | 50 |
| new_unified_ui.py | 402 | 6 | 0 | 36 |
| new_main.py | 367 | 19 | 5 | 29 |
| ui_renderers_part3.py | 255 | 2 | 0 | 10 |
| optimizer.py | 236 | 8 | 0 | 49 |
| demo_hierarchical.py | 215 | 11 | 4 | 22 |
| hierarchical_main.py | 183 | 8 | 1 | 21 |
| module_system.py | 171 | 18 | 2 | 22 |
| hierarchical_app.py | 160 | 8 | 1 | 19 |
| runtime_optimization.py | 155 | 9 | 1 | 11 |
| proof_engine.py | 153 | 5 | 0 | 22 |
| ir_model.py | 131 | 4 | 0 | 29 |
| file_utils.py | 129 | 4 | 0 | 19 |
| imports.py | 121 | 4 | 0 | 28 |
| starter_pipeline.py | 114 | 2 | 0 | 9 |
| ai_suggester.py | 61 | 3 | 0 | 7 |
| background_system.py | 51 | 7 | 1 | 9 |
| ui_utils.py | 47 | 4 | 0 | 5 |
| graph_builder.py | 42 | 1 | 0 | 13 |
| ast_explorer.py | 17 | 2 | 1 | 1 |
| exporter_optimized.py | 9 | 1 | 0 | 1 |
| exporter.py | 6 | 1 | 0 | 1 |
| utils.py | 5 | 1 | 0 | 3 |
| __init__.py | 1 | 0 | 0 | 1 |

### legacy/src/core/

- **Files:** 7
- **Lines of Code:** 1723
- **Functions:** 134
- **Classes:** 28

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| hierarchical_core.py | 747 | 44 | 12 | 70 |
| simple_hierarchical_core.py | 270 | 28 | 6 | 39 |
| unified_core.py | 199 | 11 | 1 | 14 |
| ui_components.py | 181 | 12 | 4 | 18 |
| hierarchical_module.py | 176 | 21 | 2 | 23 |
| state_manager.py | 147 | 18 | 3 | 20 |
| __init__.py | 3 | 0 | 0 | 1 |

### legacy/src/modules/

- **Files:** 11
- **Lines of Code:** 1998
- **Functions:** 67
- **Classes:** 11

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| optimization_testbed_module.py | 992 | 14 | 2 | 86 |
| shadow_tree_module.py | 349 | 13 | 1 | 66 |
| module_explorer_module.py | 309 | 13 | 1 | 58 |
| project_organizer_module.py | 246 | 9 | 1 | 44 |
| ir_generator_module.py | 26 | 3 | 1 | 8 |
| exporter_module.py | 22 | 3 | 1 | 4 |
| proof_engine_module.py | 15 | 3 | 1 | 3 |
| graph_builder_module.py | 14 | 3 | 1 | 2 |
| optimizer_module.py | 13 | 3 | 1 | 3 |
| ast_parser_module.py | 11 | 3 | 1 | 2 |
| __init__.py | 1 | 0 | 0 | 1 |

### legacy/src/modules/hierarchical/

- **Files:** 7
- **Lines of Code:** 881
- **Functions:** 30
- **Classes:** 6

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| ir_generator_module.py | 181 | 5 | 1 | 27 |
| optimization_core_module.py | 156 | 5 | 1 | 15 |
| analysis_core_module.py | 154 | 6 | 1 | 13 |
| proof_engine_module.py | 140 | 5 | 1 | 18 |
| optimizer_module.py | 133 | 5 | 1 | 23 |
| ast_parser_module.py | 114 | 4 | 1 | 10 |
| __init__.py | 3 | 0 | 0 | 1 |

### modules/

- **Files:** 3
- **Lines of Code:** 225
- **Functions:** 25
- **Classes:** 3

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| system.py | 171 | 18 | 2 | 22 |
| background.py | 51 | 7 | 1 | 9 |
| __init__.py | 3 | 0 | 0 | 1 |

### modules/hierarchical/

- **Files:** 2
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |
| hierarchical_core_initialize_all.py | 0 | 0 | 0 | 0 |

### modules/resource_oriented/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### modules/resource_oriented/cpu/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### modules/resource_oriented/gpu/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### modules/resource_oriented/memory/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### modules/resource_oriented/network/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### modules/standard/

- **Files:** 2
- **Lines of Code:** 527
- **Functions:** 20
- **Classes:** 4

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| code_mapper.py | 524 | 20 | 4 | 57 |
| __init__.py | 3 | 0 | 0 | 1 |

### modules/standard/analysis/

- **Files:** 3
- **Lines of Code:** 1304
- **Functions:** 27
- **Classes:** 3

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| optimization_testbed_module.py | 992 | 14 | 2 | 86 |
| module_explorer_module.py | 309 | 13 | 1 | 58 |
| __init__.py | 3 | 0 | 0 | 1 |

### modules/standard/export/

- **Files:** 3
- **Lines of Code:** 39
- **Functions:** 6
- **Classes:** 2

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| exporter_module.py | 22 | 3 | 1 | 4 |
| graph_builder_module.py | 14 | 3 | 1 | 2 |
| __init__.py | 3 | 0 | 0 | 1 |

### modules/standard/organization/

- **Files:** 3
- **Lines of Code:** 598
- **Functions:** 22
- **Classes:** 2

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| shadow_tree_module.py | 349 | 13 | 1 | 66 |
| project_organizer_module.py | 246 | 9 | 1 | 44 |
| __init__.py | 3 | 0 | 0 | 1 |

### modules/standard/processing/

- **Files:** 5
- **Lines of Code:** 68
- **Functions:** 12
- **Classes:** 4

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| ir_generator_module.py | 26 | 3 | 1 | 8 |
| proof_engine_module.py | 15 | 3 | 1 | 3 |
| optimizer_module.py | 13 | 3 | 1 | 3 |
| ast_parser_module.py | 11 | 3 | 1 | 2 |
| __init__.py | 3 | 0 | 0 | 1 |

### root/

- **Files:** 6
- **Lines of Code:** 946
- **Functions:** 41
- **Classes:** 1

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| summarize_codebase.py | 271 | 2 | 0 | 35 |
| verify_codebase.py | 241 | 32 | 1 | 21 |
| quick_verify.py | 164 | 3 | 0 | 24 |
| document_codebase.py | 160 | 2 | 0 | 28 |
| list_structure.py | 107 | 2 | 0 | 19 |
| __init__.py | 3 | 0 | 0 | 1 |

### tests/integration/

- **Files:** 2
- **Lines of Code:** 94
- **Functions:** 5
- **Classes:** 1

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| test_shadow_tree.py | 91 | 5 | 1 | 7 |
| __init__.py | 3 | 0 | 0 | 1 |

### tests/unit/

- **Files:** 3
- **Lines of Code:** 170
- **Functions:** 5
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| test_shadow_tree.py | 167 | 5 | 0 | 18 |
| __init__.py | 3 | 0 | 0 | 1 |
| optimization_testbed_module___init__.py | 0 | 0 | 0 | 0 |

### tools/

- **Files:** 33
- **Lines of Code:** 6816
- **Functions:** 198
- **Classes:** 21

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| shadow_tree.py | 899 | 44 | 6 | 120 |
| reorganize_codebase.py | 644 | 11 | 0 | 56 |
| fractal_organizer.py | 554 | 21 | 5 | 91 |
| simple_shadow_tree.py | 535 | 21 | 3 | 67 |
| code_mapper.py | 524 | 20 | 4 | 57 |
| resource_splitter.py | 468 | 10 | 0 | 75 |
| file_splitter.py | 438 | 8 | 1 | 55 |
| implement_reorganization.py | 359 | 6 | 0 | 43 |
| smart_splitter.py | 331 | 10 | 1 | 41 |
| scan_codebase.py | 299 | 11 | 1 | 36 |
| refactor_modules.py | 196 | 4 | 0 | 14 |
| logic_tool.py | 172 | 3 | 0 | 24 |
| run_cli.py | 172 | 3 | 0 | 24 |
| split_standard_modules.py | 154 | 3 | 0 | 21 |
| find_duplicates.py | 139 | 3 | 0 | 23 |
| safe_runner.py | 106 | 2 | 0 | 22 |
| run_complete.py | 96 | 2 | 0 | 11 |
| run_complete_system.py | 96 | 2 | 0 | 11 |
| improved_explorer.py | 92 | 1 | 0 | 19 |
| run_app.py | 85 | 2 | 0 | 24 |
| structure_analyzer.py | 81 | 3 | 0 | 14 |
| scan_files.py | 75 | 2 | 0 | 11 |
| run_explorer.py | 54 | 1 | 0 | 10 |
| run_hierarchical.py | 51 | 1 | 0 | 7 |
| run_new_architecture.py | 51 | 1 | 0 | 7 |
| cleanup_files.py | 44 | 1 | 0 | 8 |
| cleanup_final.py | 33 | 0 | 0 | 5 |
| run_bootstrap.py | 30 | 0 | 0 | 3 |
| run_new_app.py | 16 | 0 | 0 | 2 |
| decide_optimized.py | 14 | 1 | 0 | 6 |
| extract_functions_optimized.py | 5 | 1 | 0 | 2 |
| __init__.py | 3 | 0 | 0 | 1 |
| safe_eval_optimized.py | 0 | 0 | 0 | 0 |

### tools/fractal/

- **Files:** 7
- **Lines of Code:** 2169
- **Functions:** 78
- **Classes:** 11

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| fractal_organizer.py | 554 | 21 | 5 | 91 |
| organizer.py | 554 | 21 | 5 | 91 |
| structure_optimizer.py | 380 | 12 | 0 | 55 |
| dynamic_organizer.py | 259 | 10 | 1 | 26 |
| code_analyzer.py | 217 | 8 | 0 | 33 |
| clustering.py | 202 | 6 | 0 | 18 |
| __init__.py | 3 | 0 | 0 | 1 |

### tools/reorganization/

- **Files:** 4
- **Lines of Code:** 863
- **Functions:** 19
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| finalize_reorganization.py | 450 | 8 | 0 | 50 |
| complete_cleanup.py | 205 | 5 | 0 | 40 |
| final_cleanup.py | 205 | 6 | 0 | 27 |
| __init__.py | 3 | 0 | 0 | 1 |

### tools/resource/

- **Files:** 5
- **Lines of Code:** 1240
- **Functions:** 28
- **Classes:** 2

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| splitter.py | 468 | 10 | 0 | 75 |
| file_splitter.py | 438 | 8 | 1 | 55 |
| smart_splitter.py | 331 | 10 | 1 | 41 |
| __init__.py | 3 | 0 | 0 | 1 |
| code_mapper_analyze_resource_profile.py | 0 | 0 | 0 | 0 |

### tools/scripts/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/

- **Files:** 4
- **Lines of Code:** 1604
- **Functions:** 70
- **Classes:** 9

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| navigator.py | 899 | 44 | 6 | 120 |
| simple.py | 535 | 21 | 3 | 67 |
| test_shadow_tree.py | 167 | 5 | 0 | 18 |
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/core/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/core/hierarchical_core/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/core/simple_hierarchical_core/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/core/unified_core/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/file_utils/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/modules/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/new_unified_ui/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/runtime_utils/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/ui_utils/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/unified_ui/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/shadow_tree/output/src/utils/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### tools/testing/

- **Files:** 3
- **Lines of Code:** 377
- **Functions:** 13
- **Classes:** 1

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| codebase_scanner.py | 299 | 11 | 1 | 36 |
| file_scanner.py | 75 | 2 | 0 | 11 |
| __init__.py | 3 | 0 | 0 | 1 |

### ui/

- **Files:** 5
- **Lines of Code:** 2137
- **Functions:** 14
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| unified.py | 1647 | 6 | 0 | 181 |
| new_unified.py | 402 | 6 | 0 | 36 |
| run_ui.py | 85 | 2 | 0 | 24 |
| __init__.py | 3 | 0 | 0 | 1 |
| analysis_core_module_render_ui.py | 0 | 0 | 0 | 0 |

### ui/components/

- **Files:** 2
- **Lines of Code:** 50
- **Functions:** 4
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| utils.py | 47 | 4 | 0 | 5 |
| __init__.py | 3 | 0 | 0 | 1 |

### ui/pages/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### ui/renderers/

- **Files:** 5
- **Lines of Code:** 1501
- **Functions:** 8
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| advanced.py | 791 | 3 | 0 | 85 |
| base.py | 452 | 3 | 0 | 34 |
| specialized.py | 255 | 2 | 0 | 10 |
| __init__.py | 3 | 0 | 0 | 1 |
| ui_components_register_results_renderer.py | 0 | 0 | 0 | 0 |

### utils/

- **Files:** 7
- **Lines of Code:** 511
- **Functions:** 44
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| import_utils.py | 197 | 6 | 0 | 22 |
| file_utils.py | 87 | 10 | 0 | 4 |
| string_utils.py | 83 | 10 | 0 | 12 |
| json_utils.py | 67 | 6 | 0 | 9 |
| path_utils.py | 61 | 11 | 0 | 3 |
| __init__.py | 11 | 0 | 0 | 1 |
| general.py | 5 | 1 | 0 | 3 |

### utils/file/

- **Files:** 2
- **Lines of Code:** 132
- **Functions:** 4
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| operations.py | 129 | 4 | 0 | 19 |
| __init__.py | 3 | 0 | 0 | 1 |

### utils/nlp/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

### utils/runtime/

- **Files:** 2
- **Lines of Code:** 440
- **Functions:** 39
- **Classes:** 8

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| operations.py | 437 | 39 | 8 | 50 |
| __init__.py | 3 | 0 | 0 | 1 |

### utils/system/

- **Files:** 1
- **Lines of Code:** 3
- **Functions:** 0
- **Classes:** 0

| File | LOC | Functions | Classes | Complexity |
|------|-----|-----------|---------|------------|
| __init__.py | 3 | 0 | 0 | 1 |

## Top Keywords

- **path:** 85
- **print:** 55
- **name:** 36
- **sys:** 33
- **str:** 31
- **node:** 29
- **project_root:** 28
- **dirname:** 28
- **file_path:** 28
- **append:** 27
- **file:** 25
- **src:** 25
- **join:** 24
- **write:** 22
- **get:** 22
- **module:** 21
- **ast:** 21
- **imports:** 20
- **isinstance:** 19
- **__init__:** 19

## Top Imports

- **os:** 109
- **sys:** 91
- **typing.Dict:** 50
- **typing.List:** 50
- **typing.Any:** 50
- **json:** 45
- **pathlib.Path:** 41
- **typing.Optional:** 35
- **ast:** 34
- **re:** 31
- **typing.Callable:** 29
- **importlib:** 25
- **time:** 25
- **streamlit:** 25
- **typing.Set:** 22
- **src.core.state_manager.state_manager:** 21
- **argparse:** 19
- **typing.Tuple:** 19
- **typing.Union:** 18
- **utils.path_utils.ensure_dir:** 15

## Interesting Files

### legacy\src\unified_ui.py

**Lines:** 1647

**Interesting because:** high complexity

**Description:**
> No docstring

### ui\unified.py

**Lines:** 1647

**Interesting because:** high complexity

**Description:**
> No docstring

### legacy\src\modules\optimization_testbed_module.py

**Lines:** 992

**Interesting because:** high complexity, many functions, AI/ML-related docstring

**Description:**
> Optimization Testbed Module

This module provides a comprehensive testing environment for analyzing code and finding
optimal tradeoffs between memory usage, CPU performance, GPU utilization, and other...

### modules\standard\analysis\optimization_testbed_module.py

**Lines:** 992

**Interesting because:** high complexity, many functions, AI/ML-related docstring

**Description:**
> Optimization Testbed Module

This module provides a comprehensive testing environment for analyzing code and finding
optimal tradeoffs between memory usage, CPU performance, GPU utilization, and other...

### tools\shadow_tree.py

**Lines:** 899

**Interesting because:** high complexity, many functions, many classes, unusual imports: nltk, nltk.tokenize.word_tokenize, nltk.corpus.wordnet, nltk.stem.WordNetLemmatizer

**Description:**
> Shadow Tree Generator

Creates a natural language shadow tree that mirrors the code structure,
allowing intuitive navigation through the fractal codebase.

### tools\shadow_tree\navigator.py

**Lines:** 899

**Interesting because:** high complexity, many functions, many classes, unusual imports: nltk, nltk.tokenize.word_tokenize, nltk.corpus.wordnet, nltk.stem.WordNetLemmatizer

**Description:**
> Shadow Tree Generator

Creates a natural language shadow tree that mirrors the code structure,
allowing intuitive navigation through the fractal codebase.

### legacy\src\ui_renderers_part2.py

**Lines:** 791

**Interesting because:** high complexity

**Description:**
> UI Renderers Part 2 - Additional module-specific UI rendering functions

### ui\renderers\advanced.py

**Lines:** 791

**Interesting because:** high complexity

**Description:**
> UI Renderers Part 2 - Additional module-specific UI rendering functions

### legacy\src\core\hierarchical_core.py

**Lines:** 747

**Interesting because:** high complexity, many functions, many classes

**Description:**
> Hierarchical Core - Foundation for the self-bootstrapping architecture

This module provides the core components for a hierarchical, modular system
that can dynamically organize, load, and manage modu...

### legacy\src\bootstrap.py

**Lines:** 704

**Interesting because:** high complexity, many functions

**Description:**
> Bootstrap - Self-generating architecture system

This module analyzes the existing codebase and transforms it into the new
hierarchical architecture. It serves as the entry point for the self-bootstra...

### tools\reorganize_codebase.py

**Lines:** 644

**Interesting because:** high complexity, many functions

**Description:**
> Codebase Reorganization Tool

This script reorganizes the codebase according to the plan outlined in
reorganization_plan.md, using the existing fractal organizer and resource
splitter tools.

### tools\fractal_organizer.py

**Lines:** 554

**Interesting because:** high complexity, many functions, many classes

**Description:**
> Fractal Code Organizer

This module enforces extreme modularity by recursively breaking down code into
smaller and smaller components, while providing mechanisms to navigate and
"bubble up" the struct...

### tools\fractal\fractal_organizer.py

**Lines:** 554

**Interesting because:** high complexity, many functions, many classes

**Description:**
> Fractal Code Organizer

This module enforces extreme modularity by recursively breaking down code into
smaller and smaller components, while providing mechanisms to navigate and
"bubble up" the struct...

### tools\fractal\organizer.py

**Lines:** 554

**Interesting because:** high complexity, many functions, many classes

**Description:**
> Fractal Code Organizer

This module enforces extreme modularity by recursively breaking down code into
smaller and smaller components, while providing mechanisms to navigate and
"bubble up" the struct...

### tools\simple_shadow_tree.py

**Lines:** 535

**Interesting because:** high complexity, many functions

**Description:**
> No docstring

### tools\shadow_tree\simple.py

**Lines:** 535

**Interesting because:** high complexity, many functions

**Description:**
> No docstring

### modules\standard\code_mapper.py

**Lines:** 524

**Interesting because:** high complexity, many functions, many classes, AI/ML-related docstring

**Description:**
> Code Mapper Module

This module provides tools for analyzing and mapping the codebase structure,
dependencies, and resource usage patterns. It uses AST (Abstract Syntax Tree)
to parse Python files and...

### tools\code_mapper.py

**Lines:** 524

**Interesting because:** high complexity, many functions, many classes, AI/ML-related docstring

**Description:**
> Code Mapper Module

This module provides tools for analyzing and mapping the codebase structure,
dependencies, and resource usage patterns. It uses AST (Abstract Syntax Tree)
to parse Python files and...

### tools\resource_splitter.py

**Lines:** 468

**Interesting because:** high complexity

**Description:**
> Resource-Oriented File Splitter

This script splits Python files into resource-oriented components and
organizes them in a logical directory structure.

### tools\resource\splitter.py

**Lines:** 468

**Interesting because:** high complexity

**Description:**
> Resource-Oriented File Splitter

This script splits Python files into resource-oriented components and
organizes them in a logical directory structure.

### legacy\src\ui_renderers.py

**Lines:** 452

**Interesting because:** high complexity

**Description:**
> UI Renderers - Module-specific UI rendering functions

### ui\renderers\base.py

**Lines:** 452

**Interesting because:** high complexity

**Description:**
> UI Renderers - Module-specific UI rendering functions

### tools\reorganization\finalize_reorganization.py

**Lines:** 450

**Interesting because:** high complexity, AI/ML-related docstring

**Description:**
> Finalize Reorganization

This script finalizes the codebase reorganization by:
1. Removing redundant *_split directories
2. Moving any remaining important files to the new structure
3. Cleaning up dup...

### tools\file_splitter.py

**Lines:** 438

**Interesting because:** high complexity

**Description:**
> File Splitter and Merger Utility

This module provides utilities for splitting and merging files using various methods:
- Line-based splitting
- Byte-based splitting
- Token-based splitting (for Pytho...

### tools\resource\file_splitter.py

**Lines:** 438

**Interesting because:** high complexity

**Description:**
> File Splitter and Merger Utility

This module provides utilities for splitting and merging files using various methods:
- Line-based splitting
- Byte-based splitting
- Token-based splitting (for Pytho...

### legacy\src\runtime_utils.py

**Lines:** 437

**Interesting because:** high complexity, many functions, many classes, AI/ML-related docstring

**Description:**
> Runtime Utilities for the Logic Tool System.
This file provides functions that bridge the logic analysis and runtime optimization components.

### utils\runtime\operations.py

**Lines:** 437

**Interesting because:** high complexity, many functions, many classes, AI/ML-related docstring

**Description:**
> Runtime Utilities for the Logic Tool System.
This file provides functions that bridge the logic analysis and runtime optimization components.

### legacy\src\new_unified_ui.py

**Lines:** 402

**Interesting because:** high complexity

**Description:**
> New Unified UI - Redesigned UI with improved architecture

### ui\new_unified.py

**Lines:** 402

**Interesting because:** high complexity

**Description:**
> New Unified UI - Redesigned UI with improved architecture

### tools\fractal\structure_optimizer.py

**Lines:** 380

**Interesting because:** high complexity, many functions, unusual imports: networkx

**Description:**
> Structure Optimizer Module

Optimizes the directory structure based on file clusters and analysis
to create a balanced, fractal organization.

### legacy\src\new_main.py

**Lines:** 367

**Interesting because:** high complexity, many functions, many classes, AI/ML-related docstring

**Description:**
> New Main Application - Entry point for the Logic Tool with hierarchical architecture

This module serves as the main entry point for the Logic Tool, using the new
hierarchical architecture based on si...

### tools\implement_reorganization.py

**Lines:** 359

**Interesting because:** high complexity

**Description:**
> Codebase Reorganization Implementation

This script implements the reorganization plan for the codebase,
creating the directory structure and moving files to their appropriate locations.

### legacy\src\modules\shadow_tree_module.py

**Lines:** 349

**Interesting because:** high complexity, many functions

**Description:**
> Shadow Tree Module

This module integrates the Shadow Tree system with the unified UI,
allowing for natural language navigation of the codebase.

### modules\standard\organization\shadow_tree_module.py

**Lines:** 349

**Interesting because:** high complexity, many functions

**Description:**
> Shadow Tree Module

This module integrates the Shadow Tree system with the unified UI,
allowing for natural language navigation of the codebase.

### tools\smart_splitter.py

**Lines:** 331

**Interesting because:** high complexity

**Description:**
> Smart File Splitter

This script provides enhanced file splitting capabilities with a focus on:
1. Resource-oriented splitting
2. Logical directory organization
3. Reversible operations with manifests...

### tools\resource\smart_splitter.py

**Lines:** 331

**Interesting because:** high complexity

**Description:**
> Smart File Splitter

This script provides enhanced file splitting capabilities with a focus on:
1. Resource-oriented splitting
2. Logical directory organization
3. Reversible operations with manifests...

### legacy\src\modules\module_explorer_module.py

**Lines:** 309

**Interesting because:** high complexity, many functions

**Description:**
> Module Explorer Module

This module allows exploring, editing, and running other modules in the system.
It provides a unified interface for inspecting code, running tools, and executing
the entire pip...

### modules\standard\analysis\module_explorer_module.py

**Lines:** 309

**Interesting because:** high complexity, many functions

**Description:**
> Module Explorer Module

This module allows exploring, editing, and running other modules in the system.
It provides a unified interface for inspecting code, running tools, and executing
the entire pip...

### tools\scan_codebase.py

**Lines:** 299

**Interesting because:** high complexity, many functions

**Description:**
> Codebase Scanner

This script scans the entire codebase and provides a comprehensive report
of the directory structure, file types, and code organization.

### tools\testing\codebase_scanner.py

**Lines:** 299

**Interesting because:** high complexity, many functions

**Description:**
> Codebase Scanner

This script scans the entire codebase and provides a comprehensive report
of the directory structure, file types, and code organization.

### summarize_codebase.py

**Lines:** 271

**Interesting because:** high complexity

**Description:**
> Summarize Codebase

This script quickly summarizes all files in the codebase and identifies
interesting or previously unknown components.

### legacy\src\core\simple_hierarchical_core.py

**Lines:** 270

**Interesting because:** high complexity, many functions, many classes

**Description:**
> Simple Hierarchical Core - A lightweight foundation for hierarchical modules

This module provides a simplified hierarchical module system with event-based
communication and state management. It's des...

### tools\fractal\dynamic_organizer.py

**Lines:** 259

**Interesting because:** high complexity

**Description:**
> Dynamic Directory Organizer

This script analyzes the codebase and automatically determines the optimal
directory structure based on file relationships, dependencies, and complexity.
It uses AST analy...

### legacy\src\modules\project_organizer_module.py

**Lines:** 246

**Interesting because:** high complexity

**Description:**
> Project Organizer Module

This module handles project organization, file naming conventions, and project structure.
It can analyze the current project structure, suggest improvements, and apply change...

### modules\standard\organization\project_organizer_module.py

**Lines:** 246

**Interesting because:** high complexity

**Description:**
> Project Organizer Module

This module handles project organization, file naming conventions, and project structure.
It can analyze the current project structure, suggest improvements, and apply change...

### verify_codebase.py

**Lines:** 241

**Interesting because:** high complexity, many functions

**Description:**
> Verify Codebase

This script verifies that all major components of the codebase work correctly
after the reorganization.

### core\optimization\optimizer.py

**Lines:** 236

**Interesting because:** high complexity

**Description:**
> No docstring

### legacy\src\optimizer.py

**Lines:** 236

**Interesting because:** high complexity

**Description:**
> No docstring

### tools\fractal\code_analyzer.py

**Lines:** 217

**Interesting because:** high complexity

**Description:**
> Code Analyzer Module

Provides functions for analyzing Python code files to extract
dependencies, complexity metrics, and semantic information.

### legacy\src\demo_hierarchical.py

**Lines:** 215

**Interesting because:** high complexity, many functions, many classes

**Description:**
> Demo of the Hierarchical Module System

This script demonstrates the hierarchical module system by creating a simple
hierarchy of modules and showing how they interact.

### tools\reorganization\complete_cleanup.py

**Lines:** 205

**Interesting because:** high complexity, AI/ML-related docstring

**Description:**
> Complete Cleanup

This script handles the final remaining items that need to be cleaned up.

### tools\reorganization\final_cleanup.py

**Lines:** 205

**Interesting because:** high complexity

**Description:**
> Final Cleanup

This script handles the final cleanup of files and folders that don't fit
the established directory structure.

### tools\fractal\clustering.py

**Lines:** 202

**Interesting because:** high complexity, unusual imports: networkx, sklearn.feature_extraction.text.TfidfVectorizer, sklearn.cluster.AgglomerativeClustering

**Description:**
> Clustering Module

Provides functions for clustering files based on their similarity
and relationships to create a balanced directory structure.

### core\unified_core.py

**Lines:** 199

**Interesting because:** many functions, AI/ML-related docstring

**Description:**
> Unified Core Architecture

This module provides a unified core architecture that integrates all existing modules
while maintaining a clean hierarchical structure. It serves as the central hub for
all ...

### legacy\src\core\unified_core.py

**Lines:** 199

**Interesting because:** many functions, AI/ML-related docstring

**Description:**
> Unified Core Architecture

This module provides a unified core architecture that integrates all existing modules
while maintaining a clean hierarchical structure. It serves as the central hub for
all ...

### utils\import_utils.py

**Lines:** 197

**Interesting because:** high complexity

**Description:**
> Import Utility Module

Provides a centralized system for handling imports across the codebase,
supporting both the old and new directory structures during transition.

### legacy\src\hierarchical_main.py

**Lines:** 183

**Interesting because:** high complexity, AI/ML-related docstring

**Description:**
> Hierarchical Logic Tool - Main Application

This is the main entry point for the Logic Tool using the hierarchical module architecture.
It sets up the core modules and handles the main UI rendering.

### legacy\src\core\ui_components.py

**Lines:** 181

**Interesting because:** high complexity, many functions, many classes

**Description:**
> UI Components - Core components for the unified UI

### legacy\src\modules\hierarchical\ir_generator_module.py

**Lines:** 181

**Interesting because:** high complexity

**Description:**
> Hierarchical IR Generator Module

This module extends the base IR generator module with hierarchical capabilities.
It generates an Intermediate Representation (IR) model from parsed code.

### legacy\src\core\hierarchical_module.py

**Lines:** 176

**Interesting because:** high complexity, many functions

**Description:**
> Hierarchical Module System - Extends the base module system with hierarchical capabilities

This module provides a hierarchical extension to the base module system,
allowing modules to be organized in...

### tools\logic_tool.py

**Lines:** 172

**Interesting because:** high complexity

**Description:**
> No docstring

### tools\run_cli.py

**Lines:** 172

**Interesting because:** high complexity

**Description:**
> No docstring

### legacy\src\module_system.py

**Lines:** 171

**Interesting because:** high complexity, many functions

**Description:**
> No docstring

### modules\system.py

**Lines:** 171

**Interesting because:** high complexity, many functions

**Description:**
> No docstring

### tests\unit\test_shadow_tree.py

**Lines:** 167

**Interesting because:** high complexity

**Description:**
> Shadow Tree Navigation Test Script

This script tests the bubble up and drill down functionality of the Shadow Tree
to ensure it works correctly before integrating with the UI.

### tools\shadow_tree\test_shadow_tree.py

**Lines:** 167

**Interesting because:** high complexity

**Description:**
> Shadow Tree Navigation Test Script

This script tests the bubble up and drill down functionality of the Shadow Tree
to ensure it works correctly before integrating with the UI.

### quick_verify.py

**Lines:** 164

**Interesting because:** high complexity

**Description:**
> Quick Verification Script

This script performs a quick verification of the codebase by:
1. Testing imports of key modules
2. Running basic functionality tests
3. Verifying file integrity

It's design...

### document_codebase.py

**Lines:** 160

**Interesting because:** high complexity

**Description:**
> Document Codebase

This script documents every file in the project using our existing tools
for AST analysis, code exploration, and documentation generation.

### legacy\src\hierarchical_app.py

**Lines:** 160

**Interesting because:** high complexity, AI/ML-related docstring

**Description:**
> Hierarchical Logic Tool Application

This is the main entry point for the Logic Tool using the hierarchical module system.
It sets up the core modules and handles the main UI rendering.

### legacy\src\modules\hierarchical\optimization_core_module.py

**Lines:** 156

**Interesting because:** AI/ML-related docstring

**Description:**
> Optimization Core Module - Hierarchical version

This module serves as the core for all optimization-related functionality,
including logic optimization, formal verification, and performance analysis.

### core\optimization\runtime.py

**Lines:** 155

**Interesting because:** AI/ML-related docstring

**Description:**
> Runtime Optimization Module
This module provides the runtime optimization components that integrate with the logic analysis system.

### legacy\src\runtime_optimization.py

**Lines:** 155

**Interesting because:** AI/ML-related docstring

**Description:**
> Runtime Optimization Module
This module provides the runtime optimization components that integrate with the logic analysis system.

### tools\split_standard_modules.py

**Lines:** 154

**Interesting because:** high complexity, AI/ML-related docstring

**Description:**
> Split Standard Modules

This script splits the modules/standard directory into more specific categories
to maintain a balanced directory structure.

### core\proof\engine.py

**Lines:** 153

**Interesting because:** high complexity

**Description:**
> No docstring

### legacy\src\proof_engine.py

**Lines:** 153

**Interesting because:** high complexity

**Description:**
> No docstring

### legacy\src\core\state_manager.py

**Lines:** 147

**Interesting because:** high complexity, many functions

**Description:**
> State Manager - Core component for managing shared state and event communication

### legacy\src\modules\hierarchical\proof_engine_module.py

**Lines:** 140

**Interesting because:** high complexity

**Description:**
> Hierarchical Proof Engine Module

This module extends the base proof engine module with hierarchical capabilities.
It uses Z3 to formally verify the correctness of logic functions.

### tools\find_duplicates.py

**Lines:** 139

**Interesting because:** high complexity

**Description:**
> Duplicate Functionality Finder

This script identifies duplicate functionality across the codebase
and suggests helper files to consolidate them.

### legacy\src\modules\hierarchical\optimizer_module.py

**Lines:** 133

**Interesting because:** high complexity

**Description:**
> No docstring

### core\ir\model.py

**Lines:** 131

**Interesting because:** high complexity

**Description:**
> No docstring

### legacy\src\ir_model.py

**Lines:** 131

**Interesting because:** high complexity

**Description:**
> No docstring

### legacy\src\file_utils.py

**Lines:** 129

**Interesting because:** high complexity

**Description:**
> File Utilities for the Logic Tool

This module provides utility functions for working with files,
including copying, transforming, and loading Python modules.

### utils\file\operations.py

**Lines:** 129

**Interesting because:** high complexity

**Description:**
> File Utilities for the Logic Tool

This module provides utility functions for working with files,
including copying, transforming, and loading Python modules.

### legacy\src\imports.py

**Lines:** 121

**Interesting because:** high complexity

**Description:**
> Centralized imports for the Logic Tool system.
This file ensures all components can find their dependencies.

### list_structure.py

**Lines:** 107

**Interesting because:** high complexity

**Description:**
> List Directory Structure

This script displays the directory structure in a tree-like format.

### tools\safe_runner.py

**Lines:** 106

**Interesting because:** high complexity

**Description:**
> Safe Run Wrapper for Logic Tool

This script provides a robust wrapper around the Logic Tool CLI commands,
ensuring proper process termination and error handling.

### tools\run_complete.py

**Lines:** 96

**Interesting because:** AI/ML-related docstring

**Description:**
> Run the Complete Logic Tool System with Hierarchical Architecture

This script runs the complete Logic Tool system with the hierarchical architecture,
including analysis, optimization, and verificatio...

### tools\run_complete_system.py

**Lines:** 96

**Interesting because:** AI/ML-related docstring

**Description:**
> Run the Complete Logic Tool System with Hierarchical Architecture

This script runs the complete Logic Tool system with the hierarchical architecture,
including analysis, optimization, and verificatio...

### tools\improved_explorer.py

**Lines:** 92

**Interesting because:** high complexity

**Description:**
> Improved Module Explorer Script

This script provides a cleaner view of all modules in the project.

### tools\run_app.py

**Lines:** 85

**Interesting because:** high complexity

**Description:**
> Run the Logic Tool UI with safe execution

### ui\run_ui.py

**Lines:** 85

**Interesting because:** high complexity

**Description:**
> Run the Logic Tool UI with safe execution

### utils\path_utils.py

**Lines:** 61

**Interesting because:** many functions

**Description:**
> Path utility functions for common path operations.

This module provides standardized functions for path manipulation and
directory handling, reducing code duplication across the codebase.

### legacy\src\graph_builder.py

**Lines:** 42

**Interesting because:** unusual imports: networkx

**Description:**
> No docstring

### core\optimization\__init__.py

**Lines:** 3

**Interesting because:** AI/ML-related docstring

**Description:**
> optimization package.

