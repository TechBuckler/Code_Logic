import ast
import asttokens
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



def extract_ir_from_source(source_code, function_name=None):
    """Extract IR model from Python source code."""
    try:
        # Parse the source code
        atok = asttokens.ASTTokens(source_code, parse=True)
        tree = atok.tree
        
        # Find the target function
        target_func = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if function_name is None or node.name == function_name:
                    target_func = node
                    break
        
        if target_func is None:
            return None
        
        # Extract function parameters
        params = [arg.arg for arg in target_func.args.args]
        
        # Extract logic rules
        logic = []
        
        # Process the function body to extract conditional logic
        for node in target_func.body:
            if isinstance(node, ast.If):
                _extract_if_conditions(node, logic, atok)
            elif isinstance(node, ast.Return):
                # Unconditional return at the end
                logic.append({
                    'condition': 'True',
                    'return': _get_return_value(node.value)
                })
        
        return {
            'function_name': target_func.name,
            'params': params,
            'logic': logic
        }
    except Exception as e:
        print(f"Error extracting IR model: {e}")
        return None

def _extract_if_conditions(if_node, logic, atok, parent_conditions=None):
    """Recursively extract conditions from if statements."""
    if parent_conditions is None:
        parent_conditions = []
    
    # Get the condition text
    condition_text = atok.get_text(if_node.test)
    
    # For nested conditions, combine with parent conditions
    if parent_conditions:
        full_condition = f"({' and '.join(parent_conditions)}) and ({condition_text})"
    else:
        full_condition = condition_text
    
    # Process the body of this if statement
    for node in if_node.body:
        if isinstance(node, ast.If):
            # Nested if statement
            _extract_if_conditions(node, logic, atok, parent_conditions + [condition_text])
        elif isinstance(node, ast.Return):
            # Return statement
            logic.append({
                'condition': full_condition,
                'return': _get_return_value(node.value)
            })
    
    # Process the else branch if it exists
    if if_node.orelse:
        if len(if_node.orelse) == 1 and isinstance(if_node.orelse[0], ast.If):
            # This is an elif branch
            _extract_if_conditions(if_node.orelse[0], logic, atok, parent_conditions)
        else:
            # This is an else branch
            if parent_conditions:
                else_condition = f"({' and '.join(parent_conditions)}) and (not ({condition_text}))"
            else:
                else_condition = f"not ({condition_text})"
            
            for node in if_node.orelse:
                if isinstance(node, ast.If):
                    _extract_if_conditions(node, logic, atok, parent_conditions + [f"not ({condition_text})"])
                elif isinstance(node, ast.Return):
                    logic.append({
                        'condition': else_condition,
                        'return': _get_return_value(node.value)
                    })

def _get_return_value(node):
    """Extract the return value from an AST node."""
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.NameConstant):
        return node.value
    elif isinstance(node, ast.Name):
        # This is a variable, we'll just use its name as a string
        return node.id
    elif isinstance(node, ast.Constant):
        # Python 3.8+ uses Constant instead of Num/Str/NameConstant
        return node.value
    else:
        # For more complex expressions, we can't easily represent them
        # Just return a string representation
        return str(node.__class__.__name__)

def get_ir_model(source_code=None, function_name=None):
    """Get the IR model, either from provided code or use the default example."""
    if source_code:
        model = extract_ir_from_source(source_code, function_name)
        if model:
            return model
    
    # Default example if extraction fails or no source provided
    return {
        'function_name': 'decide',
        'params': ['cpu', 'is_question', 'is_command'],
        'logic': [
            {'condition': 'is_command', 'return': 3},
            {'condition': 'is_question and cpu < 95', 'return': 2},
            {'condition': 'is_question', 'return': 1},
            {'condition': 'True', 'return': 0}
        ]
    }
