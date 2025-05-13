"""
Analysis Core Module UI Renderer

This module provides a Streamlit-based UI for hierarchical code analysis and visualization.
"""
import os
import sys
import streamlit as st
from typing import Dict, List, Any, Optional
from core.hierarchical_module import HierarchicalModule
from core.state_manager import state_manager
from modules.standard.ast_parser_module import ASTParserModule
from modules.standard.ir_generator_module import IRGeneratorModule
# Fix imports for reorganized codebase
import utils.import_utils

class AnalysisCoreModuleUI:
    def __init__(self):
        self.ast_parser = ASTParserModule()
        self.ir_generator = IRGeneratorModule()

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
        st.write("Code input UI goes here.")

    def render_results(self):
        st.write("Results UI goes here.")