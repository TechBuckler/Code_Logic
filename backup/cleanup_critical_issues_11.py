"""
cleanup_critical_issues_11.py - Part 11 of 14 from cleanup_critical_issues.py
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import ast


class ImportVisitor(ast.NodeVisitor):
    """AST visitor to find unused imports."""

    def __init__(self):
        self.imports = []
        self.used_names = set()

    def visit_Import(self, node):
        """Visit Import nodes."""
        for name in node.names:
            alias = name.asname if name.asname else name.name
            self.imports.append({'name': name.name, 'alias': alias, 'node': node, 'lineno': node.lineno})
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Visit ImportFrom nodes."""
        module = node.module if node.module else ''
        for name in node.names:
            alias = name.asname if name.asname else name.name
            self.imports.append({'name': f'{module}.{name.name}' if module else name.name, 'alias': alias, 'node': node, 'lineno': node.lineno})
        self.generic_visit(node)

    def visit_Name(self, node):
        """Visit Name nodes to track used names."""
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Visit Attribute nodes to track used module attributes."""
        if isinstance(node.value, ast.Name):
            self.used_names.add(node.value.id)
        self.generic_visit(node)

