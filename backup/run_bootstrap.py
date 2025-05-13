"""
Run the bootstrap process to generate the new hierarchical architecture
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the bootstrap module

if __name__ == "__main__":
    print("Starting bootstrap process...")
    result = run_bootstrap()
    
    if "error" in result:
        print(f"Bootstrap failed: {result['error']}")
        sys.exit(1)
    else:
        print("Bootstrap completed successfully!")
        print(f"Generated {len(result['generation']['modules'])} modules")
        print(f"Transformed {len(result['transformation']['modules'])} modules")
        print(f"New entry point: {result['transformation']['entry_point']}")
        
        # Print instructions for running the new system
        print("\nTo run the new system:")
        print(f"1. Navigate to {os.path.dirname(result['transformation']['entry_point'])}")
        print("2. Run: python main.py")
