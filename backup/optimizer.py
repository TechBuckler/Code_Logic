import itertools
import sys
import os
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



# Add the current directory to the Python path
src_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(src_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from ir_model import get_ir_model

def optimize_logic(ir_model=None):
    """Optimize logic using various techniques."""
    if ir_model is None:
        ir_model = get_ir_model()
    
    print(f"Optimizing logic for function '{ir_model['function_name']}'...")
    
    # 1. Generate a lookup table for discrete inputs
    lookup_table = generate_lookup_table(ir_model)
    
    # 2. Simplify conditions using boolean algebra
    simplified_logic = simplify_conditions(ir_model)
    
    # 3. Identify redundant conditions
    redundant_conditions = find_redundant_conditions(simplified_logic)
    if redundant_conditions:
        print(f"Found {len(redundant_conditions)} redundant conditions")
    
    # 4. Merge similar branches
    merged_logic = merge_similar_branches(simplified_logic)
    
    print("Optimization complete")
    return {
        'original': ir_model,
        'simplified': simplified_logic,
        'merged': merged_logic,
        'lookup_table': lookup_table,
        'redundant_conditions': redundant_conditions
    }

def generate_lookup_table(ir_model):
    """Generate a lookup table for the function with discrete inputs."""
    # Identify parameter types and possible values
    param_values = {}
    for param in ir_model['params']:
        # For boolean parameters, use True/False
        if param.startswith('is_') or param in ['enabled', 'active', 'valid']:
            param_values[param] = [True, False]
        # For numeric parameters with clear bounds in conditions
        elif param in ['cpu']:
            # Extract bounds from conditions
            bounds = extract_numeric_bounds(param, ir_model['logic'])
            if bounds:
                low, high = bounds
                # If the range is small enough, enumerate all values
                if high - low < 100:
                    param_values[param] = list(range(low, high + 1))
                else:
                    # Otherwise sample key points around thresholds
                    thresholds = extract_thresholds(param, ir_model['logic'])
                    sample_points = set()
                    for t in thresholds:
                        sample_points.update([t-1, t, t+1])
                    param_values[param] = sorted(list(sample_points))
            else:
                # Default range if no bounds found
                param_values[param] = [0, 50, 100]
        else:
            # For other parameters, use some reasonable defaults
            param_values[param] = [None, 0, 1, ""]
    
    # Generate all combinations of parameter values
    param_names = ir_model['params']
    param_combinations = list(itertools.product(*[param_values[p] for p in param_names]))
    
    # Evaluate the function for each combination
    table = {}
    for combo in param_combinations:
        param_dict = {param_names[i]: combo[i] for i in range(len(param_names))}
        result = evaluate_logic(ir_model['logic'], param_dict)
        table[combo] = result
    
    print(f"Generated lookup table with {len(table)} entries")
    return table

def extract_numeric_bounds(param, logic):
    """Extract numeric bounds for a parameter from conditions."""
    min_val = float('inf')
    max_val = float('-inf')
    
    # Look for conditions like 'param < X' or 'param > X'
    for rule in logic:
        condition = rule['condition']
        # Simple parsing for common patterns
        if f"{param} <" in condition or f"{param}<" in condition:
            try:
                # Extract the number after '<'
                parts = condition.split('<')
                for part in parts:
                    if part.strip().startswith(param):
                        continue
                    num = int(''.join(c for c in part if c.isdigit()))
                    max_val = max(max_val, num)
            except Exception:
                pass
        if f"{param} >" in condition or f"{param}>" in condition:
            try:
                # Extract the number after '>'
                parts = condition.split('>')
                for part in parts:
                    if part.strip().startswith(param):
                        continue
                    num = int(''.join(c for c in part if c.isdigit()))
                    min_val = min(min_val, num)
            except Exception:
                pass
    
    if min_val < max_val:
        return (min_val, max_val)
    return None

def extract_thresholds(param, logic):
    """Extract threshold values for a parameter from conditions."""
    thresholds = set()
    
    # Look for conditions with numeric comparisons
    for rule in logic:
        condition = rule['condition']
        # Simple parsing for common patterns
        for op in ['<', '>', '==', '!=', '<=', '>=']:
            if f"{param} {op}" in condition or f"{param}{op}" in condition:
                try:
                    # Extract the number after the operator
                    parts = condition.split(op)
                    for part in parts:
                        if part.strip().startswith(param):
                            continue
                        num = int(''.join(c for c in part if c.isdigit()))
                        thresholds.add(num)
                except Exception:
                    pass
    
    return sorted(list(thresholds))

def evaluate_logic(logic, params):
    """Evaluate the logic rules with the given parameters."""
    for rule in logic:
        try:
            # Evaluate the condition in the context of the parameters
            if eval(rule['condition'], {}, params):
                return rule['return']
        except Exception:
            continue
    return None

def simplify_conditions(ir_model):
    """Simplify conditions using boolean algebra."""
    simplified_logic = []
    
    for rule in ir_model['logic']:
        condition = rule['condition']
        return_val = rule['return']
        
        # Skip already simplified conditions
        if condition == 'True':
            simplified_logic.append(rule)
            continue
        
        try:
            # Convert condition to sympy expression for simplification
            # This is a simplified approach - a real implementation would need more parsing
            condition = condition.replace('and', '&').replace('or', '|').replace('not', '~')
            for param in ir_model['params']:
                condition = condition.replace(param, f"symbols('{param}')")
            
            # Add the simplified rule
            simplified_logic.append({
                'condition': condition.replace('&', 'and').replace('|', 'or').replace('~', 'not'),
                'return': return_val
            })
        except Exception:
            # If simplification fails, keep the original
            simplified_logic.append(rule)
    
    return simplified_logic

def find_redundant_conditions(logic):
    """Find redundant conditions in the logic."""
    redundant = []
    
    # This is a simplified implementation
    # A real implementation would use a SAT solver or similar
    for i, rule1 in enumerate(logic):
        for j, rule2 in enumerate(logic):
            if i != j and rule1['return'] == rule2['return']:
                # Check if rule1's condition implies rule2's
                # This is a very simplified check
                if rule1['condition'] in rule2['condition']:
                    redundant.append((j, f"Condition {rule2['condition']} is redundant with {rule1['condition']}"))
    
    return redundant

def merge_similar_branches(logic):
    """Merge branches with the same return value."""
    merged = {}
    
    # Group by return value
    for rule in logic:
        ret_val = rule['return']
        if ret_val not in merged:
            merged[ret_val] = []
        merged[ret_val].append(rule['condition'])
    
    # Combine conditions for each return value
    result = []
    for ret_val, conditions in merged.items():
        if len(conditions) == 1:
            result.append({
                'condition': conditions[0],
                'return': ret_val
            })
        else:
            # Combine with OR
            combined = " or ".join([f"({c})" for c in conditions if c != 'True'])
            if not combined:  # Only 'True' conditions
                combined = 'True'
            result.append({
                'condition': combined,
                'return': ret_val
            })
    
    return result
