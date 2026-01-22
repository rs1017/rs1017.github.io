-
---
title: "스킬을 생성하는 스킬: Generated Skill Creator"
date: 2024-01-22 12:00:00 +0900
categories: [Skill]
tags: [meta, automation, skill-generation, productivity, claude-code]
description: "사용자 요구사항을 분석해 새로운 Claude Code 스킬을 자동으로 생성하는 메타 스킬. 반복 작업을 스킬로 만들어 생산성을 극대화합니다."
---

## 개요

개발하다 보면 "이 작업을 자동화하는 스킬이 있으면 좋겠는데..."라고 생각할 때가 많습니다. Generated Skill Creator는 바로 그런 순간을 위한 **메타 스킬**입니다. 사용자의 요구사항을 분석해 완전한 스킬 패키지를 자동으로 생성합니다.

### 해결하는 문제

- 스킬 작성 문법을 매번 찾아봐야 함
- 프론트매터 형식과 네이밍 규칙을 기억하기 어려움
- 스크립트와 문서를 따로 작성해야 하는 번거로움
- 반복 작업을 스킬로 만들고 싶지만 어디서 시작할지 모름

### 제공하는 가치

- **5분 안에** 완전한 스킬 패키지 생성
- 네이밍 규칙 자동 검증 (`lowercase-with-hyphens`)
- 필요시 Python/Bash 스크립트 자동 생성
- SKILL.md 템플릿과 모범 사례 자동 적용

## 스킬 구조

```
.claude/skills/generated-skill/
├── SKILL.md                 # 스킬 정의 (프론트매터 + 사용 지침)
├── scripts/
│   └── skill_generator.py   # 스킬 생성 로직
└── assets/
    └── template.md          # SKILL.md 템플릿
```

## 사용 방법

### 1. 설치

```bash
# .claude/skills/ 디렉토리에 복사
cp -r generated-skill ~/.claude/skills/
```

### 2. 실행

Claude Code에서 자연어로 요청:

```
User: Git 커밋 메시지를 분석해서 개선점을 제안하는 스킬을 만들어줘

Claude: [generated-skill 자동 실행]
git-commit-analyzer 스킬을 생성했습니다.

.claude/skills/git-commit-analyzer/
├── SKILL.md
└── scripts/
    └── analyze_commits.py
```

### 3. 트리거 조건

다음과 같은 표현에 자동으로 반응합니다:

- "~하는 스킬을 만들어줘"
- "이 작업을 자동화하고 싶어"
- "반복되는 [작업]을 스킬로 만들 수 있을까?"
- "커스텀 스킬이 필요해"

## 작동 원리

### Step 1: 요구사항 분석

사용자 설명에서 추출:
- **도메인**: Git, 파일, API, 데이터 등
- **목표**: 분석, 생성, 변환, 검증 등
- **입출력**: 파일, 텍스트, JSON 등
- **복잡도**: beginner/intermediate/advanced

### Step 2: 컴포넌트 결정

필요한 요소 판단:
- Python 스크립트 (데이터 처리)
- Bash 스크립트 (Git/CLI 작업)
- 참조 문서 (API 스펙, 예제)
- 템플릿 (설정 파일, 출력 형식)

### Step 3: SKILL.md 생성

```yaml
---
name: skill-name-in-english  # 자동 변환
description: 명확한 트리거 조건 포함
---

# Skill Title

## When to Use This Skill
(구체적인 사용 시점)

## How It Works
(작동 방식 설명)

## Usage
(실행 예제)
```

### Step 4: 지원 파일 생성

필요시 자동 생성:
- `scripts/*.py` - 자동화 로직
- `references/*.md` - API 문서, 예제
- `assets/*.json` - 설정 템플릿

### Step 5: 검증 및 출력

- 네이밍 규칙 준수 확인
- 기존 스킬과 중복 체크
- 설치 가이드 제공

## 전체 코드

### SKILL.md

```markdown
---
name: generated-skill
description: Automatically generates new Claude Code skills based on user requirements or problem descriptions. Use when users want to create custom skills, automate repetitive tasks, or extend Claude Code capabilities with specialized workflows.
---

# Generated Skill Creator

A meta-skill that helps you create new Claude Code skills by analyzing requirements, generating appropriate skill structures, and producing ready-to-use SKILL.md files with supporting scripts.

## When to Use This Skill

Invoke this skill when the user:
- Asks to "create a new skill for [task]"
- Describes a repetitive workflow that could be automated
- Wants to extend Claude Code with custom functionality
- Needs a specialized tool for their development workflow

## How It Works

1. **Requirement Analysis**: Analyzes user's problem description
2. **Skill Design**: Determines optimal skill structure
3. **Template Generation**: Creates SKILL.md with proper frontmatter
4. **Script Generation**: Generates supporting scripts if needed
5. **Validation**: Ensures naming conventions and best practices

## Implementation

[See full implementation in SKILL.md above]
```

### scripts/skill_generator.py

```python
#!/usr/bin/env python3
"""
Skill Generation Logic
Analyzes user requirements and generates complete skill packages.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

class SkillGenerator:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.template = self._load_template()
    
    def analyze_requirements(self, user_input: str) -> Dict:
        """Extract key requirements from user description."""
        return {
            'domain': self._extract_domain(user_input),
            'action': self._extract_action(user_input),
            'complexity': self._estimate_complexity(user_input),
            'needs_script': self._needs_script(user_input)
        }
    
    def generate_name(self, requirements: Dict) -> str:
        """Generate skill name following naming conventions."""
        name = f"{requirements['domain']}-{requirements['action']}"
        return self._to_kebab_case(name)
    
    def create_skill_package(self, name: str, requirements: Dict) -> Path:
        """Create complete skill directory structure."""
        skill_path = self.base_path / name
        skill_path.mkdir(exist_ok=True)
        
        # Generate SKILL.md
        self._write_skill_md(skill_path, name, requirements)
        
        # Generate scripts if needed
        if requirements['needs_script']:
            self._generate_script(skill_path, name, requirements)
        
        return skill_path
    
    def _to_kebab_case(self, text: str) -> str:
        """Convert to lowercase-with-hyphens."""
        text = re.sub(r'[^a-zA-Z0-9]+', '-', text)
        return text.lower().strip('-')
    
    def _extract_domain(self, text: str) -> str:
        """Identify problem domain."""
        domains = ['git', 'file', 'api', 'data', 'code', 'doc']
        for domain in domains:
            if domain in text.lower():
                return domain
        return 'general'
    
    def _extract_action(self, text: str) -> str:
        """Identify desired action."""
        actions = ['analyze', 'generate', 'convert', 'validate', 'format']
        for action in actions:
            if action in text.lower():
                return action
        return 'process'
    
    def _estimate_complexity(self, text: str) -> str:
        """Estimate skill complexity."""
        if any(word in text.lower() for word in ['simple', 'basic', 'quick']):
            return 'beginner'
        elif any(word in text.lower() for word in ['complex', 'advanced', 'system']):
            return 'advanced'
        return 'intermediate'
    
    def _needs_script(self, text: str) -> bool:
        """Determine if script is needed."""
        script_indicators = ['parse', 'analyze', 'process', 'calculate', 'fetch']
        return any(word in text.lower() for word in script_indicators)

# Usage example
if __name__ == '__main__':
    generator = SkillGenerator(Path('.claude/skills'))
    
    user_request = "Git 커밋 메시지를 분석해서 개선점 제안"
    requirements = generator.analyze_requirements(user_request)
    skill_name = generator.generate_name(requirements)
    skill_path = generator.create_skill_package(skill_name, requirements)
    
    print(f"✓ Created skill: {skill_name}")
    print(f"✓ Location: {skill_path}")
```

## 실전 예제

### 예제 1: 간단한 포매터 스킬

```
User: 마크다운 테이블을 예쁘게 정렬하는 스킬이 필요해

Claude: ✓ markdown-table-formatter 스킬 생성 완료

.claude/skills/markdown-table-formatter/
└── SKILL.md  # 스크립트 없이 Claude의 텍스트 처리 능력 활용
```

### 예제 2: 복잡한 분석 스킬

```
User: 코드베이스에서 사용되지 않는 함수를 찾아주는 스킬

Claude: ✓ unused-function-detector 스킬 생성 완료

.claude/skills/unused-function-detector/
├── SKILL.md
└── scripts/
    ├── ast_parser.py      # AST 기반 함수 추출
    └── usage_checker.py   # 참조 검색
```

## 모범 사례

### 1. 명확한 트리거 조건

```yaml
# Good
description: Analyzes commit messages and suggests improvements. Use when reviewing Git history or before pushing commits.

# Bad
description: Helps with Git commits.
```

### 2. 자체 완결성

스킬은 독립적으로 작동해야 합니다. 외부 의존성이 필요하면 명시:

```markdown
## Requirements
- Python 3.8+
- `pip install gitpython`
```

### 3. 에러 처리

생성된 스크립트에 에러 처리 포함:

```python
try:
    result = process_data(input)
except FileNotFoundError:
    print("Error: Input file not found")
    sys.exit(1)
```

## 한계점

- 기존 스킬 수정 불가 (Edit 도구 사용 필요)
- 생성 시 외부 API 호출 불가
- 복잡한 워크플로는 수동 조정 필요
- 생성된 스크립트는 검토 후 사용 권장

## 다운로드

> [generated-skill.zip](/assets/downloads/skills/generated-skill.zip)

스킬 패키지를 다운로드하여 `.claude/skills/` 디렉토리에 압축 해제 후 사용하세요.

## 관련 스킬

- **skill-creator**: 대화형 스킬 생성 마법사
- **slash-command-creator**: Slash Command 생성기
- **hook-creator**: Claude Code Hook 생성기
- **subagent-creator**: 서브에이전트 생성기