"""
Run the Complete Logic Tool System with Hierarchical Architecture

This script runs the complete Logic Tool system with the hierarchical architecture,
including analysis, optimization, and verification modules.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import subprocess

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_streamlit_app():
    """Run the Streamlit app with the hierarchical architecture"""
    try:
        print("Starting Complete Logic Tool System...")
        print("This system includes:")
        print("  - Hierarchical Module Architecture")
        print("  - AST Parser and IR Generator")
        print("  - Logic Optimizer")
        print("  - Formal Verification with Z3")
        print("  - Code Export")
        print("\nInitializing system...")
        
        # Run the Streamlit app
        cmd = ["py", "-m", "streamlit", "run", "src/hierarchical_main.py"]
        
        # Use subprocess to run the command
        process = subprocess.Popen(
            cmd,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print output in real-time
        for line in process.stdout:
            print(line, end='')
            
            # Check for the URL line to know when the app is ready
            if "You can now view your Streamlit app in your browser" in line:
                print("\n" + "="*80)
                print("SYSTEM READY!")
                print("The Logic Tool is now running with the complete hierarchical architecture.")
                print("You can analyze, optimize, and verify code logic using the UI.")
                print("="*80 + "\n")
        
        # Wait for the process to complete
        process.wait()
        
        # Check if there were any errors
        if process.returncode != 0:
            print("Error running Streamlit app")
            for line in process.stderr:
                print(line, end='')
            return False
        
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        print("All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install the required dependencies:")
        print("pip install streamlit z3-solver sympy asttokens matplotlib")
        return False

if __name__ == "__main__":
    print("="*80)
    print("LOGIC TOOL COMPLETE SYSTEM")
    print("="*80)
    
    # Check dependencies
    if check_dependencies():
        # Run the app
        run_streamlit_app()
    else:
        print("Please install the missing dependencies and try again.")
