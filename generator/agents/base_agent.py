"""
Base agent class for AI Skill Factory agents.
"""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from generator.clients.anthropic_client import AnthropicClient


class BaseAgent:
    """Base class for all generator agents."""

    def __init__(self, client: "AnthropicClient", prompts_dir: Path) -> None:
        self.client = client
        self.prompts_dir = prompts_dir
        self.concept = self._load_prompt("concept.md")

    def _load_prompt(self, filename: str) -> str:
        """Load prompt from file."""
        prompt_path = self.prompts_dir / filename

        if not prompt_path.exists():
            print(f"Warning: Prompt file not found: {prompt_path}")
            return ""

        content = prompt_path.read_text(encoding="utf-8")

        # Remove front matter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2].strip()

        return content

    def _build_system_prompt(self, agent_prompt: str) -> str:
        """Build full system prompt with concept context."""
        return f"{agent_prompt}\n\n---\n\n# 플랫폼 컨텍스트\n\n{self.concept}"
