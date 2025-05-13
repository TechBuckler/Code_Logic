"""
UI Renderers Part 2 - Additional module-specific UI rendering functions
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import base64

# Import core components

def render_project_organizer(module):
    """Render Project Organizer UI"""
    st.title("Project Organization")
    
    # Step 1: Project Selection
    st.header("Step 1: Select Project")
    
    # Project path input
    project_path = st.text_input(
        "Project Path",
        placeholder="Enter absolute path to project directory",
        key=state_manager.register_ui_key("po_project_path")
    )
    
    # Browse button (simulated)
    if st.button("Browse...", key=state_manager.register_ui_key("po_browse_button")):
        st.info("In a full implementation, this would open a file browser dialog.")
        st.info("For now, please enter the project path manually.")
    
    # Step 2: Analysis Options
    if project_path:
        st.header("Step 2: Analysis Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            check_structure = st.checkbox(
                "Check Project Structure",
                value=True,
                key=state_manager.register_ui_key("po_check_structure")
            )
            
            check_naming = st.checkbox(
                "Check Naming Conventions",
                value=True,
                key=state_manager.register_ui_key("po_check_naming")
            )
        
        with col2:
            check_dependencies = st.checkbox(
                "Check Dependencies",
                value=True,
                key=state_manager.register_ui_key("po_check_dependencies")
            )
            
            check_imports = st.checkbox(
                "Check Imports",
                value=True,
                key=state_manager.register_ui_key("po_check_imports")
            )
        
        # Step 3: Analyze Project
        if st.button(
            "Analyze Project",
            key=state_manager.register_ui_key("po_analyze_project"),
            use_container_width=True
        ):
            if not os.path.isdir(project_path):
                st.error(f"Directory not found: {project_path}")
            else:
                with st.spinner("Analyzing project..."):
                    # Prepare analysis options
                    options = {
                        "structure": check_structure,
                        "naming": check_naming,
                        "dependencies": check_dependencies,
                        "imports": check_imports
                    }
                    
                    # Run analysis
                    result = module.analyze_project(project_path, options)
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        # Display analysis results
                        st.subheader("Analysis Results")
                        
                        # Project structure
                        if "structure" in result:
                            with st.expander("Project Structure", expanded=True):
                                st.write(f"**Files:** {result['structure']['file_count']}")
                                st.write(f"**Directories:** {result['structure']['dir_count']}")
                                st.write(f"**Python Files:** {result['structure']['py_file_count']}")
                                
                                # Structure issues
                                if result["structure"]["issues"]:
                                    st.warning("Structure Issues Found:")
                                    for issue in result["structure"]["issues"]:
                                        st.write(f"- {issue}")
                                else:
                                    st.success("No structure issues found")
                        
                        # Naming conventions
                        if "naming" in result:
                            with st.expander("Naming Conventions", expanded=True):
                                # Naming issues
                                if result["naming"]["issues"]:
                                    st.warning("Naming Issues Found:")
                                    for issue in result["naming"]["issues"]:
                                        st.write(f"- {issue}")
                                else:
                                    st.success("No naming issues found")
                        
                        # Dependencies
                        if "dependencies" in result:
                            with st.expander("Dependencies", expanded=True):
                                st.write(f"**Found Dependencies:** {', '.join(result['dependencies']['found'])}")
                                
                                # Missing dependencies
                                if result["dependencies"]["missing"]:
                                    st.warning("Missing Dependencies:")
                                    for dep in result["dependencies"]["missing"]:
                                        st.write(f"- {dep}")
                                else:
                                    st.success("No missing dependencies found")
                        
                        # Imports
                        if "imports" in result:
                            with st.expander("Imports", expanded=True):
                                # Unused imports
                                if result["imports"]["unused"]:
                                    st.warning("Unused Imports:")
                                    for imp in result["imports"]["unused"]:
                                        st.write(f"- {imp}")
                                else:
                                    st.success("No unused imports found")
                                
                                # Missing imports
                                if result["imports"]["missing"]:
                                    st.warning("Missing Imports:")
                                    for imp in result["imports"]["missing"]:
                                        st.write(f"- {imp}")
                                else:
                                    st.success("No missing imports found")
        
        # Step 4: Reorganize Project
        st.header("Step 3: Reorganize Project")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fix_structure = st.checkbox(
                "Fix Project Structure",
                value=False,
                key=state_manager.register_ui_key("po_fix_structure")
            )
            
            fix_naming = st.checkbox(
                "Fix Naming Conventions",
                value=False,
                key=state_manager.register_ui_key("po_fix_naming")
            )
        
        with col2:
            fix_dependencies = st.checkbox(
                "Fix Dependencies",
                value=False,
                key=state_manager.register_ui_key("po_fix_dependencies")
            )
            
            fix_imports = st.checkbox(
                "Fix Imports",
                value=False,
                key=state_manager.register_ui_key("po_fix_imports")
            )
        
        # Create backup option
        create_backup = st.checkbox(
            "Create Backup Before Reorganizing",
            value=True,
            key=state_manager.register_ui_key("po_create_backup")
        )
        
        # Reorganize button
        if st.button(
            "Reorganize Project",
            key=state_manager.register_ui_key("po_reorganize_project"),
            use_container_width=True
        ):
            if not os.path.isdir(project_path):
                st.error(f"Directory not found: {project_path}")
            elif not any([fix_structure, fix_naming, fix_dependencies, fix_imports]):
                st.warning("Please select at least one fix option")
            else:
                with st.spinner("Reorganizing project..."):
                    # Prepare reorganize options
                    options = {
                        "structure": fix_structure,
                        "naming": fix_naming,
                        "dependencies": fix_dependencies,
                        "imports": fix_imports,
                        "backup": create_backup
                    }
                    
                    # Run reorganize
                    result = module.reorganize_project(project_path, options)
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        # Display reorganize results
                        st.subheader("Reorganization Results")
                        
                        # Backup info
                        if "backup" in result and result["backup"]["created"]:
                            st.success(f"Backup created at: {result['backup']['path']}")
                        
                        # Changes summary
                        if "changes" in result:
                            changes = result["changes"]
                            st.write(f"**Files Modified:** {changes['files_modified']}")
                            st.write(f"**Files Moved:** {changes['files_moved']}")
                            st.write(f"**Files Created:** {changes['files_created']}")
                            
                            # Detailed changes
                            if changes["details"]:
                                with st.expander("Detailed Changes"):
                                    for change in changes["details"]:
                                        st.write(f"- {change}")

def render_module_explorer(module):
    """Render Module Explorer UI"""
    st.title("Module Explorer")
    
    # Get available modules
    available_modules = module.list_modules()
    
    # Step 1: Select Module
    st.header("Step 1: Select Module")
    
    selected_module = st.selectbox(
        "Available Modules",
        available_modules,
        key=state_manager.register_ui_key("me_selected_module")
    )
    
    if selected_module:
        # Step 2: Module Details
        st.header("Step 2: Module Details")
        
        # Get module details
        module_details = module.get_module_details(selected_module)
        
        if "error" in module_details:
            st.error(module_details["error"])
        else:
            # Display module info
            st.subheader("Module Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Name:** {module_details['name']}")
                st.write(f"**Type:** {module_details['type']}")
            
            with col2:
                st.write(f"**Path:** {module_details['path']}")
                st.write(f"**Size:** {module_details['size']} bytes")
            
            # Module description
            if "description" in module_details:
                st.write(f"**Description:** {module_details['description']}")
            
            # Module source code
            if "source_code" in module_details:
                with st.expander("Source Code", expanded=True):
                    st.code(module_details["source_code"], language="python")
            
            # Module functions
            if "functions" in module_details and module_details["functions"]:
                with st.expander("Functions"):
                    for func in module_details["functions"]:
                        st.write(f"**{func['name']}**")
                        st.code(func["signature"], language="python")
                        if "docstring" in func and func["docstring"]:
                            st.write(func["docstring"])
            
            # Module classes
            if "classes" in module_details and module_details["classes"]:
                with st.expander("Classes"):
                    for cls in module_details["classes"]:
                        st.write(f"**{cls['name']}**")
                        if "docstring" in cls and cls["docstring"]:
                            st.write(cls["docstring"])
                        
                        # Class methods
                        if "methods" in cls and cls["methods"]:
                            for method in cls["methods"]:
                                st.write(f"- **{method['name']}**")
                                st.code(method["signature"], language="python")
        
        # Step 3: Module Actions
        st.header("Step 3: Module Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(
                "Edit Module",
                key=state_manager.register_ui_key("me_edit_module")
            ):
                st.info("Module editing would be implemented here")
        
        with col2:
            if st.button(
                "Run Module",
                key=state_manager.register_ui_key("me_run_module")
            ):
                with st.spinner(f"Running {selected_module}..."):
                    result = module.run_module(selected_module)
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success(f"Module {selected_module} executed successfully")
                        
                        # Display output
                        if "output" in result:
                            st.subheader("Module Output")
                            st.code(result["output"])
        
        with col3:
            if st.button(
                "Analyze Module",
                key=state_manager.register_ui_key("me_analyze_module")
            ):
                with st.spinner(f"Analyzing {selected_module}..."):
                    result = module.analyze_module(selected_module)
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success(f"Module {selected_module} analyzed successfully")
                        
                        # Display analysis
                        st.subheader("Module Analysis")
                        
                        # Complexity metrics
                        if "complexity" in result:
                            st.write("**Complexity Metrics:**")
                            metrics = result["complexity"]
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Cyclomatic Complexity", metrics["cyclomatic"])
                            
                            with col2:
                                st.metric("Maintainability Index", metrics["maintainability"])
                            
                            with col3:
                                st.metric("Lines of Code", metrics["loc"])
                        
                        # Dependencies
                        if "dependencies" in result:
                            st.write("**Dependencies:**")
                            for dep in result["dependencies"]:
                                st.write(f"- {dep}")
                        
                        # Issues
                        if "issues" in result and result["issues"]:
                            st.warning("**Issues Found:**")
                            for issue in result["issues"]:
                                st.write(f"- {issue}")
                        else:
                            st.success("No issues found")

def render_optimization_testbed(module):
    """Render Optimization Testbed UI"""
    st.title("Optimization Testbed")
    
    # Create a container with instructions
    with st.container(border=True):
        st.markdown("### How to Use the Optimization Testbed")
        st.markdown("""
        1. **Provide your code** in the input area below
        2. **Select an action** (Analyze, Optimize, or Benchmark)
        3. **View the results** and visualizations
        """)
        st.info("The Optimization Testbed helps you find the optimal trade-offs between memory usage, CPU performance, and GPU utilization.")
    
    # Step 1: Code Input
    st.header("Step 1: Provide Code")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Code input
        source_code = st.text_area(
            "Enter Python code to analyze",
            height=300,
            key=state_manager.register_ui_key("ot_source_code")
        )
    
    with col2:
        # Function name input
        function_name = st.text_input(
            "Function to analyze",
            key=state_manager.register_ui_key("ot_function_name")
        )
        
        st.markdown("#### Example Code")
        if st.button("Load Example", key=state_manager.register_ui_key("ot_load_example")):
            example_code = """def matrix_multiply(a, b):
    # Simple matrix multiplication
    if len(a[0]) != len(b):
        raise ValueError("Matrices dimensions don't match")
        
    result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
                
    return result
"""
            # Update the text area with example code
            st.session_state[state_manager.register_ui_key("ot_source_code")] = example_code
            # Update function name
            st.session_state[state_manager.register_ui_key("ot_function_name")] = "matrix_multiply"
            st.experimental_rerun()
    
    # Store code in shared state
    if source_code:
        state_manager.get_shared_state().set("ot_source_code", source_code)
        state_manager.get_shared_state().set("ot_function_name", function_name)
    
    # Step 2: Select Action
    if source_code and function_name:
        st.header("Step 2: Select Action")
        
        # Create tabs for different actions
        analyze_tab, optimize_tab, benchmark_tab = st.tabs(["Analyze", "Optimize", "Benchmark"])
        
        # Analyze tab
        with analyze_tab:
            st.write("Analyze code to identify optimization opportunities.")
            
            # Analysis options
            st.subheader("2.1 Analysis Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                analyze_complexity = st.checkbox(
                    "Analyze Complexity",
                    value=True,
                    key=state_manager.register_ui_key("ot_analyze_complexity")
                )
                
                analyze_memory = st.checkbox(
                    "Analyze Memory Usage",
                    value=True,
                    key=state_manager.register_ui_key("ot_analyze_memory")
                )
            
            with col2:
                analyze_performance = st.checkbox(
                    "Analyze Performance",
                    value=True,
                    key=state_manager.register_ui_key("ot_analyze_performance")
                )
                
                analyze_patterns = st.checkbox(
                    "Identify Patterns",
                    value=True,
                    key=state_manager.register_ui_key("ot_analyze_patterns")
                )
            
            # Run analysis button
            if st.button(
                "Run Analysis",
                key=state_manager.register_ui_key("ot_run_analysis"),
                use_container_width=True
            ):
                with st.spinner(f"Analyzing {function_name}..."):
                    # Prepare analysis options
                    options = {
                        "complexity": analyze_complexity,
                        "memory": analyze_memory,
                        "performance": analyze_performance,
                        "patterns": analyze_patterns
                    }
                    
                    # Run analysis
                    result = module.process({
                        "command": "analyze",
                        "source_code": source_code,
                        "function_name": function_name,
                        "options": options
                    })
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        # Store result in shared state
                        state_manager.get_shared_state().set("ot_analysis_result", result)
                        
                        # Display analysis results
                        st.subheader("Analysis Results")
                        
                        # Complexity analysis
                        if "complexity" in result:
                            st.write("**Complexity Analysis:**")
                            complexity = result["complexity"]
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Time Complexity", complexity["time_complexity"])
                            
                            with col2:
                                st.metric("Space Complexity", complexity["space_complexity"])
                            
                            with col3:
                                st.metric("Cyclomatic Complexity", complexity["cyclomatic_complexity"])
                        
                        # Memory analysis
                        if "memory" in result:
                            st.write("**Memory Analysis:**")
                            memory = result["memory"]
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Estimated Memory Usage", f"{memory['estimated_usage']} bytes")
                            
                            with col2:
                                st.metric("Memory Efficiency", f"{memory['efficiency']}%")
                        
                        # Performance analysis
                        if "performance" in result:
                            st.write("**Performance Analysis:**")
                            performance = result["performance"]
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Estimated Runtime", f"{performance['estimated_runtime']:.6f}s")
                            
                            with col2:
                                st.metric("Performance Score", f"{performance['score']}/10")
                        
                        # Optimization opportunities
                        if "opportunities" in result:
                            st.write("**Optimization Opportunities:**")
                            
                            for opportunity in result["opportunities"]:
                                with st.expander(f"{opportunity['name']} (Impact: {opportunity['impact']})"):
                                    st.write(f"**Description:** {opportunity['description']}")
                                    
                                    if "code_snippet" in opportunity:
                                        st.code(opportunity["code_snippet"], language="python")
                                    
                                    if "suggestion" in opportunity:
                                        st.write("**Suggestion:**")
                                        st.code(opportunity["suggestion"], language="python")
        
        # Optimize tab
        with optimize_tab:
            st.write("Optimize code based on different profiles and techniques.")
            
            # Optimization profile
            st.subheader("2.1 Select Optimization Profile")
            
            optimization_profile = st.selectbox(
                "Optimization Profile",
                ["Balanced", "Memory Efficient", "CPU Performance", "GPU Accelerated"],
                key=state_manager.register_ui_key("ot_optimization_profile")
            )
            
            # Profile description
            profile_descriptions = {
                "Balanced": "Balances memory usage and performance for general-purpose applications.",
                "Memory Efficient": "Prioritizes memory efficiency over raw performance. Best for memory-constrained environments.",
                "CPU Performance": "Maximizes CPU performance, potentially using more memory. Best for compute-intensive tasks.",
                "GPU Accelerated": "Utilizes GPU acceleration where possible. Best for parallel computations and matrix operations."
            }
            
            st.info(profile_descriptions[optimization_profile])
            
            # Optimization techniques
            st.subheader("2.2 Select Optimization Techniques")
            
            # Group techniques by category
            algorithm_techniques = ["Loop Optimization", "Algorithm Replacement", "Data Structure Optimization"]
            memory_techniques = ["Memory Pooling", "Lazy Evaluation", "Data Compression"]
            parallel_techniques = ["Multithreading", "Vectorization", "GPU Offloading"]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Algorithm Techniques**")
                algorithm_selected = []
                
                for technique in algorithm_techniques:
                    key = state_manager.register_ui_key(f"tech_{technique.lower().replace(' ', '_')}")
                    if st.checkbox(technique, key=key):
                        algorithm_selected.append(technique)
            
            with col2:
                st.markdown("**Memory Techniques**")
                memory_selected = []
                
                for technique in memory_techniques:
                    key = state_manager.register_ui_key(f"tech_{technique.lower().replace(' ', '_')}")
                    if st.checkbox(technique, key=key):
                        memory_selected.append(technique)
            
            with col3:
                st.markdown("**Parallel Techniques**")
                parallel_selected = []
                
                for technique in parallel_techniques:
                    key = state_manager.register_ui_key(f"tech_{technique.lower().replace(' ', '_')}")
                    if st.checkbox(technique, key=key):
                        parallel_selected.append(technique)
            
            # Optimization level
            optimization_level = st.slider(
                "Optimization Aggressiveness",
                min_value=1,
                max_value=10,
                value=5,
                help="Higher values apply more aggressive optimizations",
                key=state_manager.register_ui_key("ot_optimization_level")
            )
            
            # Run optimization button
            if st.button(
                "Run Optimization",
                key=state_manager.register_ui_key("ot_run_optimization"),
                use_container_width=True
            ):
                with st.spinner(f"Optimizing {function_name}..."):
                    # Prepare optimization options
                    options = {
                        "profile": optimization_profile,
                        "techniques": {
                            "algorithm": algorithm_selected,
                            "memory": memory_selected,
                            "parallel": parallel_selected
                        },
                        "level": optimization_level
                    }
                    
                    # Run optimization
                    result = module.process({
                        "command": "optimize",
                        "source_code": source_code,
                        "function_name": function_name,
                        "options": options
                    })
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        # Store result in shared state
                        state_manager.get_shared_state().set("ot_optimization_result", result)
                        
                        # Display optimization results
                        st.subheader("Step 3: Optimization Results")
                        
                        # Show original and optimized code side by side
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Original Code:**")
                            st.code(source_code, language="python")
                        
                        with col2:
                            st.markdown("**Optimized Code:**")
                            st.code(result["optimized_code"], language="python")
                        
                        # Applied techniques
                        if "applied_techniques" in result:
                            st.subheader("Applied Techniques")
                            
                            for technique in result["applied_techniques"]:
                                with st.expander(f"{technique['name']} - {technique['impact']} impact"):
                                    st.write(f"**Description:** {technique['description']}")
                                    
                                    if "before" in technique and "after" in technique:
                                        col1, col2 = st.columns(2)
                                        
                                        with col1:
                                            st.markdown("**Before:**")
                                            st.code(technique["before"], language="python")
                                        
                                        with col2:
                                            st.markdown("**After:**")
                                            st.code(technique["after"], language="python")
                        
                        # Performance comparison
                        if "performance_comparison" in result:
                            st.subheader("Performance Comparison")
                            
                            comparison = result["performance_comparison"]
                            
                            # Metrics
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                speedup = comparison["speedup"]
                                st.metric("Speedup", f"{speedup}x")
                            
                            with col2:
                                memory_change = comparison["memory_change"]
                                st.metric(
                                    "Memory Change", 
                                    f"{memory_change}%",
                                    delta=-memory_change if memory_change < 0 else memory_change,
                                    delta_color="inverse"
                                )
                            
                            with col3:
                                efficiency = comparison["efficiency_score"]
                                st.metric("Efficiency Score", f"{efficiency}/10")
                            
                            # Create visualization
                            if "visualization_data" in comparison:
                                data = comparison["visualization_data"]
                                
                                # Create radar chart
                                fig = plt.figure(figsize=(8, 8))
                                ax = fig.add_subplot(111, polar=True)
                                
                                # Categories and values
                                categories = ["CPU Performance", "Memory Usage", "Code Complexity", 
                                             "Parallelism", "GPU Utilization"]
                                
                                original_values = data["original"]
                                optimized_values = data["optimized"]
                                
                                # Number of categories
                                N = len(categories)
                                
                                # Angle of each axis
                                angles = [n / float(N) * 2 * np.pi for n in range(N)]
                                angles += angles[:1]  # Close the loop
                                
                                # Add original values
                                original_values += original_values[:1]  # Close the loop
                                ax.plot(angles, original_values, linewidth=1, linestyle='solid', label="Original")
                                ax.fill(angles, original_values, alpha=0.1)
                                
                                # Add optimized values
                                optimized_values += optimized_values[:1]  # Close the loop
                                ax.plot(angles, optimized_values, linewidth=1, linestyle='solid', label="Optimized")
                                ax.fill(angles, optimized_values, alpha=0.1)
                                
                                # Set category labels
                                plt.xticks(angles[:-1], categories)
                                
                                # Add legend
                                plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
                                
                                # Convert plot to base64 image
                                buffer = BytesIO()
                                plt.savefig(buffer, format="png")
                                buffer.seek(0)
                                image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                                plt.close()
                                
                                st.image(f"data:image/png;base64,{image_base64}")
                        
                        # Download optimized code
                        st.download_button(
                            "Download Optimized Code",
                            result["optimized_code"],
                            file_name=f"{function_name}_optimized.py",
                            mime="text/plain",
                            key=state_manager.register_ui_key("ot_download_optimized")
                        )
