"""
cleanup_critical_issues_6.py - Part 6 of 14 from cleanup_critical_issues.py
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import ast


def visit_Attribute(self, node):
    """Visit Attribute nodes to track used module attributes."""
    if isinstance(node.value, ast.Name):
        self.used_names.add(node.value.id)
    self.generic_visit(node)

