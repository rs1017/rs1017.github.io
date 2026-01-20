"""
Code Generator Agent for AI Skill Factory.
"""

from pathlib import Path
from typing import Any, Dict

from .base_agent import BaseAgent


class CodeGeneratorAgent(BaseAgent):
    """Agent that generates executable example code."""

    def __init__(self, client: Any, prompts_dir: Path) -> None:
        super().__init__(client, prompts_dir)
        self.agent_prompt = self._load_prompt("code-generator.md")

    def generate(self, topic_info: Dict[str, Any], skill_md: str) -> str:
        """Generate example.py code for the skill."""
        prompt = f"""다음 스킬에 대한 실행 가능한 Python 예제 코드를 작성해주세요:

## 주제 정보
- 제목: {topic_info.get('topic', 'Unknown')}
- 카테고리: {topic_info.get('category', 'Skill')}
- 난이도: {topic_info.get('difficulty', 'intermediate')}

## SKILL.md 내용
```markdown
{skill_md[:3000]}
```

## 요구사항
1. 즉시 실행 가능한 완전한 Python 스크립트
2. Anthropic API 사용 (환경변수 ANTHROPIC_API_KEY)
3. 타입 힌트 필수
4. docstring 포함
5. 에러 핸들링 포함
6. main() 함수와 if __name__ == "__main__" 블록

완전한 Python 파일 내용만 출력하세요.
코드 블록(```)이나 다른 설명은 포함하지 마세요.
#!/usr/bin/env python3 으로 시작하세요.
"""

        system = self._build_system_prompt(self.agent_prompt)
        response = self.client.generate(prompt=prompt, system=system, max_tokens=4096)

        # Clean up response - remove markdown code blocks if present
        code = response.strip()
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        code = code.strip()

        # Ensure shebang
        if not code.startswith("#!/"):
            code = "#!/usr/bin/env python3\n" + code

        return code
