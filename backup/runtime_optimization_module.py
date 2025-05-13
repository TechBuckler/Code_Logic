"""
Runtime Optimization Module (Standard)

This module provides compatibility for runtime optimization functionality
during the transition to the new directory structure.
"""
# Fix imports for reorganized codebase
import utils.import_utils



# Import from the base module to avoid duplication
from modules.runtime_optimization_module import RuntimeOptimizationModule

# Make the class available at this location
__all__ = ['RuntimeOptimizationModule']
