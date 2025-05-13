"""
Unified Core Architecture

This module provides a unified core architecture that integrates all existing modules
while maintaining a clean hierarchical structure. It serves as the central hub for
all functionality in the Logic Tool.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Make sure src is in the path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.dirname(src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


class UnifiedCore:
    """
    Unified core architecture that integrates all existing modules
    while maintaining a clean hierarchical structure.
    """
    
    def __init__(self):
        """Initialize the unified core"""
        self.module_registry = ModuleRegistry()
        self.module_hierarchy = {}
        self.event_handlers = {}
        
        # Initialize state
        self.shared_state = state_manager
        
        # Register for events
        self.shared_state.event_bus.subscribe("*", self.handle_event)
    
    def initialize(self):
        """Initialize the unified core and all modules"""
        # Register all modules
        self._register_modules()
        
        # Build module hierarchy
        self._build_hierarchy()
        
        # Initialize all modules
        self.module_registry.initialize_all()
        
        # Connect modules through events
        self._connect_modules()
    
    def _register_modules(self):
        """Register all modules with the registry"""
        # Core analysis modules
        
        # Optimization modules
        
        # Visualization modules
        
        # Advanced modules
        
        # Register all modules
        self.module_registry.register(AstParserModule())
        self.module_registry.register(IrGeneratorModule())
        self.module_registry.register(OptimizerModule())
        self.module_registry.register(ProofEngineModule())
        self.module_registry.register(GraphBuilderModule())
        self.module_registry.register(ExporterModule())
        self.module_registry.register(ProjectOrganizerModule())
        self.module_registry.register(ModuleExplorerModule())
        self.module_registry.register(OptimizationTestbedModule())
        
        # Register runtime optimization modules
        register_runtime_modules(self.module_registry)
    
    def _build_hierarchy(self):
        """Build a hierarchical structure of modules"""
        # Define the hierarchy structure
        self.module_hierarchy = {
            "analysis": {
                "name": "Analysis Core",
                "modules": ["ast_parser", "ir_generator"],
                "children": {}
            },
            "optimization": {
                "name": "Optimization Core",
                "modules": ["optimizer", "proof_engine"],
                "children": {
                    "testbed": {
                        "name": "Optimization Testbed",
                        "modules": ["optimization_testbed"],
                        "children": {}
                    }
                }
            },
            "visualization": {
                "name": "Visualization Core",
                "modules": ["graph_builder", "exporter"],
                "children": {}
            },
            "project": {
                "name": "Project Management",
                "modules": ["project_organizer", "module_explorer"],
                "children": {}
            }
        }
    
    def _connect_modules(self):
        """Connect modules through events"""
        # Define event flows between modules
        event_flows = [
            # Analysis flow
            {"from": "ast_parser", "event": "ast_parsing_complete", "to": "ir_generator"},
            {"from": "ir_generator", "event": "ir_generation_complete", "to": "optimizer"},
            
            # Optimization flow
            {"from": "optimizer", "event": "optimization_complete", "to": "proof_engine"},
            {"from": "proof_engine", "event": "proof_complete", "to": "exporter"},
            
            # Visualization flow
            {"from": "ir_generator", "event": "ir_generation_complete", "to": "graph_builder"},
            
            # Project management flow
            {"from": "*", "event": "module_state_changed", "to": "module_explorer"}
        ]
        
        # Register event handlers
        for flow in event_flows:
            source = flow["from"]
            event = flow["event"]
            target = flow["to"]
            
            # Get the target module
            target_module = self.module_registry.get_module(target)
            if target_module:
                # Create a handler that forwards the event to the target module
                handler = lambda data, module=target_module: module.process(data)
                
                # Register the handler
                if source == "*":
                    self.shared_state.event_bus.subscribe(event, handler)
                else:
                    source_module = self.module_registry.get_module(source)
                    if source_module:
                        source_module.on(event, handler)
    
    def handle_event(self, event_type, data):
        """Handle events from the event bus"""
        # Forward events to registered handlers
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Error handling event {event_type}: {e}")
    
    def register_event_handler(self, event_type, handler):
        """Register a handler for an event"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def get_module(self, name):
        """Get a module by name"""
        return self.module_registry.get_module(name)
    
    def get_modules_in_category(self, category):
        """Get all modules in a category"""
        if category in self.module_hierarchy:
            module_names = self.module_hierarchy[category]["modules"]
            return [self.module_registry.get_module(name) for name in module_names]
        return []
    
    def process_with_module(self, module_name, data, context=None):
        """Process data with a specific module"""
        module = self.module_registry.get_module(module_name)
        if module and module.can_process(data):
            return module.process(data, context)
        return None
    
    def shutdown(self):
        """Shutdown the unified core and all modules"""
        self.module_registry.shutdown_all()
        
        # Unregister from events
        self.shared_state.event_bus.unsubscribe("*", self.handle_event)
