"""
New Unified UI - Redesigned UI with improved architecture
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Import existing modules directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.code_analysis_module import CodeAnalysisModule
from modules.runtime_optimization_module import RuntimeOptimizationModule
from modules.custom_function_module import CustomFunctionModule
from modules.project_organizer_module import ProjectOrganizerModule
from modules.module_explorer_module import ModuleExplorerModule
from modules.optimization_testbed_module import OptimizationTestbedModule

def initialize_session_state():
    """Initialize session state variables"""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.modules = {}
        st.session_state.background_system = None

def initialize_modules():
    """Initialize all modules"""
    # Initialize background system
    if not st.session_state.background_system:
        st.session_state.background_system = BackgroundSystem()
        
    # Initialize module registry
    module_registry = ModuleRegistry()
    
    # Initialize and register modules
    modules = {
        "code_analysis": CodeAnalysisModule(),
        "runtime_optimization": RuntimeOptimizationModule(),
        "custom_function": CustomFunctionModule(),
        "project_organizer": ProjectOrganizerModule(),
        "module_explorer": ModuleExplorerModule(),
        "optimization_testbed": OptimizationTestbedModule()
    }
    
    # Register modules with module registry
    for module_id, module in modules.items():
        module_registry.register_module(module_id, module)
        
        # Initialize module if it has an initialize method
        if hasattr(module, "initialize"):
            module.initialize()
    
    # Store modules in session state
    st.session_state.modules = modules
    
    # Update shared state with module status
    modules_status = {module_id: "Active" for module_id in modules.keys()}
    state_manager.get_shared_state().set("modules_status", modules_status)
    
    return modules

def register_ui_components(modules):
    """Register UI components for each module"""
    # Register tools with UI manager
    ui_manager.register_tool(
        "code_analysis", 
        "Code Analysis", 
        lambda: render_code_analysis(modules["code_analysis"]),
        category="Analysis",
        icon="🔍"
    )
    
    ui_manager.register_tool(
        "runtime_optimization", 
        "Runtime Optimization", 
        lambda: render_runtime_optimization(modules["runtime_optimization"]),
        category="Optimization",
        icon="⚡"
    )
    
    ui_manager.register_tool(
        "custom_function", 
        "Custom Function", 
        lambda: render_custom_function(modules["custom_function"]),
        category="Development",
        icon="🧩"
    )
    
    ui_manager.register_tool(
        "project_organizer", 
        "Project Organization", 
        lambda: render_project_organizer(modules["project_organizer"]),
        category="Project",
        icon="📁"
    )
    
    ui_manager.register_tool(
        "module_explorer", 
        "Module Explorer", 
        lambda: render_module_explorer(modules["module_explorer"]),
        category="Development",
        icon="🔎"
    )
    
    ui_manager.register_tool(
        "optimization_testbed", 
        "Optimization Testbed", 
        lambda: render_optimization_testbed(modules["optimization_testbed"]),
        category="Optimization",
        icon="🧪"
    )
    
    # Register results renderers
    ui_manager.register_results_renderer(
        "code_analysis_result",
        render_code_analysis_results
    )
    
    ui_manager.register_results_renderer(
        "optimization_result",
        render_optimization_results
    )
    
    ui_manager.register_results_renderer(
        "benchmark_result",
        render_benchmark_results
    )

# Module-specific rendering functions
def render_code_analysis(module):
    """Render Code Analysis UI"""
    st.title("Code Analysis")
    
    # Step 1: Code Input
    st.header("Step 1: Provide Code")
    
    # Code input method selection
    input_method = st.radio(
        "Code Input Method",
        ["Upload File", "Enter Code", "Select Example"],
        key=state_manager.register_ui_key("code_input_method")
    )
    
    source_code = None
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload Python file to analyze", 
            type=["py"],
            key=state_manager.register_ui_key("code_upload")
        )
        
        if uploaded_file:
            source_code = uploaded_file.getvalue().decode("utf-8")
            st.success("File uploaded successfully!")
            
    elif input_method == "Enter Code":
        source_code = st.text_area(
            "Enter Python code to analyze",
            height=300,
            key=state_manager.register_ui_key("code_input")
        )
        
    elif input_method == "Select Example":
        example = st.selectbox(
            "Select an example",
            ["Simple Function", "Recursive Function", "Class Example"],
            key=state_manager.register_ui_key("code_example")
        )
        
        if example == "Simple Function":
            source_code = """def calculate_factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
"""
        elif example == "Recursive Function":
            source_code = """def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""
        elif example == "Class Example":
            source_code = """class Calculator:
    def __init__(self):
        self.result = 0
        
    def add(self, a, b):
        self.result = a + b
        return self.result
        
    def multiply(self, a, b):
        self.result = a * b
        return self.result
"""
        
        if source_code:
            st.code(source_code, language="python")
    
    # Store code in shared state
    if source_code:
        state_manager.get_shared_state().set("source_code", source_code)
    
    # Step 2: Analysis Options
    if source_code:
        st.header("Step 2: Select Analysis Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            analyze_syntax = st.checkbox(
                "Syntax Analysis", 
                value=True,
                key=state_manager.register_ui_key("analyze_syntax")
            )
            
            analyze_complexity = st.checkbox(
                "Complexity Analysis", 
                value=True,
                key=state_manager.register_ui_key("analyze_complexity")
            )
        
        with col2:
            analyze_patterns = st.checkbox(
                "Pattern Analysis", 
                value=True,
                key=state_manager.register_ui_key("analyze_patterns")
            )
            
            analyze_optimization = st.checkbox(
                "Optimization Opportunities", 
                value=True,
                key=state_manager.register_ui_key("analyze_optimization")
            )
        
        # Step 3: Run Analysis
        if st.button(
            "Run Analysis", 
            key=state_manager.register_ui_key("run_analysis"),
            use_container_width=True
        ):
            with st.spinner("Analyzing code..."):
                # Prepare analysis options
                options = {
                    "syntax": analyze_syntax,
                    "complexity": analyze_complexity,
                    "patterns": analyze_patterns,
                    "optimization": analyze_optimization
                }
                
                # Run analysis
                result = module.process({
                    "command": "analyze",
                    "source_code": source_code,
                    "options": options
                })
                
                # Store result in shared state
                result["type"] = "code_analysis_result"
                state_manager.get_shared_state().set("active_results", result)
        
        # Step 4: View Results
        st.header("Step 3: Analysis Results")
        
        # Get results from shared state
        results = state_manager.get_shared_state().get("active_results", {})
        
        # Render results if available
        if results and results.get("type") == "code_analysis_result":
            render_code_analysis_results(results)

def render_code_analysis_results(results):
    """Render Code Analysis Results"""
    if "error" in results:
        st.error(results["error"])
        return
    
    # Display syntax analysis
    if "syntax" in results:
        st.subheader("Syntax Analysis")
        syntax = results["syntax"]
        
        if syntax["valid"]:
            st.success("✅ Code is syntactically valid")
        else:
            st.error(f"❌ Syntax error: {syntax['error']}")
            
        # Display AST structure
        if "ast_summary" in syntax:
            with st.expander("Abstract Syntax Tree (AST) Summary"):
                st.code(syntax["ast_summary"], language="python")
    
    # Display complexity analysis
    if "complexity" in results:
        st.subheader("Complexity Analysis")
        complexity = results["complexity"]
        
        # Create metrics for complexity scores
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Cyclomatic Complexity", complexity["cyclomatic_complexity"])
            
        with col2:
            st.metric("Cognitive Complexity", complexity["cognitive_complexity"])
            
        with col3:
            st.metric("Halstead Complexity", complexity["halstead_complexity"])
            
        # Display complexity details
        with st.expander("Complexity Details"):
            st.write(f"**Lines of Code:** {complexity['loc']}")
            st.write(f"**Number of Functions:** {complexity['num_functions']}")
            st.write(f"**Number of Classes:** {complexity['num_classes']}")
            
            if "function_complexity" in complexity:
                st.write("**Function Complexity:**")
                for func, score in complexity["function_complexity"].items():
                    st.write(f"- {func}: {score}")
    
    # Display pattern analysis
    if "patterns" in results:
        st.subheader("Pattern Analysis")
        patterns = results["patterns"]
        
        if patterns["identified_patterns"]:
            for pattern in patterns["identified_patterns"]:
                st.write(f"- **{pattern['name']}**: {pattern['description']}")
                st.code(pattern["code_snippet"], language="python")
        else:
            st.info("No specific patterns identified")
    
    # Display optimization opportunities
    if "optimization" in results:
        st.subheader("Optimization Opportunities")
        optimization = results["optimization"]
        
        if optimization["opportunities"]:
            for opportunity in optimization["opportunities"]:
                with st.expander(f"{opportunity['title']} (Impact: {opportunity['impact']})"):
                    st.write(f"**Description:** {opportunity['description']}")
                    st.write(f"**Location:** {opportunity['location']}")
                    
                    if "before" in opportunity and "after" in opportunity:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Before:**")
                            st.code(opportunity["before"], language="python")
                            
                        with col2:
                            st.write("**After:**")
                            st.code(opportunity["after"], language="python")
        else:
            st.info("No optimization opportunities identified")

# Import the rest of the module-specific rendering functions

def run_ui():
    """Main function to run the UI"""
    # Set page config
    st.set_page_config(
        page_title="Logic Tool",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize modules
    modules = initialize_modules()
    
    # Register UI components
    register_ui_components(modules)
    
    # Render UI
    ui_manager.render()
    
    # Cleanup on session end
    if hasattr(st, 'session_state') and 'initialized' not in st.session_state:
        # Perform cleanup
        pass

if __name__ == "__main__":
    run_ui()
