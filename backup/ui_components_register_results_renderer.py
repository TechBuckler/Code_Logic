import streamlit as st
from typing import Dict, Any, List, Callable, Optional
from core.state_manager import state_manager
# Fix imports for reorganized codebase
import utils.import_utils





    def register_results_renderer(self, result_type: str, renderer: Callable):
        """Register a results renderer"""
        self.results.register_renderer(result_type, renderer)