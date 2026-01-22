# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Skill Factory - Jekyll 기반 Claude Code 스킬 자동 생성 플랫폼. 로컬 Claude CLI를 사용하여 Skill, Agent, Hook, Command 등을 자동 생성하고 GitHub Pages에 배포합니다.

**핵심 원칙**:
- `.claude/` = 실제 Claude Code에서 사용 가능한 파일 (Single Source of Truth)
- `assets/downloads/` = 블로그 독자가 다운로드할 복사본
- `_posts/` = `.claude/` 콘텐츠를 문서화한 블로그 포스트

## Directory Structure

```
.claude/                         # 실제 사용 가능 (Single Source of Truth)
├── skills/                      # 스킬 패키지
│   └── {skill-name}/
│       ├── SKILL.md            # 스킬 문서 (필수)
│       ├── scripts/            # 스킬 전용 스크립트
│       ├── references/         # 참조 문서
│       └── assets/             # 템플릿, 이미지 등
├── agents/                      # 서브에이전트 정의
│   └── {agent-name}.md
├── commands/                    # Slash Command
│   └── {command-name}.md
├── hooks/                       # Hook 설정
│   └── {hook-name}.md
├── scripts/                     # 공용 스크립트 (여러 스킬에서 사용)
│   └── {script-name}.py
└── rules/                       # 규칙/지침
    └── topic-selection.md

assets/downloads/                # 블로그 배포용 (복사본)
├── skills/                      # 스킬 다운로드
├── agents/                      # 에이전트 다운로드
├── commands/                    # 커맨드 다운로드
├── hooks/                       # 훅 다운로드
└── scripts/                     # 스크립트 다운로드

_posts/                          # 블로그 포스트 (문서화)
_data/skill_registry.yml         # 스킬 레지스트리
```

## Workflow

```
1. .claude/에 실제 파일 생성 (Claude Code가 사용)
      ↓
2. assets/downloads/에 복사 (블로그 첨부용)
      ↓
3. _posts/에 문서화 포스트 작성
      ↓
4. commit & push → GitHub Pages 배포
```

## Git 관리 규칙

⚠️ **중요**: `.claude/` 폴더는 git에서 추적하지 않습니다!

```
.claude/              ❌ git에 추가하지 않음 (Single Source of Truth로 로컬에만 존재)
assets/downloads/     ✅ git에 추가 (블로그 배포용 복사본)
_posts/               ✅ git에 추가 (블로그 포스트)
```

### 이유
- `.claude/`는 실제 Claude Code가 사용하는 파일
- 블로그 독자는 `assets/downloads/`의 복사본을 다운로드
- 이중 관리를 방지하기 위해 원본(.claude/)은 로컬에만 유지

## Common Commands

### Development
```bash
bundle exec jekyll serve          # Dev server at http://localhost:4000
```

### Skill Generation
```bash
python auto_generate.py           # 요일에 따라 자동 (평일 5개, 주말 50개)
python auto_generate.py --count 3 # 수동 개수 지정
```

## Naming Conventions

### 필수 규칙: 영문 lowercase + hyphen

모든 스킬, 에이전트, 훅, 커맨드 이름은 **영문 소문자와 하이픈**만 사용합니다.

| 유형 | 형식 | 예시 |
|------|------|------|
| Skill | `{기능}-{동작}` | `git-commit-analyzer`, `pdf-summarizer` |
| Agent | `{역할}` | `code-reviewer`, `test-runner` |
| Hook | `{이벤트}-{동작}` | `pre-commit-lint`, `post-edit-format` |
| Command | `{동작}` | `commit`, `review-pr`, `summarize` |

**금지**: 한글, 공백, 특수문자, CamelCase, 언더스코어

## Categories

| 카테고리 | 설명 | 저장 위치 |
|---------|------|----------|
| **Skill** | 특정 작업 수행 스킬 | `.claude/skills/{name}/` |
| **Agent** | 서브에이전트 정의 | `.claude/agents/{name}.md` |
| **Command** | Slash Command | `.claude/commands/{name}.md` |
| **Hook** | Claude Code 훅 | `.claude/hooks/{name}.md` |
| **Script** | 공용 스크립트 | `.claude/scripts/{name}.py` |

## Creation Guidelines

콘텐츠 생성 시 반드시 아래 도구와 출력 위치를 따릅니다:

| 카테고리 | 사용할 도구 | 저장 위치 |
|---------|------------|----------|
| Skill | `skill-creator` | `.claude/skills/{name}/` |
| Agent | `subagent-creator` | `.claude/agents/{name}.md` |
| Command | `slash-command-creator` | `.claude/commands/{name}.md` |
| Hook | `hook-creator` | `.claude/hooks/{name}.md` |

### 스킬 구조

```
.claude/skills/{skill-name}/
├── SKILL.md              # 필수: 프론트매터 + 사용 지침
├── scripts/              # 선택: 스킬 전용 스크립트
├── references/           # 선택: 참조 문서
└── assets/               # 선택: 템플릿, 이미지
```

### SKILL.md 프론트매터

```yaml
---
name: skill-name          # 영문 lowercase + hyphen
description: 스킬 설명. 언제 사용할지 포함 (트리거 조건)
---
```

## Blog Post Guidelines

블로그 포스트는 `.claude/`에 저장된 실제 콘텐츠를 **문서화**합니다.

### 핵심 원칙

1. **실제 사용 가능**: 포스트에서 설명하는 스킬/에이전트는 `.claude/`에 실제로 존재
2. **다운로드 제공**: `assets/downloads/`에 복사본을 넣어 독자가 다운로드 가능
3. **중복 없음**: `.claude/`가 Single Source, `assets/downloads/`는 복사본

### 포스트 구조

```markdown
---
title: "Git 커밋 분석 스킬"
categories: [Skill]
tags: [git, analysis, commit]
---

## 개요
(문제 정의 및 해결 목표)

## 스킬 구조
(폴더 트리 다이어그램)

## 사용 방법
(설치 및 실행 가이드)

## 전체 코드
(SKILL.md 및 스크립트 내용)

## 다운로드
> [git-commit-analyzer.zip](/assets/downloads/skills/git-commit-analyzer.zip)

## 관련 스킬
(연관 스킬 링크)
```

### 콘텐츠 규칙

- **코드**: 실행 가능해야 함
- **금지어**: "자동 생성", "AI Pipeline" (콘텐츠/태그에 사용 금지)

## Difficulty Levels

- `beginner`: 10분 내 이해 가능
- `intermediate`: 30분 내 적용 가능
- `advanced`: 아키텍처 레벨

## Scheduler

로컬 Windows 작업 스케줄러 사용:
- **평일 (월-금)**: 12:00, 5개 생성
- **주말 (토-일)**: 12:00, 50개 생성
- 생성 완료 후 일괄 commit & push → GitHub Actions 빌드/배포
