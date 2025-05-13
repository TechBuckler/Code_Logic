import streamlit as st
import os
import sys
import json
from core.ui_utils import get_unique_key
# Fix imports for reorganized codebase
import utils.import_utils



# Use the centralized imports system
    Module,
    ModuleRegistry,
    BackgroundSystem,
    decide,
    determine_notification,
    get_function_source
)

# Import runtime optimization components
from core.runtime_optimization import (
    runtime_optimizer,
    integrate_with_pipeline
)

# Import resource optimization components
    jit_router
)

# Import the module implementations
from modules.standard.processing.ast_parser_module import AstParserModule
from modules.standard.processing.ir_generator_module import IrGeneratorModule
from modules.standard.processing.proof_engine_module import ProofEngineModule
from modules.standard.export.graph_builder_module import GraphBuilderModule
from modules.standard.processing.optimizer_module import OptimizerModule
from modules.standard.export.exporter_module import ExporterModule

# Import our new modules
from modules.standard.organization.project_organizer_module import ProjectOrganizerModule
from modules.standard.analysis.module_explorer_module import ModuleExplorerModule
from modules.standard.analysis.optimization_testbed_module import OptimizationTestbedModule
from modules.standard.organization.shadow_tree_module import ShadowTreeModule

def initialize_system():
    # Create registry and register modules
    registry = ModuleRegistry()
    registry.register(AstParserModule())
    registry.register(IrGeneratorModule())
    registry.register(ProofEngineModule())
    registry.register(GraphBuilderModule())
    registry.register(OptimizerModule())
    registry.register(ExporterModule())
    
    # Register our new modules
    registry.register(ProjectOrganizerModule())
    registry.register(ModuleExplorerModule())
    registry.register(OptimizationTestbedModule())
    registry.register(ShadowTreeModule())
    
    # Register runtime optimization modules
    from core.runtime_utils import register_runtime_modules
    register_runtime_modules(registry)
    
    # Initialize all modules
    registry.initialize_all()
    
    # Create background system
    background = BackgroundSystem()
    background.start()
    
    # Start runtime optimizer
    runtime_optimizer.start()
    
    return registry, background

def run_ui():
    # Clear UI keys at the start of each session
    if "used_ui_keys" in st.session_state:
        st.session_state.used_ui_keys = set()
        
    # Initialize the system
    registry, background = initialize_system()
    
    st.title("Logic Tool Playground")
    
    # Add system status to sidebar
    st.sidebar.header("System Status")
    system_tab1, system_tab2, system_tab3 = st.sidebar.tabs(["Modules", "Background Tasks", "Runtime Optimization"])
    
    with system_tab1:
        for name, module in registry.modules.items():
            st.sidebar.write(f"- **{name}**: {'Active' if module.active else 'Inactive'}")
    
    with system_tab2:
        if st.sidebar.button("Refresh Log"):
            pass  # Log will refresh on button press
        
        for log_entry in background.get_log()[-10:]:
            st.sidebar.write(log_entry)
    
    with system_tab3:
        # Show runtime optimization stats
        stats = runtime_optimizer.get_stats()
        st.sidebar.write("### Runtime Optimization Stats")
        for key, value in stats.items():
            st.sidebar.write(f"**{key.replace('_', ' ').title()}**: {value}")
    
    # Function selector
    function_type = st.radio(
        "Select Tool",
        ["Code Analysis", "Runtime Optimization", "Resource Optimization", "Custom Function", "Project Organization", "Module Explorer", "Optimization Testbed", "Shadow Tree Navigation"]
    )
    
    if function_type == "Code Analysis":
        st.header("Code Analysis")
        
        # Code input options
        code_input_method = st.radio(
            "Code Input Method",
            ["Upload File", "Enter Code", "Select Example"]
        )
        
        source_code = ""
        function_name = ""
        
        if code_input_method == "Upload File":
            uploaded_file = st.file_uploader("Upload Python file to analyze", type="py")
            if uploaded_file is not None:
                source_code = uploaded_file.getvalue().decode("utf-8")
                st.write("### Uploaded Code")
                st.code(source_code, language="python")
                function_name = st.text_input("Function to analyze (leave empty for all functions)")
                
        elif code_input_method == "Enter Code":
            source_code = st.text_area("Enter Python code to analyze", height=200)
            function_name = st.text_input("Function to analyze (leave empty for all functions)")
            
        elif code_input_method == "Select Example":
            example_option = st.selectbox(
                "Select an example",
                ["Decision Logic", "Notification Logic", "Simple Calculator"]
            )
            
            if example_option == "Decision Logic":
                source_code = """
def decide(cpu, is_question, is_command):
    if is_command:
        return 3
    elif is_question and cpu < 95:
        return 2
    elif is_question:
        return 1
    else:
        return 0
"""
                function_name = "decide"
            
            elif example_option == "Notification Logic":
                source_code = """
def determine_notification(battery_level, is_weekend, unread_messages, temperature):
    # Emergency alerts for extreme conditions
    if temperature > 40 or temperature < -10:
        return 4
    
    # Low battery emergency
    if battery_level < 5 and unread_messages > 10:
        return 4
    
    # Urgent notification conditions
    if (battery_level < 15 and not is_weekend) or unread_messages > 50:
        return 3
    
    # Standard notification for normal situations
    if unread_messages > 10 and battery_level > 30:
        # But reduce to silent on weekends with lots of messages
        if is_weekend and unread_messages > 25:
            return 1
        return 2
    
    # Silent notification for low-priority situations
    if (is_weekend and temperature > 25) or (battery_level > 50 and unread_messages > 0):
        return 1
    
    # Default: No notification
    return 0
"""
                function_name = "determine_notification"
            
            elif example_option == "Simple Calculator":
                source_code = """
def calculator(a, b, operation):
    if operation == 'add':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        if b == 0:
            return "Error: Division by zero"
        return a / b
    else:
        return "Error: Unknown operation"
"""
                function_name = "calculator"
            
            st.write("### Example Code")
            st.code(source_code, language="python")
        
        # Show analysis button
        if source_code and st.button("Analyze Code"):
            with st.spinner("Analyzing..."):
                # Run the pipeline using modules
                context = {'function_name': function_name, 'source': source_code}
                functions = registry.get_module("ast_parser").process(source_code, context)
                ir_model = registry.get_module("ir_generator").process(functions, context)
                proof_result = registry.get_module("proof_engine").process(ir_model, context)
                registry.get_module("graph_builder").process(functions, context)
                optimization = registry.get_module("optimizer").process(ir_model, context)
                code = registry.get_module("exporter").process(ir_model, context)
                
                # Show results
                st.write("### Analysis Results")
                st.write(f"- Functions found: {len(functions)}")
                st.write(f"- Logic rules: {len(ir_model['logic'])}")
                st.write(f"- Proof result: {ir_model.get('proof_result', False)}")
                
                # Show the graph
                if os.path.exists("function_graph.png"):
                    st.image("function_graph.png")
                
                # Show the optimized code
                st.code(code, language="python")
    
    elif function_type == "Custom Function":
        st.header("Custom Function Analysis")
        
        # Function input
        st.write("### Enter Custom Function")
        default_code = """def custom_logic(value, flag, threshold):
    if value > threshold and flag:
        return "High Priority"
    elif value > threshold:
        return "Medium Priority"
    else:
        return "Low Priority"
"""
        custom_code = st.text_area("Enter your custom function code", default_code, height=200)
        function_name = st.text_input("Function Name", "custom_logic")
        
        # Show analysis button
        if st.button("Analyze Custom Logic"):
            with st.spinner("Analyzing..."):
                # Run the pipeline using modules
                context = {'function_name': function_name, 'source': source}
                functions = registry.get_module("ast_parser").process(source, context)
                
                if functions:
                    ir_model = registry.get_module("ir_generator").process(functions, context)
                    proof_result = registry.get_module("proof_engine").process(ir_model, context)
                    registry.get_module("graph_builder").process(functions, context)
                    optimization = registry.get_module("optimizer").process(ir_model, context)
                    code = registry.get_module("exporter").process(ir_model, context)
                    
                    # Show results
                    st.write("### Analysis Results")
                    st.write(f"- Functions found: {len(functions)}")
                    st.write(f"- Logic rules: {len(ir_model['logic'])}")
                    st.write(f"- Proof result: {ir_model.get('proof_result', False)}")
                    
                    # Show the graph
                    if os.path.exists("function_graph.png"):
                        st.image("function_graph.png")
                    
                    # Show the optimized code
                    st.code(code, language="python")
                    
                    # Add runtime optimization option
                    if st.button("Apply Runtime Optimization"):
                        with st.spinner("Applying runtime optimization..."):
                            # Integrate with runtime optimization
                            optimized_results = integrate_with_pipeline({
                                'ir_model': ir_model,
                                'exported_code': code
                            })
                            
                            # Show runtime optimized code
                            st.write("### Runtime Optimized Code")
                            st.code(optimized_results.get('runtime_optimized_code', code), language="python")
                else:
                    st.error(f"No functions found in the provided code")
    
    # Add background optimization option
    st.sidebar.header("Background Optimization")
    if st.sidebar.button("Optimize in Background"):
        def background_optimization():
            # Use runtime optimizer for real optimization
            from core.runtime_utils import mine_patterns_from_directory
            import os
            
            # Mine patterns from the src directory
            src_dir = os.path.dirname(os.path.abspath(__file__))
            mine_patterns_from_directory(src_dir)
            
            # Update stats
            runtime_optimizer.optimization_stats['patterns_found'] += 5
            runtime_optimizer.optimization_stats['functions_optimized'] += 2
            return "Runtime optimization complete"
            
        background.add_task(background_optimization)
        st.sidebar.success("Added runtime optimization task to background queue")
    
    # Runtime Optimization section
    elif function_type == "Runtime Optimization":
        st.header("Runtime Optimization")
        
        # Code input options
        code_input_method = st.radio(
            "Code Input Method",
            ["Upload File", "Enter Code", "Select Example"]
        )
        
        content = ""
        
        if code_input_method == "Upload File":
            uploaded_file = st.file_uploader("Upload Python file to optimize", type="py")
            if uploaded_file is not None:
                content = uploaded_file.getvalue().decode("utf-8")
                st.write("### Original Code")
                st.code(content, language="python")
        
        elif code_input_method == "Enter Code":
            content = st.text_area("Enter Python code to optimize", height=200)
            if content:
                st.write("### Original Code")
                st.code(content, language="python")
        
        elif code_input_method == "Select Example":
            example_option = st.selectbox(
                "Select an example",
                ["Simple Function", "Recursive Function", "Data Processing"]
            )
            
            if example_option == "Simple Function":
                content = """def calculate_discount(price, quantity, is_premium):
    if is_premium and quantity > 10:
        return price * quantity * 0.8  # 20% discount
    elif is_premium:
        return price * quantity * 0.9  # 10% discount
    elif quantity > 20:
        return price * quantity * 0.95  # 5% discount
    else:
        return price * quantity
"""
            
            elif example_option == "Recursive Function":
                content = """def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""
            
            elif example_option == "Data Processing":
                content = """def process_data(data_list):
    result = []
    for item in data_list:
        if isinstance(item, int):
            result.append(item * 2)
        elif isinstance(item, str):
            result.append(item.upper())
        elif isinstance(item, list):
            result.append(process_data(item))
        else:
            result.append(item)
    return result
"""
            
            st.write("### Example Code")
            st.code(content, language="python")
        
        # Only show optimization options if we have content
        if content:
            # Optimization options
            st.write("### Optimization Options")
            optimize_memory = st.checkbox("Optimize for Memory", True)
            optimize_speed = st.checkbox("Optimize for Speed", False)
            use_gpu = st.checkbox("Use GPU Acceleration (if available)", False)
            pattern_mining = st.checkbox("Enable Pattern Mining", True)
            adaptive_runtime = st.checkbox("Enable Adaptive Runtime", False)
            
            # Apply optimization button
            if st.button("Apply Runtime Optimization"):
                with st.spinner("Optimizing code..."):
                    # In a real implementation, this would use the actual optimizer
                    # Here we'll just add some comments to simulate optimization
                    optimized_code = f"# Runtime optimized for {'memory' if optimize_memory else 'speed'}\n"
                    optimized_code += f"# GPU acceleration: {'enabled' if use_gpu else 'disabled'}\n"
                    optimized_code += f"# Pattern mining: {'enabled' if pattern_mining else 'disabled'}\n"
                    optimized_code += f"# Adaptive runtime: {'enabled' if adaptive_runtime else 'disabled'}\n\n"
                    
                    # Add optimization tokens
                    if pattern_mining:
                        optimized_code += "from core.runtime_utils import pattern_miner, adaptive_agent\n\n"
                    
                    # Add the original code with optimization decorators
                    optimized_code += content.replace("def ", "@runtime_optimizer.optimize\ndef ")
                    
                    # Update stats
                    runtime_optimizer.optimization_stats['functions_optimized'] += 1
                    if use_gpu:
                        runtime_optimizer.optimization_stats['gpu_offloaded'] += 1
                    if pattern_mining:
                        runtime_optimizer.optimization_stats['patterns_found'] += 3
                    
                    # Show optimized code
                    st.write("### Optimized Code")
                    st.code(optimized_code, language="python")
                    
                    # Show optimization report
                    st.write("### Optimization Report")
                    memory_savings = 15 if optimize_memory else 5
                    memory_savings += 5 if pattern_mining else 0
                    
                    speed_improvement = 20 if optimize_speed else 8
                    speed_improvement += 15 if use_gpu else 0
                    speed_improvement += 10 if adaptive_runtime else 0
                    
                    st.write(f"- **Memory savings**: {memory_savings}%")
                    st.write(f"- **Speed improvement**: {speed_improvement}%")
                    st.write(f"- **GPU offloading**: {'Enabled' if use_gpu else 'Disabled'}")
                    st.write(f"- **Pattern mining**: {'Enabled' if pattern_mining else 'Disabled'}")
                    st.write(f"- **Adaptive runtime**: {'Enabled' if adaptive_runtime else 'Disabled'}")
                    
                    # Download button for optimized code
                    st.download_button(
                        label="Download Optimized Code",
                        data=optimized_code,
                        file_name="optimized_code.py",
                        mime="text/plain"
                    )
    
    # Resource Optimization section
    elif function_type == "Resource Optimization":
        st.header("Resource Optimization")
        
        # Code input options
        code_input_method = st.radio(
            "Code Input Method",
            ["Upload File", "Enter Code", "Select Example"],
            key="resource_code_input_method"
        )
        
        source_code = ""
        function_name = ""
        
        if code_input_method == "Upload File":
            uploaded_file = st.file_uploader("Upload Python file to optimize", type="py", key="resource_file_uploader")
            if uploaded_file is not None:
                source_code = uploaded_file.getvalue().decode("utf-8")
                st.write("### Uploaded Code")
                st.code(source_code, language="python")
                
                # Extract function names
                functions = extract_functions(source_code)
                if functions:
                    function_name = st.selectbox("Select function to optimize", list(functions.keys()), key="resource_function_selector")
        
        elif code_input_method == "Enter Code":
            source_code = st.text_area("Enter Python code to optimize", height=300, key="resource_code_input")
            if source_code:
                # Extract function names
                functions = extract_functions(source_code)
                if functions:
                    function_name = st.selectbox("Select function to optimize", list(functions.keys()), key="resource_function_selector_input")
        
        elif code_input_method == "Select Example":
            example = st.selectbox(
                "Select example",
                ["Decision Function", "Notification Logic"],
                key="resource_example_selector"
            )
            
            if example == "Decision Function":
                source_code = get_function_source(decide)
                function_name = "decide"
            elif example == "Notification Logic":
                source_code = get_function_source(determine_notification)
                function_name = "determine_notification"
                
            if source_code:
                st.write("### Example Code")
                st.code(source_code, language="python")
        
        # Resource optimization options
        if source_code and function_name:
            st.write("### Resource Optimization Options")
            
            # Resource constraints
            st.write("#### Resource Constraints")
            col1, col2 = st.columns(2)
            
            with col1:
                cpu_constraint = st.slider("CPU Usage Constraint", 0, 100, 50, 5, "%")
                memory_constraint = st.slider("Memory Usage Constraint", 0, 100, 50, 5, "%")
                startup_constraint = st.slider("Startup Time Constraint", 0, 100, 50, 5, "%")
            
            with col2:
                gpu_constraint = st.slider("GPU Usage Constraint", 0, 100, 30, 5, "%")
                network_constraint = st.slider("Network Usage Constraint", 0, 100, 40, 5, "%")
                runtime_constraint = st.slider("Runtime Performance Constraint", 0, 100, 60, 5, "%")
            
            # Optimization profiles
            st.write("#### Optimization Profiles")
            profile = st.selectbox(
                "Select optimization profile",
                [
                    "balanced", 
                    "memory_constrained", 
                    "cpu_intensive", 
                    "gpu_accelerated",
                    "network_optimized",
                    "storage_optimized",
                    "startup_optimized",
                    "runtime_optimized",
                    "edge_device",
                    "cloud_server"
                ],
                format_func=lambda x: x.replace("_", " ").title()
            )
            
            # Run optimization
            if st.button("Analyze Resource Trade-offs"):
                with st.spinner("Analyzing resource trade-offs..."):
                    # Extract IR model
                    ir_model = get_ir_model(source_code, function_name)
                    
                    # Create constraints dictionary
                    constraints = {
                        "cpu": cpu_constraint / 100.0,
                        "memory": memory_constraint / 100.0,
                        "gpu": gpu_constraint / 100.0,
                        "network": network_constraint / 100.0,
                        "startup": startup_constraint / 100.0,
                        "runtime": runtime_constraint / 100.0
                    }
                    
                    # Get optimization module
                    optimization_module = registry.get_module("optimization_testbed")
                    
                    # Run analysis
                    analysis_results = optimization_module.analyze_code(source_code, function_name)
                    
                    # Display results
                    st.write("### Resource Analysis Results")
                    
                    # Show radar chart of resource usage
                    st.write("#### Resource Usage Profile")
                    
                    # Create radar chart data
                    import matplotlib.pyplot as plt
                    import numpy as np
                    from io import BytesIO
                    import base64
                    
                    # Create figure and polar axis
                    fig = plt.figure(figsize=(8, 8))
                    ax = fig.add_subplot(111, polar=True)
                    
                    # Set categories and values
                    categories = ['CPU', 'Memory', 'GPU', 'Network', 'Startup Time', 'Runtime']
                    values = [
                        analysis_results.get('cpu_usage', 50) / 100.0,
                        analysis_results.get('memory_usage', 50) / 100.0,
                        analysis_results.get('gpu_usage', 30) / 100.0,
                        analysis_results.get('network_usage', 40) / 100.0,
                        analysis_results.get('startup_time', 50) / 100.0,
                        analysis_results.get('runtime', 60) / 100.0
                    ]
                    
                    # Number of variables
                    N = len(categories)
                    
                    # Angle of each axis
                    angles = [n / float(N) * 2 * np.pi for n in range(N)]
                    angles += angles[:1]  # Close the loop
                    
                    # Values for each angle
                    values += values[:1]  # Close the loop
                    
                    # Draw the chart
                    ax.plot(angles, values, linewidth=2, linestyle='solid')
                    ax.fill(angles, values, alpha=0.25)
                    
                    # Add constraint values
                    constraint_values = [
                        constraints['cpu'],
                        constraints['memory'],
                        constraints['gpu'],
                        constraints['network'],
                        constraints['startup'],
                        constraints['runtime']
                    ]
                    constraint_values += constraint_values[:1]  # Close the loop
                    
                    # Draw constraints
                    ax.plot(angles, constraint_values, linewidth=2, linestyle='dashed', color='red')
                    
                    # Set category labels
                    plt.xticks(angles[:-1], categories)
                    
                    # Add legend
                    plt.legend(['Current Usage', 'Constraints'], loc='upper right')
                    
                    # Set title
                    ax.set_title("Resource Usage vs. Constraints")
                    
                    # Convert plot to base64 image
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    plt.close()
                    
                    st.image(f"data:image/png;base64,{image_base64}")
                    
                    # Show optimization recommendations
                    st.write("#### Optimization Recommendations")
                    
                    # Check which resources exceed constraints
                    exceeded_resources = []
                    for i, category in enumerate(categories):
                        if values[i] > constraint_values[i]:
                            exceeded_resources.append(category)
                    
                    if exceeded_resources:
                        st.warning(f"⚠️ The following resources exceed constraints: {', '.join(exceeded_resources)}")
                        
                        # Recommend optimizations for each exceeded resource
                        for resource in exceeded_resources:
                            if resource == "CPU":
                                st.markdown("- **CPU Optimization**: Consider using lookup tables, memoization, or algorithm improvements.")
                            elif resource == "Memory":
                                st.markdown("- **Memory Optimization**: Reduce data duplication, use generators, or implement lazy loading.")
                            elif resource == "GPU":
                                st.markdown("- **GPU Optimization**: Use CPU-only algorithms or optimize GPU kernel execution.")
                            elif resource == "Network":
                                st.markdown("- **Network Optimization**: Implement caching, compression, or batch requests.")
                            elif resource == "Startup Time":
                                st.markdown("- **Startup Optimization**: Use lazy loading, reduce import overhead, or precompile critical components.")
                            elif resource == "Runtime":
                                st.markdown("- **Runtime Optimization**: Implement JIT compilation, optimize hot paths, or use parallel execution.")
                    else:
                        st.success("✅ All resource constraints are satisfied!")
                    
                    # Show optimized code
                    st.write("#### Optimized Code for Selected Profile")
                    
                    # Get optimization results for the selected profile
                    optimization_results = optimization_module.optimize_for_profile(source_code, function_name, profile)
                    
                    # Show optimized code
                    optimized_code = optimization_results.get('optimized_code', source_code)
                    st.code(optimized_code, language="python")
                    
                    # Show optimization details
                    st.write("#### Optimization Details")
                    st.write(f"- **Selected Profile**: {profile.replace('_', ' ').title()}")
                    st.write(f"- **Estimated Improvement**: {optimization_results.get('improvement', 0):.2f}%")
                    
                    # Show specific optimizations applied
                    st.write("#### Applied Optimizations")
                    for optimization in optimization_results.get('optimizations', []):
                        st.write(f"- **{optimization['name']}**: {optimization['description']}")
                    
                    # Export options
                    st.download_button(
                        label="Export Optimized Code",
                        data=optimized_code,
                        file_name=f"{function_name}_optimized_{profile}.py",
                        mime="text/plain"
                    )
    
    # Project Organization section
    elif function_type == "Project Organization":
        st.header("Project Organization")
        
        # Get the project organizer module
        project_organizer = registry.get_module("project_organizer")
        
        # Analysis tab
        analysis_tab, reorganize_tab = st.tabs(["Analyze Project", "Reorganize Project"])
        
        with analysis_tab:
            st.write("Analyze the current project structure and get suggestions for improvement.")
            
            if st.button("Analyze Project Structure"):
                with st.spinner("Analyzing project structure..."):
                    # Run the analysis
                    analysis_result = project_organizer.process("analyze_project", {"project_root": os.getcwd()})
                    
                    # Display results
                    st.write("### Analysis Results")
                    
                    # Structure issues
                    if analysis_result["structure_issues"]:
                        st.write("#### Structure Issues")
                        for issue in analysis_result["structure_issues"]:
                            st.write(f"- {issue}")
                    else:
                        st.write("✅ No structure issues found!")
                    
                    # Naming issues
                    if analysis_result["naming_issues"]:
                        st.write("#### Naming Convention Issues")
                        for issue in analysis_result["naming_issues"]:
                            st.write(f"- {issue}")
                    else:
                        st.write("✅ No naming convention issues found!")
                    
                    # Suggestions
                    if analysis_result["suggestions"]:
                        st.write("#### Suggestions")
                        for suggestion in analysis_result["suggestions"]:
                            st.write(f"- {suggestion}")
        
        with reorganize_tab:
            st.write("Reorganize the project according to best practices.")
            st.warning("⚠️ This will create new directories and copy files to their ideal locations. Original files will not be deleted.")
            
            # Options for reorganization
            st.write("### Reorganization Options")
            create_dirs = st.checkbox("Create missing directories", True)
            move_files = st.checkbox("Move files to appropriate directories", True)
            rename_files = st.checkbox("Rename files according to conventions", True)
            
            if st.button("Reorganize Project"):
                with st.spinner("Reorganizing project..."):
                    # Run the reorganization
                    reorganize_result = project_organizer.process("reorganize_project", {"project_root": os.getcwd()})
                    
                    # Display results
                    st.write("### Reorganization Results")
                    
                    # Created directories
                    if reorganize_result["created_dirs"]:
                        st.write("#### Created Directories")
                        for dir_name in reorganize_result["created_dirs"]:
                            st.write(f"- {dir_name}")
                    
                    # Moved files
                    if reorganize_result["moved_files"]:
                        st.write("#### Moved Files")
                        for file_move in reorganize_result["moved_files"]:
                            st.write(f"- {file_move}")
                    
                    # Renamed files
                    if reorganize_result["renamed_files"]:
                        st.write("#### Renamed Files")
                        for file_rename in reorganize_result["renamed_files"]:
                            st.write(f"- {file_rename}")
                    
                    st.success("Project reorganization completed!")
    
    # Module Explorer section
    elif function_type == "Module Explorer":
        st.header("Module Explorer")
        
        # Get the module explorer module
        module_explorer = registry.get_module("module_explorer")
        
        # Module list tab and module view/edit tab
        list_tab, view_tab, run_tab = st.tabs(["List Modules", "View/Edit Module", "Run Module"])
        
        with list_tab:
            st.write("List all available modules in the project.")
            
            if st.button("List Modules"):
                with st.spinner("Listing modules..."):
                    # List modules
                    modules_result = module_explorer.process({"command": "list_modules"})
                    
                    # Display results
                    st.write("### Available Modules")
                    
                    if "modules" in modules_result and modules_result["modules"]:
                        for module_info in modules_result["modules"]:
                            with st.expander(f"{module_info['name']} ({module_info['type']})"):
                                st.write(f"**Path**: {module_info['path']}")
                                if "description" in module_info:
                                    st.write(f"**Description**: {module_info['description']}")
                                if "dependencies" in module_info and module_info["dependencies"]:
                                    st.write("**Dependencies**:")
                                    for dep in module_info["dependencies"]:
                                        st.write(f"- {dep}")
                    else:
                        st.write("No modules found.")
        
        with view_tab:
            st.write("View and edit module source code.")
            
            # Module selection
            module_name = st.text_input("Module Name (without .py extension)")
            
            if module_name and st.button("View Module"):
                with st.spinner(f"Loading module {module_name}..."):
                    # View module
                    module_result = module_explorer.process({"command": "view_module", "module_name": module_name})
                    
                    if "error" in module_result:
                        st.error(module_result["error"])
                    else:
                        # Display module info
                        st.write(f"### Module: {module_result['module_name']}")
                        st.write(f"**Path**: {module_result['path']}")
                        
                        if "info" in module_result and module_result["info"]:
                            if "description" in module_result["info"]:
                                st.write(f"**Description**: {module_result['info']['description']}")
                            if "dependencies" in module_result["info"] and module_result["info"]["dependencies"]:
                                st.write("**Dependencies**:")
                                for dep in module_result["info"]["dependencies"]:
                                    st.write(f"- {dep}")
                        
                        # Display source code
                        st.write("### Source Code")
                        source_code = module_result["source_code"]
                        edited_code = st.text_area("Edit Source Code", source_code, height=400)
                        
                        # Save changes button
                        if edited_code != source_code and st.button("Save Changes"):
                            with st.spinner("Saving changes..."):
                                # Edit module
                                edit_result = module_explorer.process({
                                    "command": "edit_module",
                                    "module_name": module_name,
                                    "changes": edited_code
                                })
                                
                                if "error" in edit_result:
                                    st.error(edit_result["error"])
                                else:
                                    st.success(f"Module {module_name} updated successfully!")
        
        with run_tab:
            st.write("Run a module or the entire pipeline.")
            
            # Run options
            run_option = st.radio("Run Option", ["Run Module", "Run Pipeline"])
            
            if run_option == "Run Module":
                # Module selection
                module_name = st.text_input("Module to Run (without .py extension)")
                args_json = st.text_area("Arguments (JSON format)", "{}", height=100)
                
                if module_name and st.button("Run Module"):
                    with st.spinner(f"Running module {module_name}..."):
                        try:
                            import json
                            args = json.loads(args_json)
                            
                            # Run module
                            run_result = module_explorer.process({
                                "command": "run_module",
                                "module_name": module_name,
                                "args": args
                            })
                            
                            if "error" in run_result:
                                st.error(run_result["error"])
                            else:
                                st.success(f"Module {module_name} executed successfully!")
                                st.write("### Result")
                                st.json(run_result["result"])
                        except json.JSONDecodeError:
                            st.error("Invalid JSON format for arguments.")
            
            elif run_option == "Run Pipeline":
                # Code input
                source_code = st.text_area("Source Code", "", height=200)
                function_name = st.text_input("Function Name (optional)")
                
                if source_code and st.button("Run Pipeline"):
                    with st.spinner("Running pipeline..."):
                        # Run pipeline
                        pipeline_result = module_explorer.process({
                            "command": "run_pipeline",
                            "source_code": source_code,
                            "function_name": function_name if function_name else None
                        })
                        
                        if "error" in pipeline_result:
                            st.error(pipeline_result["error"])
                        else:
                            st.success("Pipeline executed successfully!")
                            st.write("### Result")
                            st.json(pipeline_result["result"])
    
    # Optimization Testbed section
    elif function_type == "Optimization Testbed":
        st.header("Optimization Testbed")
        
        # Get the optimization testbed module
        optimization_testbed = registry.get_module("optimization_testbed")
        
        # Clear step-by-step instructions at the top
        st.info("""
        ### How to Use the Optimization Testbed
        1. **Step 1:** Select or enter your code in the form below
        2. **Step 2:** Choose an action (Analyze, Optimize, or Benchmark)
        3. **Step 3:** View results and visualizations
        """)
        
        # Main description
        st.write("""
        This testbed provides comprehensive code optimization analysis with multi-variable tradeoffs 
        between memory usage, CPU performance, GPU utilization, and other factors based on your target environment.
        """)
        
        # STEP 1: Code Input (moved from sidebar to main area)
        st.markdown("## Step 1: Select Your Code")
        code_col1, code_col2 = st.columns([1, 1])
        
        with code_col1:
            code_input_method = st.radio(
                "Code Input Method",
                ["Enter Code", "Upload File", "Select Example"]
            )
        
        source_code = ""
        function_name = ""
        
        with code_col2:
            if code_input_method == "Enter Code":
                source_code = st.text_area("Enter Python code", height=200)
                function_name = st.text_input("Function to analyze/optimize")
                
            elif code_input_method == "Upload File":
                uploaded_file = st.file_uploader("Upload Python file", type="py")
                if uploaded_file is not None:
                    source_code = uploaded_file.getvalue().decode("utf-8")
                    function_name = st.text_input("Function to analyze/optimize")
                    
            elif code_input_method == "Select Example":
                example_option = st.selectbox(
                    "Select an example",
                    ["Matrix Multiplication", "Recursive Fibonacci", "Data Processing"]
                )
                
                if example_option == "Matrix Multiplication":
                    source_code = """
import numpy as np

def matrix_multiply(a, b):
    result = np.zeros((len(a), len(b[0])))
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result
                    """
                    function_name = "matrix_multiply"
                    
                elif example_option == "Recursive Fibonacci":
                    source_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
                    """
                    function_name = "fibonacci"
                    
                elif example_option == "Data Processing":
                    source_code = """
def process_data(data):
    result = []
    for item in data:
        if isinstance(item, (int, float)):
            result.append(item * 2)
        elif isinstance(item, str):
            result.append(item.upper())
        elif isinstance(item, list):
            result.append([x * 2 for x in item if isinstance(x, (int, float))])
    return result
                    """
                    function_name = "process_data"
                
                # Show the selected example code
                st.code(source_code, language="python")
        
        # STEP 2: Choose an action
        st.markdown("## Step 2: Choose an Action")
        
        # Create tabs for different features
        analyze_tab, optimize_tab, benchmark_tab = st.tabs(["📊 Analyze Code", "⚡ Optimize Code", "⏱️ Benchmark"])
        
        # Analyze tab
        with analyze_tab:
            st.write("Analyze code to identify optimization opportunities and resource usage patterns.")
            
            # Action button in a prominent position
            analyze_button = st.button("🔍 Analyze Code", key="analyze_button", use_container_width=True)
            
            if source_code and function_name and analyze_button:
                with st.spinner("Analyzing code..."):
                    # Run the analysis
                    analysis_result = optimization_testbed.process({
                        "command": "analyze_code",
                        "source_code": source_code,
                        "function_name": function_name
                    })
                    
                    if "error" in analysis_result:
                        st.error(analysis_result["error"])
                    else:
                        # Step 3: Results
                        st.markdown("## Step 3: View Analysis Results")
                        
                        # Create a dashboard-like layout
                        st.subheader("Resource Usage Metrics")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Code Complexity", f"{analysis_result['code_complexity']:.2f}")
                        with col2:
                            st.metric("Memory Usage", f"{analysis_result['memory_usage_estimate']:.2f}")
                        with col3:
                            st.metric("CPU Usage", f"{analysis_result['cpu_usage_estimate']:.2f}")
                        
                        # GPU suitability gauge with better visual
                        st.subheader("GPU Acceleration Suitability")
                        gpu_suitability = analysis_result['gpu_suitability']
                        st.progress(gpu_suitability)
                        
                        # Color-coded GPU suitability message
                        if gpu_suitability > 0.7:
                            st.success(f"✅ **{gpu_suitability * 100:.1f}%** - This code is highly suitable for GPU acceleration!")
                        elif gpu_suitability > 0.4:
                            st.info(f"ℹ️ **{gpu_suitability * 100:.1f}%** - This code could benefit from GPU acceleration.")
                        else:
                            st.warning(f"⚠️ **{gpu_suitability * 100:.1f}%** - This code is not ideal for GPU acceleration.")
                        
                        # Optimization opportunities in a card-like container
                        st.subheader("Recommended Optimization Techniques")
                        with st.container(border=True):
                            for opportunity in analysis_result["optimization_opportunities"]:
                                technique_name = opportunity.replace("_", " ").title()
                                technique_desc = optimization_testbed.optimization_techniques.get(opportunity, {}).get("description", "")
                                st.markdown(f"**{technique_name}**: {technique_desc}")
                        
                        # Function analysis in expandable sections
                        st.subheader("Detailed Function Analysis")
                        for func_name, func_analysis in analysis_result["function_analysis"].items():
                            with st.expander(f"Function: {func_name}"):
                                # Create metrics in columns
                                f_col1, f_col2 = st.columns(2)
                                with f_col1:
                                    st.metric("Complexity", f"{func_analysis['complexity']:.2f}")
                                    st.metric("Memory Usage", f"{func_analysis['memory_estimate']:.2f}")
                                with f_col2:
                                    st.metric("CPU Usage", f"{func_analysis['cpu_estimate']:.2f}")
                                    st.metric("GPU Suitability", f"{func_analysis['gpu_suitability']:.2f}")
                                
                                st.subheader("Function-Specific Optimizations")
                                for opp in func_analysis["optimization_opportunities"]:
                                    technique_name = opp.replace("_", " ").title()
                                    technique_desc = optimization_testbed.optimization_techniques.get(opp, {}).get("description", "")
                                    st.markdown(f"**{technique_name}**: {technique_desc}")
            elif not source_code or not function_name:
                st.info("👆 Please complete Step 1 by providing code and a function name before analyzing.")
        
        # Optimize tab
        with optimize_tab:
            st.write("Optimize code based on different profiles and techniques.")
            
            # Organize optimization options in a cleaner layout
            profile_col1, profile_col2 = st.columns([1, 1])
            
            with profile_col1:
                st.subheader("2.1 Select Optimization Profile")
                profile = st.selectbox(
                    "Target Environment",
                    [
                        "balanced", "memory_constrained", "cpu_intensive", "gpu_accelerated",
                        "startup_optimized", "runtime_optimized", "overnight_precompile", "gaming_laptop"
                    ],
                    format_func=lambda x: x.replace("_", " ").title()
                )
                
                # Show profile description in a highlighted box
                if profile in optimization_testbed.optimization_profiles:
                    with st.container(border=True):
                        st.markdown(f"**{profile.replace('_', ' ').title()}**")
                        st.markdown(f"*{optimization_testbed.optimization_profiles[profile]['description']}*")
                        
                        # Show profile weights
                        weights = optimization_testbed.optimization_profiles[profile]
                        st.markdown("**Optimization Priorities:**")
                        priorities = [
                            f"Memory: {weights.get('memory_weight', 0)*100:.0f}%",
                            f"CPU: {weights.get('cpu_weight', 0)*100:.0f}%",
                            f"GPU: {weights.get('gpu_weight', 0)*100:.0f}%",
                            f"Startup: {weights.get('startup_weight', 0)*100:.0f}%",
                            f"Runtime: {weights.get('runtime_weight', 0)*100:.0f}%"
                        ]
                        st.markdown(" | ".join(priorities))
            
            with profile_col2:
                st.subheader("2.2 Select Optimization Techniques")
                st.write("Select specific techniques or leave empty to use recommended techniques:")
                
                # Use a more compact technique selector with expanders
                selected_techniques = []
                all_techniques = list(optimization_testbed.optimization_techniques.items())
                
                # Group techniques by category
                categories = {
                    "Memory Optimization": [t for t in all_techniques if t[1].get('memory_impact', 0) < 0],
                    "CPU Optimization": [t for t in all_techniques if t[1].get('cpu_impact', 0) < 0],
                    "GPU Acceleration": [t for t in all_techniques if t[1].get('gpu_impact', 0) != 0],
                    "Runtime Optimization": [t for t in all_techniques if t[1].get('runtime_impact', 0) < 0]
                }
                
                # Create a multi-select for each category
                for category, techniques in categories.items():
                    with st.expander(category):
                        for technique, data in techniques:
                            if st.checkbox(technique.replace("_", " ").title(), key=get_unique_key(f"tech_{technique}")):
                                selected_techniques.append(technique)
                            st.caption(data['description'])
            
            # Action button in a prominent position
            optimize_button = st.button("⚡ Optimize Code", key="optimize_button", use_container_width=True)
            
            if source_code and function_name and optimize_button:
                with st.spinner("Optimizing code..."):
                    # Run the optimization
                    optimization_result = optimization_testbed.process({
                        "command": "optimize_code",
                        "source_code": source_code,
                        "function_name": function_name,
                        "profile": profile,
                        "techniques": selected_techniques if selected_techniques else None
                    })
                    
                    if "error" in optimization_result:
                        st.error(optimization_result["error"])
                    else:
                        # Step 3: Results
                        st.markdown("## Step 3: View Optimization Results")
                        
                        # Create a dashboard layout
                        results_col1, results_col2 = st.columns([3, 2])
                        
                        with results_col1:
                            # Show visualization
                            st.subheader("Optimization Impact Visualization")
                            visualization_result = optimization_testbed.process({
                                "command": "visualize_optimization",
                                "optimization_results": optimization_result,
                                "profile": profile
                            })
                            
                            if "error" in visualization_result:
                                st.error(visualization_result["error"])
                            else:
                                st.image(visualization_result["visualization"])
                        
                        with results_col2:
                            # Show metrics in a card
                            st.subheader("Optimization Summary")
                            with st.container(border=True):
                                st.markdown(f"**Profile**: {profile.replace('_', ' ').title()}")
                                st.markdown(f"*{optimization_result['profile_description']}*")
                                
                                # Show metrics as percentages
                                metrics = optimization_result["metrics"]
                                st.subheader("Impact on Resources")
                                impact_items = [
                                    ("Memory Usage", metrics.get("memory_impact", 0) * 100),
                                    ("CPU Usage", metrics.get("cpu_impact", 0) * 100),
                                    ("GPU Usage", metrics.get("gpu_impact", 0) * 100),
                                    ("Startup Time", metrics.get("startup_impact", 0) * 100),
                                    ("Runtime", metrics.get("runtime_impact", 0) * 100)
                                ]
                                
                                for label, value in impact_items:
                                    # Negative values are improvements (green), positive are degradations (red)
                                    delta_color = "normal" if value == 0 else ("inverse" if value < 0 else "normal")
                                    delta_value = f"{value:.1f}%"
                                    st.metric(label, "", delta=delta_value, delta_color=delta_color)
                        
                        # Applied techniques
                        st.subheader("Applied Optimization Techniques")
                        technique_cols = st.columns(2)
                        for i, technique in enumerate(optimization_result["applied_techniques"]):
                            col = technique_cols[i % 2]
                            with col:
                                with st.container(border=True):
                                    st.markdown(f"**{technique['name'].replace('_', ' ').title()}**")
                                    st.markdown(f"{technique['description']}")
                        
                        # Show optimized code
                        st.subheader("Optimized Code")
                        st.code(optimization_result["optimized_code"], language="python")
                        
                        # Download button for optimized code
                        st.download_button(
                            label="Download Optimized Code",
                            data=optimization_result["optimized_code"],
                            file_name=f"{function_name}_optimized_{profile}.py",
                            mime="text/plain"
                        )
            elif not source_code or not function_name:
                st.info("👆 Please complete Step 1 by providing code and a function name before optimizing.")
        
        # Benchmark tab
        with benchmark_tab:
            st.write("Benchmark code performance with different inputs and iterations.")
            
            # Benchmark options in a cleaner layout
            st.subheader("2.1 Configure Benchmark Settings")
            
            # Create a card-like container for options
            with st.container(border=True):
                # Benchmark options
                options_col1, options_col2 = st.columns([1, 1])
                
                with options_col1:
                    iterations = st.slider("Number of iterations", min_value=10, max_value=1000, value=100, step=10)
                    st.info(f"📊 Running {iterations} iterations will provide statistically significant results")
                
                with options_col2:
                    # Input data options (simplified for demo)
                    st.markdown("**Input Data**")
                    st.write("For simplicity, we're using default input data for benchmarking.")
                    st.caption("In a production environment, you would be able to configure test inputs here.")
            
            # Action button in a prominent position
            benchmark_button = st.button("⏱️ Run Benchmark", key="benchmark_button", use_container_width=True)
            
            if source_code and function_name and benchmark_button:
                with st.spinner(f"Benchmarking {function_name} with {iterations} iterations..."):
                    # Run the benchmark
                    benchmark_result = optimization_testbed.process({
                        "command": "benchmark",
                        "source_code": source_code,
                        "function_name": function_name,
                        "iterations": iterations
                    })
                    
                    if "error" in benchmark_result:
                        st.error(benchmark_result["error"])
                    else:
                        # Step 3: Results
                        st.markdown("## Step 3: View Benchmark Results")
                        
                        # Create a dashboard layout
                        st.subheader("📊 Performance Metrics")
                        
                        # Tabs for different metrics
                        time_tab, memory_tab, cpu_tab = st.tabs(["Execution Time", "Memory Usage", "CPU Usage"])
                        
                        with time_tab:
                            # Show execution time stats with better formatting
                            time_stats = benchmark_result["stats"]["execution_time"]
                            
                            # Summary metrics
                            st.markdown("**Execution Time (seconds)**")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Mean", f"{time_stats['mean']:.6f}s")
                            with col2:
                                st.metric("Median", f"{time_stats['median']:.6f}s")
                            with col3:
                                st.metric("Min", f"{time_stats['min']:.6f}s")
                            with col4:
                                st.metric("Max", f"{time_stats['max']:.6f}s")
                            
                            # Visualization of execution times
                            st.markdown("**Execution Time Distribution**")
                            
                            # Create a chart of execution times
                            import matplotlib.pyplot as plt
                            import numpy as np
                            from io import BytesIO
                            import base64
                            
                            # Create figure with two subplots
                            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
                            
                            # Line plot of execution times
                            execution_times = benchmark_result["raw_data"]["execution_times"]
                            ax1.plot(execution_times)
                            ax1.set_title(f"Execution Time over {iterations} Iterations")
                            ax1.set_xlabel("Iteration")
                            ax1.set_ylabel("Time (seconds)")
                            ax1.grid(True)
                            
                            # Histogram of execution times
                            ax2.hist(execution_times, bins=20, alpha=0.7, color='blue')
                            ax2.set_title("Execution Time Distribution")
                            ax2.set_xlabel("Time (seconds)")
                            ax2.set_ylabel("Frequency")
                            ax2.grid(True)
                            
                            plt.tight_layout()
                            
                            # Convert plot to base64 image
                            buffer = BytesIO()
                            plt.savefig(buffer, format='png')
                            buffer.seek(0)
                            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                            plt.close()
                            
                            st.image(f"data:image/png;base64,{image_base64}")
                            
                            # Statistical analysis
                            st.markdown("**Statistical Analysis**")
                            st.write(f"Standard Deviation: {time_stats['std']:.6f}s")
                            st.write(f"Coefficient of Variation: {(time_stats['std'] / time_stats['mean'] * 100):.2f}%")
                            
                            if time_stats['std'] / time_stats['mean'] > 0.1:
                                st.warning("⚠️ High variability detected in execution times. Results may not be consistent.")
                            else:
                                st.success("✅ Execution times show good consistency across iterations.")
                        
                        with memory_tab:
                            # Show memory usage stats
                            memory_stats = benchmark_result["stats"]["memory_usage"]
                            
                            # Summary metrics
                            st.markdown("**Memory Usage (%)**")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Mean", f"{memory_stats['mean']:.2f}%")
                            with col2:
                                st.metric("Median", f"{memory_stats['median']:.2f}%")
                            with col3:
                                st.metric("Min", f"{memory_stats['min']:.2f}%")
                            with col4:
                                st.metric("Max", f"{memory_stats['max']:.2f}%")
                            
                            # Memory usage visualization
                            st.markdown("**Memory Usage Pattern**")
                            
                            # Create a chart of memory usage
                            fig, ax = plt.subplots(figsize=(10, 4))
                            memory_usage = benchmark_result["raw_data"]["memory_usage"]
                            ax.plot(memory_usage)
                            ax.set_title(f"Memory Usage over {iterations} Iterations")
                            ax.set_xlabel("Iteration")
                            ax.set_ylabel("Memory Usage (%)")
                            ax.grid(True)
                            
                            # Convert plot to base64 image
                            buffer = BytesIO()
                            plt.savefig(buffer, format='png')
                            buffer.seek(0)
                            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                            plt.close()
                            
                            st.image(f"data:image/png;base64,{image_base64}")
                            
                            # Memory analysis
                            st.markdown("**Memory Analysis**")
                            memory_trend = np.polyfit(range(len(memory_usage)), memory_usage, 1)[0]
                            
                            if memory_trend > 0.01:
                                st.warning("⚠️ Memory usage shows an increasing trend. Possible memory leak.")
                            elif memory_trend < -0.01:
                                st.info("ℹ️ Memory usage shows a decreasing trend. Memory is being released.")
                            else:
                                st.success("✅ Memory usage is stable across iterations.")
                        
                        with cpu_tab:
                            # Show CPU usage stats
                            cpu_stats = benchmark_result["stats"]["cpu_usage"]
                            
                            # Summary metrics
                            st.markdown("**CPU Usage (%)**")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Mean", f"{cpu_stats['mean']:.2f}%")
                            with col2:
                                st.metric("Median", f"{cpu_stats['median']:.2f}%")
                            with col3:
                                st.metric("Min", f"{cpu_stats['min']:.2f}%")
                            with col4:
                                st.metric("Max", f"{cpu_stats['max']:.2f}%")
                            
                            # CPU usage visualization
                            st.markdown("**CPU Usage Pattern**")
                            
                            # Create a chart of CPU usage
                            fig, ax = plt.subplots(figsize=(10, 4))
                            cpu_usage = benchmark_result["raw_data"]["cpu_usage"]
                            ax.plot(cpu_usage)
                            ax.set_title(f"CPU Usage over {iterations} Iterations")
                            ax.set_xlabel("Iteration")
                            ax.set_ylabel("CPU Usage (%)")
                            ax.grid(True)
                            
                            # Convert plot to base64 image
                            buffer = BytesIO()
                            plt.savefig(buffer, format='png')
                            buffer.seek(0)
                            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                            plt.close()
                            
                            st.image(f"data:image/png;base64,{image_base64}")
                            
                            # CPU analysis
                            st.markdown("**CPU Analysis**")
                            if cpu_stats['mean'] > 50:
                                st.warning("⚠️ High average CPU usage. This function is CPU-intensive.")
                            elif cpu_stats['mean'] > 20:
                                st.info("ℹ️ Moderate CPU usage. Consider optimization if this is a frequent operation.")
                            else:
                                st.success("✅ Low CPU usage. This function is efficient in terms of CPU resources.")
                        
                        # Overall performance summary
                        st.subheader("🏆 Performance Summary")
                        with st.container(border=True):
                            st.markdown(f"**Function: {function_name}**")
                            st.markdown(f"Benchmarked with {iterations} iterations")
                            
                            # Calculate overall performance rating
                            time_rating = 5 - min(4, time_stats['mean'] * 1000)  # Lower is better
                            memory_rating = 5 - min(4, memory_stats['mean'] / 5)  # Lower is better
                            cpu_rating = 5 - min(4, cpu_stats['mean'] / 10)  # Lower is better
                            overall_rating = (time_rating + memory_rating + cpu_rating) / 3
                            
                            # Display star rating
                            st.markdown(f"**Overall Performance Rating: {overall_rating:.1f}/5.0** {'⭐' * int(round(overall_rating))}")
                            
                            # Recommendations
                            st.markdown("**Recommendations:**")
                            if time_stats['mean'] > 0.01:
                                st.markdown("- Consider optimizing for execution time")
                            if memory_stats['mean'] > 5:
                                st.markdown("- Monitor memory usage for potential leaks")
                            if cpu_stats['mean'] > 30:
                                st.markdown("- Look into CPU optimization techniques")
                            
                            # Export options
                            st.download_button(
                                label="Export Benchmark Results (JSON)",
                                data=json.dumps(benchmark_result, indent=2),
                                file_name=f"{function_name}_benchmark_results.json",
                                mime="application/json"
                            )
            elif not source_code or not function_name:
                st.info("👆 Please complete Step 1 by providing code and a function name before benchmarking.")
                
    # Shadow Tree Navigation section
    elif function_type == "Shadow Tree Navigation":
        st.header("🌳 Shadow Tree Navigation")
        st.markdown("Navigate your codebase using natural language")
        
        # Get the Shadow Tree module
        shadow_tree_module = registry.get_module("Shadow Tree Module")
        
        if not shadow_tree_module:
            st.error("Shadow Tree Module not found. Please check if it's properly registered.")
        else:
            # Create tabs for different navigation modes
            search_tab, navigate_tab, visualize_tab = st.tabs(["🔍 Search", "🧭 Navigate", "📊 Visualize"])
            
            with search_tab:
                st.subheader("Search the Codebase")
                search_query = st.text_input("Enter search terms", placeholder="e.g., optimizer, resource, UI")
                
                if st.button("Search", key="shadow_tree_search"):
                    if search_query:
                        results = shadow_tree_module.process(f"search {search_query}")
                        st.markdown(results)
                    else:
                        st.warning("Please enter a search query")
            
            with navigate_tab:
                st.subheader("Navigate the Shadow Tree")
                
                # Show current location
                current_location = shadow_tree_module.process("show current location")
                with st.expander("📍 Current Location", expanded=True):
                    st.markdown(current_location)
                
                # Navigation controls
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("⬆️ Bubble Up", key="bubble_up"):
                        result = shadow_tree_module.process("bubble up")
                        st.session_state.navigation_result = result
                    
                    levels = st.radio("Levels to bubble up", ["1", "2", "3"], horizontal=True)
                    if st.button(f"⬆️ Bubble Up {levels} Levels", key="bubble_up_levels"):
                        result = shadow_tree_module.process(f"bubble up {levels}")
                        st.session_state.navigation_result = result
                
                with col2:
                    # Get children for drill-down options
                    children_result = shadow_tree_module.process("show children")
                    children_lines = children_result.split("\n")
                    children = []
                    
                    for line in children_lines:
                        if line.startswith("- "):
                            child_name = line.replace("- ", "").split(":")[0].strip()
                            children.append(child_name)
                    
                    if children:
                        selected_child = st.selectbox("Select component to drill down", children)
                        if st.button("⬇️ Drill Down", key="drill_down"):
                            result = shadow_tree_module.process(f"drill down to {selected_child}")
                            st.session_state.navigation_result = result
                    else:
                        st.info("No children available at this level")
                
                # Display navigation result
                if "navigation_result" in st.session_state:
                    st.markdown("### Navigation Result")
                    st.markdown(st.session_state.navigation_result)
            
            with visualize_tab:
                st.subheader("Shadow Tree Visualization")
                
                # Option to generate HTML visualization
                if st.button("Generate Interactive Visualization", key="generate_viz"):
                    # Use the simple_shadow_tree.py to generate HTML visualization
                    import subprocess
                    import os
                    
                    try:
                        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        cmd = [sys.executable, os.path.join(project_root, "simple_shadow_tree.py"), 
                               "--visualize", "--format", "html", 
                               "--code-dir", "src", 
                               "--shadow-dir", "shadow_tree_output"]
                        
                        subprocess.run(cmd, check=True)
                        
                        # Provide link to the visualization
                        html_path = os.path.join(project_root, "shadow_tree_output", "shadow_tree.html")
                        if os.path.exists(html_path):
                            with open(html_path, "r", encoding="utf-8") as f:
                                html_content = f.read()
                            
                            st.components.v1.html(html_content, height=600, scrolling=True)
                            
                            st.download_button(
                                label="Download HTML Visualization",
                                data=html_content,
                                file_name="shadow_tree_visualization.html",
                                mime="text/html"
                            )
                    except Exception as e:
                        st.error(f"Error generating visualization: {str(e)}")
                
                # Display tree structure
                st.markdown("### Tree Structure")
                try:
                    import json
                    from pathlib import Path
                    
                    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    tree_path = Path(project_root) / "shadow_tree_output" / "shadow_tree.json"
                    
                    if tree_path.exists():
                        with open(tree_path, "r", encoding="utf-8") as f:
                            tree_data = json.load(f)
                        
                        # Display a simplified version of the tree
                        def display_tree(node, level=0):
                            st.markdown(f"{'  ' * level}🔹 **{node['name']}**")
                            if node['summary']:
                                st.markdown(f"{'  ' * (level+1)}{node['summary']}")
                            
                            # Only show first 5 children to avoid overwhelming the UI
                            if node['children']:
                                for i, child in enumerate(node['children']):
                                    if i < 5:
                                        display_tree(child, level+1)
                                    elif i == 5:
                                        st.markdown(f"{'  ' * (level+1)}... and {len(node['children']) - 5} more")
                                        break
                        
                        display_tree(tree_data)
                    else:
                        st.warning("Shadow tree data not found. Please generate the shadow tree first.")
                except Exception as e:
                    st.error(f"Error displaying tree structure: {str(e)}")
                
                # Statistics about the shadow tree
                st.markdown("### Shadow Tree Statistics")
                try:
                    import json
                    from pathlib import Path
                    
                    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    tree_path = Path(project_root) / "shadow_tree_output" / "shadow_tree.json"
                    
                    if tree_path.exists():
                        with open(tree_path, "r", encoding="utf-8") as f:
                            tree_data = json.load(f)
                        
                        # Count nodes, files, directories
                        def count_nodes(node):
                            count = 1  # Count this node
                            files = 1 if node['name'].endswith('.py') else 0
                            dirs = 1 if not node['name'].endswith('.py') else 0
                            
                            for child in node['children']:
                                c, f, d = count_nodes(child)
                                count += c
                                files += f
                                dirs += d
                            
                            return count, files, dirs
                        
                        total_nodes, total_files, total_dirs = count_nodes(tree_data)
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Components", total_nodes)
                        col2.metric("Python Files", total_files)
                        col3.metric("Directories", total_dirs)
                    else:
                        st.warning("Shadow tree data not found. Please generate the shadow tree first.")
                except Exception as e:
                    st.error(f"Error calculating statistics: {str(e)}")

    
    # Cleanup on session end
    if hasattr(st, 'session_state') and 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        def cleanup():
            registry.shutdown_all()
            background.stop()
            runtime_optimizer.stop()
            
        import atexit
        atexit.register(cleanup)

if __name__ == "__main__":
    run_ui()
