"""
Runtime Utilities for the Logic Tool System.
This file provides functions that bridge the logic analysis and runtime optimization components.
"""
import os
import ast
import inspect
import time
import threading
import json
import hashlib
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



# Pattern mining and optimization utilities
class PatternMiner:
    """Mines patterns from Python code for optimization."""
    
    def __init__(self, cache_dir="./pdict-cache"):
        self.cache_dir = cache_dir
        self.patterns = defaultdict(int)
        self.function_patterns = {}
        os.makedirs(cache_dir, exist_ok=True)
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file for patterns."""
        try:
            with open(file_path, 'r') as f:
                source = f.read()
            
            tree = ast.parse(source)
            file_patterns = self._extract_patterns(tree)
            
            # Update global patterns
            for pattern, count in file_patterns.items():
                self.patterns[pattern] += count
                
            return file_patterns
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return {}
    
    def analyze_directory(self, directory: str) -> Dict[str, Any]:
        """Analyze all Python files in a directory."""
        results = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    results[file_path] = self.analyze_file(file_path)
        return results
    
    def save_patterns(self, output_file: str = None) -> str:
        """Save mined patterns to a file."""
        if output_file is None:
            output_file = os.path.join(self.cache_dir, f"patterns_{int(time.time())}.json")
            
        with open(output_file, 'w') as f:
            json.dump({
                'patterns': dict(self.patterns),
                'function_patterns': self.function_patterns,
                'timestamp': time.time()
            }, f, indent=2)
            
        return output_file
    
    def load_patterns(self, input_file: str) -> Dict[str, Any]:
        """Load patterns from a file."""
        with open(input_file, 'r') as f:
            data = json.load(f)
            
        self.patterns = defaultdict(int, data.get('patterns', {}))
        self.function_patterns = data.get('function_patterns', {})
        return data
    
    def _extract_patterns(self, tree: ast.AST) -> Dict[str, int]:
        """Extract patterns from an AST."""
        patterns = Counter()
        
        # Extract condition patterns
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                pattern = self._serialize_condition(node.test)
                if pattern:
                    patterns[pattern] += 1
                    
            elif isinstance(node, ast.FunctionDef):
                # Store patterns by function
                func_patterns = {}
                for subnode in ast.walk(node):
                    if isinstance(subnode, ast.If):
                        pattern = self._serialize_condition(subnode.test)
                        if pattern:
                            func_patterns[pattern] = func_patterns.get(pattern, 0) + 1
                
                if func_patterns:
                    self.function_patterns[node.name] = func_patterns
        
        return patterns
    
    def _serialize_condition(self, node: ast.AST) -> str:
        """Serialize a condition node to a pattern string."""
        try:
            if isinstance(node, ast.Compare):
                # Handle comparisons like a < b, a == b, etc.
                left = self._get_node_type(node.left)
                ops = [type(op).__name__ for op in node.ops]
                comparators = [self._get_node_type(comp) for comp in node.comparators]
                return f"{left}{''.join(f'{op}{comp}' for op, comp in zip(ops, comparators))}"
                
            elif isinstance(node, ast.BoolOp):
                # Handle boolean operations like and, or
                op_name = type(node.op).__name__
                values = [self._serialize_condition(val) for val in node.values]
                return f"({op_name.join(values)})"
                
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
                # Handle not operations
                return f"Not({self._serialize_condition(node.operand)})"
                
            else:
                # Generic fallback
                return type(node).__name__
        except Exception:
            return ""
    
    def _get_node_type(self, node: ast.AST) -> str:
        """Get a type descriptor for a node."""
        if isinstance(node, ast.Name):
            return f"Var({node.id})"
        elif isinstance(node, ast.Num):
            return f"Num({type(node.n).__name__})"
        elif isinstance(node, ast.Str):
            return "Str"
        elif isinstance(node, ast.NameConstant) and node.value in (True, False, None):
            return str(node.value)
        else:
            return type(node).__name__

class TokenInjector:
    """Injects optimization tokens into Python code."""
    
    def __init__(self, pattern_file: str = None):
        self.patterns = {}
        if pattern_file and os.path.exists(pattern_file):
            self.load_patterns(pattern_file)
    
    def load_patterns(self, pattern_file: str) -> None:
        """Load patterns from a file."""
        with open(pattern_file, 'r') as f:
            data = json.load(f)
        self.patterns = data.get('patterns', {})
    
    def inject_tokens(self, source_file: str, output_file: str = None) -> str:
        """Inject optimization tokens into a Python file."""
        if output_file is None:
            base, ext = os.path.splitext(source_file)
            output_file = f"{base}_optimized{ext}"
            
        with open(source_file, 'r') as f:
            source = f.read()
            
        # Parse the source code
        tree = ast.parse(source)
        
        # Modify the AST to add optimization tokens
        transformer = self._OptimizationTransformer(self.patterns)
        optimized_tree = transformer.visit(tree)
        
        # Generate the optimized source code
        optimized_source = ast.unparse(optimized_tree)
        
        # Add imports for runtime optimization
        imports = "\n".join([
            "# Runtime optimization imports",
            "import runtime_optimization as rtopt",
            ""
        ])
        
        optimized_source = imports + optimized_source
        
        # Write the optimized source to the output file
        with open(output_file, 'w') as f:
            f.write(optimized_source)
            
        return output_file
    
    class _OptimizationTransformer(ast.NodeTransformer):
        """AST transformer for adding optimization tokens."""
        
        def __init__(self, patterns: Dict[str, int]):
            self.patterns = patterns
            
        def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
            """Add optimization decorators to functions."""
            # Process the function body
            self.generic_visit(node)
            
            # Add optimization decorator
            node.decorator_list.append(
                ast.Call(
                    func=ast.Name(id='rtopt.optimize', ctx=ast.Load()),
                    args=[],
                    keywords=[]
                )
            )
            
            return node
            
        def visit_If(self, node: ast.If) -> ast.If:
            """Add optimization hints to if statements."""
            # Process the if statement body
            self.generic_visit(node)
            
            # Wrap the test condition in an optimization hint
            node.test = ast.Call(
                func=ast.Name(id='rtopt.condition', ctx=ast.Load()),
                args=[node.test],
                keywords=[]
            )
            
            return node

# Runtime optimization utilities
class AdaptiveAgent:
    """Agent for adaptive runtime optimization."""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.optimized_functions = {}
        self.performance_metrics = defaultdict(list)
        
    def start(self, daemon: bool = True) -> None:
        """Start the adaptive agent."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop)
            self.thread.daemon = daemon
            self.thread.start()
            
    def stop(self) -> None:
        """Stop the adaptive agent."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
    def register_function(self, func: Callable, metadata: Dict[str, Any] = None) -> None:
        """Register a function for optimization."""
        func_name = func.__name__
        func_hash = self._hash_function(func)
        
        self.optimized_functions[func_name] = {
            'function': func,
            'hash': func_hash,
            'metadata': metadata or {},
            'calls': 0,
            'total_time': 0,
            'last_optimized': 0
        }
        
    def _monitor_loop(self) -> None:
        """Background monitoring loop."""
        while self.running:
            # Check for functions that need optimization
            current_time = time.time()
            for func_name, data in self.optimized_functions.items():
                # Only optimize functions that have been called recently
                if data['calls'] > 0 and current_time - data['last_optimized'] > 60:
                    self._optimize_function(func_name)
                    data['last_optimized'] = current_time
                    
            # Sleep for a bit
            time.sleep(10)
            
    def _optimize_function(self, func_name: str) -> None:
        """Optimize a function based on runtime metrics."""
        if func_name not in self.optimized_functions:
            return
            
        data = self.optimized_functions[func_name]
        func = data['function']
        
        # Calculate average execution time
        avg_time = data['total_time'] / data['calls'] if data['calls'] > 0 else 0
        
        # Reset metrics
        data['calls'] = 0
        data['total_time'] = 0
        
        # Log optimization
        print(f"Optimizing {func_name} (avg time: {avg_time:.6f}s)")
        
    def _hash_function(self, func: Callable) -> str:
        """Generate a hash for a function."""
        try:
            source = inspect.getsource(func)
            return hashlib.md5(source.encode()).hexdigest()
        except Exception:
            return ""

# JIT routing utilities
class JitRouter:
    """Routes function execution to CPU or GPU."""
    
    def __init__(self):
        self.gpu_available = self._check_gpu()
        self.routing_cache = {}
        
    def route(self, func: Callable) -> Callable:
        """Route a function to CPU or GPU."""
        func_name = func.__name__
        
        # Check if we've already decided for this function
        if func_name in self.routing_cache:
            return self.routing_cache[func_name]
            
        # Determine if the function should run on GPU
        if self.gpu_available and self._is_gpu_candidate(func):
            # In a real implementation, this would compile for GPU
            print(f"Routing {func_name} to GPU")
            self.routing_cache[func_name] = func  # Placeholder for GPU version
        else:
            # Keep on CPU
            self.routing_cache[func_name] = func
            
        return self.routing_cache[func_name]
        
    def _check_gpu(self) -> bool:
        """Check if GPU is available."""
        # This would be a real check in production
        return False
        
    def _is_gpu_candidate(self, func: Callable) -> bool:
        """Determine if a function is a good GPU candidate."""
        # This would be a real analysis in production
        try:
            source = inspect.getsource(func)
            # Simple heuristic: functions with loops might benefit from GPU
            return 'for ' in source or 'while ' in source
        except Exception:
            return False

# Create singleton instances
pattern_miner = PatternMiner()
token_injector = TokenInjector()
adaptive_agent = AdaptiveAgent()
jit_router = JitRouter()

# Decorator for runtime optimization
def optimize(func: Callable) -> Callable:
    """Decorator for runtime optimization."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Register with adaptive agent if not already
        if func.__name__ not in adaptive_agent.optimized_functions:
            adaptive_agent.register_function(func)
            
        # Update metrics
        data = adaptive_agent.optimized_functions[func.__name__]
        data['calls'] += 1
        data['total_time'] += (end_time - start_time)
        
        return result
    
    return wrapper

# Function for optimizing conditions
def condition(cond):
    """Runtime optimization for conditions."""
    # In a real implementation, this would do something useful
    return cond

# Main functions that can be called from outside
def start_runtime_optimization():
    """Start the runtime optimization system."""
    adaptive_agent.start()
    print("Runtime optimization system started")
    
def stop_runtime_optimization():
    """Stop the runtime optimization system."""
    adaptive_agent.stop()
    print("Runtime optimization system stopped")
    
def mine_patterns_from_directory(directory: str, output_file: str = None) -> str:
    """Mine patterns from a directory of Python files."""
    pattern_miner.analyze_directory(directory)
    return pattern_miner.save_patterns(output_file)
    
def optimize_file(input_file: str, output_file: str = None, pattern_file: str = None) -> str:
    """Optimize a Python file using mined patterns."""
    if pattern_file:
        token_injector.load_patterns(pattern_file)
    return token_injector.inject_tokens(input_file, output_file)

# Integration with the module system
def register_runtime_modules(registry):
    """Register runtime modules with the module registry."""
    
    class PatternMiningModule(Module):
        def __init__(self):
            super().__init__("pattern_mining")
            
        def process(self, data, context=None):
            if isinstance(data, str) and os.path.isdir(data):
                return mine_patterns_from_directory(data)
            return data
    
    class TokenInjectionModule(Module):
        def __init__(self):
            super().__init__("token_injection")
            self.dependencies = ["ir_generator"]
            
        def process(self, data, context=None):
            if isinstance(data, dict) and 'function_name' in data:
                # This would optimize the generated code in a real implementation
                return data
            return data
    
    class JitRoutingModule(Module):
        def __init__(self):
            super().__init__("jit_routing")
            
        def process(self, data, context=None):
            # This would route functions to CPU/GPU in a real implementation
            return data
    
    # Register the modules
    registry.register(PatternMiningModule())
    registry.register(TokenInjectionModule())
    registry.register(JitRoutingModule())
    
    return registry
