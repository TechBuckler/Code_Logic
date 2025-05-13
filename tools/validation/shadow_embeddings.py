#!/usr/bin/env python
"""
Shadow Embeddings

This module provides local embeddings functionality for code validation,
allowing for semantic similarity matching and pattern-based caching.
"""

import os
import re
import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="validator.log",
)
logger = logging.getLogger("shadow_embeddings")

# Cache directories
CACHE_DIR = "validation_cache"
PATTERN_DIR = os.path.join(CACHE_DIR, "patterns")
EMBEDDING_DIR = os.path.join(CACHE_DIR, "embeddings")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(PATTERN_DIR, exist_ok=True)
os.makedirs(EMBEDDING_DIR, exist_ok=True)

# Try to import sentence_transformers for embeddings
try:
    from sentence_transformers import SentenceTransformer

    EMBEDDINGS_AVAILABLE = True
except ImportError:
    logger.warning("sentence_transformers not available. Embeddings will be disabled.")
    EMBEDDINGS_AVAILABLE = False


class LocalEmbeddings:
    """
    A class that uses sentence embeddings for semantic similarity matching.
    """

    def __init__(self, cache_dir=EMBEDDING_DIR):
        """Initialize the embeddings model."""
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.model = None
        self.embeddings_cache = {}
        self.loaded = False

        # Only load the model if available
        if EMBEDDINGS_AVAILABLE:
            try:
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                self.loaded = True
                logger.info("Loaded embeddings model successfully")
            except Exception as e:
                logger.error(f"Error loading embeddings model: {str(e)}")
                self.loaded = False

    def get_embedding(self, text: str) -> List[float]:
        """
        Get the embedding for a text string.

        Args:
            text: The text to embed

        Returns:
            The embedding vector as a list of floats
        """
        if not self.loaded or not self.model:
            return []

        try:
            # Check cache first
            text_hash = hashlib.md5(text.encode()).hexdigest()
            cache_path = os.path.join(self.cache_dir, f"{text_hash}.json")

            if text_hash in self.embeddings_cache:
                return self.embeddings_cache[text_hash]

            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "r") as f:
                        embedding = json.load(f)
                    self.embeddings_cache[text_hash] = embedding
                    return embedding
                except Exception:
                    pass

            # Generate new embedding
            embedding = self.model.encode(text).tolist()

            # Cache the embedding
            self.embeddings_cache[text_hash] = embedding
            try:
                with open(cache_path, "w") as f:
                    json.dump(embedding, f)
            except Exception as e:
                logger.error(f"Error caching embedding: {str(e)}")

            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return []

    def find_similar(
        self, text: str, threshold: float = 0.7
    ) -> Optional[Dict[str, Any]]:
        """
        Find similar code based on embeddings.

        Args:
            text: The text to find similar code for
            threshold: The similarity threshold (0.0 to 1.0)

        Returns:
            A dictionary with the most similar code and its validation result, or None if no match
        """
        if not self.loaded or not self.model:
            return None

        try:
            # Get embedding for the query text
            query_embedding = self.get_embedding(text)
            if not query_embedding:
                return None

            # Find all embedding files
            embedding_files = [
                f for f in os.listdir(self.cache_dir) if f.endswith(".json")
            ]

            best_match = None
            best_score = 0.0

            # Compare with all cached embeddings
            for embedding_file in embedding_files:
                try:
                    # Skip if this is the query itself
                    if (
                        embedding_file
                        == f"{hashlib.md5(text.encode()).hexdigest()}.json"
                    ):
                        continue

                    # Load the embedding
                    with open(os.path.join(self.cache_dir, embedding_file), "r") as f:
                        stored_embedding = json.load(f)

                    # Calculate similarity
                    similarity = self._cosine_similarity(
                        query_embedding, stored_embedding
                    )

                    # Update best match if this is better
                    if similarity > best_score and similarity >= threshold:
                        best_score = similarity

                        # Get the validation result for this embedding
                        result_file = os.path.join(
                            CACHE_DIR, f"{embedding_file[:-5]}.json"
                        )
                        if os.path.exists(result_file):
                            with open(result_file, "r") as f:
                                result = json.load(f)
                                best_match = {
                                    "similarity": similarity,
                                    "result": result,
                                }
                except Exception as e:
                    logger.error(f"Error comparing embeddings: {str(e)}")
                    continue

            return best_match
        except Exception as e:
            logger.error(f"Error finding similar code: {str(e)}")
            return None

    def save_result(self, text: str, result: Dict[str, Any]) -> None:
        """
        Save a result with its embedding.

        Args:
            text: The text associated with the result
            result: The validation result to save
        """
        if not self.loaded:
            return

        try:
            # Generate embedding and hash
            self.get_embedding(text)
            text_hash = hashlib.md5(text.encode()).hexdigest()

            # Save the result
            result_path = os.path.join(CACHE_DIR, f"{text_hash}.json")
            with open(result_path, "w") as f:
                json.dump(result, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving result: {str(e)}")

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity (0.0 to 1.0)
        """
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        try:
            # Calculate dot product
            dot_product = sum(a * b for a, b in zip(vec1, vec2))

            # Calculate magnitudes
            magnitude1 = sum(a * a for a in vec1) ** 0.5
            magnitude2 = sum(b * b for b in vec2) ** 0.5

            # Calculate cosine similarity
            if magnitude1 > 0 and magnitude2 > 0:
                return dot_product / (magnitude1 * magnitude2)
            else:
                return 0.0
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {str(e)}")
            return 0.0


class ResponseCache:
    """
    A smart cache for validation responses that learns from past validations.
    """

    def __init__(self):
        """Initialize the cache."""
        self.cache_dir = CACHE_DIR
        self.pattern_dir = PATTERN_DIR
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.pattern_dir, exist_ok=True)
        self.pattern_stats = self._load_pattern_stats()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get a cached response.

        Args:
            key: The cache key (usually a hash of the code)

        Returns:
            The cached response, or None if not found
        """
        cache_path = os.path.join(self.cache_dir, f"{key}.json")

        if not os.path.exists(cache_path):
            return None

        try:
            with open(cache_path, "r") as f:
                result = json.load(f)

            # Update pattern stats if this has a pattern key
            if "pattern_key" in result:
                self._update_pattern_stats(result["pattern_key"], "hits", 1)

            return result
        except Exception as e:
            logger.error(f"Error reading from cache: {str(e)}")
            return None

    def set(self, key: str, value: Dict[str, Any]) -> None:
        """
        Set a cached response and extract patterns.

        Args:
            key: The cache key (usually a hash of the code)
            value: The response to cache
        """
        cache_path = os.path.join(self.cache_dir, f"{key}.json")

        try:
            # Extract and store patterns
            self._extract_and_store_patterns(key, value)

            # Write to cache
            with open(cache_path, "w") as f:
                json.dump(value, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing to cache: {str(e)}")

    def _extract_and_store_patterns(
        self, code_hash: str, value: Dict[str, Any]
    ) -> None:
        """
        Extract and store code patterns from validation results.

        Args:
            code_hash: The hash of the code
            value: The validation result
        """
        if "status" not in value or "explanation" not in value:
            return

        try:
            # Create a pattern key from the status and key terms
            status = value["status"]
            explanation = value.get("explanation", "")
            suggestions = value.get("suggestions", [])

            # Extract key terms from the explanation and suggestions
            key_terms = self._extract_key_terms(explanation)
            for suggestion in suggestions:
                key_terms.extend(self._extract_key_terms(suggestion))

            # Create a unique pattern key
            pattern_key = f"{status}_{'-'.join(sorted(set(key_terms)))}"
            pattern_path = os.path.join(self.pattern_dir, f"{pattern_key}.json")

            # Store the pattern with a reference to the original validation
            pattern_data = {
                "status": status,
                "key_terms": list(set(key_terms)),
                "examples": [code_hash],
                "created": datetime.now().isoformat(),
                "hits": 0,
            }

            # Update the original value with the pattern key
            value["pattern_key"] = pattern_key

            # Save the pattern
            with open(pattern_path, "w") as f:
                json.dump(pattern_data, f, indent=2)

            # Update pattern stats
            self._update_pattern_stats(pattern_key, "count", 1)
        except Exception as e:
            logger.error(f"Error extracting patterns: {str(e)}")

    def _extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key terms from text for pattern matching.

        Args:
            text: The text to extract key terms from

        Returns:
            A list of key terms
        """
        if not text:
            return []

        # Convert to lowercase and split into words
        words = re.findall(r"\b\w+\b", text.lower())

        # Filter out common words and keep only significant terms
        common_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "with",
            "by",
            "about",
            "as",
            "of",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "should",
            "could",
            "may",
            "might",
            "must",
            "can",
        }
        significant_terms = [
            word for word in words if word not in common_words and len(word) > 2
        ]

        # Return up to 10 most significant terms
        return significant_terms[:10]

    def _load_pattern_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Load pattern statistics from disk.

        Returns:
            A dictionary of pattern statistics
        """
        stats_path = os.path.join(self.cache_dir, "pattern_stats.json")

        if not os.path.exists(stats_path):
            return {}

        try:
            with open(stats_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading pattern stats: {str(e)}")
            return {}

    def _save_pattern_stats(self) -> None:
        """Save pattern statistics to disk."""
        stats_path = os.path.join(self.cache_dir, "pattern_stats.json")

        try:
            with open(stats_path, "w") as f:
                json.dump(self.pattern_stats, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving pattern stats: {str(e)}")

    def _update_pattern_stats(
        self, pattern_key: str, stat_key: str, value: int
    ) -> None:
        """
        Update statistics for a pattern.

        Args:
            pattern_key: The pattern key
            stat_key: The statistic key
            value: The value to add
        """
        if pattern_key not in self.pattern_stats:
            self.pattern_stats[pattern_key] = {}

        if stat_key not in self.pattern_stats[pattern_key]:
            self.pattern_stats[pattern_key][stat_key] = 0

        self.pattern_stats[pattern_key][stat_key] += value
        self._save_pattern_stats()


def test_embeddings():
    """Test the embeddings functionality."""
    embeddings = LocalEmbeddings()

    if not embeddings.loaded:
        print("Embeddings model not loaded. Please install sentence-transformers.")
        return

    # Test with a simple code snippet
    code1 = """
def calculate_sum(a, b):
    return a + b
"""

    code2 = """
def add_numbers(x, y):
    return x + y
"""

    code3 = """
def multiply_numbers(x, y):
    return x * y
"""

    # Get embeddings
    embedding1 = embeddings.get_embedding(code1)
    embedding2 = embeddings.get_embedding(code2)
    embedding3 = embeddings.get_embedding(code3)

    # Calculate similarities
    similarity12 = embeddings._cosine_similarity(embedding1, embedding2)
    similarity13 = embeddings._cosine_similarity(embedding1, embedding3)
    similarity23 = embeddings._cosine_similarity(embedding2, embedding3)

    print(f"Similarity between code1 and code2: {similarity12:.4f}")
    print(f"Similarity between code1 and code3: {similarity13:.4f}")
    print(f"Similarity between code2 and code3: {similarity23:.4f}")

    # Test caching
    cache = ResponseCache()

    # Cache a result
    result1 = {
        "status": "VALID",
        "confidence": 0.9,
        "explanation": "The code is valid and follows good practices.",
        "suggestions": [],
    }

    code1_hash = hashlib.md5(code1.encode()).hexdigest()
    cache.set(code1_hash, result1)

    # Retrieve the result
    retrieved_result = cache.get(code1_hash)
    print(f"Retrieved result: {retrieved_result}")

    # Save embedding with result
    embeddings.save_result(code1, result1)

    # Find similar code
    similar = embeddings.find_similar(code2, threshold=0.7)
    if similar:
        print(f"Found similar code with similarity: {similar['similarity']:.4f}")
        print(f"Result: {similar['result']}")
    else:
        print("No similar code found.")


if __name__ == "__main__":
    test_embeddings()
