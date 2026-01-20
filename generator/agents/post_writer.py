"""
Post Writer Agent for AI Skill Factory.
"""

from pathlib import Path
from typing import Any, Dict

from .base_agent import BaseAgent


class PostWriterAgent(BaseAgent):
    """Agent that writes blog posts for skills."""

    def __init__(self, client: Any, prompts_dir: Path) -> None:
        super().__init__(client, prompts_dir)
        self.agent_prompt = self._load_prompt("post-writer.md")

    def write(
        self,
        topic_info: Dict[str, Any],
        skill_md: str,
        code: str,
        date_str: str,
        slug: str,
    ) -> str:
        """Write a blog post for the skill."""
        skill_name = slug
        category = topic_info.get("category", "Skill")
        difficulty = topic_info.get("difficulty", "intermediate")
        tags = topic_info.get("tags", [])

        prompt = f"""다음 스킬에 대한 블로그 포스트를 작성해주세요:

## 주제 정보
- 제목: {topic_info.get('topic', 'Unknown')}
- 카테고리: {category}
- 난이도: {difficulty}
- 태그: {', '.join(tags)}
- 설명: {topic_info.get('description', '')}
- 스킬 경로: /skills/{skill_name}/

## SKILL.md 요약
```markdown
{skill_md[:2000]}
```

## 예제 코드
```python
{code[:1500]}
```

## 메타 정보
- 날짜: {date_str}
- 슬러그: {slug}
- 이미지 경로: /assets/img/posts/{date_str}-{slug}/

## 요구사항
1. Front Matter 필수 (layout: post)
2. 이미지 플레이스홀더 최소 3개 ([IMAGE_DESC: 설명])
3. 코드 블록 포함
4. skill_path 링크 참조
5. 친근하지만 전문적인 톤
6. 한국어로 작성

Jekyll 마크다운 포스트 전체 내용만 출력하세요.
---로 시작하는 Front Matter부터 시작해야 합니다.
"""

        system = self._build_system_prompt(self.agent_prompt)
        response = self.client.generate(prompt=prompt, system=system, max_tokens=4096)

        # Clean up and ensure proper front matter
        content = response.strip()

        # Ensure it starts with front matter
        if not content.startswith("---"):
            content = self._add_front_matter(content, topic_info, date_str, slug)

        return content

    def _add_front_matter(
        self, content: str, topic_info: Dict[str, Any], date_str: str, slug: str
    ) -> str:
        """Add front matter if missing."""
        category = topic_info.get("category", "Skill")
        difficulty = topic_info.get("difficulty", "intermediate")
        tags = topic_info.get("tags", ["Claude", "Skill"])

        tags_yaml = "\n".join(f"  - {tag}" for tag in tags[:5])

        front_matter = f"""---
layout: post
title: "{topic_info.get('topic', 'New Skill')}"
date: {date_str} 09:00:00 +0900
categories: [{category}]
tags:
{tags_yaml}
skill_path: /skills/{slug}/
difficulty: {difficulty}
generated_by: claude-sonnet-4
image:
  path: /assets/img/posts/{date_str}-{slug}/thumbnail.jpg
  alt: {topic_info.get('topic', 'Skill')} 썸네일
---

"""
        return front_matter + content
