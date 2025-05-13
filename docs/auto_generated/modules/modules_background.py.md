# background.py

**Path:** `modules\background.py`

## Metrics

- **Lines of Code:** 51
- **Functions:** 7
- **Classes:** 1
- **Imports:** 4
- **Complexity:** 9

## Imports

- `import threading`
- `import time`
- `import queue`
- `import psutil`

## Classes

### BackgroundSystem

#### Methods

- `__init__`
- `start`
- `stop`
- `add_task`
- `get_log`
- `_worker`
- `_is_idle`

## Functions

### `__init__(self)`

**Complexity:** 1

### `start(self)`

**Complexity:** 2

### `stop(self)`

**Complexity:** 2

### `add_task(self, task, priority)`

**Complexity:** 1

### `get_log(self)`

**Complexity:** 1

### `_worker(self)`

**Complexity:** 6

### `_is_idle(self)`

**Complexity:** 2

## Keywords

`log, thread, task, task_queue, running, append, priority, cpu_usage, is_idle, threading, time, queue, psutil, start, _worker, _is_idle, Task, BackgroundSystem, __init__, PriorityQueue`

