---
layout: post
title: "MCP Builder - MCP 서버 개발 가이드 스킬"
date: 2026-01-23 10:07:00 +0900
categories: [AI, Skill]
tags: [claude-code, skill, mcp, server, api, integration]
---

## 개요

MCP Builder는 LLM이 외부 서비스와 상호작용할 수 있게 하는 고품질 MCP(Model Context Protocol) 서버를 구축하기 위한 가이드 스킬입니다.

## 4단계 프로세스

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ 1. 연구/계획  │───▶│ 2. 구현       │───▶│ 3. 리뷰/테스트│───▶│ 4. 평가 생성  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

## Phase 1: 연구 및 계획

### 1.1 현대적 MCP 디자인 이해

- API 커버리지 vs 워크플로우 도구 밸런스
- 명확하고 발견 가능한 도구 네이밍
- 실행 가능한 에러 메시지

### 1.2 MCP 프로토콜 문서 학습

```
https://modelcontextprotocol.io/sitemap.xml
```

### 1.3 프레임워크 선택

- **권장**: TypeScript (고품질 SDK 지원)
- **Transport**: Streamable HTTP (원격) / stdio (로컬)

## Phase 2: 구현

### 도구 구현 체크리스트

- Zod(TS) / Pydantic(Python)으로 입력 스키마
- outputSchema로 출력 스키마 정의
- 도구 설명 (기능, 파라미터, 반환 타입)
- 어노테이션 (readOnlyHint, destructiveHint 등)

## Phase 3: 리뷰 및 테스트

```bash
# TypeScript 빌드 검증
npm run build

# MCP Inspector로 테스트
npx @modelcontextprotocol/inspector
```

## Phase 4: 평가 생성

10개의 복잡하고 현실적인 질문으로 평가 세트 생성

## 첨부 파일

> [mcp-builder SKILL.md](/assets/downloads/skills/mcp-builder/SKILL.md)

## 관련 스킬

- [skill-creator](/posts/skill-creator/) - 스킬 생성
- [hook-creator](/posts/hook-creator/) - Hook 생성
