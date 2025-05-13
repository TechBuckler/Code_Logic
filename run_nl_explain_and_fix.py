"""
Combined Import Fixer and NL Explanation Script

This script merges the import fixing and NL docstring explanation pipeline.
It ensures all imports are fixed, then generates NL summaries for all modules.
Use this as the main entry point for codebase mapping and documentation.
"""
import sys
import types
import os
from pathlib import Path
import traceback

# ---- SIMPLE IMPORT FIXER ----
def fix_imports_simple():
    """Fixes sys.modules for reorganized codebase imports."""
    # Create import_utils if needed
    try:
        import utils.import_utils
    except ImportError:
        utils_module = types.ModuleType('utils')
        sys.modules['utils'] = utils_module
        import_utils_module = types.ModuleType('utils.import_utils')
        sys.modules['utils.import_utils'] = import_utils_module
    # Create RuntimeOptimizationModule
    runtime_module = types.ModuleType('modules.runtime_optimization')
    class RuntimeOptimizationModule:
        def __init__(self, name=None, parent=None):
            self.name = name
            self.parent = parent
            self.optimizations = []
    runtime_module.RuntimeOptimizationModule = RuntimeOptimizationModule
    sys.modules['modules.runtime_optimization'] = runtime_module
    sys.modules['modules.runtime_optimization_module'] = runtime_module
    sys.modules['modules.standard.runtime_optimization_module'] = runtime_module
    print("Fixed RuntimeOptimizationModule imports")
    # Create HierarchicalModule
    hierarchical_module = types.ModuleType('modules.standard.hierarchical_module')
    class HierarchicalModule:
        def __init__(self, name=None, root_dir=None):
            self.name = name
            self.root_dir = root_dir
            self.children = []
    hierarchical_module.HierarchicalModule = HierarchicalModule
    sys.modules['modules.standard.hierarchical_module'] = hierarchical_module
    sys.modules['modules.hierarchical_module'] = hierarchical_module
    sys.modules['hierarchical_module'] = hierarchical_module
    # Make HierarchicalModule available globally and at all required paths
    sys.modules['HierarchicalModule'] = types.ModuleType('HierarchicalModule')
    sys.modules['HierarchicalModule'].HierarchicalModule = HierarchicalModule
    sys.modules['hierarchical_module'] = types.ModuleType('hierarchical_module')
    sys.modules['hierarchical_module'].HierarchicalModule = HierarchicalModule
    sys.modules['modules.hierarchical_module'] = sys.modules['hierarchical_module']
    sys.modules['modules.standard.hierarchical_module'] = sys.modules['hierarchical_module']
    sys.modules['core.hierarchical_module'] = sys.modules['hierarchical_module']
    globals()['HierarchicalModule'] = HierarchicalModule
    print("Fixed HierarchicalModule imports")
    print("All imports fixed successfully")

# ---- NL EXPLANATION ----
import nltk
nltk.data.path.insert(0, './nltk_data')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir='./nltk_data', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', download_dir='./nltk_data', quiet=True)
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import ast

MAX_SUMMARY_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 250
lemmatizer = WordNetLemmatizer()

def summarize_text(text, max_length=MAX_SUMMARY_LENGTH):
    sentences = sent_tokenize(text)
    summary = ''
    for sent in sentences:
        if len(summary) + len(sent) > max_length:
            break
        summary += sent + ' '
    return summary.strip()

def extract_keywords(content):
    tokens = word_tokenize(content)
    lemmatized = [lemmatizer.lemmatize(t) for t in tokens if t.isalpha()]
    keywords = list(set(lemmatized))
    return keywords

def explain_code_docstring(docstring):
    if not docstring:
        return "No docstring provided."
    return summarize_text(docstring, max_length=MAX_DESCRIPTION_LENGTH)

def explain_all_modules(root_dirs=None, output_file=None):
    if root_dirs is None:
        root_dirs = [
            Path('.'),
            Path('./backup'),
            Path('./legacy'),
            Path('./src'),
            Path('./modules'),
            Path('./tools'),
            Path('./utils')
        ]
    seen = set()
    summaries = []
    for root in root_dirs:
        for py_file in root.rglob('*.py'):
            py_file = py_file.resolve()
            if py_file in seen:
                continue
            seen.add(py_file)
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    src = f.read()
                mod = ast.parse(src)
                docstring = ast.get_docstring(mod)
                summary = explain_code_docstring(docstring) if docstring else "No docstring found."
                summaries.append({
                    'file': str(py_file),
                    'summary': summary
                })
            except Exception as e:
                summaries.append({
                    'file': str(py_file),
                    'summary': f'Error: {e}'
                })
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in summaries:
                f.write(f"{item['file']}\n{item['summary']}\n\n")
    else:
        for item in summaries:
            print(f"{item['file']}\n{item['summary']}\n")
    return summaries

# ---- MAIN ----
if __name__ == "__main__":
    try:
        fix_imports_simple()
    except Exception as e:
        with open("fix_imports_error.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        print("Error in fix_imports_simple(). See fix_imports_error.log for details.")
        sys.exit(1)
    try:
        explain_all_modules(output_file="all_module_nl_summaries.txt")
        print("All module NL summaries written to all_module_nl_summaries.txt")
    except Exception as e:
        with open("explain_all_modules_error.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        print("Error in explain_all_modules(). See explain_all_modules_error.log for details.")
        sys.exit(1)
