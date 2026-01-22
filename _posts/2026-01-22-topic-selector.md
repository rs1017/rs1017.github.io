---
layout: post
title: "Topic Selector Agent - 블로그 주제 선정 에이전트"
date: 2026-01-22 10:50:00 +0900
categories: [AI, Agent]
tags: [claude-code, agent, topic-selection, automation]
---

## 개요

Topic Selector Agent는 AI Skill Factory 블로그의 주제를 선정하고 작업 계획을 수립하는 전문 에이전트입니다.

## 역할

- `.claude/rules/topic-selection.md` 규칙 준수
- 키워드 풀 + 트렌드 기반 주제 선정
- 중복 방지를 위한 기존 스킬 확인
- 작업 계획 수립

## 주제 선정 전략

```
┌─────────────────┐
│  우선순위 1     │  사용자 요청 주제
├─────────────────┤
│  우선순위 2     │  트렌드 기반 (MCP, Multi-Agent 등)
├─────────────────┤
│  우선순위 3     │  키워드 조합
├─────────────────┤
│  우선순위 4     │  기존 스킬 확장
└─────────────────┘
```

## 출력 형식

```
---TOPIC---
name: {english-name}
title: {한글 제목}
category: {카테고리}
difficulty: {난이도}
tags: {tag1}, {tag2}, {tag3}
description: {한 줄 설명}

---WORK_PLAN---
1. {단계 1}
2. {단계 2}
3. {단계 3}

---NOTES---
- {특이사항}
```

## 사용 예시

### 트렌드 기반 선정

입력:
```
새로운 주제를 선정해줘
```

출력:
```
---TOPIC---
name: mcp-server-builder
title: MCP 서버 빌더 스킬
category: Skill
difficulty: intermediate
tags: mcp, server, protocol
description: Model Context Protocol 서버를 쉽게 구축하는 스킬

---WORK_PLAN---
1. MCP 프로토콜 기본 구조 설계
2. 서버 템플릿 SKILL.md 작성
3. 예제 MCP 서버 스크립트 작성
4. 블로그 포스트 작성
5. 실제 동작 검증

---NOTES---
- MCP는 현재 Hot 트렌드 토픽
```

## 허용 도구

- `Glob`: 기존 스킬/에이전트 목록 확인
- `Read`: 규칙 파일 및 기존 스킬 내용 확인
- `Grep`: 중복 키워드 검색

## 첨부 파일

> [topic-selector.md](/assets/downloads/agents/topic-selector.html)

## 관련 에이전트

- [developer](/posts/developer/) - 스킬/포스트 개발
- [reviewer](/posts/reviewer/) - 검토 및 QA
