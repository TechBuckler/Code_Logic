"""
Background System Utility

This module manages background task execution and system resource monitoring for the codebase.
"""
import threading
import time
import queue
import psutil
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



class BackgroundSystem:
    def __init__(self):
        self.task_queue = queue.PriorityQueue()
        self.running = False
        self.thread = None
        self.log = []
        
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._worker)
            self.thread.daemon = True
            self.thread.start()
            
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
    def add_task(self, task, priority=0):
        self.task_queue.put((priority, task))
        self.log.append(f"Added task with priority {priority}")
        
    def get_log(self):
        return self.log
        
    def _worker(self):
        while self.running:
            if self._is_idle() and not self.task_queue.empty():
                _, task = self.task_queue.get()
                self.log.append(f"Running background task")
                try:
                    task()
                    self.log.append(f"Task completed successfully")
                except Exception as e:
                    self.log.append(f"Task error: {e}")
                self.task_queue.task_done()
            time.sleep(1.0)
            
    def _is_idle(self):
        # Simple idle detection based on CPU usage
        cpu_usage = psutil.cpu_percent(interval=0.5)
        is_idle = cpu_usage < 30.0
        if is_idle:
            self.log.append(f"System idle (CPU: {cpu_usage}%)")
        return is_idle
