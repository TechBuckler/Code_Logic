#!/usr/bin/env python
"""
Shadow AI Validator

This module provides AI-powered code validation using OpenAI models.
It implements a cost-effective approach by using a cascade of models.
"""

import os
import re
import json
import time
import random
import logging
import hashlib
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="validator.log",
)
logger = logging.getLogger("shadow_ai_validator")

# Try to import OpenAI
try:
    import openai
    from openai import AsyncOpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("OpenAI not available. AI validation will be disabled.")
    OPENAI_AVAILABLE = False

# Model selection weights (higher = more frequent use)
MODEL_WEIGHTS = {
    "gpt-3.5-turbo": 100,  # Use 100x more often than GPT-4o
    "gpt-4-turbo": 20,  # Use 20x more often than GPT-4o
    "gpt-4o-mini": 5,  # Use 5x more often than GPT-4o
    "gpt-4o": 1,  # Baseline (used least frequently)
}

# Model costs per 1K tokens (input/output)
MODEL_COSTS = {
    "gpt-3.5-turbo": (
        0.0015,
        0.002,
    ),  # $0.0015 per 1K input tokens, $0.002 per 1K output tokens
    "gpt-4-turbo": (
        0.01,
        0.03,
    ),  # $0.01 per 1K input tokens, $0.03 per 1K output tokens
    "gpt-4o-mini": (
        0.005,
        0.015,
    ),  # $0.005 per 1K input tokens, $0.015 per 1K output tokens
    "gpt-4o": (0.01, 0.03),  # $0.01 per 1K input tokens, $0.03 per 1K output tokens
}


class AIValidator:
    """
    AI-powered code validator using OpenAI models.
    """

    def __init__(self):
        """Initialize the AI validator."""
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = None

        if OPENAI_AVAILABLE and self.api_key:
            try:
                openai.api_key = self.api_key
                self.client = AsyncOpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {str(e)}")

    def is_available(self) -> bool:
        """
        Check if AI validation is available.

        Returns:
            True if AI validation is available, False otherwise
        """
        return OPENAI_AVAILABLE and self.api_key is not None and self.client is not None

    def select_model(self) -> str:
        """
        Select a model based on weighted probability.

        Returns:
            The selected model name
        """
        # Create a list of models with weights
        models = []
        weights = []

        for model, weight in MODEL_WEIGHTS.items():
            models.append(model)
            weights.append(weight)

        # Normalize weights
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        # Select a model based on weights
        return random.choices(models, normalized_weights, k=1)[0]

    async def validate_code(
        self, code: str, model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate code using an AI model.

        Args:
            code: The code to validate
            model: The model to use (if None, a model will be selected automatically)

        Returns:
            A dictionary with validation results
        """
        if not self.is_available():
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": "OpenAI API not available or API key not set.",
                "suggestions": ["Set the OPENAI_API_KEY environment variable."],
                "source": "error",
                "cost": 0.0,
            }

        # Select a model if not specified
        if model is None:
            model = self.select_model()

        try:
            # Prepare the prompt
            prompt = f"""
            You are a Python code validator. Analyze the following code and determine if it is valid, not valid, or mostly valid.
            If there are issues, explain them and provide suggestions for improvement.
            
            Code to validate:
            ```python
            {code}
            ```
            
            Respond in the following JSON format:
            {{
                "status": "VALID" or "NOT_VALID" or "MOSTLY_VALID",
                "confidence": a number between 0 and 1 indicating your confidence,
                "explanation": "Your explanation of the validation result",
                "suggestions": ["suggestion1", "suggestion2", ...]
            }}
            """

            start_time = time.time()

            # Call the OpenAI API
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python code validator assistant.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=1000,
            )

            # Extract the response content
            content = response.choices[0].message.content.strip()

            # Parse the JSON response
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # If the response is not valid JSON, extract it using regex
                status_match = re.search(r'"status":\s*"([^"]+)"', content)
                confidence_match = re.search(r'"confidence":\s*([\d.]+)', content)
                explanation_match = re.search(r'"explanation":\s*"([^"]+)"', content)
                suggestions_match = re.search(
                    r'"suggestions":\s*\[(.*?)\]', content, re.DOTALL
                )

                result = {
                    "status": status_match.group(1) if status_match else "UNKNOWN",
                    "confidence": float(confidence_match.group(1))
                    if confidence_match
                    else 0.5,
                    "explanation": explanation_match.group(1)
                    if explanation_match
                    else "No explanation provided.",
                    "suggestions": [],
                }

                if suggestions_match:
                    suggestions_text = suggestions_match.group(1)
                    suggestions = re.findall(r'"([^"]+)"', suggestions_text)
                    result["suggestions"] = suggestions

            # Calculate the cost
            input_tokens = len(prompt) / 4  # Approximate token count
            output_tokens = len(content) / 4  # Approximate token count

            if model in MODEL_COSTS:
                input_cost, output_cost = MODEL_COSTS[model]
                cost = (input_tokens * input_cost / 1000) + (
                    output_tokens * output_cost / 1000
                )
            else:
                cost = 0.0

            # Add metadata to the result
            result["source"] = model
            result["cost"] = cost
            result["models_used"] = [model]
            result["execution_time"] = time.time() - start_time

            return result
        except Exception as e:
            logger.error(f"Error in OpenAI validation: {str(e)}")
            return {
                "status": "ERROR",
                "confidence": 0.0,
                "explanation": f"Error in OpenAI validation: {str(e)}",
                "suggestions": [
                    "Try again with a different model or check your API key."
                ],
                "source": "error",
                "cost": 0.0,
                "execution_time": time.time() - start_time,
            }


class AIValidatorSync:
    """
    Synchronous wrapper for the AIValidator class.
    """

    def __init__(self):
        """Initialize the synchronous AI validator."""
        self.validator = AIValidator()

    def validate_code(self, code: str, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate code using an AI model (synchronous version).

        Args:
            code: The code to validate
            model: The model to use (if None, a model will be selected automatically)

        Returns:
            A dictionary with validation results
        """
        import asyncio

        # Create an event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Run the async validation
        return loop.run_until_complete(self.validator.validate_code(code, model))

    def is_available(self) -> bool:
        """
        Check if AI validation is available.

        Returns:
            True if AI validation is available, False otherwise
        """
        return self.validator.is_available()

    def select_model(self) -> str:
        """
        Select a model based on weighted probability.

        Returns:
            The selected model name
        """
        return self.validator.select_model()


async def test_ai_validator():
    """Test the AI validator."""
    validator = AIValidator()

    if not validator.is_available():
        print(
            "AI validation not available. Please set the OPENAI_API_KEY environment variable."
        )
        return

    # Test with a simple code snippet
    code = """
def calculate_sum(a, b):
    # This function calculates the sum of two numbers
    return a + b
"""

    # Test with different models
    for model in ["gpt-3.5-turbo", "gpt-4o-mini"]:
        print(f"\nTesting with model: {model}")
        result = await validator.validate_code(code, model)

        print(f"Status: {result.get('status', 'UNKNOWN')}")
        print(f"Confidence: {result.get('confidence', 0.0):.2f}")
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Cost: ${result.get('cost', 0.0):.6f}")
        print(f"Execution time: {result.get('execution_time', 0.0):.2f} seconds")

        if "explanation" in result:
            print(f"\nExplanation: {result['explanation']}")

        if "suggestions" in result and result["suggestions"]:
            print("\nSuggestions:")
            for i, suggestion in enumerate(result["suggestions"], 1):
                print(f"{i}. {suggestion}")

    # Test model selection
    print("\nTesting model selection:")
    model_counts = {model: 0 for model in MODEL_WEIGHTS}

    for _ in range(100):
        model = validator.select_model()
        model_counts[model] += 1

    print("Model selection distribution:")
    for model, count in model_counts.items():
        print(f"{model}: {count}%")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_ai_validator())
