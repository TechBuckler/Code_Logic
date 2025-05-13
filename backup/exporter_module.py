import os
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



class ExporterModule(Module):
    def __init__(self):
        super().__init__("exporter")
        self.dependencies = ["ir_generator"]
        
    def can_process(self, data):
        return super().can_process(data) and isinstance(data, dict) and 'logic' in data
        
    def process(self, data, context=None):
        output_dir = context.get('output_dir', '.') if context else '.'
        python_code = export_to_python(data)
        
        # Save the exported code
        if 'function_name' in data:
            code_path = os.path.join(output_dir, f"{data['function_name']}_optimized.py")
            with open(code_path, "w") as f:
                f.write(python_code)
                
        return python_code
