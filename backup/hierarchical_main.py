"""
Hierarchical Logic Tool - Main Application

This is the main entry point for the Logic Tool using the hierarchical module architecture.
It sets up the core modules and handles the main UI rendering.
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
    page_title="Logic Tool",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

class LogicToolApp(HierarchicalModule):
    """Main application module for the Logic Tool"""
    
    def __init__(self):
        super().__init__("logic_tool")
        self.hierarchy = ModuleHierarchy(self)
        
        # Initialize session state
        if "page" not in st.session_state:
            st.session_state.page = "home"
        
        if "event_log" not in st.session_state:
            st.session_state.event_log = []
        
        # Subscribe to navigation events
        self.event_bus.subscribe("navigate", self.handle_navigation)
        
        # Subscribe to all important events for logging
        for event_type in ["code_input_ready", "ast_parsing_complete", "ast_parsing_error", 
                          "ir_generation_complete", "ir_generation_error",
                          "optimization_complete", "optimization_error",
                          "proof_complete", "proof_error"]:
            self.event_bus.subscribe(event_type, self.log_event)
        
        # Load core modules
        self.load_core_modules()
    
    def load_core_modules(self):
        """Load the core modules of the application"""
        from modules.standard.analysis_core_module import AnalysisCoreModule
        from modules.standard.optimization_core_module import OptimizationCoreModule
        
        # Create core modules
        self.analysis_core = AnalysisCoreModule(self)
        self.optimization_core = OptimizationCoreModule(self)
    
    def handle_navigation(self, data):
        """Handle navigation events"""
        if isinstance(data, dict) and "page" in data:
            st.session_state.page = data["page"]
    
    def log_event(self, data):
        """Log an event to the event log"""
        event_type = getattr(data, "event_type", "unknown")
        if isinstance(data, dict):
            data_str = ", ".join([f"{k}: {v}" for k, v in data.items() if k != "code"])
        else:
            data_str = str(data)
        
        # Add to event log
        if len(st.session_state.event_log) >= 100:
            st.session_state.event_log.pop(0)  # Remove oldest event if log is too long
        st.session_state.event_log.append(f"{event_type}: {data_str}")
    
    def render_ui(self):
        """Render the main application UI"""
        # Render sidebar
        self.render_sidebar()
        
        # Render main content based on current page
        page = st.session_state.page
        
        if page == "home":
            self.render_home()
        elif page == "analysis":
            self.analysis_core.render_ui()
        elif page == "optimization":
            self.optimization_core.render_ui()
        else:
            st.error(f"Unknown page: {page}")
    
    def render_sidebar(self):
        """Render the application sidebar"""
        with st.sidebar:
            st.title("Logic Tool 🧠")
            st.markdown("---")
            
            # Navigation
            if st.button("Home", key=state_manager.register_ui_key("nav_home")):
                self.event_bus.publish("navigate", {"page": "home"})
            
            if st.button("Analysis", key=state_manager.register_ui_key("nav_analysis")):
                self.event_bus.publish("navigate", {"page": "analysis"})
            
            if st.button("Optimization", key=state_manager.register_ui_key("nav_optimization")):
                self.event_bus.publish("navigate", {"page": "optimization"})
            
            st.markdown("---")
            
            # Module hierarchy
            st.subheader("Module Hierarchy")
            
            # Display the module hierarchy as a tree
            modules = self.get_all_children(recursive=True)
            modules.insert(0, self)  # Add self to the list
            
            for module in modules:
                indent = "  " * (len(module.get_path()) - 1)
                st.text(f"{indent}📂 {module.name}")
            
            st.markdown("---")
            st.text("Logic Tool v2.0")
            
            # Event log
            if st.checkbox("Show Event Log", key=state_manager.register_ui_key("show_log")):
                st.subheader("Event Log")
                for event in st.session_state.event_log[-10:]:  # Show last 10 events
                    st.text(event)
    
    def render_home(self):
        """Render the home page"""
        st.title("Welcome to Logic Tool")
        st.markdown("""
        Logic Tool is a comprehensive environment for analyzing, optimizing, and managing code logic.
        
        ### Features:
        
        - **Analysis**: Parse and analyze code to understand its structure and logic
        - **IR Generation**: Generate Intermediate Representation models from code
        - **Visualization**: Visualize code structure and logic flow
        
        Use the sidebar to navigate between different modules.
        """)
        
        # Display module cards
        st.subheader("Core Modules")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Analysis")
            st.markdown("Analyze code structure and logic")
            if st.button("Go to Analysis", key=state_manager.register_ui_key("home_analysis")):
                self.event_bus.publish("navigate", {"page": "analysis"})
        
        with col2:
            st.markdown("### Optimization")
            st.markdown("Optimize and verify code logic")
            if st.button("Go to Optimization", key=state_manager.register_ui_key("home_optimization")):
                self.event_bus.publish("navigate", {"page": "optimization"})

def main():
    """Main entry point for the application"""
    # Create the main application
    app = LogicToolApp()
    
    # Initialize all modules
    app.initialize()
    
    # Render the application
    app.render_ui()

if __name__ == "__main__":
    main()
