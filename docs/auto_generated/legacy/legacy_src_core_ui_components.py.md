# ui_components.py

**Path:** `legacy\src\core\ui_components.py`

## Description

UI Components - Core components for the unified UI

## Metrics

- **Lines of Code:** 181
- **Functions:** 12
- **Classes:** 4
- **Imports:** 3
- **Complexity:** 18

## Imports

- `import streamlit as st`
- `from typing.Dict`
- `from typing.Any`
- `from typing.List`
- `from typing.Callable`
- `from typing.Optional`
- `from src.core.state_manager.state_manager`

## Classes

### NavigationComponent

Handles navigation and tool selection in the UI

#### Methods

- `__init__`
- `render_sidebar`

### ContentComponent

Handles the main content area of the UI

#### Methods

- `__init__`
- `register_renderer`
- `render_content`

### ResultsComponent

Handles the results display area of the UI

#### Methods

- `__init__`
- `register_renderer`
- `render_results`

### UIManager

Main UI manager that combines all UI components

#### Methods

- `__new__`
- `register_tool`
- `register_results_renderer`
- `render`

## Functions

### `__init__(self)`

**Complexity:** 1

### `render_sidebar(self, tools)`

Render the sidebar navigation

**Complexity:** 8

### `__init__(self)`

**Complexity:** 1

### `register_renderer(self, tool_id, renderer)`

Register a content renderer for a specific tool

**Complexity:** 1

### `render_content(self)`

Render the main content area based on active tool

**Complexity:** 6

### `__init__(self)`

**Complexity:** 1

### `register_renderer(self, result_type, renderer)`

Register a results renderer for a specific result type

**Complexity:** 1

### `render_results(self, container)`

Render results in the specified container or create a new one

**Complexity:** 5

### `__new__(cls)`

**Complexity:** 2

### `register_tool(self, tool_id, tool_name, content_renderer, category, icon)`

Register a tool with the UI manager

**Complexity:** 1

### `register_results_renderer(self, result_type, renderer)`

Register a results renderer

**Complexity:** 1

### `render(self)`

Render the complete UI

**Complexity:** 1

## Keywords

`state_manager, shared_state, tool, category, tool_id, _instance, active_tool, str, sidebar, result_type, get, key, results, renderer, Callable, event_bus, tools, tool_categories, register_ui_key, container`

