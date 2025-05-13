"""
Centralized imports for the Logic Tool system.
This file ensures all components can find their dependencies.
"""
import os
import sys
import inspect
import importlib
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



# Add the project root to the Python path
src_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import core components
try:
    # Try absolute imports first
    IMPORTS_SUCCESSFUL = True
    
except ImportError as e:
    print(f"Warning: Absolute imports failed ({e}), trying relative imports...")
    try:
        # Try relative imports as fallback
        IMPORTS_SUCCESSFUL = True
        
    except ImportError as e:
        print(f"Warning: Both absolute and relative imports failed ({e})")
        IMPORTS_SUCCESSFUL = False

# Example functions (defined inline since we removed the example files)
def decide(cpu, is_question, is_command):
    """Example decision function (previously in original_decision.py)"""
    if is_command:
        return 3
    elif is_question and cpu < 95:
        return 2
    elif is_question:
        return 1
    else:
        return 0

def determine_notification(battery_level, is_weekend, unread_messages, temperature):
    """Example notification function (previously in notification_logic.py)"""
    # Emergency alerts for extreme conditions
    if temperature > 40 or temperature < -10:
        return 4
    
    # Low battery emergency
    if battery_level < 5 and unread_messages > 10:
        return 4
    
    # Urgent notification conditions
    if (battery_level < 15 and not is_weekend) or unread_messages > 50:
        return 3
    
    # Standard notification for normal situations
    if unread_messages > 10 and battery_level > 30:
        # But reduce to silent on weekends with lots of messages
        if is_weekend and unread_messages > 25:
            return 1
        return 2
    
    # Silent notification for low-priority situations
    if (is_weekend and temperature > 25) or (battery_level > 50 and unread_messages > 0):
        return 1
    
    # Default: No notification
    return 0

# Function to dynamically load a module from a file path
def load_module_from_file(file_path, module_name=None):
    """
    Dynamically load a module from a file path.
    """
    if module_name is None:
        module_name = os.path.basename(file_path).replace('.py', '')
    
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        return None
        
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading module {module_name} from {file_path}: {e}")
        return None

# Function to get the source code of a function
def get_function_source(func):
    """
    Get the source code of a function.
    """
    try:
        return inspect.getsource(func)
    except Exception as e:
        print(f"Error getting source for function {func.__name__}: {e}")
        return None
