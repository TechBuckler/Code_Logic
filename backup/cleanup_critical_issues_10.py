"""
cleanup_critical_issues_10.py - Part 10 of 14 from cleanup_critical_issues.py
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase





def visit_FunctionDef(self, node):
    """Visit FunctionDef nodes to find complex functions."""
    if hasattr(node, 'end_lineno') and node.end_lineno is not None:
        lines = node.end_lineno - node.lineno
        if lines > 50:
            self.complex_functions.append({'name': node.name, 'lines': lines, 'node': node, 'lineno': node.lineno})
    self.generic_visit(node)

