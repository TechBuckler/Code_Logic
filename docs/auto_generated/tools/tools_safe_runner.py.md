# safe_runner.py

**Path:** `tools\safe_runner.py`

## Description

Safe Run Wrapper for Logic Tool

This script provides a robust wrapper around the Logic Tool CLI commands,
ensuring proper process termination and error handling.

## Metrics

- **Lines of Code:** 106
- **Functions:** 2
- **Classes:** 0
- **Imports:** 5
- **Complexity:** 22

## Imports

- `import os`
- `import sys`
- `import subprocess`
- `import time`
- `import psutil`

## Functions

### `kill_process_tree(pid)`

Kill a process and all its children.

**Complexity:** 13

### `main()`

**Complexity:** 9

## Keywords

`print, timeout, subprocess, time, parent, process, pid, children, child, seconds, stderr, sys, psutil, kill_process_tree, cmd, stdout, Process, terminate, still_alive, kill`

