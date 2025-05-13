# Fix imports for reorganized codebase



class GraphBuilderModule(Module):
    def __init__(self):
        super().__init__("graph_builder")
        self.dependencies = ["ast_parser"]
        
    def can_process(self, data):
        return super().can_process(data) and isinstance(data, list)
        
    def process(self, data, context=None):
        output_path = context.get('output_path', 'function_graph.png') if context else 'function_graph.png'
        build_function_graph(data)
        return data  # Pass through the functions
