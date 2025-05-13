"""
Legacy compatibility package for hierarchical modules.
This imports from the new modules.standard package.
"""

# Import from the new location
try:
    from modules.standard import *
except ImportError:
    pass
