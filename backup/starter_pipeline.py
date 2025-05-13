import argparse
import os
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



# Use the centralized imports system
    extract_functions,
    run_z3_proof,
    build_function_graph,
    get_ir_model,
    extract_ir_from_source,
    optimize_logic,
    export_to_python,
    load_module_from_file
)

# Default sample code if no file is provided
DEFAULT_CODE = """
def decide(cpu, is_question, is_command):
    if is_command:
        return 3
    elif is_question and cpu < 95:
        return 2
    elif is_question:
        return 1
    else:
        return 0
"""

def run_pipeline(source_code=None, function_name=None, output_dir="."):
    """Run the complete logic analysis pipeline."""
    # Use default code if none provided
    if source_code is None:
        source_code = DEFAULT_CODE
        print("Using default example code...")
    
    # Step 1: Extract functions from the code
    print("\nExtracting functions...")
    functions = extract_functions(source_code)
    print(f"Found {len(functions)} functions")
    
    # If function_name is not specified but there's only one function, use it
    if function_name is None and len(functions) == 1:
        function_name = functions[0]['name']
        print(f"Using function: {function_name}")
    
    # Step 2: Extract IR model
    print("\nExtracting IR model...")
    ir_model = get_ir_model(source_code, function_name)
    if ir_model:
        print(f"Extracted IR model for '{ir_model['function_name']}' with {len(ir_model['logic'])} logic rules")
    else:
        print("Failed to extract IR model")
        return
    
    # Step 3: Run formal proof
    print("\nRunning formal proof...")
    run_z3_proof(ir_model)
    
    # Step 4: Generate function graph
    print("\nGenerating function graph...")
    graph_path = os.path.join(output_dir, "function_graph.png")
    build_function_graph(functions)
    print(f"Graph saved to {graph_path}")
    
    # Step 5: Optimize the logic
    print("\nOptimizing logic...")
    optimization_results = optimize_logic(ir_model)
    
    # Step 6: Export to Python
    print("\nExporting to Python...")
    python_code = export_to_python(ir_model)
    print("\nGenerated Python code:")
    print("------------------------")
    print(python_code)
    print("------------------------")
    
    # Save the exported code
    code_path = os.path.join(output_dir, f"{ir_model['function_name']}_optimized.py")
    with open(code_path, "w") as f:
        f.write(python_code)
    print(f"Exported code saved to {code_path}")
    
    print("\nPipeline completed successfully!")
    return {
        'functions': functions,
        'ir_model': ir_model,
        'optimization': optimization_results,
        'exported_code': python_code
    }

def parse_arguments():
    parser = argparse.ArgumentParser(description='Logic Tool Pipeline')
    parser.add_argument('--file', '-f', help='Path to Python file to analyze')
    parser.add_argument('--function', '-n', help='Name of function to analyze')
    parser.add_argument('--output', '-o', default='.', help='Output directory for generated files')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Load source code from file if specified
    source_code = None
    if args.file:
        try:
            with open(args.file, 'r') as f:
                source_code = f.read()
            print(f"Loaded source code from {args.file}")
        except Exception as e:
            print(f"Error loading file: {e}")
            source_code = DEFAULT_CODE
    
    # Run the pipeline
    run_pipeline(source_code, args.function, args.output)
