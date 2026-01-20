"""
Google Gemini API Client wrapper for AI Skill Factory.
"""

import os
import time
from typing import Optional, List

import google.generativeai as genai


MODEL_CANDIDATES = [
    "gemini-2.0-flash-exp",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
]


class GeminiClient:
    """Wrapper for Google Gemini API with retry logic and model fallback."""

    def __init__(self) -> None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")

        genai.configure(api_key=api_key)
        self.working_model: Optional[str] = None
        self.max_retries = 3

        print("[Init] Gemini client initialized")

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

        # Combine system prompt with user prompt if provided
        full_prompt = prompt
        if system:
            full_prompt = f"{system}\n\n---\n\n{prompt}"

        for model_name in models_to_try:
            print(f"  [AI] Trying {model_name}...", flush=True)

            for attempt in range(self.max_retries):
                try:
                    model = genai.GenerativeModel(model_name)

                    generation_config = genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=temperature,
                    )

                    response = model.generate_content(
                        full_prompt,
                        generation_config=generation_config,
                    )

                    if not response.text:
                        raise Exception("Empty response")

                    self.working_model = model_name
                    print(f"  [AI] Success with {model_name}")
                    return response.text

                except Exception as e:
                    last_error = e
                    error_str = str(e).lower()

                    if "rate" in error_str or "quota" in error_str or "429" in error_str:
                        print(f"    - Rate limit hit on {model_name}. Trying next model...")
                        break
                    elif "not found" in error_str or "404" in error_str:
                        print(f"    - Model {model_name} not found. Skipping.")
                        break
                    elif "500" in error_str or "503" in error_str:
                        print(f"    - Server error. Retrying...")
                        time.sleep(5 * (attempt + 1))
                    else:
                        print(f"    - Error: {e}")
                        time.sleep(2)

        raise Exception(f"All models failed. Last error: {last_error}")

    def _get_model_order(self) -> List[str]:
        """Get models in priority order, with working model first."""
        if self.working_model:
            others = [m for m in MODEL_CANDIDATES if m != self.working_model]
            return [self.working_model] + others
        return MODEL_CANDIDATES
