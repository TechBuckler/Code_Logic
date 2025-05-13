
"""Pipeline Functions

This module contains LINQ-like pipeline functions for data processing.
"""

def where(iterable, predicate):
    """Filter items in an iterable based on a predicate function."""
    return [item for item in iterable if predicate(item)]

def select(iterable, selector):
    """Transform items in an iterable using a selector function."""
    return [selector(item) for item in iterable]

def group_by(iterable, key_selector):
    """Group items in an iterable by a key selector function."""
    result = {}
    for item in iterable:
        key = key_selector(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result

def order_by(iterable, key_selector, reverse=False):
    """Order items in an iterable by a key selector function."""
    return sorted(iterable, key=key_selector, reverse=reverse)

def first_or_default(iterable, predicate=None, default=None):
    """Get the first item that matches a predicate, or a default value."""
    if predicate is None:
        try:
            return next(iter(iterable))
        except StopIteration:
            return default
    
    for item in iterable:
        if predicate(item):
            return item
    
    return default

class Pipeline:
    """A pipeline for chaining operations on an iterable."""
    
    def __init__(self, iterable):
        self.iterable = iterable
    
    def where(self, predicate):
        """Filter items in the pipeline."""
        self.iterable = where(self.iterable, predicate)
        return self
    
    def select(self, selector):
        """Transform items in the pipeline."""
        self.iterable = select(self.iterable, selector)
        return self
    
    def group_by(self, key_selector):
        """Group items in the pipeline."""
        self.iterable = group_by(self.iterable, key_selector)
        return self
    
    def order_by(self, key_selector, reverse=False):
        """Order items in the pipeline."""
        self.iterable = order_by(self.iterable, key_selector, reverse)
        return self
    
    def first_or_default(self, predicate=None, default=None):
        """Get the first item that matches a predicate."""
        return first_or_default(self.iterable, predicate, default)
    
    def to_list(self):
        """Convert the pipeline to a list."""
        return list(self.iterable)
    
    def to_dict(self):
        """Convert the pipeline to a dictionary."""
        return dict(self.iterable)
    
    def to_set(self):
        """Convert the pipeline to a set."""
        return set(self.iterable)

def from_iterable(iterable):
    """Create a pipeline from an iterable."""
    return Pipeline(iterable)
