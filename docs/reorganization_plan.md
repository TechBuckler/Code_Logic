# Project Reorganization Plan

## Current Issues
- Too many files in the root directory
- Inconsistent organization (some modules in `src/modules`, others scattered)
- Mixture of core functionality and utilities at the same level
- Duplicate/experimental code mixed with production code

## Target Structure (5-7 Top-Level Folders)

```
code_logic_tool_full/
├── core/                  # Core functionality and algorithms
│   ├── ast/               # AST parsing and manipulation
│   ├── ir/                # Intermediate representation
│   ├── proof/             # Proof engine components
│   ├── optimization/      # Optimization algorithms
│   └── export/            # Export and code generation
│
├── modules/               # Module implementations
│   ├── hierarchical/      # Hierarchical module versions
│   ├── resource_oriented/ # Resource-specific implementations
│   └── standard/          # Standard module implementations
│
├── ui/                    # User interface components
│   ├── components/        # Reusable UI components
│   ├── renderers/         # Visualization renderers
│   └── pages/             # Page layouts and navigation
│
├── utils/                 # Utility functions and helpers
│   ├── file/              # File manipulation utilities
│   ├── nlp/               # Natural language processing
│   ├── runtime/           # Runtime optimization utilities
│   └── system/            # System integration utilities
│
├── tools/                 # Standalone tools and scripts
│   ├── shadow_tree/       # Shadow Tree generation and navigation
│   ├── fractal/           # Fractal organization tools
│   ├── resource/          # Resource optimization tools
│   └── testing/           # Testing and validation tools
│
├── docs/                  # Documentation
│   ├── architecture/      # Architecture documentation
│   ├── api/               # API documentation
│   └── examples/          # Example usage and tutorials
│
└── tests/                 # Test suite
    ├── unit/              # Unit tests
    ├── integration/       # Integration tests
    └── resources/         # Test resources and fixtures
```

## Implementation Plan

### Phase 1: Analysis
1. Use the Shadow Tree to generate a complete map of the codebase
2. Identify dependencies between components
3. Classify files by their primary function (core, module, UI, utility, etc.)

### Phase 2: Resource-Based Splitting
1. Use the Resource Splitter to categorize files based on their resource usage
2. Create resource-oriented subdirectories within each top-level folder
3. Move files to their appropriate resource category

### Phase 3: Fractal Organization
1. Apply the Fractal Organizer to each top-level folder
2. Ensure each directory has between 5-20 items
3. Create hierarchical structures where needed to maintain balance

### Phase 4: Dependency Resolution
1. Update import statements to reflect the new structure
2. Create proper package initialization files
3. Ensure all modules can be imported correctly

### Phase 5: Documentation
1. Update documentation to reflect the new structure
2. Generate a new Shadow Tree for the reorganized codebase
3. Create a migration guide for any external dependencies

## Implementation Tools

We'll use our existing tools to implement this reorganization:

1. **Shadow Tree Generator**: To analyze and document the current structure
2. **Resource Splitter**: To categorize files by resource usage
3. **Fractal Organizer**: To create balanced directory structures
4. **Import Updater**: To fix imports after reorganization

## Metrics for Success

1. No directory contains more than 20 items
2. No directory contains fewer than 5 items (except leaf directories)
3. Maximum directory depth is 5 levels
4. All imports work correctly after reorganization
5. Shadow Tree navigation works seamlessly with the new structure
