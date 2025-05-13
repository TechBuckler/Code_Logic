# Fix imports for reorganized codebase



class OptimizerModule(Module):
    def __init__(self):
        super().__init__("optimizer")
        self.dependencies = ["ir_generator"]
        
    def can_process(self, data):
        return super().can_process(data) and isinstance(data, dict) and 'logic' in data
        
    def process(self, data, context=None):
        optimization_results = optimize_logic(data)
        return optimization_results
