# Fix imports for reorganized codebase



class ProofEngineModule(Module):
    def __init__(self):
        super().__init__("proof_engine")
        self.dependencies = ["ir_generator"]
        
    def can_process(self, data):
        return super().can_process(data) and isinstance(data, dict) and 'logic' in data
        
    def process(self, data, context=None):
        result = run_z3_proof(data)
        # Add proof result to the IR model
        data['proof_result'] = result
        return data
