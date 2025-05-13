"""
Analysis Core Module - Hierarchical version

This module serves as the core for all analysis-related functionality,
including code parsing, AST exploration, and logic analysis.
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


class AnalysisCoreModule(HierarchicalModule):
    """Core module for all analysis functionality"""
    
    def __init__(self, parent=None):
        super().__init__("analysis", parent)
        
        # Load child modules
        self.load_child_modules()
        
    def load_child_modules(self):
        """Load all analysis-related child modules"""
        
        # Create child modules
        self.ast_parser = ASTParserModule(self)
        self.ir_generator = IRGeneratorModule(self)
        
    def render_ui(self):
        """Render the analysis UI"""
        st.title("Code Analysis")
        
        # Tabs for different analysis features
        tabs = st.tabs(["Code Input", "AST Parser", "IR Generator", "Results"])
        
        with tabs[0]:
            self.render_code_input()
            
        with tabs[1]:
            self.ast_parser.render_ui()
            
        with tabs[2]:
            self.ir_generator.render_ui()
            
        with tabs[3]:
            self.render_results()
    
    def render_code_input(self):
        """Render the code input section"""
        st.header("Code Input")
        
        # Code input options
        input_method = st.radio(
            "Input Method",
            ["Text Input", "File Upload"],
            key=state_manager.register_ui_key("analysis_input_method")
        )
        
        if input_method == "Text Input":
            code = st.text_area(
                "Enter your code here",
                height=300,
                key=state_manager.register_ui_key("analysis_code_input")
            )
            
            if st.button("Analyze Code", key=state_manager.register_ui_key("analyze_code_btn")):
                if code.strip():
                    # Store code in shared state
                    self.shared_state.set("current_code", code)
                    # Publish event
                    self.event_bus.publish("code_input_ready", {"source": "text_input", "code": code})
                    st.success("Code ready for analysis!")
                else:
                    st.warning("Please enter some code to analyze")
                    
        elif input_method == "File Upload":
            uploaded_file = st.file_uploader(
                "Upload a Python file",
                type=["py"],
                key=state_manager.register_ui_key("analysis_file_upload")
            )
            
            if uploaded_file is not None:
                code = uploaded_file.getvalue().decode("utf-8")
                st.code(code, language="python")
                
                if st.button("Analyze File", key=state_manager.register_ui_key("analyze_file_btn")):
                    # Store code in shared state
                    self.shared_state.set("current_code", code)
                    # Publish event
                    self.event_bus.publish("code_input_ready", {
                        "source": "file_upload",
                        "filename": uploaded_file.name,
                        "code": code
                    })
                    st.success(f"File '{uploaded_file.name}' ready for analysis!")
    
    def render_results(self):
        """Render the analysis results"""
        st.header("Analysis Results")
        
        # Check if we have results to display
        ast_result = self.shared_state.get("ast_result")
        ir_model = self.shared_state.get("ir_model")
        
        if ast_result or ir_model:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("AST Structure")
                if ast_result:
                    st.json(ast_result)
                else:
                    st.info("No AST results available.")
            
            with col2:
                st.subheader("IR Model")
                if ir_model:
                    st.json(ir_model)
                else:
                    st.info("No IR model available.")
        else:
            st.info("No analysis results available yet. Use the Code Input tab to submit code for analysis.")
    
    def process(self, data, context=None):
        """Process data through the analysis pipeline"""
        # Pass data through each child module in sequence
        result = data
        
        # Process with AST parser
        if self.ast_parser.can_process(result):
            result = self.ast_parser.process(result, context)
            
        # Process with IR generator if we have AST results
        if self.ir_generator.can_process(result):
            ir_result = self.ir_generator.process(result, context)
            # Store both results
            return {
                "ast_result": result,
                "ir_result": ir_result
            }
        
        return result
