"""
UI Renderers - Module-specific UI rendering functions
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import base64

# Import core components

def render_runtime_optimization(module):
    """Render Runtime Optimization UI"""
    st.title("Runtime Optimization")
    
    # Step 1: Code Input
    st.header("Step 1: Provide Code")
    
    # Code input method selection
    input_method = st.radio(
        "Code Input Method",
        ["Upload File", "Enter Code", "Select Example"],
        key=state_manager.register_ui_key("rt_code_input_method")
    )
    
    source_code = None
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload Python file to optimize", 
            type=["py"],
            key=state_manager.register_ui_key("rt_code_upload")
        )
        
        if uploaded_file:
            source_code = uploaded_file.getvalue().decode("utf-8")
            st.success("File uploaded successfully!")
            
    elif input_method == "Enter Code":
        source_code = st.text_area(
            "Enter Python code to optimize",
            height=300,
            key=state_manager.register_ui_key("rt_code_input")
        )
        
    elif input_method == "Select Example":
        example = st.selectbox(
            "Select an example",
            ["Loop Example", "Data Processing Example", "Recursive Example"],
            key=state_manager.register_ui_key("rt_code_example")
        )
        
        if example == "Loop Example":
            source_code = """def process_data(data):
    result = []
    for item in data:
        if item % 2 == 0:
            result.append(item * 2)
        else:
            result.append(item + 1)
    return result
"""
        elif example == "Data Processing Example":
            source_code = """def analyze_text(text):
    words = text.split()
    word_counts = {}
    for word in words:
        word = word.lower().strip('.,!?;:()"\'')
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return word_counts
"""
        elif example == "Recursive Example":
            source_code = """def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""
        
        if source_code:
            st.code(source_code, language="python")
    
    # Store code in shared state
    if source_code:
        state_manager.get_shared_state().set("rt_source_code", source_code)
    
    # Step 2: Optimization Options
    if source_code:
        st.header("Step 2: Select Optimization Options")
        
        # Function name input
        function_name = st.text_input(
            "Function to optimize (leave empty to optimize all)",
            key=state_manager.register_ui_key("rt_function_name")
        )
        
        # Optimization techniques
        st.subheader("Optimization Techniques")
        
        col1, col2 = st.columns(2)
        
        with col1:
            use_loop_optimization = st.checkbox(
                "Loop Optimization", 
                value=True,
                key=state_manager.register_ui_key("use_loop_optimization")
            )
            
            use_memoization = st.checkbox(
                "Memoization", 
                value=True,
                key=state_manager.register_ui_key("use_memoization")
            )
            
            use_parallelization = st.checkbox(
                "Parallelization", 
                value=False,
                key=state_manager.register_ui_key("use_parallelization")
            )
        
        with col2:
            use_data_structures = st.checkbox(
                "Data Structure Optimization", 
                value=True,
                key=state_manager.register_ui_key("use_data_structures")
            )
            
            use_algorithm_replacement = st.checkbox(
                "Algorithm Replacement", 
                value=True,
                key=state_manager.register_ui_key("use_algorithm_replacement")
            )
            
            use_code_generation = st.checkbox(
                "Code Generation", 
                value=False,
                key=state_manager.register_ui_key("use_code_generation")
            )
        
        # Optimization level
        optimization_level = st.slider(
            "Optimization Level",
            min_value=1,
            max_value=3,
            value=2,
            help="Higher levels apply more aggressive optimizations",
            key=state_manager.register_ui_key("optimization_level")
        )
        
        # Step 3: Run Optimization
        if st.button(
            "Optimize Code", 
            key=state_manager.register_ui_key("run_optimization"),
            use_container_width=True
        ):
            with st.spinner("Optimizing code..."):
                # Prepare optimization options
                options = {
                    "loop_optimization": use_loop_optimization,
                    "memoization": use_memoization,
                    "parallelization": use_parallelization,
                    "data_structures": use_data_structures,
                    "algorithm_replacement": use_algorithm_replacement,
                    "code_generation": use_code_generation,
                    "level": optimization_level
                }
                
                # Run optimization
                result = module.process({
                    "command": "optimize",
                    "source_code": source_code,
                    "function_name": function_name if function_name else None,
                    "options": options
                })
                
                # Store result in shared state
                result["type"] = "optimization_result"
                state_manager.get_shared_state().set("active_results", result)
        
        # Step 4: View Results
        st.header("Step 3: Optimization Results")
        
        # Get results from shared state
        results = state_manager.get_shared_state().get("active_results", {})
        
        # Render results if available
        if results and results.get("type") == "optimization_result":
            render_optimization_results(results)

def render_optimization_results(results):
    """Render Optimization Results"""
    if "error" in results:
        st.error(results["error"])
        return
    
    # Display optimized code
    if "optimized_code" in results:
        st.subheader("Optimized Code")
        
        # Show original and optimized code side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original Code:**")
            st.code(results["original_code"], language="python")
            
        with col2:
            st.markdown("**Optimized Code:**")
            st.code(results["optimized_code"], language="python")
    
    # Display optimization summary
    if "summary" in results:
        st.subheader("Optimization Summary")
        
        summary = results["summary"]
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if "performance_improvement" in summary:
                st.metric(
                    "Performance Improvement", 
                    f"{summary['performance_improvement']}%"
                )
            
        with col2:
            if "memory_impact" in summary:
                memory_impact = summary["memory_impact"]
                st.metric(
                    "Memory Impact", 
                    f"{memory_impact}%",
                    delta=-memory_impact if memory_impact < 0 else memory_impact,
                    delta_color="inverse"
                )
            
        with col3:
            if "complexity_change" in summary:
                complexity_change = summary["complexity_change"]
                st.metric(
                    "Complexity Change", 
                    f"{complexity_change}%",
                    delta=-complexity_change if complexity_change < 0 else complexity_change,
                    delta_color="inverse"
                )
        
        # Display applied optimizations
        if "applied_optimizations" in summary:
            st.markdown("**Applied Optimizations:**")
            
            for opt in summary["applied_optimizations"]:
                with st.expander(f"{opt['name']} - {opt['impact']} impact"):
                    st.write(f"**Description:** {opt['description']}")
                    
                    if "before" in opt and "after" in opt:
                        st.markdown("**Before:**")
                        st.code(opt["before"], language="python")
                        
                        st.markdown("**After:**")
                        st.code(opt["after"], language="python")
    
    # Display performance comparison
    if "performance" in results:
        st.subheader("Performance Comparison")
        
        performance = results["performance"]
        
        # Create chart
        fig, ax = plt.subplots(figsize=(10, 5))
        
        x = ["Original", "Optimized"]
        y = [performance["original_time"], performance["optimized_time"]]
        
        ax.bar(x, y, color=["#ff9999", "#66b3ff"])
        ax.set_ylabel("Execution Time (seconds)")
        ax.set_title("Performance Comparison")
        
        for i, v in enumerate(y):
            ax.text(i, v + 0.01, f"{v:.6f}s", ha="center")
        
        # Convert plot to base64 image
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close()
        
        st.image(f"data:image/png;base64,{image_base64}")
        
        # Display speedup
        speedup = performance["speedup"]
        st.success(f"Speedup: {speedup:.2f}x faster")

def render_custom_function(module):
    """Render Custom Function UI"""
    st.title("Custom Function")
    
    # Step 1: Function Definition
    st.header("Step 1: Define Your Function")
    
    # Function name input
    function_name = st.text_input(
        "Function Name",
        key=state_manager.register_ui_key("cf_function_name")
    )
    
    # Function parameters
    st.subheader("Function Parameters")
    
    # Add parameter button
    if "cf_parameters" not in st.session_state:
        st.session_state.cf_parameters = []
    
    # Display existing parameters
    for i, param in enumerate(st.session_state.cf_parameters):
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        
        with col1:
            param_name = st.text_input(
                "Name",
                value=param["name"],
                key=state_manager.register_ui_key(f"cf_param_name_{i}")
            )
        
        with col2:
            param_type = st.selectbox(
                "Type",
                ["int", "float", "str", "list", "dict", "bool", "any"],
                index=["int", "float", "str", "list", "dict", "bool", "any"].index(param["type"]),
                key=state_manager.register_ui_key(f"cf_param_type_{i}")
            )
        
        with col3:
            param_required = st.checkbox(
                "Required",
                value=param["required"],
                key=state_manager.register_ui_key(f"cf_param_required_{i}")
            )
        
        with col4:
            if st.button("Remove", key=state_manager.register_ui_key(f"cf_remove_param_{i}")):
                st.session_state.cf_parameters.pop(i)
                st.experimental_rerun()
        
        # Update parameter
        param["name"] = param_name
        param["type"] = param_type
        param["required"] = param_required
    
    # Add new parameter
    if st.button("Add Parameter", key=state_manager.register_ui_key("cf_add_param")):
        st.session_state.cf_parameters.append({
            "name": f"param{len(st.session_state.cf_parameters) + 1}",
            "type": "any",
            "required": True
        })
        st.experimental_rerun()
    
    # Function implementation
    st.subheader("Function Implementation")
    
    function_code = st.text_area(
        "Python Code",
        height=300,
        key=state_manager.register_ui_key("cf_function_code")
    )
    
    # Step 2: Function Options
    st.header("Step 2: Function Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        add_docstring = st.checkbox(
            "Generate Docstring",
            value=True,
            key=state_manager.register_ui_key("cf_add_docstring")
        )
        
        add_type_hints = st.checkbox(
            "Add Type Hints",
            value=True,
            key=state_manager.register_ui_key("cf_add_type_hints")
        )
    
    with col2:
        add_validation = st.checkbox(
            "Add Input Validation",
            value=True,
            key=state_manager.register_ui_key("cf_add_validation")
        )
        
        optimize_function = st.checkbox(
            "Optimize Function",
            value=False,
            key=state_manager.register_ui_key("cf_optimize_function")
        )
    
    # Step 3: Generate Function
    if st.button(
        "Generate Function",
        key=state_manager.register_ui_key("cf_generate_function"),
        use_container_width=True
    ):
        if not function_name:
            st.error("Function name is required")
        elif not function_code:
            st.error("Function implementation is required")
        else:
            with st.spinner("Generating function..."):
                # Prepare function data
                function_data = {
                    "name": function_name,
                    "parameters": st.session_state.cf_parameters,
                    "code": function_code,
                    "options": {
                        "docstring": add_docstring,
                        "type_hints": add_type_hints,
                        "validation": add_validation,
                        "optimize": optimize_function
                    }
                }
                
                # Generate function
                result = module.process({
                    "command": "generate",
                    "function_data": function_data
                })
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    # Display generated function
                    st.subheader("Generated Function")
                    st.code(result["generated_code"], language="python")
                    
                    # Download button
                    st.download_button(
                        "Download Function",
                        result["generated_code"],
                        file_name=f"{function_name}.py",
                        mime="text/plain",
                        key=state_manager.register_ui_key("cf_download_function")
                    )
