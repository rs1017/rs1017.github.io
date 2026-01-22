---
layout: post
title: "코드 리뷰를 AI에게 맡기는 법 - Code Review Assistant"
date: 2026-01-22 15:11:00 +0900
categories: [AI, Skill]
tags: [code-review, pull-request, quality, automation, claude-code]
---

## 왜 AI 코드 리뷰가 필요한가?

코드 리뷰는 소프트웨어 품질을 보장하는 핵심 프로세스입니다. 하지만 현실적인 문제들이 있습니다:

- ⏰ **시간 부족**: 리뷰어의 시간은 한정적
- 👀 **피로도**: 반복적인 체크로 중요한 이슈 놓침
- 📏 **일관성 부족**: 리뷰어마다 다른 기준
- 🔄 **반복 작업**: 매번 같은 패턴의 이슈 지적

**Code Review Assistant 스킬**은 이런 문제를 해결합니다. AI가 1차 검토를 수행하고, 개발자는 비즈니스 로직과 아키텍처 검토에 집중할 수 있습니다.

## 스킬 구조

```
.claude/skills/code-review-assistant/
├── SKILL.md                 # 스킬 메인 문서
├── scripts/
│   ├── review_analyzer.py   # Git diff 분석
│   ├── issue_detector.py    # 이슈 탐지 엔진
│   └── report_generator.py  # 리포트 생성
├── references/
│   ├── security-rules.yml   # 보안 체크리스트
│   ├── quality-metrics.yml  # 코드 품질 기준
│   └── language-patterns/   # 언어별 패턴
│       ├── python.yml
│       ├── javascript.yml
│       └── java.yml
└── assets/
    └── templates/
        └── review-template.md
```

## 사용 방법

### 1. 기본 리뷰

현재 브랜치의 변경사항을 리뷰합니다:

```bash
# Claude Code에서
현재 브랜치 변경사항을 리뷰해줘
```

### 2. Pull Request 리뷰

GitHub PR을 직접 분석합니다:

```bash
# GitHub CLI 연동
gh pr view 123 --json files,diff | claude "이 PR을 리뷰해줘"
```

### 3. 특정 파일 집중 리뷰

```bash
src/auth/login.py 파일을 보안 관점에서 리뷰해줘
```

### 4. Git Hook 자동화

커밋 전 자동 리뷰:

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "🤖 AI 코드 리뷰 실행 중..."
REVIEW=$(git diff --cached | claude "커밋 전 코드를 리뷰해줘")

if echo "$REVIEW" | grep -q "🔴 Critical"; then
    echo "❌ Critical 이슈 발견! 커밋 중단"
    echo "$REVIEW"
    exit 1
fi

echo "✅ 리뷰 통과"
```

## 리뷰 분석 체계

### 🔴 Critical Issues (즉시 수정 필수)

**보안 취약점**:
- SQL Injection
- XSS (Cross-Site Scripting)
- CSRF 취약점
- 하드코딩된 비밀키

**안정성 문제**:
- Null Reference Exception
- Array Index Out of Bounds
- 메모리 누수 패턴
- Race Condition

**예시**:

```python
# ❌ Critical: SQL Injection 위험
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)

# ✅ 수정: Parameterized Query
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    return db.execute(query, (user_id,))
```

### 🟡 Code Quality Issues (권장 수정)

**구조적 문제**:
- 중복 코드 (DRY 원칙 위반)
- 높은 복잡도 (Cyclomatic Complexity > 10)
- 과도한 결합도
- 단일 책임 원칙 위반

**가독성**:
- 불명확한 변수명
- 과도한 중첩
- 주석 부족
- 네이밍 컨벤션 위반

**예시**:

```javascript
// 🟡 Quality: 복잡도 높음 (15)
function processOrder(order) {
    if (order.items.length > 0) {
        if (order.user.isPremium) {
            if (order.total > 100) {
                // ... 많은 중첩된 로직
            }
        }
    }
}

// ✅ 개선: 조기 반환 + 함수 분리
function processOrder(order) {
    if (!hasItems(order)) return;
    if (!order.user.isPremium) return;
    
    const discount = calculateDiscount(order);
    const total = applyDiscount(order.total, discount);
    return saveOrder(order, total);
}
```

### 🟢 Suggestions (최적화 아이디어)

**성능 개선**:
- 불필요한 반복문
- 캐싱 기회
- 비동기 처리 가능 지점
- 데이터베이스 쿼리 최적화

**모던 패턴**:
- 최신 언어 기능 활용
- 디자인 패턴 적용
- 함수형 프로그래밍 스타일

**예시**:

```python
# 🟢 Suggestion: 성능 개선
# Before: 리스트 전체를 메모리에 로드
results = [process(item) for item in huge_dataset]

# After: 제너레이터로 메모리 절약
results = (process(item) for item in huge_dataset)
```

## 실전 활용 시나리오

### Scenario 1: PR 리뷰 자동화

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: AI Review
        run: |
          gh pr diff ${{ github.event.pull_request.number }} | \
            claude "이 PR을 리뷰해줘" > review.md
          
      - name: Post Comment
        run: |
          gh pr comment ${{ github.event.pull_request.number }} \
            --body-file review.md
```

### Scenario 2: Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Staged 파일만 리뷰
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

for FILE in $STAGED_FILES; do
    echo "Reviewing $FILE..."
    git diff --cached $FILE | claude "이 변경사항을 리뷰해줘"
done
```

### Scenario 3: 레거시 코드 점진적 개선

```bash
# 주간 코드 품질 리포트
git log --since="1 week ago" --name-only --pretty=format: | \
  sort | uniq | \
  xargs -I {} claude "{}를 리뷰하고 개선점을 알려줘"
```

## 전체 코드

### SKILL.md