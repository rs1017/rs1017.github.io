---
layout: post
title: "Claude Code Sub-agent Creator - 서브에이전트 생성"
date: 2026-01-22 10:30:00 +0900
categories: [AI, Agent]
tags: [claude-code, subagent, automation, multi-agent]
---

## 개요

Sub-agent Creator는 Claude Code에서 특정 작업을 처리하는 전문화된 AI 서브에이전트를 생성하는 스킬입니다.

## 서브에이전트 파일 형식

서브에이전트는 YAML frontmatter가 포함된 Markdown 파일입니다:

```markdown
---
name: subagent-name
description: 사용 시점 설명 ("use proactively" 포함 시 자동 위임)
tools: Tool1, Tool2, Tool3  # 선택 - 생략 시 전체 상속
model: sonnet               # 선택 - sonnet/opus/haiku/inherit
permissionMode: default     # 선택
skills: skill1, skill2      # 선택 - 자동 로드 스킬
---

시스템 프롬프트가 여기에 들어갑니다.
역할, 책임, 행동을 정의합니다.
```

## 저장 위치

| 범위 | 경로 | 우선순위 |
|------|------|----------|
| 프로젝트 | `.claude/agents/` | 높음 |
| 사용자 | `~/.claude/agents/` | 낮음 |

## 설정 필드

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | Yes | 소문자 + 하이픈 |
| `description` | Yes | 목적 및 사용 시점 |
| `tools` | No | 쉼표 구분 도구 목록 |
| `model` | No | sonnet/opus/haiku/inherit |
| `permissionMode` | No | default/acceptEdits/bypassPermissions/plan |

## Description 작성 팁

```yaml
# Good - 구체적 트리거
description: 코드 리뷰 전문가. 코드 작성/수정 후 PROACTIVELY 사용.

# Good - 명확한 사용 사례
description: 에러, 테스트 실패, 예상치 못한 동작을 위한 디버깅 전문가.

# Bad - 너무 모호
description: 코드 도움
```

## 도구 선택 가이드

| 작업 유형 | 도구 |
|----------|------|
| 읽기 전용 | Read, Grep, Glob, Bash |
| 코드 수정 | Read, Write, Edit, Grep, Glob, Bash |
| 전체 접근 | tools 필드 생략 |

## 예제: 코드 리뷰어

```markdown
---
name: code-reviewer
description: 코드 품질과 보안을 리뷰합니다. 코드 변경 후 proactively 사용.
tools: Read, Grep, Glob, Bash
model: inherit
---

당신은 시니어 코드 리뷰어입니다.

호출 시:
1. git diff로 변경사항 확인
2. 수정된 파일 리뷰
3. 우선순위별 이슈 보고

집중 영역:
- 코드 가독성
- 보안 취약점
- 에러 처리
- 모범 사례
```

## 생성 워크플로우

```
1. 요구사항 수집
       ↓
2. 범위 선택 (.claude/agents/ 또는 ~/.claude/agents/)
       ↓
3. 설정 정의 (name, description, tools, model)
       ↓
4. 시스템 프롬프트 작성
       ↓
5. 파일 생성
```

## 첨부 파일

> [subagent-creator SKILL.md](/assets/downloads/skills/subagent-creator/SKILL.html)

## 관련 스킬

- [skill-creator](/posts/skill-creator/) - Skill 생성
- [hook-creator](/posts/hook-creator/) - Hook 생성
