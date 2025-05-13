"""
New Main Application - Entry point for the Logic Tool with hierarchical architecture

This module serves as the main entry point for the Logic Tool, using the new
hierarchical architecture based on simple_hierarchical_core.py.
"""
# Fix imports for reorganized codebase
import utils.import_utils



import os
import sys
from typing import Dict, List, Any, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the hierarchical core using the flexible import system
try:
    # Try the new location first
    from modules.standard.simple_hierarchical_core import (
        HierarchicalModule, 
        Event, 
        EventBus, 
        StateStore, 
        ModuleRegistry,
        ui_key_manager
    )
except ImportError:
    try:
        # Fall back to the old location
        from core.simple_hierarchical_core import (
            HierarchicalModule, 
            Event, 
            EventBus, 
            StateStore, 
            ModuleRegistry,
            ui_key_manager
        )
    except ImportError:
        # Use the import_utils flexible import
        import utils.import_utils
        simple_hierarchical_core = utils.import_utils.import_module_flexible('core.simple_hierarchical_core')
        if simple_hierarchical_core:
            HierarchicalModule = simple_hierarchical_core.HierarchicalModule
            Event = simple_hierarchical_core.Event
            EventBus = simple_hierarchical_core.EventBus
            StateStore = simple_hierarchical_core.StateStore
            ModuleRegistry = simple_hierarchical_core.ModuleRegistry
            ui_key_manager = simple_hierarchical_core.ui_key_manager
        else:
            raise ImportError("Could not import simple_hierarchical_core from any location")

# Set up Streamlit page config if available
try:
    import streamlit as st
    st.set_page_config(
        page_title="Logic Tool",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except ImportError:
    # Streamlit not available, skip UI setup
    pass

class LogicToolApp(HierarchicalModule):
    """Main application module for the Logic Tool"""
    
    def __init__(self):
        super().__init__("LogicToolApp")
        self.registry = ModuleRegistry()
        self.registry.register_module(self)
        
        # Initialize session state for UI
        if "page" not in st.session_state:
            st.session_state.page = "home"
        
        # Subscribe to navigation events
        self.event_bus.subscribe("navigate", self.handle_navigation)
        
        # Load core modules
        self.load_core_modules()
    
    def load_core_modules(self):
        """Load the core modules of the application"""
        # Analysis Core
        self.analysis_core = AnalysisCoreModule("AnalysisCore", self)
        
        # Optimization Core
        self.optimization_core = OptimizationCoreModule("OptimizationCore", self)
        
        # Project Core
        self.project_core = ProjectCoreModule("ProjectCore", self)
        
        # UI Core
        self.ui_core = UICoreModule("UICore", self)
    
    def handle_navigation(self, event: Event):
        """Handle navigation events"""
        page = event.data.get("page")
        if page:
            st.session_state.page = page
    
    def render(self):
        """Render the main application UI"""
        # Render sidebar
        self.render_sidebar()
        
        # Render main content based on current page
        page = st.session_state.page
        
        if page == "home":
            self.render_home()
        elif page == "analysis":
            self.analysis_core.render()
        elif page == "optimization":
            self.optimization_core.render()
        elif page == "projects":
            self.project_core.render()
        else:
            st.error(f"Unknown page: {page}")
    
    def render_sidebar(self):
        """Render the application sidebar"""
        with st.sidebar:
            st.title("Logic Tool 🧠")
            st.markdown("---")
            
            # Navigation
            if st.button("Home", key=ui_key_manager.get_unique_key("nav_home")):
                self.event_bus.publish("navigate", {"page": "home"})
            
            if st.button("Analysis", key=ui_key_manager.get_unique_key("nav_analysis")):
                self.event_bus.publish("navigate", {"page": "analysis"})
            
            if st.button("Optimization", key=ui_key_manager.get_unique_key("nav_optimization")):
                self.event_bus.publish("navigate", {"page": "optimization"})
            
            if st.button("Projects", key=ui_key_manager.get_unique_key("nav_projects")):
                self.event_bus.publish("navigate", {"page": "projects"})
            
            st.markdown("---")
            st.text("Logic Tool v2.0")
    
    def render_home(self):
        """Render the home page"""
        st.title("Welcome to Logic Tool")
        st.markdown("""
        Logic Tool is a comprehensive environment for analyzing, optimizing, and managing code logic.
        
        ### Features:
        
        - **Analysis**: Parse and analyze code to understand its structure and logic
        - **Optimization**: Test and optimize code for better performance
        - **Project Management**: Manage your code projects and files
        
        Use the sidebar to navigate between different modules.
        """)
        
        # Display module cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Analysis")
            st.markdown("Analyze code structure and logic")
            if st.button("Go to Analysis", key=ui_key_manager.get_unique_key("home_analysis")):
                self.event_bus.publish("navigate", {"page": "analysis"})
        
        with col2:
            st.markdown("### Optimization")
            st.markdown("Test and optimize code performance")
            if st.button("Go to Optimization", key=ui_key_manager.get_unique_key("home_optimization")):
                self.event_bus.publish("navigate", {"page": "optimization"})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Projects")
            st.markdown("Manage your code projects")
            if st.button("Go to Projects", key=ui_key_manager.get_unique_key("home_projects")):
                self.event_bus.publish("navigate", {"page": "projects"})


class AnalysisCoreModule(HierarchicalModule):
    """Core module for code analysis functionality"""
    
    def __init__(self, module_id: str, parent=None):
        super().__init__(module_id, parent)
    
    def render(self):
        """Render the analysis module UI"""
        st.title("Code Analysis")
        st.markdown("""
        Analyze your code to understand its structure and logic.
        
        Upload a file or paste code to get started.
        """)
        
        # File upload
        uploaded_file = st.file_uploader("Upload a file", key=ui_key_manager.get_unique_key("analysis_upload"))
        
        # Code input
        code = st.text_area("Or paste your code here", height=300, key=ui_key_manager.get_unique_key("analysis_code"))
        
        if st.button("Analyze", key=ui_key_manager.get_unique_key("analysis_button")):
            if uploaded_file is not None:
                content = uploaded_file.getvalue().decode("utf-8")
                self.analyze_code(content)
            elif code:
                self.analyze_code(code)
            else:
                st.warning("Please upload a file or paste code to analyze")
    
    def analyze_code(self, code: str):
        """Analyze the provided code"""
        st.info("Analysis in progress...")
        
        # Placeholder for actual analysis
        st.success("Analysis complete!")
        
        # Display results
        st.subheader("Analysis Results")
        st.markdown("This is a placeholder for analysis results.")


class OptimizationCoreModule(HierarchicalModule):
    """Core module for code optimization functionality"""
    
    def __init__(self, module_id: str, parent=None):
        super().__init__(module_id, parent)
    
    def render(self):
        """Render the optimization module UI"""
        st.title("Code Optimization")
        st.markdown("""
        Test and optimize your code for better performance.
        
        Upload a file or paste code to get started.
        """)
        
        # File upload
        uploaded_file = st.file_uploader("Upload a file", key=ui_key_manager.get_unique_key("optimization_upload"))
        
        # Code input
        code = st.text_area("Or paste your code here", height=300, key=ui_key_manager.get_unique_key("optimization_code"))
        
        # Optimization options
        st.subheader("Optimization Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            optimize_time = st.checkbox("Optimize for Time", key=ui_key_manager.get_unique_key("opt_time"))
            optimize_memory = st.checkbox("Optimize for Memory", key=ui_key_manager.get_unique_key("opt_memory"))
        
        with col2:
            optimize_readability = st.checkbox("Maintain Readability", key=ui_key_manager.get_unique_key("opt_readability"))
            optimize_complexity = st.checkbox("Reduce Complexity", key=ui_key_manager.get_unique_key("opt_complexity"))
        
        if st.button("Optimize", key=ui_key_manager.get_unique_key("optimization_button")):
            if uploaded_file is not None:
                content = uploaded_file.getvalue().decode("utf-8")
                self.optimize_code(content, {
                    "time": optimize_time,
                    "memory": optimize_memory,
                    "readability": optimize_readability,
                    "complexity": optimize_complexity
                })
            elif code:
                self.optimize_code(code, {
                    "time": optimize_time,
                    "memory": optimize_memory,
                    "readability": optimize_readability,
                    "complexity": optimize_complexity
                })
            else:
                st.warning("Please upload a file or paste code to optimize")
    
    def optimize_code(self, code: str, options: Dict[str, bool]):
        """Optimize the provided code with the given options"""
        st.info("Optimization in progress...")
        
        # Placeholder for actual optimization
        st.success("Optimization complete!")
        
        # Display results
        st.subheader("Optimization Results")
        st.markdown("This is a placeholder for optimization results.")


class ProjectCoreModule(HierarchicalModule):
    """Core module for project management functionality"""
    
    def __init__(self, module_id: str, parent=None):
        super().__init__(module_id, parent)
        
        # Initialize project state
        if "projects" not in self.state_store.get("projects", {}):
            self.state_store.set("projects", {})
    
    def render(self):
        """Render the project module UI"""
        st.title("Project Management")
        st.markdown("""
        Manage your code projects and files.
        
        Create a new project or select an existing one.
        """)
        
        # Project creation
        with st.expander("Create New Project"):
            project_name = st.text_input("Project Name", key=ui_key_manager.get_unique_key("project_name"))
            project_desc = st.text_area("Project Description", key=ui_key_manager.get_unique_key("project_desc"))
            
            if st.button("Create Project", key=ui_key_manager.get_unique_key("create_project")):
                if project_name:
                    self.create_project(project_name, project_desc)
                else:
                    st.warning("Please enter a project name")
        
        # Project list
        st.subheader("Your Projects")
        projects = self.state_store.get("projects", {})
        
        if not projects:
            st.info("No projects yet. Create one to get started!")
        else:
            for project_id, project in projects.items():
                with st.expander(project["name"]):
                    st.markdown(f"**Description:** {project.get('description', 'No description')}")
                    st.markdown(f"**Created:** {project.get('created_at', 'Unknown')}")
                    
                    if st.button("Open Project", key=ui_key_manager.get_unique_key(f"open_{project_id}")):
                        self.open_project(project_id)
    
    def create_project(self, name: str, description: str):
        """Create a new project"""
        import datetime
        
        project_id = name.lower().replace(" ", "_")
        projects = self.state_store.get("projects", {})
        
        if project_id in projects:
            st.error(f"A project with the name '{name}' already exists")
            return
        
        projects[project_id] = {
            "id": project_id,
            "name": name,
            "description": description,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "files": []
        }
        
        self.state_store.set("projects", projects)
        st.success(f"Project '{name}' created successfully")
    
    def open_project(self, project_id: str):
        """Open an existing project"""
        projects = self.state_store.get("projects", {})
        
        if project_id not in projects:
            st.error(f"Project with ID '{project_id}' not found")
            return
        
        self.state_store.set("current_project", project_id)
        self.event_bus.publish("project_opened", {"project_id": project_id})


class UICoreModule(HierarchicalModule):
    """Core module for UI components and utilities"""
    
    def __init__(self, module_id: str, parent=None):
        super().__init__(module_id, parent)
    
    def render(self):
        """Render the UI module (not directly accessible)"""
        st.title("UI Components")
        st.markdown("""
        This module provides UI components and utilities for the Logic Tool.
        
        It is not directly accessible from the navigation menu.
        """)


def main():
    """Main entry point for the application"""
    # Create the main application
    app = LogicToolApp()
    
    # Initialize all modules
    app.initialize()
    
    # Render the application
    app.render()


if __name__ == "__main__":
    main()
