"""
Run NL docstring explanation on all modules in the project, backup, and legacy.
Uses the project import fixer for robust imports from any directory.
Outputs NL summaries to a specified file for documentation and mapping.
"""
# Run NL docstring explanation on all modules in the project, backup, and legacy
# Uses the project import fixer for robust imports from any directory

import sys
import os
from pathlib import Path

# Ensure project root is in sys.path
project_root = Path(__file__).parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import importlib.util

fixer_path = project_root / "utils" / "import" / "fix_imports_simple.py"
spec = importlib.util.spec_from_file_location("fix_imports_simple", str(fixer_path))
fixer_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixer_mod)
try:
    fixer_mod.fix_imports_simple()
except Exception as e:
    import traceback
    print("Error in fix_imports_simple():")
    traceback.print_exc()
    raise

from utils.nlp.shadow_tree_nlp import explain_all_modules

if __name__ == "__main__":
    # Output to file in project root
    explain_all_modules(output_file="all_module_nl_summaries.txt")
    print("All module NL summaries written to all_module_nl_summaries.txt")
