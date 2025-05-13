"""
Background System Compatibility Module

This module provides compatibility for the background_system module during the transition
to the new directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import threading
import utils.time
import queue

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to import from the new location
try:
    from modules.background import *
except ImportError:
    # Define minimal functionality to satisfy imports
    class BackgroundSystem:
        """System for running tasks in the background."""
        
        def __init__(self):
            """Initialize the background system."""
            self.task_queue = queue.PriorityQueue()
            self.running = False
            self.thread = None
            self.log = []
            
        def start(self):
            """Start the background system."""
            if not self.running:
                self.running = True
                self.thread = threading.Thread(target=self._worker)
                self.thread.daemon = True
                self.thread.start()
                return True
            return False
        
        def stop(self):
            """Stop the background system."""
            if self.running:
                self.running = False
                if self.thread:
                    self.thread.join(timeout=1.0)
                return True
            return False
        
        def add_task(self, task, priority=0):
            """Add a task to the queue."""
            self.task_queue.put((priority, task))
            return True
        
        def _worker(self):
            """Worker thread that processes tasks."""
            while self.running:
                try:
                    if not self.task_queue.empty():
                        priority, task = self.task_queue.get(block=False)
                        try:
                            result = task()
                            self.log.append({
                                'task': task.__name__ if hasattr(task, '__name__') else str(task),
                                'priority': priority,
                                'result': result,
                                'time': time.time()
                            })
                        except Exception as e:
                            self.log.append({
                                'task': task.__name__ if hasattr(task, '__name__') else str(task),
                                'priority': priority,
                                'error': str(e),
                                'time': time.time()
                            })
                    else:
                        time.sleep(0.1)
                except Exception:
                    time.sleep(0.1)
        
        def get_log(self):
            """Get the task execution log."""
            return self.log

# Create a singleton instance
background_system = BackgroundSystem()

# Export symbols
__all__ = ['BackgroundSystem', 'background_system']
