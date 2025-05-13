"""
Optimization Core Module - Hierarchical version

This module serves as the core for all optimization-related functionality,
including logic optimization, formal verification, and performance analysis.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Make sure src is in the path
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
project_root = os.path.dirname(src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


class OptimizationCoreModule(HierarchicalModule):
    """Core module for all optimization functionality"""
    
    def __init__(self, parent=None):
        super().__init__("optimization", parent)
        
        # Load child modules
        self.load_child_modules()
        
    def load_child_modules(self):
        """Load all optimization-related child modules"""
        
        # Create child modules
        self.optimizer = OptimizerModule(self)
        self.proof_engine = ProofEngineModule(self)
    
    def render_ui(self):
        """Render the optimization UI"""
        st.title("Code Optimization & Verification")
        
        # Tabs for different optimization features
        tabs = st.tabs(["Optimizer", "Formal Verification", "Results"])
        
        with tabs[0]:
            self.optimizer.render_ui()
            
        with tabs[1]:
            self.proof_engine.render_ui()
            
        with tabs[2]:
            self.render_results()
    
    def render_results(self):
        """Render the combined optimization results"""
        st.header("Optimization Results")
        
        # Check if we have results to display
        optimization_results = self.shared_state.get("optimization_results")
        proof_result = self.shared_state.get("proof_result")
        
        if optimization_results or proof_result:
            # Function info
            ir_model = self.shared_state.get("ir_model")
            if ir_model:
                st.subheader(f"Function: {ir_model.get('function_name')}")
            
            # Summary
            st.subheader("Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Optimization")
                if optimization_results and "error" not in optimization_results:
                    original = optimization_results.get("original", {})
                    merged = optimization_results.get("merged", [])
                    
                    original_count = len(original.get("logic", []))
                    merged_count = len(merged)
                    
                    if merged_count < original_count:
                        reduction = ((original_count - merged_count) / original_count) * 100
                        st.success(f"✅ Reduced logic rules by {reduction:.1f}%")
                        st.markdown(f"- Original: {original_count} rules")
                        st.markdown(f"- Optimized: {merged_count} rules")
                    else:
                        st.info("ℹ️ No reduction in logic rules")
                else:
                    st.info("No optimization results available")
            
            with col2:
                st.markdown("### Verification")
                if proof_result and "error" not in proof_result:
                    if proof_result.get("verified"):
                        st.success("✅ Logic formally verified")
                    else:
                        st.error("❌ Verification failed")
                else:
                    st.info("No verification results available")
            
            # Export button
            if optimization_results and "error" not in optimization_results:
                st.subheader("Export")
                if st.button("Export Optimized Code", key=state_manager.register_ui_key("export_btn")):
                    
                    # Get the optimized IR model
                    merged = optimization_results.get("merged", [])
                    optimized_ir = {
                        "function_name": ir_model.get("function_name"),
                        "params": ir_model.get("params"),
                        "logic": merged
                    }
                    
                    # Export to Python
                    python_code = export_to_python(optimized_ir)
                    
                    # Display the code
                    st.code(python_code, language="python")
                    
                    # Add download button
                    st.download_button(
                        label="Download Python File",
                        data=python_code,
                        file_name=f"{ir_model.get('function_name')}_optimized.py",
                        mime="text/plain",
                        key=state_manager.register_ui_key("download_btn")
                    )
        else:
            st.info("No optimization or verification results available yet. Use the Optimizer and Formal Verification tabs to generate results.")
    
    def process(self, data, context=None):
        """Process data through the optimization pipeline"""
        # Pass data through each child module in sequence
        result = data
        
        # Process with optimizer
        if self.optimizer.can_process(result):
            optimization_results = self.optimizer.process(result, context)
            
            # Process with proof engine
            if self.proof_engine.can_process(result):
                proof_result = self.proof_engine.process(result, context)
                
                # Return combined results
                return {
                    "optimization": optimization_results,
                    "verification": proof_result
                }
            
            return {"optimization": optimization_results}
        
        return result
