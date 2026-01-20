"""
Anthropic Claude API Client wrapper for AI Skill Factory.
"""

import os
import time
from typing import Optional, List

from anthropic import Anthropic, APIError, RateLimitError


MODEL_CANDIDATES = [
    "claude-sonnet-4-20250514",
    "claude-3-5-sonnet-20241022",
    "claude-3-haiku-20240307",
]


class AnthropicClient:
    """Wrapper for Anthropic API with retry logic and model fallback."""

    def __init__(self) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is missing.")

        self.client = Anthropic(api_key=api_key)
        self.working_model: Optional[str] = None
        self.max_retries = 3

        print("[Init] Anthropic client initialized")

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate content with automatic model fallback."""
        models_to_try = self._get_model_order()
        last_error: Optional[Exception] = None

        for model_name in models_to_try:
            print(f"  [AI] Trying {model_name}...", flush=True)

            for attempt in range(self.max_retries):
                try:
                    messages = [{"role": "user", "content": prompt}]

                    kwargs = {
                        "model": model_name,
                        "max_tokens": max_tokens,
                        "messages": messages,
                        "temperature": temperature,
                    }

                    if system:
                        kwargs["system"] = system

                    response = self.client.messages.create(**kwargs)

                    if not response.content or not response.content[0].text:
                        raise Exception("Empty response")

                    self.working_model = model_name
                    print(f"  [AI] Success with {model_name}")
                    return response.content[0].text

                except RateLimitError as e:
                    print(f"    - Rate limit hit on {model_name}. Failing immediately.")
                    raise e

                except APIError as e:
                    last_error = e
                    if "not found" in str(e).lower() or e.status_code == 404:
                        print(f"    - Model {model_name} not found. Skipping.")
                        break
                    elif e.status_code >= 500:
                        print(f"    - Server error. Retrying...")
                        time.sleep(5 * (attempt + 1))
                    else:
                        print(f"    - API Error: {e}")
                        time.sleep(2)

                except Exception as e:
                    last_error = e
                    print(f"    - Error: {e}")
                    time.sleep(2)

        raise Exception(f"All models failed. Last error: {last_error}")

    def _get_model_order(self) -> List[str]:
        """Get models in priority order, with working model first."""
        if self.working_model:
            others = [m for m in MODEL_CANDIDATES if m != self.working_model]
            return [self.working_model] + others
        return MODEL_CANDIDATES
