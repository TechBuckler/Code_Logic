#!/usr/bin/env python
"""
Circular Dependency Breaker

Breaks circular dependencies by pre-loading all modules in the directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
import types
import importlib.util
import queue
import threading
import time

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def create_common_modules():
    """Create common modules that are needed across the codebase."""
    # First create the Module class as a base for HierarchicalModule
    module_system = types.ModuleType('module_system')
    
    class Module:
        """Base module class."""
        def __init__(self, name):
            self.name = name
            self.dependencies = []
            self.active = False
        
        def activate(self):
            """Activate the module."""
            self.active = True
            return True
        
        def deactivate(self):
            """Deactivate the module."""
            self.active = False
            return True
    
    module_system.Module = Module
    sys.modules['module_system'] = module_system
    
    # Create HierarchicalModule - needed in multiple locations
    hierarchical_module = types.ModuleType('modules.standard.hierarchical_module')
    
    class HierarchicalModule(Module):
        """Hierarchical module that extends the base Module class."""
        def __init__(self, name, parent=None):
            super().__init__(name)
            self.parent = parent
            self.children = {}
            self.event_bus = None
            self.shared_state = None
            
            # Register with parent if provided
            if parent:
                parent.add_child(self)
        
        def add_child(self, module):
            """Add a child module."""
            self.children[module.name] = module
            return self
        
        def remove_child(self, name):
            """Remove a child module by name."""
            if name in self.children:
                del self.children[name]
            return self
        
        def get_child(self, name):
            """Get a child module by name."""
            return self.children.get(name)
        
        def get_path(self):
            """Get the path from the root to this module."""
            if self.parent:
                return self.parent.get_path() + [self.name]
            return [self.name]
        
        def get_full_name(self):
            """Get the full name including the path."""
            return ".".join(self.get_path())
    
    # Add the class to the module
    hierarchical_module.HierarchicalModule = HierarchicalModule
    
    # Make it available at all known import locations
    sys.modules['modules.standard.hierarchical_module'] = hierarchical_module
    sys.modules['core.hierarchical_module'] = hierarchical_module
    sys.modules['hierarchical_module'] = hierarchical_module
    
    print("Created HierarchicalModule in multiple locations")
    
    # RuntimeOptimizationModule - needed in multiple locations
    runtime_module = types.ModuleType('modules.runtime_optimization')
    
    class RuntimeOptimizationModule:
        """Module for runtime optimization."""
        def __init__(self, name=None, parent=None):
            self.name = name
            self.parent = parent
            self.optimizations = []
        
        def add_optimization(self, optimization):
            """Add an optimization to the module."""
            self.optimizations.append(optimization)
            return self
        
        def optimize(self, code):
            """Apply optimizations to code."""
            for optimization in self.optimizations:
                code = optimization(code)
            return code
    
    # Add the class to the module
    runtime_module.RuntimeOptimizationModule = RuntimeOptimizationModule
    
    # Make it available at all known import locations
    sys.modules['modules.runtime_optimization'] = runtime_module
    sys.modules['modules.runtime_optimization_module'] = runtime_module
    sys.modules['modules.standard.runtime_optimization_module'] = runtime_module
    
    print("Created RuntimeOptimizationModule in multiple locations")
    
    # Create BackgroundSystem module
    background_module = types.ModuleType('modules.background')
    
    class BackgroundSystem:
        """System for running tasks in the background."""
        
        def __init__(self):
            """Initialize the background system."""
            self.task_queue = queue.Queue()
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
                                'time': 0  # Placeholder for time
                            })
                        except Exception as e:
                            self.log.append({
                                'task': task.__name__ if hasattr(task, '__name__') else str(task),
                                'priority': priority,
                                'error': str(e),
                                'time': 0  # Placeholder for time
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
    
    # Add to the module
    background_module.BackgroundSystem = BackgroundSystem
    background_module.background_system = background_system
    
    # Make it available at all known import locations
    sys.modules['modules.background'] = background_module
    
    print("Created BackgroundSystem in modules.background")

def preload_modules(directory=None):
    """Preload all modules to break circular dependencies."""
    directory = directory or PROJECT_ROOT
    preloaded = []
    
    # First create common modules that are needed in multiple places
    create_common_modules()
    
    # Find all Python files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, PROJECT_ROOT)
                
                # Convert to module path
                module_path = os.path.splitext(rel_path)[0].replace(os.path.sep, '.')
                
                # Skip if already in sys.modules
                if module_path in sys.modules:
                    continue
                
                # Create an empty module and add it to sys.modules
                module = types.ModuleType(module_path)
                sys.modules[module_path] = module
                preloaded.append(module_path)
    
    # Now actually load the modules
    for module_path in preloaded:
        try:
            importlib.import_module(module_path)
        except:
            pass
    
    return preloaded

if __name__ == "__main__":
    preloaded = preload_modules()
    print(f"Preloaded {len(preloaded)} modules to break circular dependencies")
