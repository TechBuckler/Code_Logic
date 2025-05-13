import os
import sys
import importlib
import inspect
import json
import uuid
import weakref
from typing import Dict, List, Any, Callable, Optional, Set, Union, Type, Tuple
from abc import ABC, abstractmethod
from enum import Enum, auto
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
import ast
import ast
# Fix imports for reorganized codebase
import utils.import_utils





    def initialize_all(self):
        """Initialize all modules"""
        for module in list(self.root_modules.values()):
            self._initialize_module(module)