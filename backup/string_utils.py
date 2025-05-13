"""String utility functions for common string operations.

This module provides standardized functions for string processing,
cleaning, and manipulation, reducing code duplication across the codebase.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import re
import unicodedata

def clean_text(text):
    """Clean text by removing special characters and extra whitespace."""
    if not text:
        return ""
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_string(text):
    """Normalize a string by converting to lowercase and removing special characters."""
    if not text:
        return ""
    return clean_text(text.lower())

def extract_keywords(text, min_length=3):
    """Extract keywords from text."""
    if not text:
        return []
    words = re.findall(r'\b\w+\b', text.lower())
    return [word for word in words if len(word) >= min_length]

def camel_to_snake(text):
    """Convert camelCase to snake_case."""
    if not text:
        return ""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(text):
    """Convert snake_case to camelCase."""
    if not text:
        return ""
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def truncate(text, max_length=100, suffix="..."):
    """Truncate text to a maximum length, adding a suffix if truncated."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + suffix

def slugify(text):
    """Convert text to a URL-friendly slug."""
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-_')

def is_empty_or_whitespace(text):
    """Check if a string is empty or contains only whitespace."""
    if text is None:
        return True
    return len(text.strip()) == 0

def contains_any(text, substrings):
    """Check if text contains any of the given substrings."""
    if not text or not substrings:
        return False
    return any(s in text for s in substrings)

def replace_multiple(text, replacements):
    """Replace multiple substrings in a single pass.
    
    Args:
        text: The string to perform replacements on
        replacements: A dictionary of {old: new} replacements
    """
    if not text:
        return ""
    pattern = re.compile("|".join(map(re.escape, replacements.keys())))
    return pattern.sub(lambda m: replacements[m.group(0)], text)
