---
layout: post
title: "Developer Agent - 스킬 개발 에이전트"
date: 2026-01-22 11:00:00 +0900
categories: [AI, Agent]
tags: [claude-code, agent, developer, skill-creation]
---

## 개요

Developer Agent는 Topic Selector가 선정한 주제를 바탕으로 실제 스킬 파일과 블로그 포스트를 작성하는 개발 전문 에이전트입니다.

## 역할

- Topic Selector로부터 주제 정보 수신
- 카테고리별 적절한 위치에 파일 생성
- SKILL.md 및 블로그 포스트 작성
- 실행 가능한 예제 코드 작성

## 카테고리별 저장 위치

| 카테고리 | 저장 위치 |
|---------|----------|
| Skill | `.claude/skills/{name}/SKILL.md` |
| Agent | `.claude/agents/{name}.md` |
| Hook | `.claude/hooks/{name}.md` |
| Command | `.claude/commands/{name}.md` |
| Script | `.claude/scripts/{name}.py` |
| Workflow | `.claude/workflows/{name}.md` |

## SKILL.md 작성 규칙

```markdown
---
name: {skill-name}
description: {한 줄 설명}
version: 1.0.0
author: AI Skill Factory
---

# {스킬 제목}

## 개요
{스킬이 해결하는 문제와 목적}

## 사용법
{실행 방법 및 명령어}

## 구성
{파일 구조 및 각 파일 설명}

## 예제
{실제 사용 예제 코드}

## 참고
{관련 문서 및 링크}
```

## 블로그 포스트 구조

```markdown
---
layout: post
title: "{한글 제목}"
date: {YYYY-MM-DD HH:MM:SS +0900}
categories: [AI, {카테고리}]
tags: [{태그들}]
---

## 개요
## 폴더 구조
## 동작 흐름
## 구현
## 전체 코드
## 첨부 파일
## 관련 스킬
```

## 코드 품질 기준

| 기준 | 설명 |
|------|------|
| 실행 가능 | 복사-붙여넣기로 바로 실행 |
| 주석 포함 | 핵심 로직에 한글 주석 |
| 에러 처리 | 기본적인 예외 처리 포함 |
| 의존성 명시 | 필요한 패키지/설치 방법 안내 |

## 출력 형식

```
---SKILL.md---
(SKILL.md 전체 내용)

---POST---
(블로그 포스트 전체 내용)

---FILES---
- {생성된 파일 경로 1}
- {생성된 파일 경로 2}
```

## 허용 도구

- `Write`: 스킬 파일 및 포스트 작성
- `Read`: 기존 스킬 참조
- `Bash`: 디렉토리 생성

## 첨부 파일

> [developer.md](/assets/downloads/agents/developer.html)

## 관련 에이전트

- [topic-selector](/posts/topic-selector/) - 주제 선정
- [reviewer](/posts/reviewer/) - 검토 및 QA
