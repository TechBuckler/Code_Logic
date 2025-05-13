"""
Demo of the Hierarchical Module System

This script demonstrates the hierarchical module system by creating a simple
hierarchy of modules and showing how they interact.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Make sure src is in the path
src_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# Set up Streamlit page config
st.set_page_config(
    page_title="Hierarchical Module Demo",
    page_icon="🧠",
    layout="wide"
)

class AnalysisModule(HierarchicalModule):
    """Root module for analysis functionality"""
    
    def __init__(self, parent=None):
        super().__init__("analysis", parent)
        
    def render_ui(self):
        st.header("Analysis Module")
        st.write("This is the root analysis module")
        
        # Show children
        if self.children:
            st.subheader("Child Modules")
            for child in self.children.values():
                st.write(f"- {child.name}")
        
        # Demo action
        if st.button("Analyze", key=state_manager.register_ui_key("analyze_btn")):
            st.success("Analysis complete!")
            # Publish an event
            self.event_bus.publish("analysis_complete", {"result": "success"})

class ParserModule(HierarchicalModule):
    """Child module for parsing code"""
    
    def __init__(self, parent=None):
        super().__init__("parser", parent)
        
    def render_ui(self):
        st.header("Parser Module")
        st.write("This module parses code into an AST")
        
        # Demo input
        code = st.text_area("Enter code to parse", 
                           value="def hello():\n    print('Hello, world!')", 
                           key=state_manager.register_ui_key("parser_code"))
        
        if st.button("Parse", key=state_manager.register_ui_key("parse_btn")):
            # Simple parsing demo
            lines = code.split("\n")
            st.json({
                "type": "function",
                "name": "hello",
                "body": [
                    {"type": "call", "name": "print", "args": ["Hello, world!"]}
                ]
            })
            
            # Publish an event
            self.event_bus.publish("code_parsed", {"code": code})

class OptimizationModule(HierarchicalModule):
    """Root module for optimization functionality"""
    
    def __init__(self, parent=None):
        super().__init__("optimization", parent)
        
        # Subscribe to events from other modules
        self.event_bus.subscribe("code_parsed", self.handle_parsed_code)
        
    def handle_parsed_code(self, data):
        """Handle parsed code event"""
        if "code" in data:
            st.success("Received parsed code from Parser Module!")
            st.code(data["code"])
    
    def render_ui(self):
        st.header("Optimization Module")
        st.write("This module optimizes code for performance")
        
        # Show children
        if self.children:
            st.subheader("Child Modules")
            for child in self.children.values():
                st.write(f"- {child.name}")
        
        # Demo action
        if st.button("Optimize", key=state_manager.register_ui_key("optimize_btn")):
            st.success("Optimization complete!")
            # Publish an event
            self.event_bus.publish("optimization_complete", {"result": "success"})

class PerformanceTestModule(HierarchicalModule):
    """Child module for performance testing"""
    
    def __init__(self, parent=None):
        super().__init__("performance_test", parent)
        
    def render_ui(self):
        st.header("Performance Test Module")
        st.write("This module tests code performance")
        
        # Demo input
        iterations = st.slider("Test iterations", 1, 100, 10, 
                              key=state_manager.register_ui_key("perf_iterations"))
        
        if st.button("Run Tests", key=state_manager.register_ui_key("test_btn")):
            # Simple performance test demo
            import time
            start = time.time()
            for i in range(iterations):
                # Simulate work
                pass
            end = time.time()
            
            st.success(f"Test completed in {end - start:.6f} seconds")
            
            # Publish an event
            self.event_bus.publish("performance_test_complete", {
                "iterations": iterations,
                "time": end - start
            })

def main():
    """Main function to run the demo"""
    st.title("Hierarchical Module System Demo")
    st.write("This demo shows how modules can be organized in a hierarchy and communicate via events.")
    
    # Create the module hierarchy
    hierarchy = ModuleHierarchy()
    
    # Create root modules
    analysis = AnalysisModule()
    optimization = OptimizationModule()
    
    # Add child modules
    parser = ParserModule(analysis)
    performance = PerformanceTestModule(optimization)
    
    # Add root modules to hierarchy
    hierarchy.add_root_module(analysis)
    hierarchy.add_root_module(optimization)
    
    # Initialize all modules
    hierarchy.initialize_all()
    
    # Create sidebar for navigation
    st.sidebar.title("Navigation")
    
    # Get all modules for navigation
    all_modules = hierarchy.get_all_modules()
    module_names = [module.get_full_name() for module in all_modules]
    
    # Store selected module in session state
    if "selected_module" not in st.session_state:
        st.session_state.selected_module = module_names[0]
    
    # Navigation buttons
    for name in module_names:
        if st.sidebar.button(name, key=state_manager.register_ui_key(f"nav_{name}")):
            st.session_state.selected_module = name
    
    # Display selected module
    selected_name = st.session_state.selected_module
    selected_module = None
    
    for module in all_modules:
        if module.get_full_name() == selected_name:
            selected_module = module
            break
    
    if selected_module:
        selected_module.render_ui()
    else:
        st.error(f"Module {selected_name} not found")
    
    # Event log in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Event Log")
    
    if "event_log" not in st.session_state:
        st.session_state.event_log = []
    
    # Add event listener
    def log_event(event_type, data):
        st.session_state.event_log.append(f"{event_type}: {data}")
    
    # Subscribe to all events
    event_bus = state_manager.get_event_bus()
    for event_type in ["analysis_complete", "code_parsed", "optimization_complete", "performance_test_complete"]:
        event_bus.subscribe(event_type, lambda data, event=event_type: log_event(event, data))
    
    # Display event log
    for event in st.session_state.event_log:
        st.sidebar.text(event)

if __name__ == "__main__":
    main()
