"""
cleanup_critical_issues_9.py - Part 9 of 14 from cleanup_critical_issues.py
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import ast


def visit_With(self, node):
    """Visit With nodes to track context manager usage."""
    for item in node.items:
        if isinstance(item.context_expr, ast.Call):
            call = item.context_expr
            if isinstance(call.func, ast.Name) and call.func.id in ['open', 'file'] or (isinstance(call.func, ast.Attribute) and call.func.attr in ['open', 'file']):
                self.with_contexts.append({'node': node, 'lineno': node.lineno})
    self.generic_visit(node)

