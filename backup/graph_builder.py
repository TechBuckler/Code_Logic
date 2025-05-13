import ast
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



def build_function_graph(functions):
    G = nx.DiGraph()
    
    # Add all functions as nodes
    function_names = {f['name']: f for f in functions}
    for f in functions:
        G.add_node(f['name'])
    
    # Analyze function bodies for calls to other functions
    for f in functions:
        # Extract function calls from the AST body
        calls = []
        for node in ast.walk(ast.Module(body=f['body'])):
            if isinstance(node, ast.Call) and hasattr(node, 'func'):
                if hasattr(node.func, 'id') and node.func.id in function_names:
                    calls.append(node.func.id)
                elif hasattr(node.func, 'attr') and node.func.attr in function_names:
                    calls.append(node.func.attr)
        
        # Add edges for function calls
        for called_func in calls:
            G.add_edge(f['name'], called_func)
    
    # If no edges were found, add a note to the graph
    if len(G.edges()) == 0:
        G.add_node("No function calls detected")
        for f in functions:
            G.add_edge(f['name'], "No function calls detected")
    
    # Draw the graph with a better layout
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=2000, font_size=10, font_weight='bold', 
            arrows=True, arrowsize=15)
    plt.savefig("function_graph.png", dpi=300, bbox_inches='tight')
    print("Graph saved to function_graph.png")
