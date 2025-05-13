# run_app.py

**Path:** `tools\run_app.py`

## Description

Run the Logic Tool UI with safe execution

## Metrics

- **Lines of Code:** 85
- **Functions:** 2
- **Classes:** 0
- **Imports:** 5
- **Complexity:** 24

## Imports

- `import sys`
- `import os`
- `import streamlit.web.cli as stcli`
- `import subprocess`
- `import psutil`

## Functions

### `kill_process_tree(pid)`

Kill a process and all its children.

**Complexity:** 13

### `main()`

Run the Streamlit app with proper Python module imports and safe execution.

**Complexity:** 11

## Keywords

`psutil, sys, parent, path, proc, streamlit, pid, children, child, current_dir, cmdline, cmd, main, ui_path, print, name, info, lower, stcli, kill_process_tree`

