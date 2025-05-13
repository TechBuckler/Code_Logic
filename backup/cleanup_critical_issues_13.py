"""
cleanup_critical_issues_13.py - Part 13 of 14 from cleanup_critical_issues.py
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import ast


class ResourceManagementVisitor(ast.NodeVisitor):
    """AST visitor to find resource management issues."""

    def __init__(self):
        self.file_ops = []
        self.with_contexts = []

    def visit_Call(self, node):
        """Visit Call nodes to find file operations."""
        if isinstance(node.func, ast.Name) and node.func.id in ['open', 'file']:
            self.file_ops.append({'node': node, 'lineno': node.lineno})
        elif isinstance(node.func, ast.Attribute) and node.func.attr in ['open', 'file']:
            self.file_ops.append({'node': node, 'lineno': node.lineno})
        self.generic_visit(node)

    def visit_With(self, node):
        """Visit With nodes to track context manager usage."""
        for item in node.items:
            if isinstance(item.context_expr, ast.Call):
                call = item.context_expr
                if isinstance(call.func, ast.Name) and call.func.id in ['open', 'file'] or (isinstance(call.func, ast.Attribute) and call.func.attr in ['open', 'file']):
                    self.with_contexts.append({'node': node, 'lineno': node.lineno})
        self.generic_visit(node)

