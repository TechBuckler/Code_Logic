# Code Logic Tool

## Project Structure

This codebase follows a balanced directory structure with 9 top-level folders:

```
code_logic_tool/
├── core/              # Core algorithms and processing
│   ├── ast/           # Abstract Syntax Tree handling
│   ├── ir/            # Intermediate Representation
│   ├── proof/         # Proof generation and validation
│   ├── optimization/  # Optimization algorithms
│   └── export/        # Export functionality
│
├── modules/           # Module implementations
│   ├── standard/      # Standard modules
│   │   ├── processing/    # Processing modules
│   │   ├── analysis/      # Analysis modules
│   │   ├── export/        # Export modules
│   │   └── organization/  # Organization modules
│   ├── hierarchical/  # Hierarchical modules
│   └── resource_oriented/ # Resource-specific implementations
│
├── ui/                # User interface components
│   ├── components/    # Reusable UI components
│   ├── renderers/     # Output renderers
│   └── pages/         # Page definitions
│
├── utils/             # Utility functions and helpers
│   ├── file/          # File operations
│   ├── runtime/       # Runtime utilities
│   ├── system/        # System interaction
│   └── nlp/           # Natural language processing
│
├── tools/             # Standalone tools
│   ├── shadow_tree/   # Shadow Tree navigation
│   ├── fractal/       # Fractal organization tools
│   ├── resource/      # Resource management
│   └── testing/       # Testing tools
│
├── docs/              # Documentation
│   ├── api/           # API documentation
│   ├── guides/        # User guides
│   └── examples/      # Example code
│
├── tests/             # Test suite
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── e2e/           # End-to-end tests
│
├── data/              # Data files
│   ├── cache/         # Cached data
│   ├── input/         # Input data
│   └── output/        # Output data
│
└── config/            # Configuration files
```

## Utility Functions

Common functionality has been consolidated into utility modules:

- `utils.path_utils`: Path manipulation and directory handling
- `utils.file_utils`: File reading, writing, and manipulation
- `utils.json_utils`: JSON parsing and serialization
- `utils.string_utils`: String processing and manipulation

Import these utilities instead of reimplementing common functionality.

## Running the Application

To run the main application:

```bash
py run_ui.py
```

For command-line interface:

```bash
py run_cli.py
```

## Development

This project follows a fractal organization approach, ensuring each directory has a balanced number of items (5-20) and uses resource-based splitting for optimal performance.
