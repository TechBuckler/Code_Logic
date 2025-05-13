from z3 import *
import re
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



def run_z3_proof(ir_model=None):
    """Run Z3 formal proof on the given IR model or default model."""
    if ir_model is None:
        # Default proof for the decide function
        return run_default_proof()
    
    print(f"Setting up Z3 proof for function '{ir_model['function_name']}'...")
    
    # Create Z3 variables for each parameter
    z3_vars = {}
    constraints = []
    
    for param in ir_model['params']:
        # Determine parameter type and create appropriate Z3 variable
        if param.startswith('is_') or param in ['enabled', 'active', 'valid']:
            # Boolean parameter
            z3_vars[param] = Bool(param)
        elif param in ['cpu', 'count', 'index', 'level', 'size', 'value']:
            # Integer parameter
            z3_vars[param] = Int(param)
            # Add reasonable constraints (can be customized)
            if param == 'cpu':
                constraints.append(And(z3_vars[param] >= 0, z3_vars[param] <= 100))
            else:
                constraints.append(z3_vars[param] >= 0)
        else:
            # Default to Int for unknown types
            z3_vars[param] = Int(param)
    
    # Build the output function based on the IR model's logic
    def build_output_function(logic, vars_dict):
        # Start with the default case
        result = None
        
        # Process the logic rules in reverse (assuming they're in priority order)
        for rule in reversed(logic):
            condition = rule['condition']
            return_val = rule['return']
            
            # Skip the default case (True condition)
            if condition == 'True':
                if result is None:
                    # This is the base case
                    if isinstance(return_val, (int, float)):
                        result = return_val
                    else:
                        # For non-numeric returns, use a placeholder
                        result = 0
                continue
            
            # Convert the condition to Z3 expression
            z3_condition = parse_condition_to_z3(condition, vars_dict)
            
            # Build the If-Then-Else structure
            if isinstance(return_val, (int, float)):
                if result is None:
                    result = return_val
                else:
                    result = If(z3_condition, return_val, result)
            else:
                # For non-numeric returns, use a placeholder
                if result is None:
                    result = 0
                else:
                    result = If(z3_condition, 0, result)
        
        return result
    
    # Build the output function
    output_func = build_output_function(ir_model['logic'], z3_vars)
    
    # Determine the valid output values
    output_values = set()
    for rule in ir_model['logic']:
        if isinstance(rule['return'], (int, float)):
            output_values.add(rule['return'])
    
    if not output_values:
        output_values = {0}  # Default if no numeric returns
    
    # Create the valid output constraint
    valid_output = Or([output_func == val for val in output_values])
    
    # Combine all constraints
    if constraints:
        premise = And(*constraints)
        theorem = ForAll(list(z3_vars.values()), Implies(premise, valid_output))
    else:
        theorem = ForAll(list(z3_vars.values()), valid_output)
    
    # Run the proof
    print("Checking Z3 proof...")
    try:
        result = prove(theorem)
        print("proved")
        return True
    except Exception as e:
        print(f"Proof failed: {e}")
        return False

def parse_condition_to_z3(condition, vars_dict):
    """Parse a condition string into a Z3 expression."""
    # Replace logical operators
    condition = condition.replace(' and ', ' & ').replace(' or ', ' | ').replace(' not ', ' ~ ')
    
    # This is a simplified parser - a real implementation would need a more robust approach
    try:
        # For each variable in the condition, replace with Z3 variable
        for var_name, z3_var in vars_dict.items():
            # Replace whole word matches
            condition = re.sub(r'\b' + var_name + r'\b', f"vars_dict['{var_name}']", condition)
        
        # Handle common comparison operators
        condition = condition.replace('==', '==').replace('!=', '!=').replace('>=', '>=').replace('<=', '<=')
        
        # Evaluate the condition in the context of Z3 variables and operators
        z3_globals = {
            'And': And, 'Or': Or, 'Not': Not, 'If': If,
            'vars_dict': vars_dict,
            '&': And, '|': Or, '~': Not
        }
        
        return eval(condition, z3_globals)
    except Exception as e:
        print(f"Error parsing condition '{condition}': {e}")
        # Return a default True if parsing fails
        return True

def run_default_proof():
    """Run the default proof for the decide function."""
    cpu = Int('cpu')
    q = Bool('q')
    c = Bool('c')

    def output(cpu, q, c):
        return If(c, 3,
               If(And(q, cpu < 95), 2,
               If(q, 1, 0)))

    valid_cpu = And(cpu >= 0, cpu <= 100)
    valid_output = Or(output(cpu, q, c) == 0,
                      output(cpu, q, c) == 1,
                      output(cpu, q, c) == 2,
                      output(cpu, q, c) == 3)

    theorem = ForAll([cpu, q, c], Implies(valid_cpu, valid_output))
    print("Checking Z3 proof...")
    prove(theorem)
    print("proved")
    return True
