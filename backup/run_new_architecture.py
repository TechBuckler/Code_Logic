"""
Run the new hierarchical architecture for the Logic Tool
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
    """Run the Streamlit app with the new architecture"""
    try:
        print("Starting Logic Tool with new hierarchical architecture...")
        
        # Run the Streamlit app
        cmd = ["streamlit", "run", "src/new_main.py"]
        
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

if __name__ == "__main__":
    run_streamlit_app()
