"""
AST Explorer Utility

This module provides tools for exploring and visualizing Python ASTs for analysis and transformation.
"""
import ast
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



def extract_functions(source):
    tree = ast.parse(source)
    functions = []

    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            functions.append({
                'name': node.name,
                'args': [arg.arg for arg in node.args.args],
                'body': node.body
            })
            self.generic_visit(node)

    FunctionVisitor().visit(tree)
    return functions
