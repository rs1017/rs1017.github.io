"""
Skill Designer Agent for AI Skill Factory.
"""

from pathlib import Path
from typing import Any, Dict

from .base_agent import BaseAgent


class SkillDesignerAgent(BaseAgent):
    """Agent that designs SKILL.md documents."""

    def __init__(self, client: Any, prompts_dir: Path) -> None:
        super().__init__(client, prompts_dir)
        self.agent_prompt = self._load_prompt("skill-designer.md")

    def design(self, topic_info: Dict[str, Any]) -> str:
        """Design a SKILL.md document for the given topic."""
        prompt = f"""다음 주제에 대한 SKILL.md 문서를 작성해주세요:

## 주제 정보
- 제목: {topic_info.get('topic', 'Unknown')}
- 카테고리: {topic_info.get('category', 'Skill')}
- 난이도: {topic_info.get('difficulty', 'intermediate')}
- 태그: {', '.join(topic_info.get('tags', []))}
- 설명: {topic_info.get('description', '')}

## 요구사항
1. 실행 가능한 코드 예제 포함
2. 명확한 파라미터 문서화
3. 실용적인 사용 시나리오
4. Anthropic Claude API 사용

SKILL.md 전체 내용만 출력하세요. 다른 설명은 포함하지 마세요.
Front Matter (---)로 시작해야 합니다.
"""

        system = self._build_system_prompt(self.agent_prompt)
        response = self.client.generate(prompt=prompt, system=system, max_tokens=4096)

        # Clean up response
        content = response.strip()

        # Ensure it starts with front matter
        if not content.startswith("---"):
            content = f"""---
name: {self._to_kebab_case(topic_info.get('topic', 'unknown-skill'))}
version: "1.0.0"
author: AI Skill Factory
category: {topic_info.get('category', 'Skill')}
difficulty: {topic_info.get('difficulty', 'intermediate')}
tags: {topic_info.get('tags', [])}
requires:
  - python>=3.9
  - anthropic>=0.35.0
---

{content}"""

        return content

    def _to_kebab_case(self, text: str) -> str:
        """Convert text to kebab-case."""
        import re
        # Remove special characters and convert to lowercase
        text = re.sub(r"[^\w\s-]", "", text.lower())
        # Replace spaces with hyphens
        text = re.sub(r"[\s_]+", "-", text)
        # Remove consecutive hyphens
        text = re.sub(r"-+", "-", text)
        return text.strip("-")
