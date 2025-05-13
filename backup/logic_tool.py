import argparse
import sys
import os
import importlib
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the centralized imports module
importlib.import_module('src.imports')

# Import runtime optimization components
    runtime_optimizer,
    integrate_with_pipeline,
    initialize as initialize_runtime
)

def main():
    parser = argparse.ArgumentParser(description="Logic Optimization Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    # Analysis command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze decision logic")
    analyze_parser.add_argument("--file", "-f", help="Path to Python file")
    analyze_parser.add_argument("--function", "-n", help="Function name")
    analyze_parser.add_argument("--output", "-o", default=".", help="Output directory")
    analyze_parser.add_argument("--runtime", "-r", action="store_true", help="Apply runtime optimization")
    
    # UI command
    ui_parser = subparsers.add_parser("ui", help="Start the UI")
    ui_parser.add_argument("--port", "-p", type=int, default=8501, help="UI port")
    
    # Background command
    bg_parser = subparsers.add_parser("background", help="Run background tasks")
    bg_parser.add_argument("--task", "-t", choices=["optimize", "mine"], default="optimize", help="Task to run")
    
    # Runtime optimization commands
    runtime_parser = subparsers.add_parser("runtime", help="Runtime optimization commands")
    runtime_subparsers = runtime_parser.add_subparsers(dest="runtime_command")
    
    # Pattern mining command
    mine_parser = runtime_subparsers.add_parser("mine", help="Mine patterns from code")
    mine_parser.add_argument("--directory", "-d", required=True, help="Directory to mine patterns from")
    mine_parser.add_argument("--output", "-o", help="Output file for patterns")
    
    # Optimize file command
    optimize_parser = runtime_subparsers.add_parser("optimize", help="Optimize a Python file")
    optimize_parser.add_argument("--file", "-f", required=True, help="File to optimize")
    optimize_parser.add_argument("--output", "-o", help="Output file for optimized code")
    optimize_parser.add_argument("--patterns", "-p", help="Patterns file to use")
    
    # Agent command
    agent_parser = runtime_subparsers.add_parser("agent", help="Control the adaptive agent")
    agent_parser.add_argument("--action", "-a", choices=["start", "stop", "status"], default="status", help="Agent action")
    
    args = parser.parse_args()
    
    # Initialize runtime optimization system
    initialize_runtime()
    
    if args.command == "analyze":
        # Import here to avoid circular imports
        
        if args.file:
            with open(args.file, 'r') as f:
                source_code = f.read()
            
            # Run the pipeline
            results = run_pipeline(source_code, args.function, args.output)
            
            # Apply runtime optimization if requested
            if args.runtime and results:
                print("\nApplying runtime optimization...")
                optimized_results = integrate_with_pipeline(results)
                
                # Generate optimized file
                if 'ir_model' in optimized_results and 'function_name' in optimized_results['ir_model']:
                    func_name = optimized_results['ir_model']['function_name']
                    output_file = os.path.join(args.output, f"{func_name}_runtime_optimized.py")
                    
                    with open(output_file, 'w') as f:
                        f.write(optimized_results.get('runtime_optimized_code', ''))
                    
                    print(f"Runtime optimized code saved to {output_file}")
        else:
            print("No file specified")
            return 1
    
    elif args.command == "ui":
        # Run the Streamlit UI
        os.system(f"streamlit run src/unified_ui.py --browser.gatherUsageStats=false --server.port={args.port}")
    
    elif args.command == "background":
        # Import here to avoid circular imports
        
        bg = BackgroundSystem()
        bg.start()
        
        if args.task == "optimize":
            def optimize_task():
                print("Running optimization in background")
                # Use runtime optimizer
                stats = runtime_optimizer.get_stats()
                print(f"Current optimization stats: {stats}")
                
            bg.add_task(optimize_task)
            print("Added optimization task to background queue")
            
        elif args.task == "mine":
            def mine_task():
                print("Mining patterns in background")
                # Use pattern miner from runtime utils
                mine_patterns_from_directory(current_dir)
                
            bg.add_task(mine_task)
            print("Added pattern mining task to background queue")
            
        # Keep running until interrupted
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping background system")
            bg.stop()
    
    elif args.command == "runtime":
        if args.runtime_command == "mine":
            # Mine patterns from code
            output_file = mine_patterns_from_directory(args.directory, args.output)
            print(f"Mined patterns saved to {output_file}")
            
        elif args.runtime_command == "optimize":
            # Optimize a file
            output_file = optimize_file(args.file, args.output, args.patterns)
            print(f"Optimized code saved to {output_file}")
            
        elif args.runtime_command == "agent":
            # Control the adaptive agent
            if args.action == "start":
                runtime_optimizer.start()
                print("Adaptive agent started")
                
            elif args.action == "stop":
                runtime_optimizer.stop()
                print("Adaptive agent stopped")
                
            elif args.action == "status":
                stats = runtime_optimizer.get_stats()
                print("Adaptive Agent Status:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
        else:
            parser.print_help()
            return 1
    
    else:
        parser.print_help()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
