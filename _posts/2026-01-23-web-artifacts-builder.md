---
layout: post
title: "Web Artifacts Builder - React 웹 아티팩트 생성 스킬"
date: 2026-01-23 10:13:00 +0900
categories: [AI, Skill]
tags: [claude-code, skill, react, frontend, artifacts]
---

## 개요

Web Artifacts Builder는 React, Tailwind CSS, shadcn/ui를 사용하여 정교한 멀티 컴포넌트 claude.ai HTML 아티팩트를 생성하는 도구 모음입니다. 상태 관리, 라우팅, shadcn/ui 컴포넌트가 필요한 복잡한 아티팩트용입니다.

## 기술 스택

- React 18 + TypeScript + Vite
- Parcel (번들링)
- Tailwind CSS + shadcn/ui
- 40+ shadcn/ui 컴포넌트 사전 설치

## 빠른 시작

### Step 1: 프로젝트 초기화

```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

생성되는 구성:
- React + TypeScript (Vite)
- Tailwind CSS 3.4.1 + shadcn/ui 테마 시스템
- 경로 별칭 (`@/`) 설정
- 40+ shadcn/ui 컴포넌트
- Parcel 번들링 설정

### Step 2: 아티팩트 개발

생성된 파일들을 편집하여 아티팩트 구축

### Step 3: 단일 HTML로 번들

```bash
bash scripts/bundle-artifact.sh
```

`bundle.html` 생성 - 모든 JavaScript, CSS, 의존성이 인라인된 자체 완결형 아티팩트

### Step 4: 사용자와 공유

번들된 HTML 파일을 대화에서 공유하여 아티팩트로 표시

### Step 5: 테스트 (선택사항)

필요시 Playwright 또는 Puppeteer로 테스트

## 디자인 가이드라인

**피해야 할 것** (AI 슬롭):
- 과도한 중앙 정렬 레이아웃
- 보라색 그라디언트
- 균일한 둥근 모서리
- Inter 폰트

## 번들링 스크립트 동작

1. 번들링 의존성 설치 (parcel, html-inline)
2. 경로 별칭 지원으로 `.parcelrc` 설정 생성
3. Parcel로 빌드 (소스맵 없음)
4. html-inline으로 모든 자산을 단일 HTML에 인라인

## 첨부 파일

> [web-artifacts-builder SKILL.md](/assets/downloads/skills/web-artifacts-builder/SKILL.md)

## 관련 스킬

- [frontend-design](/posts/frontend-design/) - 프론트엔드 디자인
- [webapp-testing](/posts/webapp-testing/) - 웹앱 테스트
