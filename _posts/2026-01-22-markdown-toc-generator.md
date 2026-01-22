-
---
layout: post
title: "Markdown TOC Generator - 마크다운 목차 자동 생성 스킬"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [markdown, toc, documentation, automation, python]
---

## 개요

긴 마크다운 문서를 작성하다 보면 목차(Table of Contents)가 필요한 순간이 옵니다. 하지만 헤딩을 추가하거나 수정할 때마다 목차를 수동으로 업데이트하는 것은 번거로운 일입니다.

**Markdown TOC Generator**는 마크다운 문서의 헤딩 구조를 자동으로 분석하여 계층적 목차를 생성하고, GitHub 스타일의 앵커 링크까지 자동으로 만들어주는 스킬입니다.

### 해결하는 문제

- ❌ 목차를 수동으로 작성하고 업데이트하는 번거로움
- ❌ 헤딩 변경 시 목차 링크가 깨지는 문제
- ❌ 앵커 링크를 일일이 만들어야 하는 수고
- ❌ 일관성 없는 목차 형식

### 제공하는 솔루션

- ✅ 헤딩 구조 자동 파싱
- ✅ GitHub 호환 앵커 링크 자동 생성
- ✅ 기존 TOC 자동 업데이트
- ✅ 깊이와 레벨 커스터마이징

## 스킬 구조

```
.claude/skills/markdown-toc-generator/
├── SKILL.md              # 스킬 정의 및 사용법
└── scripts/
    └── toc_generator.py  # TOC 생성 스크립트
```

## 주요 기능

### 1. 헤딩 자동 감지

마크다운의 H1~H6 헤딩을 정규표현식으로 파싱하여 추출합니다.

```python
def extract_headings(content):
    pattern = r'^(#{1,6})\s+(.+)$'
    headings = []
    
    for line in content.split('\n'):
        match = re.match(pattern, line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append({'level': level, 'text': text})
    
    return headings
```

### 2. GitHub 스타일 앵커 생성

헤딩 텍스트를 GitHub 호환 앵커 ID로 변환합니다.

- 소문자 변환
- 특수문자 제거
- 공백을 하이픈(`-`)으로 변환

```python
def create_anchor(text):
    anchor = text.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor)
    return anchor.strip('-')
```

**예시:**
- `Installation Guide` → `installation-guide`
- `API Reference` → `api-reference`
- `What is Claude Code?` → `what-is-claude-code`

### 3. 계층적 목차 생성

헤딩 레벨에 따라 들여쓰기를 적용하여 계층 구조를 표현합니다.

```markdown
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
```

### 4. 유연한 삽입 옵션

- **자동 위치**: 첫 H1 헤딩 다음에 삽입
- **기존 TOC 업데이트**: `<!-- TOC -->` 마커 사이의 내용을 교체
- **커스터마이징**: 최대 깊이, H1 포함 여부 설정

## 사용 방법

### 설치

1. 스킬 폴더를 `.claude/skills/`에 복사
2. 스크립트 실행 권한 확인

### 기본 사용

```bash
# README.md에 TOC 생성 (H2~H4, H1 제외)
python .claude/skills/markdown-toc-generator/scripts/toc_generator.py README.md
```

### 고급 옵션

```bash
# H1 포함
python toc_generator.py README.md --include-h1

# 최대 깊이 H6까지
python toc_generator.py README.md --max-depth 6

# H1 포함 + H6까지
python toc_generator.py README.md --include-h1 --max-depth 6
```

### Claude Code에서 사용

사용자가 다음과 같이 요청하면 자동으로 실행됩니다:

- "README에 목차 추가해줘"
- "마크다운 TOC 생성해줘"
- "이 문서에 Table of Contents 넣어줘"

## 실행 예시

### Before

```markdown
# My Project

## Installation

### Prerequisites

### Setup

## Usage
```

### After

```markdown
# My Project

<!-- TOC -->

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)

<!-- /TOC -->

## Installation

### Prerequisites

### Setup

## Usage
```

## 전체 코드

### SKILL.md

위의 ---SKILL.md--- 섹션 참조

### toc_generator.py

위의 "전체 스크립트" 섹션 참조

## 활용 시나리오

### 1. 프로젝트 README

```bash
python toc_generator.py README.md
```

### 2. 기술 문서

```bash
python toc_generator.py docs/API.md --max-depth 6
```

### 3. 튜토리얼/가이드

```bash
python toc_generator.py guides/tutorial.md --include-h1
```

### 4. Batch 처리

```bash
for file in docs/*.md; do
    python toc_generator.py "$file"
done
```

## 주의사항

1. **중복 헤딩**: 동일한 텍스트의 헤딩이 여러 개 있으면 앵커가 충돌할 수 있습니다
2. **특수문자**: 이모지나 특수문자는 앵커 생성 시 제거됩니다
3. **플랫폼 차이**: GitHub/GitLab/Bitbucket은 앵커 생성 규칙이 다를 수 있습니다

## 확장 아이디어

- 중복 앵커 처리 (접미사 `-1`, `-2` 추가)
- 플랫폼별 앵커 모드 (GitHub/GitLab/Bitbucket)
- 번호 매기기 목차 (`1.`, `1.1.`, `1.1.1.`)
- 특정 헤딩 패턴 제외 기능
- VSCode Extension 또는 GUI 버전

## 다운로드

> [SKILL.md 보기](/assets/downloads/skills/markdown-toc-generator/SKILL.md)

## 관련 스킬

- **[markdown-doc-auto-generator](/posts/markdown-doc-auto-generator/)**: 마크다운 문서 자동 생성
- **[code-review-assistant](/posts/code-review-assistant/)**: AI 기반 코드 리뷰