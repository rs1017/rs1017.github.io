"""
Validation utilities for AI Skill Factory.
Re-exports from validator agent for convenience.
"""

from typing import Any, Dict

# Note: Full validation logic is in agents/validator.py
# This module provides a standalone function for external use


def validate_skill_content(
    skill_md: str, code: str, post: str
) -> Dict[str, Any]:
    """
    Validate skill content without AI.
    For full validation, use ValidatorAgent.

    Returns a dict with:
        - approved: bool
        - score: int (0-100)
        - errors: list of error messages
        - warnings: list of warning messages
        - reason: first error or None
    """
    from generator.agents.validator import ValidatorAgent

    # Create a minimal validator (no client needed for basic validation)
    class MinimalClient:
        def generate(self, **kwargs: Any) -> str:
            return ""

    from pathlib import Path
    prompts_dir = Path(__file__).parent.parent / "prompts"

    validator = ValidatorAgent(MinimalClient(), prompts_dir)
    return validator.validate(skill_md, code, post)


class SkillValidator:
    """Wrapper class for skill validation."""

    def __init__(self) -> None:
        pass

    def validate_all(
        self, skill_md: str, code: str, post: str
    ) -> Dict[str, Any]:
        """Run all validations."""
        return validate_skill_content(skill_md, code, post)
