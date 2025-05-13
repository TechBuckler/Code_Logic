"""
UI Utilities for the Logic Tool
"""
# Fix imports for reorganized codebase




# Global registry of used keys
if "used_ui_keys" not in st.session_state:
    st.session_state.used_ui_keys = set()

def get_unique_key(base_key: str) -> str:
    """
    Generate a unique key for UI components to avoid duplicate key errors.
    
    Args:
        base_key: The base key to use
        
    Returns:
        A unique key based on the base key
    """
    # If the key is already unique, return it
    if base_key not in st.session_state.used_ui_keys:
        st.session_state.used_ui_keys.add(base_key)
        return base_key
    
    # Otherwise, append a number to make it unique
    counter = 1
    while f"{base_key}_{counter}" in st.session_state.used_ui_keys:
        counter += 1
    
    unique_key = f"{base_key}_{counter}"
    st.session_state.used_ui_keys.add(unique_key)
    return unique_key

def clear_keys():
    """Clear all registered UI keys"""
    st.session_state.used_ui_keys = set()

def register_keys(keys: Set[str]):
    """Register multiple keys at once"""
    for key in keys:
        st.session_state.used_ui_keys.add(key)

def is_key_used(key: str) -> bool:
    """Check if a key is already used"""
    return key in st.session_state.used_ui_keys
