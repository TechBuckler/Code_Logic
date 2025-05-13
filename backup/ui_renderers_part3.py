"""
UI Renderers Part 3 - Final module-specific UI rendering functions
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import json
import base64

# Import core components

def render_benchmark_results(results):
    """Render Benchmark Results"""
    if "error" in results:
        st.error(results["error"])
        return
    
    # Display benchmark results
    st.subheader("Step 3: View Benchmark Results")
    
    # Create a dashboard layout
    st.subheader("📊 Performance Metrics")
    
    # Tabs for different metrics
    time_tab, memory_tab, cpu_tab = st.tabs(["Execution Time", "Memory Usage", "CPU Usage"])
    
    with time_tab:
        # Show execution time stats with better formatting
        time_stats = results["stats"]["execution_time"]
        
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
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Line plot of execution times
        execution_times = results["raw_data"]["execution_times"]
        ax1.plot(execution_times)
        ax1.set_title(f"Execution Time over {len(execution_times)} Iterations")
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
        memory_stats = results["stats"]["memory_usage"]
        
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
        memory_usage = results["raw_data"]["memory_usage"]
        ax.plot(memory_usage)
        ax.set_title(f"Memory Usage over {len(memory_usage)} Iterations")
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
        cpu_stats = results["stats"]["cpu_usage"]
        
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
        cpu_usage = results["raw_data"]["cpu_usage"]
        ax.plot(cpu_usage)
        ax.set_title(f"CPU Usage over {len(cpu_usage)} Iterations")
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
        st.markdown(f"**Function: {results.get('function_name', 'Unknown')}**")
        st.markdown(f"Benchmarked with {len(execution_times)} iterations")
        
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
            data=json.dumps(results, indent=2),
            file_name=f"{results.get('function_name', 'benchmark')}_results.json",
            mime="application/json",
            key=state_manager.register_ui_key("export_benchmark_results")
        )

# Complete the new_unified_ui.py file with the main function
def complete_unified_ui():
    """
    Add the main function to new_unified_ui.py
    """
    main_function = """
def run_ui():
    \"\"\"Main function to run the UI\"\"\"
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
"""
    
    # Return the main function code
    return main_function
