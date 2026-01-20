"""
Validator Agent for AI Skill Factory.
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

from .base_agent import BaseAgent


class ValidatorAgent(BaseAgent):
    """Agent that validates generated skill content."""

    REQUIRED_SKILL_FIELDS = ["name", "version", "category", "difficulty"]
    REQUIRED_POST_FIELDS = ["title", "date", "categories", "skill_path", "difficulty"]
    FORBIDDEN_WORDS = [
        "자동 생성",
        "AI Pipeline",
        "Gemini",
        "AutoBlog",
        "auto-generated",
        "자동생성",
    ]
    VALID_CATEGORIES = ["Workflow", "Agent", "Skill"]
    VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"]

    def __init__(self, client: Any, prompts_dir: Path) -> None:
        super().__init__(client, prompts_dir)
        self.agent_prompt = self._load_prompt("validator.md")

    def validate(
        self, skill_md: str, code: str, post: str
    ) -> Dict[str, Any]:
        """Run all validations and return result."""
        errors: List[str] = []
        warnings: List[str] = []

        # Validate SKILL.md
        skill_errors, skill_warnings = self._validate_skill_md(skill_md)
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)

        # Validate code
        code_errors, code_warnings = self._validate_code(code)
        errors.extend(code_errors)
        warnings.extend(code_warnings)

        # Validate post
        post_errors, post_warnings = self._validate_post(post)
        errors.extend(post_errors)
        warnings.extend(post_warnings)

        # Calculate score
        score = 100 - (len(errors) * 10) - (len(warnings) * 2)
        score = max(0, min(100, score))

        return {
            "approved": len(errors) == 0,
            "score": score,
            "errors": errors,
            "warnings": warnings,
            "reason": errors[0] if errors else None,
        }

    def _validate_skill_md(self, content: str) -> Tuple[List[str], List[str]]:
        """Validate SKILL.md content."""
        errors: List[str] = []
        warnings: List[str] = []

        if not content.startswith("---"):
            errors.append("SKILL.md: Missing front matter")
            return errors, warnings

        try:
            parts = content.split("---", 2)
            if len(parts) < 3:
                errors.append("SKILL.md: Invalid front matter format")
                return errors, warnings

            front_matter = yaml.safe_load(parts[1])

            for field in self.REQUIRED_SKILL_FIELDS:
                if field not in front_matter:
                    errors.append(f"SKILL.md: Missing required field '{field}'")

            if "category" in front_matter:
                if front_matter["category"] not in self.VALID_CATEGORIES:
                    errors.append(
                        f"SKILL.md: Invalid category '{front_matter['category']}'"
                    )

            if "difficulty" in front_matter:
                if front_matter["difficulty"] not in self.VALID_DIFFICULTIES:
                    errors.append(
                        f"SKILL.md: Invalid difficulty '{front_matter['difficulty']}'"
                    )

        except yaml.YAMLError as e:
            errors.append(f"SKILL.md: YAML parse error - {e}")

        if "```python" not in content and "```bash" not in content:
            warnings.append("SKILL.md: No code examples found")

        return errors, warnings

    def _validate_code(self, code: str) -> Tuple[List[str], List[str]]:
        """Validate Python code."""
        errors: List[str] = []
        warnings: List[str] = []

        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(f"Code: Syntax error at line {e.lineno}: {e.msg}")
            return errors, warnings

        # Check for hardcoded API keys
        api_key_patterns = [
            r"sk-ant-[a-zA-Z0-9-_]{40,}",
            r'api_key\s*=\s*["\'][^"\']{20,}["\']',
            r'ANTHROPIC_API_KEY\s*=\s*["\'][^"\']+["\']',
        ]
        for pattern in api_key_patterns:
            if re.search(pattern, code):
                errors.append("Code: Possible hardcoded API key detected")
                break

        if "anthropic" not in code.lower() and "from anthropic" not in code:
            warnings.append("Code: No Anthropic import found")

        if "def main" not in code and 'if __name__' not in code:
            warnings.append("Code: No main function or entry point")

        if "try:" not in code and "except" not in code:
            warnings.append("Code: No error handling found")

        return errors, warnings

    def _validate_post(self, content: str) -> Tuple[List[str], List[str]]:
        """Validate blog post content."""
        errors: List[str] = []
        warnings: List[str] = []

        if not content.startswith("---"):
            errors.append("Post: Missing front matter")
            return errors, warnings

        try:
            parts = content.split("---", 2)
            if len(parts) < 3:
                errors.append("Post: Invalid front matter format")
                return errors, warnings

            front_matter = yaml.safe_load(parts[1])
            body = parts[2]

            for field in self.REQUIRED_POST_FIELDS:
                if field not in front_matter:
                    errors.append(f"Post: Missing required field '{field}'")

            if "categories" in front_matter:
                cats = front_matter["categories"]
                if isinstance(cats, list):
                    for cat in cats:
                        if cat not in self.VALID_CATEGORIES:
                            errors.append(f"Post: Invalid category '{cat}'")

        except yaml.YAMLError as e:
            errors.append(f"Post: YAML parse error - {e}")
            return errors, warnings

        # Check for forbidden words
        for word in self.FORBIDDEN_WORDS:
            if word.lower() in content.lower():
                errors.append(f"Post: Forbidden word found '{word}'")

        # Check for image placeholders
        image_count = content.count("[IMAGE_DESC:")
        if image_count < 3:
            errors.append(
                f"Post: Only {image_count} images found (minimum 3 required)"
            )

        if "```" not in body:
            warnings.append("Post: No code blocks found")

        if "skill_path" in front_matter:
            skill_path = front_matter["skill_path"]
            if skill_path not in body and "/skills/" not in body:
                warnings.append("Post: skill_path not referenced in body")

        return errors, warnings
