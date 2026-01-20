"""
Topic Selector Agent for AI Skill Factory.
"""

import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .base_agent import BaseAgent


class TopicSelectorAgent(BaseAgent):
    """Agent that selects skill topics using various strategies."""

    def __init__(self, client: Any, prompts_dir: Path) -> None:
        super().__init__(client, prompts_dir)
        self.agent_prompt = self._load_prompt("skill-topic-selector.md")

    def select(
        self,
        strategy: str = "auto",
        user_topic: Optional[str] = None,
        existing_skills: Optional[List[str]] = None,
        sources: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Select a topic using the specified strategy."""
        existing_skills = existing_skills or []
        sources = sources or {}

        # If user provided a specific topic
        if user_topic:
            return self._process_user_topic(user_topic)

        # Auto strategy: pick one randomly
        if strategy == "auto":
            strategies = ["keyword", "trend", "extend"]
            if sources.get("requests"):
                strategies.append("request")
            strategy = random.choice(strategies)

        # Build prompt based on strategy
        prompt = self._build_selection_prompt(strategy, existing_skills, sources)
        system = self._build_system_prompt(self.agent_prompt)

        # Call AI
        response = self.client.generate(prompt=prompt, system=system, temperature=0.8)

        # Parse response
        return self._parse_response(response, strategy)

    def _process_user_topic(self, topic: str) -> Dict[str, Any]:
        """Process a user-provided topic."""
        prompt = f"""사용자가 다음 주제로 스킬 생성을 요청했습니다:

"{topic}"

이 주제에 대해 적절한 카테고리, 난이도, 태그를 결정해주세요.

출력 형식:
```yaml
topic: "{topic}"
category: Workflow | Agent | Skill
difficulty: beginner | intermediate | advanced
strategy_used: user_request
tags:
  - tag1
  - tag2
  - tag3
description: "한 줄 설명"
```"""

        system = self._build_system_prompt(self.agent_prompt)
        response = self.client.generate(prompt=prompt, system=system, temperature=0.5)
        return self._parse_response(response, "user_request")

    def _build_selection_prompt(
        self,
        strategy: str,
        existing_skills: List[str],
        sources: Dict[str, Any],
    ) -> str:
        """Build the prompt for topic selection."""
        existing_list = "\n".join(f"- {s}" for s in existing_skills) if existing_skills else "없음"

        base_prompt = f"""기존 스킬 목록 (중복 방지):
{existing_list}

"""

        if strategy == "keyword":
            keywords = [
                "PDF", "API", "Git", "문서", "코드", "데이터", "파일", "이미지",
                "분석", "생성", "변환", "요약", "검증", "자동화", "모니터링"
            ]
            sample = random.sample(keywords, min(5, len(keywords)))
            base_prompt += f"""전략: 키워드 조합 (keyword_combination)

다음 키워드들을 조합하여 새로운 스킬 주제를 만들어주세요:
{', '.join(sample)}

예시:
- "PDF" + "요약" → "PDF 자동 요약 스킬"
- "Git" + "분석" → "Git 커밋 분석 스킬"
"""

        elif strategy == "trend":
            trending = sources.get("trending", {})
            topics = trending.get("sources", {})
            base_prompt += f"""전략: 트렌드 기반 (trend_based)

현재 트렌드 토픽:
{json.dumps(topics, indent=2, ensure_ascii=False) if topics else "MCP, Claude Code, AI Agent, Workflow Automation"}

이 트렌드를 반영한 스킬 주제를 선정해주세요.
"""

        elif strategy == "request":
            requests = sources.get("requests", {}).get("queue", [])
            if requests:
                req = requests[0]
                base_prompt += f"""전략: 사용자 요청 (user_request)

대기 중인 요청:
- 주제: {req.get('topic', 'N/A')}
- 카테고리 힌트: {req.get('category_hint', 'N/A')}
- 우선순위: {req.get('priority', 'normal')}

이 요청을 반영한 스킬을 정의해주세요.
"""
            else:
                return self._build_selection_prompt("keyword", existing_skills, sources)

        elif strategy == "extend":
            if existing_skills:
                base_skill = random.choice(existing_skills)
                base_prompt += f"""전략: 스킬 확장 (skill_extension)

기존 스킬 "{base_skill}"을 확장하거나 보완하는 새 스킬을 제안해주세요.

예시 확장:
- "기본 API 호출" → "Rate Limiting이 포함된 API 호출"
- "단일 파일 분석" → "디렉토리 전체 분석"
"""
            else:
                return self._build_selection_prompt("keyword", existing_skills, sources)

        base_prompt += """

반드시 아래 YAML 형식으로만 출력하세요:

```yaml
topic: "스킬 제목"
category: Workflow | Agent | Skill
difficulty: beginner | intermediate | advanced
strategy_used: keyword_combination | trend_based | user_request | skill_extension
tags:
  - tag1
  - tag2
  - tag3
description: "한 줄 설명"
```"""

        return base_prompt

    def _parse_response(self, response: str, strategy: str) -> Dict[str, Any]:
        """Parse the AI response into structured data."""
        # Extract YAML block
        yaml_content = response
        if "```yaml" in response:
            start = response.find("```yaml") + 7
            end = response.find("```", start)
            yaml_content = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            yaml_content = response[start:end].strip()

        try:
            data = yaml.safe_load(yaml_content)
            if isinstance(data, dict):
                # Ensure required fields
                data.setdefault("strategy_used", strategy)
                data.setdefault("difficulty", "intermediate")
                data.setdefault("tags", [])
                return data
        except yaml.YAMLError as e:
            print(f"  Warning: Failed to parse YAML: {e}")

        # Fallback
        return {
            "topic": "Claude Code 기본 스킬",
            "category": "Skill",
            "difficulty": "beginner",
            "strategy_used": strategy,
            "tags": ["Claude", "기본"],
            "description": "Claude Code 기본 사용법 스킬",
        }
