---
layout: post
title: "Claude Code Slash Command Creator - 슬래시 명령 생성"
date: 2026-01-22 10:20:00 +0900
categories: [AI, Skill]
tags: [claude-code, slash-command, automation, cli]
---

## 개요

Slash Command Creator는 Claude Code에서 자주 사용하는 프롬프트를 커스텀 슬래시 명령으로 자동화하는 스킬입니다.

## 명령 구조

슬래시 명령은 YAML frontmatter가 포함된 Markdown 파일입니다:

```markdown
---
description: /help에 표시될 설명
---

프롬프트 지침이 여기에 들어갑니다.

$ARGUMENTS
```

## 저장 위치

| 범위 | 경로 | 표시 |
|------|------|------|
| 프로젝트 | `.claude/commands/` | (project) |
| 개인 | `~/.claude/commands/` | (user) |

## 네임스페이싱

하위 디렉토리로 명령을 구성:

```
.claude/commands/frontend/component.md → /component (project:frontend)
~/.claude/commands/backend/api.md → /api (user:backend)
```

## 주요 기능

### 1. 인자 처리

**전체 인자** - `$ARGUMENTS`:
```markdown
이슈 #$ARGUMENTS 수정하기
# /fix-issue 123 → "이슈 #123 수정하기"
```

**위치 인자** - `$1`, `$2`:
```markdown
PR #$1을 우선순위 $2로 리뷰
# /review 456 high → "PR #456을 우선순위 high로 리뷰"
```

### 2. Bash 실행

`!` 접두사로 셸 명령 실행:

```markdown
---
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

현재 상태: !`git status`
변경사항: !`git diff HEAD`
```

### 3. 파일 참조

`@` 접두사로 파일 내용 포함:

```markdown
@src/utils/helpers.js 검토하기
@$1과 @$2 비교하기
```

## Frontmatter 옵션

| 필드 | 목적 | 필수 |
|------|------|------|
| `description` | /help 설명 | Yes |
| `allowed-tools` | 허용 도구 | No |
| `argument-hint` | 인자 힌트 | No |
| `model` | 사용 모델 | No |

## 생성 워크플로우

```
1. 사용 사례 파악
       ↓
2. 범위 선택 (프로젝트/개인)
       ↓
3. 초기화: scripts/init_command.py <name>
       ↓
4. 편집: description, body 수정
       ↓
5. 테스트: Claude Code에서 실행
```

## 첨부 파일

> [slash-command-creator SKILL.md](/assets/downloads/skills/slash-command-creator/SKILL.html)

## 관련 스킬

- [hook-creator](/posts/hook-creator/) - Hook 생성
- [subagent-creator](/posts/subagent-creator/) - Sub-agent 생성
