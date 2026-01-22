# 블로그 주제 선택 규칙

AI Skill Factory 블로그 포스트 주제를 선정할 때 따라야 하는 규칙입니다.

## 카테고리

| 카테고리 | 설명 | 저장 위치 |
|----------|------|----------|
| **Skill** | 특정 작업 수행 스킬 | `.claude/skills/{name}/` |
| **Agent** | 서브에이전트 정의 | `.claude/agents/{name}.md` |
| **Hook** | Claude Code 훅 | `.claude/hooks/{name}.md` |
| **Command** | Slash Command | `.claude/commands/{name}.md` |

## 이름 규칙 (필수)

### 영문 lowercase + hyphen

모든 이름은 **영문 소문자와 하이픈**만 사용합니다.

| 유형 | 예시 |
|------|------|
| Skill | `git-commit-analyzer`, `pdf-summarizer` |
| Agent | `code-reviewer`, `test-runner` |
| Hook | `pre-commit-lint`, `post-edit-format` |
| Command | `commit`, `review-pr`, `summarize` |

**금지**: 한글, 공백, 특수문자, CamelCase, 언더스코어

### 변환 예시

| 한글 주제 | 영문 이름 |
|----------|----------|
| Git 커밋 분석 스킬 | `git-commit-analyzer` |
| PDF 자동 요약 | `pdf-auto-summarizer` |
| 유튜브 자막 추출 | `youtube-transcript-extractor` |

## 난이도 레벨

| 레벨 | 기준 |
|------|------|
| **beginner** | 10분 내 이해 가능 |
| **intermediate** | 30분 내 적용 가능 |
| **advanced** | 아키텍처 레벨 |

## 주제 선정 전략

### 1. 키워드 조합
키워드 풀에서 조합하여 새로운 스킬 주제 생성

### 2. 트렌드 기반
트렌드 토픽 섹션 참조

### 3. 스킬 확장
기존 스킬을 확장하거나 보완

## 키워드 풀

### 개발
Git, API, 코드, 리팩토링, 디버깅, 테스트, CI/CD, 배포, 모니터링, 로깅, 성능, 보안, 리뷰

### 문서
PDF, 문서, 보고서, 발표자료, PPT, 엑셀, 마크다운, README, Wiki, 매뉴얼, 가이드

### 데이터
데이터, 분석, 시각화, 차트, 그래프, 통계, CSV, JSON, XML, 변환, 파싱, 크롤링

### 미디어
이미지, 사진, 썸네일, 배너, 아이콘, 로고, 영상, 유튜브, 숏츠, 오디오, 팟캐스트, 자막, 번역

### 창작
글쓰기, 소설, 스토리, 시나리오, 블로그, 뉴스레터, 카피라이팅, 광고, 마케팅, 디자인, UI, UX

### AI 도구
프롬프트, 챗봇, 에이전트, 자동화, 생성, 요약, 번역, 교정, 검수, 추천, 분류

### 생산성
일정, 캘린더, 할일, 태스크, 노트, 메모, 이메일, 슬랙, 노션, 트렐로

### Claude Code
MCP, Hook, Command, Slash, Claude, Anthropic, 세션, 컨텍스트, 도구, 확장

## 트렌드 토픽

### Hot (높은 관련성)
- MCP (Model Context Protocol) → Agent
- Structured Output Parsing → Skill
- Claude Code Extensions → Skill
- Multi-Agent Systems → Agent
- LLM Tool Use Patterns → Agent

### Rising (떠오르는)
- Structured Output
- Memory
- RAG
- Function Calling
- Streaming

## 제외 조건

다음 주제는 선정하지 않습니다:

1. 이미 존재하는 스킬과 80% 이상 유사
2. 실행 불가능하거나 검증 어려움
3. 특정 유료 서비스에 의존 (Anthropic API 제외)
4. 금지어 포함: "자동 생성", "AI Pipeline"

## 출력 형식

```yaml
name: skill-name-in-english
title: "한글 블로그 포스트 제목"
category: Skill | Agent | Hook | Command
difficulty: beginner | intermediate | advanced
tags:
  - tag1
  - tag2
description: "한 줄 설명"
```
