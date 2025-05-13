"""Utils package - provides utility functions for the codebase.

This package contains various utility modules for file operations, path handling,
string manipulation, and import management.
"""

# DO NOT import utils.import_utils here - that creates a circular import
# Instead, define a minimal set of utilities needed at the package level

# Define package exports - these will be available when importing the package
__all__ = [
    # Core utility functions that can be imported directly from utils
    'ensure_dir',
    'read_file',
    'write_file',
    'join_paths'
]

# Define minimal versions of critical functions to avoid circular imports
def ensure_dir(directory):
    """Ensure a directory exists, creating it if necessary."""
    import os
    os.makedirs(directory, exist_ok=True)
    return directory

def read_file(file_path):
    """Read a file and return its contents."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path, content):
    """Write content to a file."""
    ensure_dir(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path

def join_paths(*paths):
    """Join paths together."""
    import os
    return os.path.join(*paths)

# Import os here for use in the write_file function
import os
from .file.ir_model import *
from .file.new_main import *
from .file.new_unified_ui import *
from .file.optimizer import *
from .file.path_utils import *
from .file.proof_engine import *
from .file.quick_verify import *
from .file.runtime_optimization import *
from .file.simple_hierarchical_core import *
from .file.starter_pipeline import *
from .file.state_manager import *
from .file.summarize_codebase import *
from .file.ui_components import *
from .file.ui_renderers import *
from .file.ui_renderers_part2 import *
from .file.ui_renderers_part3 import *
from .file.ui_utils import *
from .file.unified_core import *
from .file.unified_ui import *
from .file.utils import *
from .file.verify_codebase import *
from .system.background_system import *
from .system.module_system import *
from .string.bootstrap import *
from .string.list_structure import *
from .string.string_utils import *
# Import utilities will be added by the fix_imports.py script
from .data.json_utils import *
from .time.runtime_utils import *
