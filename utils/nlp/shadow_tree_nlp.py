"""
Restored Shadow Tree NLP Utilities

Provides natural language processing (NLP) utilities for code structure analysis and explanation, using NLTK for tokenization, lemmatization, and summarization.
"""
import os
import nltk

# Set NLTK data path to use local directory
nltk.data.path.insert(0, './nltk_data')

# Ensure NLTK resources are available
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

MAX_SUMMARY_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 250

lemmatizer = WordNetLemmatizer()

def summarize_text(text, max_length=MAX_SUMMARY_LENGTH):
    """Summarize a text to a short description."""
    sentences = sent_tokenize(text)
    summary = ''
    for sent in sentences:
        if len(summary) + len(sent) > max_length:
            break
        summary += sent + ' '
    return summary.strip()

def extract_keywords(content):
    """Extract keywords from content using tokenization and lemmatization."""
    tokens = word_tokenize(content)
    lemmatized = [lemmatizer.lemmatize(t) for t in tokens if t.isalpha()]
    keywords = list(set(lemmatized))
    return keywords

def explain_code_docstring(docstring):
    """Generate a readable explanation from a code docstring."""
    if not docstring:
        return "No docstring provided."
    return summarize_text(docstring, max_length=MAX_DESCRIPTION_LENGTH)

import ast
from pathlib import Path

def explain_all_modules(root_dirs=None, output_file=None):
    """
    Recursively find all .py files in root_dirs (default: project root, backup, legacy),
    extract top-level docstrings, run NL explanation, and print/save a summary.
    """
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
