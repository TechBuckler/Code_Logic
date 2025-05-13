"""
AST Parser Module

This module defines an AST parser for extracting function definitions and code structure from Python source files.
"""
# Fix imports for reorganized codebase



class AstParserModule(Module):
    def __init__(self):
        super().__init__("ast_parser")
        
    def can_process(self, data):
        return super().can_process(data) and isinstance(data, str)
        
    def process(self, data, context=None):
        return extract_functions(data)
