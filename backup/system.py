# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase


# Basic imports needed for the module system
import sys
import os

# Make sure src is in the path
src_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class Module:
    def __init__(self, name):
        self.name = name
        self.dependencies = []
        self.active = False
        self.resource_profile = {
            'cpu': 0.5,     # Default CPU usage (0.0-1.0)
            'memory': 0.5,  # Default memory usage (0.0-1.0)
            'gpu': 0.0,     # Default GPU usage (0.0-1.0)
            'network': 0.0, # Default network usage (0.0-1.0)
            'startup': 0.3, # Default startup time impact (0.0-1.0)
            'runtime': 0.5  # Default runtime impact (0.0-1.0)
        }
        self.resource_type = 'core'  # Default resource focus: 'core', 'cpu', 'memory', 'gpu', 'network', 'ui'
        
    def initialize(self):
        self.active = True
        return True
        
    def shutdown(self):
        self.active = False
        
    def can_process(self, data):
        return self.active
        
    def process(self, data, context=None):
        pass
        
    def get_resource_profile(self):
        """Return the resource profile for this module."""
        return self.resource_profile
        
    def set_resource_profile(self, profile):
        """Set the resource profile for this module."""
        self.resource_profile.update(profile)
        return self

class ModuleRegistry:
    def __init__(self):
        self.modules = {}
        self.resource_constraints = {
            'cpu': 1.0,     # Maximum CPU usage allowed (0.0-1.0)
            'memory': 1.0,  # Maximum memory usage allowed (0.0-1.0)
            'gpu': 1.0,     # Maximum GPU usage allowed (0.0-1.0)
            'network': 1.0, # Maximum network usage allowed (0.0-1.0)
            'startup': 1.0, # Maximum startup time impact allowed (0.0-1.0)
            'runtime': 1.0  # Maximum runtime impact allowed (0.0-1.0)
        }
        
    def register(self, module):
        self.modules[module.name] = module
        return self
        
    def initialize_all(self):
        for module in self.modules.values():
            module.initialize()
            
    def shutdown_all(self):
        for module in self.modules.values():
            module.shutdown()
            
    def get_module(self, name):
        return self.modules.get(name)
        
    def process_chain(self, data, module_names, context=None):
        result = data
        for name in module_names:
            module = self.get_module(name)
            if module and module.can_process(result):
                result = module.process(result, context)
        return result
        
    def get_modules_by_resource_type(self, resource_type):
        """Get all modules of a specific resource type."""
        return [m for m in self.modules.values() if m.resource_type == resource_type]
        
    def set_resource_constraints(self, constraints):
        """Set resource constraints for the module registry."""
        self.resource_constraints.update(constraints)
        return self
        
    def get_resource_constraints(self):
        """Get current resource constraints."""
        return self.resource_constraints
        
    def optimize_module_chain(self, module_names, optimization_profile):
        """Optimize a module chain based on resource constraints.
        Returns an optimized list of module names that satisfy the constraints."""
        # Start with the original chain
        optimized_chain = module_names.copy()
        
        # Calculate total resource usage
        total_usage = {resource: 0.0 for resource in self.resource_constraints}
        for name in module_names:
            module = self.get_module(name)
            if module:
                profile = module.get_resource_profile()
                for resource, usage in profile.items():
                    if resource in total_usage:
                        total_usage[resource] += usage
        
        # Check if any resource exceeds constraints
        exceeded_resources = []
        for resource, usage in total_usage.items():
            if usage > self.resource_constraints.get(resource, 1.0):
                exceeded_resources.append(resource)
        
        # If no constraints are exceeded, return the original chain
        if not exceeded_resources:
            return optimized_chain
        
        # Otherwise, optimize the chain based on the profile
        # Import modules
        from modules.ast_parser_module import AstParserModule
        from modules.exporter_module import ExporterModule
        from modules.graph_builder_module import GraphBuilderModule
        from modules.ir_generator_module import IRGeneratorModule
        from modules.optimizer_module import OptimizerModule
        from modules.proof_engine_module import ProofEngineModule
        from modules.module_explorer_module import ModuleExplorerModule
        from modules.shadow_tree_module import ShadowTreeModule
        
        # Sort modules by their importance for the given profile
        modules = [self.get_module(name) for name in module_names if self.get_module(name)]
        
        # Calculate a score for each module based on the optimization profile
        def calculate_score(module):
            profile = module.get_resource_profile()
            score = 0
            for resource, weight in optimization_profile.items():
                # Higher score for modules that use less of constrained resources
                if resource in exceeded_resources:
                    score += (1.0 - profile.get(resource, 0.0)) * weight
                else:
                    score += 0.5 * weight  # Neutral score for non-constrained resources
            return score
        
        # Sort modules by score (highest first)
        sorted_modules = sorted(modules, key=calculate_score, reverse=True)
        
        # Rebuild the chain with the highest scoring modules first, as long as constraints are met
        optimized_chain = []
        current_usage = {resource: 0.0 for resource in self.resource_constraints}
        
        for module in sorted_modules:
            # Check if adding this module would exceed any constraint
            can_add = True
            profile = module.get_resource_profile()
            
            for resource in exceeded_resources:
                if current_usage[resource] + profile.get(resource, 0.0) > self.resource_constraints.get(resource, 1.0):
                    can_add = False
                    break
            
            if can_add:
                optimized_chain.append(module.name)
                for resource, usage in profile.items():
                    if resource in current_usage:
                        current_usage[resource] += usage
        
        return optimized_chain
