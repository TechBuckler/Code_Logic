# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



class IrGeneratorModule(Module):
    def __init__(self):
        super().__init__("ir_generator")
        self.dependencies = ["ast_parser"]
        
    def can_process(self, data):
        return super().can_process(data) and (isinstance(data, str) or isinstance(data, list))
        
    def process(self, data, context=None):
        function_name = context.get('function_name') if context else None
        
        if isinstance(data, str):
            # Raw source code
            return get_ir_model(data, function_name)
        elif isinstance(data, list) and len(data) > 0:
            # List of functions from AST parser
            if function_name is None and len(data) == 1:
                function_name = data[0]['name']
                
            # We need the original source for IR generation
            source = context.get('source') if context else None
            if source:
                return get_ir_model(source, function_name)
        return None
