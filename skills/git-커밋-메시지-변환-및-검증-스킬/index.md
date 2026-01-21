---
name: git-커밋-메시지-변환-및-검증-스킬
version: "1.0.0"
author: AI Skill Factory
category: Workflow
difficulty: intermediate
tags: ['git', '변환', '검증', '커밋메시지', '자동화']
requires:
  - python>=3.9
  - anthropic>=0.35.0
---

```markdown
---
title: "Git 커밋 메시지 변환 및 검증 스킬"
category: Workflow
difficulty: intermediate
tags: [git, 변환, 검증, 커밋메시지, 자동화]
description: "Git 커밋 메시지를 다양한 컨벤션(Conventional Commits, Gitmoji 등)으로 변환하고, 규칙 준수 여부를 자동 검증하는 스킬"
version: "1.0.0"
last_updated: "2024-01-21"
---

# Git 커밋 메시지 변환 및 검증 스킬

## 개요

Git 커밋 메시지를 Conventional Commits, Gitmoji, Angular 등 다양한 컨벤션으로 자동 변환하고, 팀의 커밋 메시지 규칙 준수 여부를 검증하는 Claude 기반 워크플로우 자동화 스킬입니다.

## 주요 기능

- **다중 컨벤션 변환**: Conventional Commits, Gitmoji, Angular, Semantic 등 주요 컨벤션 지원
- **실시간 검증**: 커밋 메시지가 지정된 규칙을 준수하는지 즉시 확인
- **개선 제안**: 규칙 위반 시 자동으로 수정된 메시지 제안
- **배치 처리**: 여러 커밋 메시지를 한 번에 변환/검증
- **Git Hook 통합**: pre-commit 훅과 연동하여 자동 검증

## 사용 시나리오

### 시나리오 1: 레거시 커밋 메시지 일괄 변환
오래된 프로젝트의 커밋 히스토리를 Conventional Commits 형식으로 표준화

### 시나리오 2: 팀 코드 리뷰 자동화
PR의 모든 커밋 메시지가 팀 규칙을 준수하는지 자동 검증

### 시나리오 3: 다국적 팀 협업
영어로 작성된 커밋 메시지를 한국어 Conventional Commits로 변환

## 파라미터

### ConventionType
```python
class ConventionType(Enum):
    CONVENTIONAL = "conventional"  # feat:, fix:, docs: 등
    GITMOJI = "gitmoji"           # :sparkles:, :bug:, :memo: 등
    ANGULAR = "angular"           # build, ci, docs, feat, fix 등
    SEMANTIC = "semantic"         # major, minor, patch 구분
```

### ValidationRule
```python
@dataclass
class ValidationRule:
    convention: ConventionType
    max_length: int = 72           # 제목 최대 길이
    require_scope: bool = False    # 스코프 필수 여부
    require_body: bool = False     # 본문 필수 여부
    allowed_types: List[str] = None  # 허용된 타입 목록
    custom_pattern: str = None     # 커스텀 정규식
```

### TransformRequest
```python
@dataclass
class TransformRequest:
    message: str                   # 원본 커밋 메시지
    source_convention: ConventionType = None  # 원본 컨벤션 (자동 감지)
    target_convention: ConventionType  # 변환할 대상 컨벤션
    preserve_body: bool = True     # 본문 유지 여부
    language: str = "en"           # 출력 언어 (en, ko, ja 등)
```

## 실행 가능한 코드 예제

### 기본 설정

```python
import anthropic
import os
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple

class ConventionType(Enum):
    CONVENTIONAL = "conventional"
    GITMOJI = "gitmoji"
    ANGULAR = "angular"
    SEMANTIC = "semantic"

@dataclass
class ValidationRule:
    convention: ConventionType
    max_length: int = 72
    require_scope: bool = False
    require_body: bool = False
    allowed_types: List[str] = None
    custom_pattern: str = None

@dataclass
class TransformRequest:
    message: str
    source_convention: Optional[ConventionType] = None
    target_convention: ConventionType = ConventionType.CONVENTIONAL
    preserve_body: bool = True
    language: str = "en"

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    suggestions: List[str]
    corrected_message: Optional[str] = None

class GitCommitSkill:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    def transform_message(self, request: TransformRequest) -> str:
        """커밋 메시지를 지정된 컨벤션으로 변환"""
        
        prompt = f"""You are a Git commit message expert. Transform the following commit message to {request.target_convention.value} format.

Original message:
{request.message}

Requirements:
- Target convention: {request.target_convention.value}
- Preserve body: {request.preserve_body}
- Output language: {request.language}

Convention guidelines:
{self._get_convention_guide(request.target_convention)}

Output ONLY the transformed commit message, nothing else."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text.strip()
    
    def validate_message(self, message: str, rule: ValidationRule) -> ValidationResult:
        """커밋 메시지가 규칙을 준수하는지 검증"""
        
        errors = []
        suggestions = []
        
        # 기본 검증
        lines = message.split('\n')
        subject = lines[0]
        
        if len(subject) > rule.max_length:
            errors.append(f"Subject exceeds {rule.max_length} characters (current: {len(subject)})")
            suggestions.append(f"Shorten subject to under {rule.max_length} characters")
        
        # 컨벤션별 검증
        if rule.convention == ConventionType.CONVENTIONAL:
            if not re.match(r'^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .+', subject):
                errors.append("Does not follow Conventional Commits format")
                suggestions.append("Use format: type(scope): description")
        
        elif rule.convention == ConventionType.GITMOJI:
            if not re.match(r'^:[a-z_]+: .+', subject):
                errors.append("Missing gitmoji at the start")
                suggestions.append("Start with emoji like :sparkles: or :bug:")
        
        # 스코프 검증
        if rule.require_scope:
            if rule.convention == ConventionType.CONVENTIONAL:
                if not re.search(r'\(.+\)', subject):
                    errors.append("Scope is required")
                    suggestions.append("Add scope in parentheses, e.g., feat(api): ...")
        
        # 본문 검증
        if rule.require_body and len(lines) < 3:
            errors.append("Commit body is required")
            suggestions.append("Add detailed description after blank line")
        
        # 타입 검증
        if rule.allowed_types:
            commit_type = subject.split('(')[0].split(':')[0].strip(':')
            if commit_type not in rule.allowed_types:
                errors.append(f"Type '{commit_type}' not in allowed types: {rule.allowed_types}")
                suggestions.append(f"Use one of: {', '.join(rule.allowed_types)}")
        
        # 에러가 있으면 Claude로 수정본 생성
        corrected = None
        if errors:
            corrected = self._generate_corrected_message(message, rule, errors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            suggestions=suggestions,
            corrected_message=corrected
        )
    
    def batch_transform(self, messages: List[str], target: ConventionType) -> List[str]:
        """여러 커밋 메시지를 일괄 변환"""
        results = []
        for msg in messages:
            request = TransformRequest(message=msg, target_convention=target)
            transformed = self.transform_message(request)
            results.append(transformed)
        return results
    
    def _get_convention_guide(self, convention: ConventionType) -> str:
        """컨벤션별 가이드 반환"""
        guides = {
            ConventionType.CONVENTIONAL: """
Format: type(scope): description

Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
Example: feat(auth): add OAuth2 login support
""",
            ConventionType.GITMOJI: """
Format: :emoji: description

Common emojis:
- :sparkles: New feature
- :bug: Bug fix
- :memo: Documentation
- :recycle: Refactoring
- :zap: Performance improvement
Example: :sparkles: Add user profile page
""",
            ConventionType.ANGULAR: """
Format: type(scope): subject

Types: build, ci, docs, feat, fix, perf, refactor, style, test
Example: fix(compiler): handle edge case in parser
""",
            ConventionType.SEMANTIC: """
Format: [MAJOR|MINOR|PATCH] description

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes
Example: [MINOR] Add export to CSV feature
"""
        }
        return guides.get(convention, "")
    
    def _generate_corrected_message(self, message: str, rule: ValidationRule, errors: List[str]) -> str:
        """규칙 위반 시 수정된 메시지 생성"""
        
        prompt = f"""Fix the following Git commit message to comply with {rule.convention.value} convention.

Original message:
{message}

Errors found:
{chr(10).join(f'- {e}' for e in errors)}

Rules:
- Convention: {rule.convention.value}
- Max subject length: {rule.max_length}
- Require scope: {rule.require_scope}
- Require body: {rule.require_body}

Output ONLY the corrected commit message."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text.strip()
```

### 예제 1: 기본 변환

```python
# 초기화
skill = GitCommitSkill(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# 일반 메시지를 Conventional Commits으로 변환
original = "Added user authentication"
request = TransformRequest(
    message=original,
    target_convention=ConventionType.CONVENTIONAL
)
transformed = skill.transform_message(request)
print(f"Original: {original}")
print(f"Transformed: {transformed}")
# Output: feat(auth): add user authentication
```

### 예제 2: 한국어로 변환

```python
# 영어 메시지를 한국어 Conventional Commits으로 변환
request = TransformRequest(
    message="Fixed bug in payment processing",
    target_convention=ConventionType.CONVENTIONAL,
    language="ko"
)
transformed = skill.transform_message(request)
print(transformed)
# Output: fix(payment): 결제 처리 버그 수정
```

### 예제 3: Gitmoji 변환

```python
# Conventional Commits를 Gitmoji로 변환
request = TransformRequest(
    message="feat(api): add rate limiting middleware",
    source_convention=ConventionType.CONVENTIONAL,
    target_convention=ConventionType.GITMOJI
)
transformed = skill.transform_message(request)
print(transformed)
# Output: :sparkles: Add rate limiting middleware for API
```

### 예제 4: 커밋 메시지 검증

```python
# 엄격한 규칙으로 검증
rule = ValidationRule(
    convention=ConventionType.CONVENTIONAL,
    max_length=50,
    require_scope=True,
    require_body=True,
    allowed_types=["feat", "fix", "docs"]
)

message = """feat: add user profile
This is a new feature"""

result = skill.validate_message(message, rule)

if not result.is_valid:
    print("Validation failed!")
    print("\nErrors:")
    for error in result.errors:
        print(f"  - {error}")
    
    print("\nSuggestions:")
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
    
    print(f"\nCorrected message:\n{result.corrected_message}")
else:
    print("✓ Commit message is valid!")
```

### 예제 5: 배치 처리

```python
# Git 로그에서 여러 커밋 메시지 변환
legacy_commits = [
    "Fixed typo in README",
    "Added new API endpoint",
    "Updated dependencies",
    "Improved performance"
]

converted = skill.batch_transform(
    messages=legacy_commits,
    target=ConventionType.CONVENTIONAL
)

for original, converted_msg in zip(legacy_commits, converted):
    print(f"{original:40} → {converted_msg}")

# Output:
# Fixed typo in README                     → docs(readme): fix typo
# Added new API endpoint                   → feat(api): add new endpoint
# Updated dependencies                     → chore(deps): update dependencies
# Improved performance                     → perf: improve application performance
```

### 예제 6: Git Hook 통합

```python
#!/usr/bin/env python3
"""
.git/hooks/commit-msg 파일로 저장하고 실행 권한 부여:
chmod +x .git/hooks/commit-msg
"""

import sys
from git_commit_skill import GitCommitSkill, ValidationRule, ConventionType

def main():
    commit_msg_file = sys.argv[1]
    
    # 커밋 메시지 읽기
    with open(commit_msg_file, 'r', encoding='utf-8') as f:
        message = f.read()
    
    # 검증 규칙 설정
    rule = ValidationRule(
        convention=ConventionType.CONVENTIONAL,
        max_length=72,
        require_scope=False,
        allowed_types=["feat", "fix", "docs", "style", "refactor", "test", "chore"]
    )
    
    # 검증 실행
    skill = GitCommitSkill(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    result = skill.validate_message(message, rule)
    
    if not result.is_valid:
        print("❌ Commit message validation failed!\n")
        print("Errors:")
        for error in result.errors:
            print(f"  • {error}")
        
        print("\n💡 Suggested fix:")
        print(result.corrected_message)
        
        print("\n🔧 To use the corrected message, run:")
        print(f"   git commit --amend -m \"{result.corrected_message}\"")
        
        sys.exit(1)
    
    print("✅ Commit message is valid!")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 예제 7: CI/CD 통합 (GitHub Actions)

```yaml
name: Validate Commit Messages

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  validate-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install anthropic
      
      - name: Validate all commits in PR
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python << 'EOF'
          import os
          import subprocess
          from git_commit_skill import GitCommitSkill, ValidationRule, ConventionType
          
          # PR의 모든 커밋 메시지 가져오기
          result = subprocess.run(
              ['git', 'log', '--format=%B%n---COMMIT---', 'origin/main..HEAD'],
              capture_output=True,
              text=True
          )
          commits = result.stdout.split('---COMMIT---')[:-1]
          
          # 검증 규칙
          rule = ValidationRule(
              convention=ConventionType.CONVENTIONAL,
              max_length=72,
              allowed_types=["feat", "fix", "docs", "style", "refactor", "test", "chore", "ci"]
          )
          
          skill = GitCommitSkill(api_key=os.environ["ANTHROPIC_API_KEY"])
          
          failed = []
          for i, commit in enumerate(commits, 1):
              result = skill.validate_message(commit.strip(), rule)
              if not result.is_valid:
                  failed.append((i, commit.strip(), result))
          
          if failed:
              print(f"❌ {len(failed)} commit(s) failed validation:\n")
              for idx, msg, result in failed:
                  print(f"Commit #{idx}:")
                  print(f"  Message: {msg.split(chr(10))[0]}")
                  print(f"  Errors: {', '.join(result.errors)}")
                  print(f"  Suggestion: {result.corrected_message}\n")
              exit(1)
          else:
              print(f"✅ All {len(commits)} commits are valid!")
          EOF
```

## 고급 사용법

### 커스텀 컨벤션 정의

```python
# 회사 내부 커밋 규칙 정의
custom_rule = ValidationRule(
    convention=ConventionType.CONVENTIONAL,
    max_length=60,
    require_scope=True,
    require_body=True,
    allowed_types=["feature", "bugfix", "hotfix", "release", "docs"],
    custom_pattern=r'^(feature|bugfix|hotfix)\([A-Z]+-\d+\): .+'  # JIRA 티켓 포함
)

message = "feature(AUTH-123): implement SSO login"
result = skill.validate_message(message, custom_rule)
```

### 다국어 지원

```python
# 일본어로 커밋 메시지 변환
request = TransformRequest(
    message="Add user registration form",
    target_convention=ConventionType.CONVENTIONAL,
    language="ja"
)
print(skill.transform_message(request))
# Output: feat(auth): ユーザー登録フォームを追加
```

## 베스트 프랙티스

1. **API 키 보안**: 환경 변수나 Secret Manager 사용
2. **캐싱**: 동일한 메시지 반복 변환 시 결과 캐시
3. **배치 크기**: 한 번에 50개 이하의 커밋 처리 권장
4. **오류 처리**: API 호출 실패 시 재시도 로직 구현
5. **Git Hook 성능**: pre-commit 훅은 빠르게 실행되도록 최적화

## 제한 사항

- Claude API 호출 비용 발생 (토큰 사용량 고려)
- 매우 긴 커밋 메시지(>2000자)는 처리 시간 증가
- 네트워크 연결 필수
- Rate limiting 고려 필요 (배치 처리 시)

## 라이선스

MIT License

## 기여

이슈 및 PR은 GitHub 저장소에서 환영합니다.
```