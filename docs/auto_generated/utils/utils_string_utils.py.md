# string_utils.py

**Path:** `utils\string_utils.py`

## Description

String utility functions for common string operations.

This module provides standardized functions for string processing,
cleaning, and manipulation, reducing code duplication across the codebase.

## Metrics

- **Lines of Code:** 83
- **Functions:** 10
- **Classes:** 0
- **Imports:** 2
- **Complexity:** 12

## Imports

- `import re`
- `import unicodedata`

## Functions

### `clean_text(text)`

Clean text by removing special characters and extra whitespace.

**Complexity:** 2

### `normalize_string(text)`

Normalize a string by converting to lowercase and removing special characters.

**Complexity:** 2

### `extract_keywords(text, min_length)`

Extract keywords from text.

**Complexity:** 2

### `camel_to_snake(text)`

Convert camelCase to snake_case.

**Complexity:** 2

### `snake_to_camel(text)`

Convert snake_case to camelCase.

**Complexity:** 2

### `truncate(text, max_length, suffix)`

Truncate text to a maximum length, adding a suffix if truncated.

**Complexity:** 3

### `slugify(text)`

Convert text to a URL-friendly slug.

**Complexity:** 2

### `is_empty_or_whitespace(text)`

Check if a string is empty or contains only whitespace.

**Complexity:** 2

### `contains_any(text, substrings)`

Check if text contains any of the given substrings.

**Complexity:** 2

### `replace_multiple(text, replacements)`

Replace multiple substrings in a single pass.

Args:
    text: The string to perform replacements on
    replacements: A dictionary of {old: new} replacements

**Complexity:** 2

## Keywords

`text, sub, lower, strip, word, len, components, max_length, substrings, replacements, unicodedata, clean_text, min_length, words, join, suffix, ascii, pattern, normalize_string, extract_keywords`

