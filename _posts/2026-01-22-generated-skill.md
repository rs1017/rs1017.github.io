-
---
layout: post
title: "스킬을 만드는 스킬: Generated Skill Creator"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [meta-skill, automation, code-generation, claude-code]
---

## 개요

"스킬을 만들어주는 스킬"이 필요하다면? **Generated Skill Creator**는 사용자 요청을 분석하여 완전한 Claude Code 스킬을 자동으로 생성하는 메타-스킬입니다.

### 해결하는 문제

- 매번 스킬 구조를 처음부터 설계하는 번거로움
- 명명 규칙 및 프론트매터 형식 실수
- 일관성 없는 문서화 및 코드 스타일
- 반복적인 파일 생성 및 폴더 구조 작업

### 핵심 기능

1. **요구사항 분석**: 사용자 입력에서 핵심 기능 자동 추출
2. **스킬 설계**: 필요한 도구, 에이전트, 스크립트 결정
3. **코드 생성**: 규칙을 준수하는 완전한 스킬 파일 생성
4. **문서화**: 블로그 포스트 초안까지 자동 생성

## 스킬 구조

```
.claude/skills/generated-skill/
└── SKILL.md                    # 메타-스킬 정의 및 사용 지침
```

이 스킬은 단일 파일로 구성되지만, 실행 시 다음 파일들을 생성합니다:

```
.claude/skills/{새-스킬-이름}/
├── SKILL.md                    # 생성된 스킬 정의
├── scripts/                    # 필요 시 스크립트
├── references/                 # 필요 시 참조 문서
└── assets/                     # 필요 시 템플릿 등

assets/downloads/skills/{새-스킬-이름}.zip  # 블로그 배포용

_posts/YYYY-MM-DD-새-스킬-포스트.md         # 문서화 포스트
```

## 사용 방법

### 기본 사용

```
User: "Git 커밋 메시지 컨벤션을 검증하는 스킬 만들어줘"

Generated Skill Creator 실행:
→ 분석: Git 작업, 커밋 메시지 검증, 규칙 체크
→ 설계: Bash(git log), Grep(패턴 매칭), Python 스크립트
→ 생성: git-commit-validator 스킬 완성
→ 문서화: 블로그 포스트 초안 생성
```

### 고급 사용

복잡한 워크플로우도 처리 가능:

```
User: "YouTube 자막 추출 → 번역 → 요약 → 블로그 포스트 생성하는 스킬"

Generated Skill Creator 실행:
→ 분석: 다단계 파이프라인, 외부 API 호출, 파일 변환
→ 설계: Python 스크립트, API 래퍼, 템플릿 엔진
→ 생성: youtube-content-pipeline 스킬
→ 검증: 의존성 체크, 실행 가능성 확인
```

## 생성 프로세스

### 1단계: 요구사항 수집
- 사용자 입력 분석
- 기능 키워드 추출
- 카테고리 분류 (Skill/Agent/Hook/Command)
- 난이도 평가 (beginner/intermediate/advanced)

### 2단계: 스킬 설계
- 필요한 Claude Code 도구 식별
- 서브에이전트 필요 여부 판단
- 스크립트 언어 및 구조 결정
- 파일 구조 설계

### 3단계: 코드 생성
- SKILL.md 프론트매터 작성
- 본문 섹션 작성 (사용 시점, 기능, 사용 방법)
- 스크립트 코드 생성
- 참조 문서 및 템플릿 생성

### 4단계: 검증
- 명명 규칙 준수 확인 (영문 소문자 + 하이픈)
- 필수 프론트매터 필드 확인
- 금지어 사용 여부 체크
- 실행 가능성 검증

### 5단계: 문서화
- 블로그 포스트 초안 생성
- 코드 블록 및 사용 예시 포함
- 다운로드 링크 생성

## 전체 코드

### SKILL.md

```markdown
---
name: generated-skill
description: 사용자 요구사항에 맞춰 Claude Code 스킬을 자동으로 생성하는 메타-스킬
version: 1.0.0
author: AI Skill Factory
---

# Generated Skill Creator

사용자가 요청한 기능을 분석하여 완전한 Claude Code 스킬을 자동으로 생성하는 메타-스킬입니다.

## 사용 시점

다음과 같은 상황에서 이 스킬을 사용하세요:

1. 사용자가 "~하는 스킬 만들어줘" 요청 시
2. 기존 스킬을 확장하거나 변형해야 할 때
3. 특정 워크플로우를 자동화하는 스킬이 필요할 때
4. 반복적인 작업을 스킬로 패키징해야 할 때

## 기능

- **요구사항 분석**: 사용자 요청에서 핵심 기능 추출
- **스킬 구조 설계**: 필요한 도구, 에이전트, 스크립트 결정
- **코드 생성**: SKILL.md 및 관련 파일 자동 작성
- **문서화**: 블로그 포스트 형식 문서 생성
- **검증**: 명명 규칙 및 구조 검증

## 생성 규칙

### 명명 규칙
- **필수**: 영문 소문자 + 하이픈만 사용
- **금지**: 한글, 공백, CamelCase, 언더스코어, 특수문자

### 프론트매터 필수 필드
```yaml
---
name: skill-name-here
description: 한 줄 설명 (트리거 조건 포함)
version: 1.0.0
author: AI Skill Factory
---
```

### 검증 체크리스트

- [ ] 이름이 영문 소문자 + 하이픈 형식
- [ ] SKILL.md에 필수 프론트매터 포함
- [ ] description에 트리거 조건 명시
- [ ] 실행 가능한 코드 포함
- [ ] 금지어 미사용
- [ ] 카테고리 명확
- [ ] 난이도 지정
```

## 사용 예시

### 예시 1: 간단한 스킬

**입력**:
```
"README 파일을 분석해서 누락된 섹션을 찾는 스킬"
```

**생성 결과**:
- 이름: `readme-section-checker`
- 카테고리: Skill
- 난이도: beginner
- 도구: Read, Grep
- 파일: SKILL.md, scripts/check.py

### 예시 2: 복잡한 파이프라인

**입력**:
```
"코드 리뷰 코멘트를 수집 → 분석 → 개선 제안 생성하는 스킬"
```

**생성 결과**:
- 이름: `code-review-analyzer`
- 카테고리: Skill
- 난이도: advanced
- 도구: Bash(gh api), Python(분석), Grep(패턴)
- 파일: SKILL.md, scripts/collect.py, scripts/analyze.py, scripts/suggest.py

## 제한사항

1. **외부 의존성**: 특정 유료 서비스 의존 금지 (Anthropic API 제외)
2. **추상성**: 실행 불가능한 추상적 스킬 금지
3. **중복성**: 기존 스킬과 80% 이상 유사 시 경고
4. **검증 필요**: 생성된 코드는 반드시 실행 테스트 필요

## 확장 가능성

이 메타-스킬은 다음과 같이 발전 가능합니다:

1. **템플릿 라이브러리**: 자주 사용되는 패턴 템플릿화
2. **의존성 자동 탐지**: 필요한 Python 패키지 requirements.txt 생성
3. **테스트 자동 생성**: 스킬 검증용 테스트 케이스 생성
4. **버전 관리**: 스킬 업데이트 및 변경 이력 추적
5. **AI 학습**: 사용 패턴 학습으로 생성 품질 향상

## 다운로드

> [generated-skill.zip](/assets/downloads/skills/generated-skill.zip)

## 관련 스킬

- **skill-creator**: 대화형 스킬 생성 가이드 (빌트인)
- **subagent-creator**: 서브에이전트 생성 (빌트인)
- **hook-creator**: Hook 생성 (빌트인)
- **slash-command-creator**: Slash Command 생성 (빌트인)