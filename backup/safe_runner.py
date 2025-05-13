"""
Safe Run Wrapper for Logic Tool

This script provides a robust wrapper around the Logic Tool CLI commands,
ensuring proper process termination and error handling.
"""
import os
import sys
import subprocess
import time
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
    # Default timeout
    timeout = 60
    
    # Get all arguments after the script name
    args = sys.argv[1:]
    
    # Check if --safe-timeout is specified
    if len(args) >= 2 and args[0] == "--safe-timeout":
        try:
            timeout = int(args[1])
            # Remove these arguments so they're not passed to logic_tool.py
            args = args[2:]
        except ValueError:
            print("Invalid timeout value, using default 60 seconds")
    
    # Build the command with all remaining arguments
    cmd = ["py", "logic_tool.py"] + args
    
    print(f"Running command: {' '.join(cmd)}")
    print(f"Timeout set to {timeout} seconds")
    
    start_time = time.time()
    
    # Start the process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        
        elapsed = time.time() - start_time
        print(f"Command completed in {elapsed:.2f} seconds")
        print("Output:")
        print(stdout)
        
        if stderr:
            print("Errors:")
            print(stderr)
            
        return process.returncode
        
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds")
        kill_process_tree(process.pid)
        print("Process terminated")
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        kill_process_tree(process.pid)
        return 130

if __name__ == "__main__":
    sys.exit(main())
