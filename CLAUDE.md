# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

낙현아빠의 개발 블로그 - Jekyll 기반 게임 서버 개발자의 IT 블로그. 게임 서버 개발, AI, 서버 아키텍처, DB, Redis, DevOps 등 개발자 관점의 기술 블로그를 운영합니다. 에이전트 파이프라인을 통해 주제 선정 → 글 작성 → 유튜브 기획 → 리뷰 과정을 자동화합니다.

**핵심 원칙**:
- `.claude/` = 실제 Claude Code에서 사용 가능한 파일 (Single Source of Truth)
- `assets/downloads/` = 블로그 독자가 다운로드할 복사본
- `_posts/` = 개발자 관점의 기술 블로그 포스트

## Directory Structure

```
.claude/                         # 실제 사용 가능 (Single Source of Truth)
├── agents/                      # 에이전트 정의
│   ├── topic-selector.md       # 주제 선정 에이전트
│   ├── writer.md               # 블로그 작성 에이전트
│   ├── youtube-creator.md      # 유튜브 기획 에이전트
│   └── reviewer.md             # 리뷰/QA 에이전트
├── skills/                      # 스킬 패키지
│   └── {skill-name}/
│       ├── SKILL.md            # 스킬 문서 (필수)
│       ├── scripts/            # 스킬 전용 스크립트
│       ├── references/         # 참조 문서
│       └── assets/             # 템플릿, 이미지 등
├── commands/                    # Slash Command
│   └── {command-name}.md
├── hooks/                       # Hook 설정
│   └── {hook-name}.md
├── scripts/                     # 공용 스크립트
│   └── {script-name}.py
└── rules/                       # 규칙/지침
    └── topic-selection.md

assets/downloads/                # 블로그 배포용 (복사본)
├── agents/                      # 에이전트 다운로드
├── skills/                      # 스킬 다운로드
├── commands/                    # 커맨드 다운로드
├── hooks/                       # 훅 다운로드
└── scripts/                     # 스크립트 다운로드

_posts/                          # 블로그 포스트
_data/skill_registry.yml         # 포스트 레지스트리
```

## Agent Pipeline

블로그 콘텐츠 생성은 4단계 에이전트 파이프라인을 통해 진행됩니다:

```
Topic Selector → Writer → YouTube Creator → Reviewer
  (주제 선정)    (글 작성)   (영상 기획)      (리뷰/QA)
                                               │
                              ▲    반려 시       │
                              └─────────────────┘
```

### 1. Topic Selector (주제 선정)
- `.claude/rules/topic-selection.md` 규칙 준수
- 게임서버, AI, DB, 아키텍처, DevOps 등 IT 주제 선정
- 기존 포스트와 중복 방지

### 2. Writer (블로그 작성)
- 선정된 주제로 개발자 관점의 블로그 포스트 작성
- 실무 경험 기반의 기술 글 작성
- 코드 예제, 아키텍처 다이어그램 포함

### 3. YouTube Creator (유튜브 기획)
- 완성된 블로그 글을 유튜브 영상 대본/기획으로 변환
- 영상 구성: 인트로, 본문(코드/아키텍처 설명), 아웃트로
- 썸네일 텍스트, 태그, 설명란 등 메타데이터 생성

### 4. Reviewer (리뷰/QA)
- 블로그 포스트: 기술적 정확성, 가독성, 코드 품질 검토
- 유튜브 기획: 영상 흐름, 시청자 관점 검토
- 반려 시 Writer에게 재작업 요청 (최대 3회)

## Workflow

```
1. 주제 선정 (Topic Selector)
      ↓
2. 블로그 포스트 작성 (Writer)
      ↓
3. 유튜브 영상 기획 (YouTube Creator)
      ↓
4. 리뷰/QA (Reviewer) → 반려 시 2번으로 복귀
      ↓
5. assets/downloads/에 에이전트 파일 복사 (블로그 첨부용)
      ↓
6. git add assets/downloads/ (⚠️ 필수! 복사 직후 즉시 실행)
      ↓
7. _posts/에 포스트 파일 저장
      ↓
8. commit & push → GitHub Pages 배포
```

### ⚠️ 중요: assets/downloads/ 복사 후 반드시 git add

**문제**: 파일을 복사만 하고 git add를 하지 않으면 GitHub Pages 배포 시 파일이 없어 링크가 깨짐

**해결**: 복사 직후 반드시 아래 명령 실행:
```bash
git add assets/downloads/
```

**검증**: 게시글 작성 전 파일이 git에 추가되었는지 확인:
```bash
git status assets/downloads/
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

### Blog Post Generation
```bash
python auto_generate.py           # 기본 5개 포스트 생성
python auto_generate.py --count 3 # 수동 개수 지정
```

## Categories

블로그 포스트 카테고리:

| 카테고리 | 설명 |
|---------|------|
| **Server** | 게임 서버 아키텍처, 네트워크, 동시성 처리 |
| **AI** | LLM, 프롬프트 엔지니어링, AI 도구 활용 |
| **Database** | Redis, MySQL, MongoDB, 쿼리 최적화 |
| **DevOps** | CI/CD, Docker, Kubernetes, 모니터링 |
| **Architecture** | 설계 패턴, MSA, 분산 시스템 |
| **Career** | 개발자 성장, 팀 관리, 커리어 |
| **Claude Code** | Claude Code 스킬, 에이전트, 훅, 커맨드 |

## Blog Post Guidelines

### 핵심 원칙

1. **개발자 관점**: 16년차 게임 서버 개발자의 실무 경험 기반
2. **실용적 내용**: 이론보다 실전에서 바로 적용 가능한 내용
3. **코드 포함**: 설명에는 실행 가능한 코드 예제 포함

### 포스트 구조

```markdown
---
title: "포스트 제목"
categories: [Server]
tags: [game-server, architecture, mmorpg]
---

## 개요
(문제 정의 및 해결 목표)

## 배경
(왜 이 주제가 중요한지)

## 본론
### 핵심 개념
### 구현/적용
### 코드 예제

## 실전 적용
(실무에서 어떻게 활용하는지)

## 마무리
(요약 및 핵심 포인트)
```

### 콘텐츠 규칙

- **코드**: 실행 가능해야 함
- **금지어**: "자동 생성", "AI Pipeline" (콘텐츠/태그에 사용 금지)
- **톤**: 개발자 동료에게 설명하는 톤 (친근하지만 전문적)

### ⚠️ 다운로드 링크 작성 규칙 (필수)

**문제**: `assets/downloads/`에 파일이 git에 추가되지 않으면 배포 후 링크가 깨짐

**필수 절차**:
1. 게시글 작성 **전에** 반드시 `git add assets/downloads/` 실행
2. `git status`로 파일이 스테이징되었는지 확인
3. 확인 후에만 게시글에 다운로드 링크 추가

**절대 금지**:
- git add 없이 게시글에 다운로드 링크 작성
- 존재하지 않는 파일 경로 링크
- `assets/downloads/`의 .md 파일에 프론트매터(`---`) 포함

### ⚠️ assets/downloads/ SKILL.md 프론트매터 금지

**문제**: Jekyll은 프론트매터가 있는 .md 파일을 .html로 변환합니다. 따라서 .md 링크가 깨집니다.

**해결**: `assets/downloads/`에 복사되는 .md 파일에서 프론트매터를 **반드시 제거**해야 합니다.

### ⚠️ About 페이지 업데이트 (필수)

새 에이전트나 주요 변경 시 `_tabs/about.md`의 관련 섹션도 업데이트해야 합니다.

## Difficulty Levels

- `beginner`: 10분 내 이해 가능
- `intermediate`: 30분 내 적용 가능
- `advanced`: 아키텍처 레벨

## Scheduler

로컬 Windows 작업 스케줄러 사용:
- **평일 (월-금)**: 12:00, 5개 생성
- **주말 (토-일)**: 12:00, 50개 생성
- 생성 완료 후 일괄 commit & push → GitHub Actions 빌드/배포
