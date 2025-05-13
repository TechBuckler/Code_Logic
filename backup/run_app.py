#!/usr/bin/env python3
"""
Run the Logic Tool UI with safe execution
"""
import sys
import os
import psutil
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



def kill_process_tree(pid):
    """Kill a process and all its children."""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        # Kill children
        for child in children:
            try:
                child.terminate()
            except Exception:
                pass
        
        # Wait for children to terminate
        gone, still_alive = psutil.wait_procs(children, timeout=3)
        
        # Force kill any remaining children
        for child in still_alive:
            try:
                child.kill()
            except Exception:
                pass
                
        # Kill parent
        try:
            parent.terminate()
            parent.wait(3)
        except Exception:
            try:
                parent.kill()
            except Exception:
                pass
    except Exception:
        pass

def main():
    """
    Run the Streamlit app with proper Python module imports and safe execution.
    """
    # Add the current directory to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Get the path to the unified UI
    ui_path = os.path.join(current_dir, "src", "unified_ui.py")
    
    # Run the Streamlit app with safety wrapper
    try:
        print(f"Starting Logic Tool UI from {ui_path}")
        sys.argv = [
            "streamlit", "run", 
            ui_path,
            "--browser.gatherUsageStats=false"
        ]
        return stcli.main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        # Find and kill any streamlit processes
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'streamlit' in proc.info['name'].lower() or 'python' in proc.info['name'].lower():
                    # Check if this is one of our streamlit processes
                    cmdline = proc.cmdline()
                    if any('streamlit' in cmd.lower() for cmd in cmdline) and any('unified_ui.py' in cmd for cmd in cmdline):
                        kill_process_tree(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return 130
    except Exception as e:
        print(f"Error running UI: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
