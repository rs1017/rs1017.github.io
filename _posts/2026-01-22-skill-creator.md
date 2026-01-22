---
layout: post
title: "Claude Code Skill Creator - 스킬 생성 가이드"
date: 2026-01-22 10:10:00 +0900
categories: [AI, Skill]
tags: [claude-code, skill, automation, guide]
---

## 개요

Skill Creator는 Claude Code 스킬을 효과적으로 생성하기 위한 가이드입니다. 스킬은 Claude의 기능을 확장하는 모듈형 패키지입니다.

## 스킬이란?

스킬은 Claude를 특정 도메인의 전문가로 변환시키는 "온보딩 가이드"입니다:

1. **전문화된 워크플로우** - 특정 도메인의 다단계 절차
2. **도구 통합** - 특정 파일 형식이나 API 작업 지침
3. **도메인 전문 지식** - 회사별 지식, 스키마, 비즈니스 로직
4. **번들 리소스** - 스크립트, 참조 문서, 에셋

## 폴더 구조

```
skill-name/
├── SKILL.md (필수)
│   ├── YAML frontmatter (name, description)
│   └── Markdown 지침
└── Bundled Resources (선택)
    ├── scripts/          - 실행 코드
    ├── references/       - 참조 문서
    └── assets/           - 출력용 파일
```

## 핵심 원칙

### 1. 간결함이 핵심

컨텍스트 윈도우는 공공재입니다. Claude가 이미 알고 있는 것은 설명하지 마세요.

### 2. 적절한 자유도 설정

| 자유도 | 사용 시점 |
|--------|----------|
| 높음 | 여러 접근법이 유효할 때 |
| 중간 | 선호 패턴이 있지만 변형 가능할 때 |
| 낮음 | 작업이 민감하고 일관성이 중요할 때 |

### 3. 점진적 공개

```
1단계: 메타데이터 (항상 로드) ~100 단어
2단계: SKILL.md 본문 (트리거 시) <5k 단어
3단계: 번들 리소스 (필요 시) 무제한
```

## 스킬 생성 프로세스

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 1. 이해     │───▶│ 2. 계획     │───▶│ 3. 초기화   │
│ (예제 수집) │    │ (리소스)    │    │ (스크립트)  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                                     │
       ▼                                     ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 6. 반복     │◀───│ 5. 패키징   │◀───│ 4. 편집     │
│ (개선)      │    │ (검증)      │    │ (구현)      │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 초기화 명령

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

## 첨부 파일

> [skill-creator SKILL.md](/assets/downloads/skills/skill-creator/SKILL.html)

## 관련 스킬

- [hook-creator](/posts/hook-creator/) - Hook 생성
- [slash-command-creator](/posts/slash-command-creator/) - Slash Command 생성
