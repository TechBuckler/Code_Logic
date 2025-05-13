"""
Simple File Scanner

This script scans the codebase and prints each file as it's found,
without storing everything in memory.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import time

def scan_directory(directory_path: str, exclude_dirs: List[str] = None, 
                  max_depth: Optional[int] = None, current_depth: int = 0):
    """
    Scan a directory and print each file as it's found
    
    Args:
        directory_path: Path to the directory to scan
        exclude_dirs: Directories to exclude
        max_depth: Maximum depth to scan
        current_depth: Current depth in the directory tree
    """
    if exclude_dirs is None:
        exclude_dirs = ["__pycache__", ".git", "pdict-cache"]
        
    # Check if we've reached the maximum depth
    if max_depth is not None and current_depth > max_depth:
        return
    
    try:
        # List all items in the directory
        items = os.listdir(directory_path)
        
        # Process each item
        for item_name in sorted(items):
            item_path = os.path.join(directory_path, item_name)
            
            # Skip excluded directories
            if os.path.isdir(item_path) and item_name in exclude_dirs:
                continue
            
            # Print the current item with proper indentation
            prefix = "  " * current_depth
            if os.path.isdir(item_path):
                print(f"{prefix}📁 {item_name}/")
                
                # Recursively scan subdirectory
                scan_directory(item_path, exclude_dirs, max_depth, current_depth + 1)
            else:
                # Print file with extension
                _, ext = os.path.splitext(item_name)
                print(f"{prefix}📄 {item_name}")
    
    except Exception as e:
        print(f"Error scanning {directory_path}: {e}")

def main():
    """Main entry point for the script"""
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Scanning directory: {script_dir}")
    print("=" * 50)
    
    # Start the scan
    start_time = time.time()
    scan_directory(script_dir)
    end_time = time.time()
    
    print("=" * 50)
    print(f"Scan completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
