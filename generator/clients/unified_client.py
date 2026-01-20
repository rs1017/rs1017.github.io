"""
Unified AI Client with Gemini -> Anthropic fallback for AI Skill Factory.
"""

import os
import time
from typing import Optional, List

# Gemini
from google import genai
from google.genai import types as genai_types

# Anthropic
from anthropic import Anthropic, APIError, RateLimitError


GEMINI_MODELS = [
    "gemini-2.0-flash-001",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-8b",
]

ANTHROPIC_MODELS = [
    "claude-sonnet-4-20250514",
    "claude-3-5-sonnet-20241022",
    "claude-3-haiku-20240307",
]


class UnifiedAIClient:
    """
    Unified AI Client that tries Gemini first, then falls back to Anthropic.

    Priority:
    1. Gemini models (free tier)
    2. Anthropic models (paid)
    """

    def __init__(self) -> None:
        self.gemini_client = None
        self.anthropic_client = None
        self.working_model: Optional[str] = None
        self.working_provider: Optional[str] = None
        self.max_retries = 2

        # Initialize Gemini if API key exists
        gemini_key = os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            try:
                self.gemini_client = genai.Client(api_key=gemini_key)
                print("[Init] Gemini client initialized")
            except Exception as e:
                print(f"[Init] Gemini init failed: {e}")

        # Initialize Anthropic if API key exists
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        if anthropic_key:
            try:
                self.anthropic_client = Anthropic(api_key=anthropic_key)
                print("[Init] Anthropic client initialized")
            except Exception as e:
                print(f"[Init] Anthropic init failed: {e}")

        if not self.gemini_client and not self.anthropic_client:
            raise ValueError(
                "No API client available. Set GEMINI_API_KEY or ANTHROPIC_API_KEY."
            )

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate content with Gemini -> Anthropic fallback."""
        last_error: Optional[Exception] = None

        # Try Gemini first
        if self.gemini_client:
            try:
                result = self._try_gemini(prompt, system, max_tokens, temperature)
                if result:
                    return result
            except Exception as e:
                last_error = e
                print(f"  [Gemini] All models exhausted: {e}")

        # Fallback to Anthropic
        if self.anthropic_client:
            try:
                result = self._try_anthropic(prompt, system, max_tokens, temperature)
                if result:
                    return result
            except Exception as e:
                last_error = e
                print(f"  [Anthropic] All models exhausted: {e}")

        raise Exception(f"All AI providers failed. Last error: {last_error}")

    def _try_gemini(
        self,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> Optional[str]:
        """Try all Gemini models."""
        models = self._get_ordered_models(GEMINI_MODELS, "gemini")

        for model_name in models:
            print(f"  [Gemini] Trying {model_name}...", flush=True)

            for attempt in range(self.max_retries):
                try:
                    contents = prompt
                    if system:
                        contents = f"System Instructions:\n{system}\n\n---\n\nUser Request:\n{prompt}"

                    response = self.gemini_client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=genai_types.GenerateContentConfig(
                            max_output_tokens=max_tokens,
                            temperature=temperature,
                        ),
                    )

                    if not response.text:
                        raise Exception("Empty response")

                    self.working_model = model_name
                    self.working_provider = "gemini"
                    print(f"  [Gemini] Success with {model_name}")
                    return response.text

                except Exception as e:
                    error_str = str(e).lower()

                    if any(x in error_str for x in ["rate", "quota", "429", "resource", "exhausted"]):
                        print(f"    - Rate limit on {model_name}. Next model...")
                        break  # Try next model
                    elif "not found" in error_str or "404" in error_str:
                        print(f"    - Model {model_name} not found. Skipping.")
                        break
                    elif "500" in error_str or "503" in error_str:
                        print(f"    - Server error. Retrying...")
                        time.sleep(3 * (attempt + 1))
                    else:
                        print(f"    - Error: {e}")
                        break

        return None

    def _try_anthropic(
        self,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> Optional[str]:
        """Try all Anthropic models."""
        models = self._get_ordered_models(ANTHROPIC_MODELS, "anthropic")

        for model_name in models:
            print(f"  [Anthropic] Trying {model_name}...", flush=True)

            for attempt in range(self.max_retries):
                try:
                    kwargs = {
                        "model": model_name,
                        "max_tokens": max_tokens,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature,
                    }

                    if system:
                        kwargs["system"] = system

                    response = self.anthropic_client.messages.create(**kwargs)

                    if not response.content or not response.content[0].text:
                        raise Exception("Empty response")

                    self.working_model = model_name
                    self.working_provider = "anthropic"
                    print(f"  [Anthropic] Success with {model_name}")
                    return response.content[0].text

                except RateLimitError:
                    print(f"    - Rate limit on {model_name}. Next model...")
                    break

                except APIError as e:
                    if e.status_code == 404:
                        print(f"    - Model {model_name} not found. Skipping.")
                        break
                    elif e.status_code >= 500:
                        print(f"    - Server error. Retrying...")
                        time.sleep(3 * (attempt + 1))
                    else:
                        print(f"    - API Error: {e}")
                        break

                except Exception as e:
                    print(f"    - Error: {e}")
                    break

        return None

    def _get_ordered_models(self, models: List[str], provider: str) -> List[str]:
        """Get models with working model first if same provider."""
        if self.working_provider == provider and self.working_model in models:
            others = [m for m in models if m != self.working_model]
            return [self.working_model] + others
        return models
