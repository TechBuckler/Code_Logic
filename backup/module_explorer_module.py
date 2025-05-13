"""
Module Explorer Module

This module allows exploring, editing, and running other modules in the system.
It provides a unified interface for inspecting code, running tools, and executing
the entire pipeline or specific components.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import inspect
import importlib
import importlib.util


class ModuleExplorerModule:
    """Module for exploring, editing, and running other modules."""
    
    def __init__(self):
        self.name = "module_explorer"
        self.description = "Explores, edits, and runs other modules"
        self.dependencies = []
        self.module_cache = {}
        self.project_root = self._find_project_root()
        self.active = True
        
    def initialize(self):
        """Initialize the module."""
        pass
    
    def can_process(self, data):
        """Check if this module can process the given data."""
        if not isinstance(data, dict):
            return False
        
        command = data.get('command')
        return command in ['list_modules', 'view_module', 'edit_module', 'run_module', 'run_pipeline']
    
    def process(self, data, context=None):
        """Process the command."""
        command = data.get('command')
        
        if command == 'list_modules':
            return self.list_modules()
        elif command == 'view_module':
            return self.view_module(data.get('module_name'))
        elif command == 'edit_module':
            return self.edit_module(data.get('module_name'), data.get('changes'))
        elif command == 'run_module':
            return self.run_module(data.get('module_name'), data.get('args', {}))
        elif command == 'run_pipeline':
            return self.run_pipeline(data.get('source_code'), data.get('function_name'), data.get('options', {}))
        
        return {"error": "Unknown command"}
    
    def list_modules(self):
        """List all available modules in the project."""
        modules = []
        
        # Check src/modules directory
        modules_dir = os.path.join(self.project_root, 'src', 'modules')
        if os.path.exists(modules_dir):
            for file in os.listdir(modules_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    module_name = file[:-3]  # Remove .py extension
                    module_info = self._get_module_info(module_name)
                    modules.append(module_info)
        
        # Check src directory for other Python files
        src_dir = os.path.join(self.project_root, 'src')
        if os.path.exists(src_dir):
            for file in os.listdir(src_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    module_name = file[:-3]  # Remove .py extension
                    module_path = os.path.join(src_dir, file)
                    modules.append({
                        "name": module_name,
                        "path": module_path,
                        "type": "utility" if module_name.endswith('_utils') else "component"
                    })
        
        return {"modules": modules}
    
    def view_module(self, module_name):
        """View the source code of a module."""
        if not module_name:
            return {"error": "Module name is required"}
        
        # Try to find the module file
        module_path = self._find_module_path(module_name)
        if not module_path:
            return {"error": f"Module {module_name} not found"}
        
        # Read the module source code
        try:
            with open(module_path, 'r') as f:
                source_code = f.read()
            
            # Get module info if it's a proper module
            module_info = self._get_module_info(module_name)
            
            return {
                "module_name": module_name,
                "path": module_path,
                "source_code": source_code,
                "info": module_info
            }
        except Exception as e:
            return {"error": f"Error reading module {module_name}: {str(e)}"}
    
    def edit_module(self, module_name, changes):
        """Edit a module's source code."""
        if not module_name:
            return {"error": "Module name is required"}
        if not changes:
            return {"error": "Changes are required"}
        
        # Try to find the module file
        module_path = self._find_module_path(module_name)
        if not module_path:
            return {"error": f"Module {module_name} not found"}
        
        # Read the current source code
        try:
            with open(module_path, 'r') as f:
                current_source = f.read()
            
            # Apply changes (this is a simple implementation, could be more sophisticated)
            if isinstance(changes, str):
                # Replace the entire file
                new_source = changes
            elif isinstance(changes, dict) and 'replacements' in changes:
                # Apply specific replacements
                new_source = current_source
                for replacement in changes['replacements']:
                    target = replacement.get('target')
                    replacement_text = replacement.get('replacement')
                    if target and replacement_text:
                        new_source = new_source.replace(target, replacement_text)
            else:
                return {"error": "Invalid changes format"}
            
            # Write the new source code
            with open(module_path, 'w') as f:
                f.write(new_source)
            
            return {
                "module_name": module_name,
                "path": module_path,
                "status": "updated"
            }
        except Exception as e:
            return {"error": f"Error editing module {module_name}: {str(e)}"}
    
    def run_module(self, module_name, args):
        """Run a specific module with the given arguments."""
        if not module_name:
            return {"error": "Module name is required"}
        
        # Try to find and import the module
        try:
            module = self._import_module(module_name)
            if not module:
                return {"error": f"Module {module_name} could not be imported"}
            
            # Find the main class in the module
            module_class = None
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and name.lower().endswith('module'):
                    module_class = obj
                    break
            
            if not module_class:
                return {"error": f"No module class found in {module_name}"}
            
            # Instantiate the module
            module_instance = module_class()
            
            # Check if the module has a process method
            if hasattr(module_instance, 'process') and callable(module_instance.process):
                result = module_instance.process(args)
                return {
                    "module_name": module_name,
                    "status": "executed",
                    "result": result
                }
            else:
                return {"error": f"Module {module_name} does not have a process method"}
        except Exception as e:
            return {"error": f"Error running module {module_name}: {str(e)}"}
    
    def run_pipeline(self, source_code, function_name=None, options=None):
        """Run the entire processing pipeline on the given source code."""
        try:
            # Import the starter pipeline
            sys.path.insert(0, os.path.join(self.project_root, 'src'))
            
            # Run the pipeline
            result = run_pipeline(source_code, function_name, options)
            
            return {
                "status": "pipeline_executed",
                "result": result
            }
        except Exception as e:
            return {"error": f"Error running pipeline: {str(e)}"}
    
    def _find_project_root(self):
        """Find the project root directory."""
        # Start with the current directory and go up until we find a directory with src/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        while current_dir != os.path.dirname(current_dir):  # Stop at the root directory
            if os.path.exists(os.path.join(current_dir, 'src')):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        
        # If we couldn't find it, use the parent directory of the current file
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    def _find_module_path(self, module_name):
        """Find the path to a module file."""
        # Check in src/modules
        module_path = os.path.join(self.project_root, 'src', 'modules', f"{module_name}.py")
        if os.path.exists(module_path):
            return module_path
        
        # Check in src
        module_path = os.path.join(self.project_root, 'src', f"{module_name}.py")
        if os.path.exists(module_path):
            return module_path
        
        # Check in root
        module_path = os.path.join(self.project_root, f"{module_name}.py")
        if os.path.exists(module_path):
            return module_path
        
        return None
    
    def _import_module(self, module_name):
        """Import a module by name."""
        if module_name in self.module_cache:
            return self.module_cache[module_name]
        
        module_path = self._find_module_path(module_name)
        if not module_path:
            return None
        
        try:
            # Prepare the import
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Cache the module
            self.module_cache[module_name] = module
            
            return module
        except Exception as e:
            print(f"Error importing module {module_name}: {str(e)}")
            return None
    
    def _get_module_info(self, module_name):
        """Get information about a module."""
        module = self._import_module(module_name)
        if not module:
            module_path = self._find_module_path(module_name)
            return {
                "name": module_name,
                "path": module_path,
                "type": "unknown"
            }
        
        # Find the main class in the module
        module_class = None
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and name.lower().endswith('module'):
                module_class = obj
                break
        
        if not module_class:
            module_path = self._find_module_path(module_name)
            return {
                "name": module_name,
                "path": module_path,
                "type": "utility"
            }
        
        # Get module info from the class
        try:
            instance = module_class()
            return {
                "name": module_name,
                "path": self._find_module_path(module_name),
                "type": "module",
                "description": getattr(instance, 'description', 'No description'),
                "dependencies": getattr(instance, 'dependencies', [])
            }
        except Exception:
            module_path = self._find_module_path(module_name)
            return {
                "name": module_name,
                "path": module_path,
                "type": "module",
                "description": "Could not instantiate module",
                "dependencies": []
            }
