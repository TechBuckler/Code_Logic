"""
UI Components - Core components for the unified UI
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase




class NavigationComponent:
    """
    Handles navigation and tool selection in the UI
    """
    def __init__(self):
        self.event_bus = state_manager.get_event_bus()
        self.shared_state = state_manager.get_shared_state()
        
    def render_sidebar(self, tools: List[Dict[str, Any]]):
        """Render the sidebar navigation"""
        st.sidebar.title("Logic Tool")
        
        # Tool selection
        st.sidebar.subheader("Navigation")
        
        # Group tools by category
        tool_categories = {}
        for tool in tools:
            category = tool.get("category", "General")
            if category not in tool_categories:
                tool_categories[category] = []
            tool_categories[category].append(tool)
        
        # Display tools by category
        for category, category_tools in tool_categories.items():
            with st.sidebar.expander(category, expanded=True):
                for tool in category_tools:
                    tool_id = tool["id"]
                    tool_name = tool["name"]
                    tool_icon = tool.get("icon", "🔧")
                    
                    # Generate a unique key for this button
                    key = state_manager.register_ui_key(f"nav_{tool_id}")
                    
                    if st.button(f"{tool_icon} {tool_name}", key=key):
                        # Set the active tool in shared state
                        self.shared_state.set("active_tool", tool_id)
                        # Publish navigation event
                        self.event_bus.publish("navigation", {"tool_id": tool_id})
        
        # Additional sidebar components
        st.sidebar.divider()
        
        # System status
        if st.sidebar.checkbox("Show System Status", value=True, 
                               key=state_manager.register_ui_key("show_system_status")):
            st.sidebar.subheader("System Status")
            # Get status from shared state
            modules_status = self.shared_state.get("modules_status", {})
            for module, status in modules_status.items():
                st.sidebar.text(f"{module}: {status}")

class ContentComponent:
    """
    Handles the main content area of the UI
    """
    def __init__(self):
        self.event_bus = state_manager.get_event_bus()
        self.shared_state = state_manager.get_shared_state()
        self.content_renderers = {}
        
    def register_renderer(self, tool_id: str, renderer: Callable):
        """Register a content renderer for a specific tool"""
        self.content_renderers[tool_id] = renderer
        
    def render_content(self):
        """Render the main content area based on active tool"""
        # Get active tool from shared state
        active_tool = self.shared_state.get("active_tool")
        
        if active_tool and active_tool in self.content_renderers:
            # Render the content for the active tool
            self.content_renderers[active_tool]()
        else:
            # Default content
            st.title("Logic Tool Playground")
            st.write("Select a tool from the sidebar to get started.")
            
            # Quick access buttons
            st.subheader("Quick Start")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Code Analysis", 
                             key=state_manager.register_ui_key("quick_code_analysis")):
                    self.shared_state.set("active_tool", "code_analysis")
                    
            with col2:
                if st.button("Runtime Optimization", 
                             key=state_manager.register_ui_key("quick_runtime_optimization")):
                    self.shared_state.set("active_tool", "runtime_optimization")
                    
            with col3:
                if st.button("Optimization Testbed", 
                             key=state_manager.register_ui_key("quick_optimization_testbed")):
                    self.shared_state.set("active_tool", "optimization_testbed")

class ResultsComponent:
    """
    Handles the results display area of the UI
    """
    def __init__(self):
        self.event_bus = state_manager.get_event_bus()
        self.shared_state = state_manager.get_shared_state()
        self.results_renderers = {}
        
    def register_renderer(self, result_type: str, renderer: Callable):
        """Register a results renderer for a specific result type"""
        self.results_renderers[result_type] = renderer
        
    def render_results(self, container=None):
        """Render results in the specified container or create a new one"""
        # Get active results from shared state
        results = self.shared_state.get("active_results", {})
        result_type = results.get("type")
        
        if not container:
            container = st
            
        if result_type and result_type in self.results_renderers:
            # Render the results
            with container:
                self.results_renderers[result_type](results)
        elif results:
            # Default results rendering
            with container:
                st.subheader("Results")
                st.json(results)

class UIManager:
    """
    Main UI manager that combines all UI components
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UIManager, cls).__new__(cls)
            cls._instance.navigation = NavigationComponent()
            cls._instance.content = ContentComponent()
            cls._instance.results = ResultsComponent()
            cls._instance.event_bus = state_manager.get_event_bus()
            cls._instance.shared_state = state_manager.get_shared_state()
            cls._instance.tools = []
        return cls._instance
    
    def register_tool(self, tool_id: str, tool_name: str, 
                     content_renderer: Callable, category: str = "General",
                     icon: str = "🔧"):
        """Register a tool with the UI manager"""
        tool = {
            "id": tool_id,
            "name": tool_name,
            "category": category,
            "icon": icon
        }
        self.tools.append(tool)
        self.content.register_renderer(tool_id, content_renderer)
        
    def register_results_renderer(self, result_type: str, renderer: Callable):
        """Register a results renderer"""
        self.results.register_renderer(result_type, renderer)
        
    def render(self):
        """Render the complete UI"""
        # Render sidebar navigation
        self.navigation.render_sidebar(self.tools)
        
        # Render main content
        self.content.render_content()

# Singleton instance
ui_manager = UIManager()
