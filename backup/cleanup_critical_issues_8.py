"""
cleanup_critical_issues_8.py - Part 8 of 14 from cleanup_critical_issues.py
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import ast


def visit_Call(self, node):
    """Visit Call nodes to find file operations."""
    if isinstance(node.func, ast.Name) and node.func.id in ['open', 'file']:
        self.file_ops.append({'node': node, 'lineno': node.lineno})
    elif isinstance(node.func, ast.Attribute) and node.func.attr in ['open', 'file']:
        self.file_ops.append({'node': node, 'lineno': node.lineno})
    self.generic_visit(node)

