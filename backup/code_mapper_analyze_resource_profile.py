import os
import sys
import ast
import json
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple, Optional, Union, Callable
from module_system import Module, ModuleRegistry
from resource_splitter import analyze_resource_focus, analyze_resource_profile
import importlib.util
import argparse
# Fix imports for reorganized codebase
import utils.import_utils





    def analyze_resource_profile(func_code):
        """Analyze the resource profile of a function."""
        return {
            'cpu': 0.5, 'memory': 0.5, 'gpu': 0.0, 
            'network': 0.0, 'startup': 0.3, 'runtime': 0.5