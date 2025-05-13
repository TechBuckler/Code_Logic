"""
Hierarchical Logic Tool Application

This is the main entry point for the Logic Tool using the hierarchical module system.
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
        
        # Load core modules
        self.load_core_modules()
    
    def load_core_modules(self):
        """Load the core modules of the application"""
        
        # Create core modules
        self.analysis_core = AnalysisCoreModule(self)
        self.optimization_core = OptimizationCoreModule(self)
    
    def handle_navigation(self, data):
        """Handle navigation events"""
        if isinstance(data, dict) and "page" in data:
            st.session_state.page = data["page"]
    
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
        - **Optimization**: Test and optimize code for better performance
        
        Use the sidebar to navigate between different modules.
        """)
        
        # Display module cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Analysis")
            st.markdown("Analyze code structure and logic")
            if st.button("Go to Analysis", key=state_manager.register_ui_key("home_analysis")):
                self.event_bus.publish("navigate", {"page": "analysis"})
        
        with col2:
            st.markdown("### Optimization")
            st.markdown("Test and optimize code performance")
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
    
    # Log events
    def log_event(event_type, data):
        if isinstance(data, dict):
            data_str = ", ".join([f"{k}: {v}" for k, v in data.items()])
        else:
            data_str = str(data)
        st.session_state.event_log.append(f"{event_type}: {data_str}")
    
    # Subscribe to all events
    event_bus = state_manager.get_event_bus()
    for event_type in ["navigate", "analysis_complete", "optimization_complete"]:
        event_bus.subscribe(event_type, lambda data, event=event_type: log_event(event, data))

if __name__ == "__main__":
    main()
