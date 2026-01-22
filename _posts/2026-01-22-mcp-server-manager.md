-
---
layout: post
title: "MCP 서버 통합 관리 스킬"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [mcp, server, management, monitoring, claude-code]
---

## 개요

Claude Code에서 MCP(Model Context Protocol) 서버를 사용하다 보면, 여러 서버를 동시에 관리해야 하는 상황이 생깁니다. 어떤 서버가 연결되어 있는지, 각 서버가 어떤 리소스를 제공하는지, 새로운 서버를 추가하려면 어떻게 해야 하는지 등 관리 포인트가 많아집니다.

**MCP Server Manager**는 이러한 MCP 서버 관리 작업을 체계적으로 수행하는 스킬입니다. 서버 연결 상태 확인부터 리소스 탐색, 설정 관리까지 원스톱으로 처리합니다.

## 스킬 구조

```
.claude/skills/mcp-server-manager/
├── SKILL.md              # 스킬 정의 및 사용 가이드
└── scripts/
    └── server_check.py   # 서버 상태 체크 헬퍼
```

## 주요 기능

### 1. 서버 상태 모니터링

연결된 모든 MCP 서버의 상태를 한눈에 확인할 수 있습니다.

```
사용자: MCP 서버 상태 보여줘
```

**출력 예시:**
- 서버별 연결 상태 (✅ 연결됨 / ⚠️ 오프라인)
- 제공 리소스 개수
- 마지막 활동 시간

### 2. 리소스 탐색

특정 MCP 서버가 제공하는 모든 리소스를 탐색하고, 내용을 미리 볼 수 있습니다.

```
사용자: serena 서버의 리소스를 확인해줘
```

**제공 정보:**
- 리소스 URI
- 리소스 타입 (text, json, markdown 등)
- 설명 및 메타데이터
- 내용 미리보기

### 3. 서버 설정 관리

MCP 서버 추가, 제거, 수정 작업을 대화형으로 진행합니다.

```
사용자: 새 MCP 서버를 추가하고 싶어
```

**처리 과정:**
1. 서버 이름 입력
2. 실행 커맨드 설정
3. 환경 변수 구성 (선택)
4. 설정 파일 자동 업데이트

## 사용 예시

### Case 1: 서버 상태 일괄 체크

프로젝트 시작 전, 필요한 MCP 서버가 모두 연결되어 있는지 확인합니다.

```
사용자: MCP 서버들 연결 상태 확인해줘

Claude: 
✅ serena - 15개 리소스
✅ filesystem - 8개 리소스
⚠️ database - 연결 실패 (포트 충돌 가능성)
```

### Case 2: 새 서버 리소스 탐색

처음 사용하는 MCP 서버의 기능을 파악합니다.

```
사용자: weather 서버가 뭘 제공하는지 보여줘

Claude:
📄 weather://current (현재 날씨)
📄 weather://forecast (일기예보)
📄 weather://alerts (기상특보)
```

### Case 3: 서버 설정 백업

현재 MCP 설정을 백업 파일로 저장합니다.

```
사용자: MCP 설정 백업해줘

Claude: 
✅ 설정 파일 백업 완료
   위치: ~/.claude/mcp-config-backup-2026-01-22.json
```

## 기술적 특징

### MCP 도구 활용

- `ListMcpResourcesTool`: 서버 및 리소스 목록 조회
- `ReadMcpResourceTool`: 특정 리소스 내용 읽기

### 설정 파일 관리

- JSON/YAML 파싱 및 유효성 검사
- 안전한 설정 파일 수정 (백업 자동 생성)
- 크로스 플랫폼 경로 처리

### 에러 핸들링

- 서버 연결 실패 시 원인 분석
- 설정 오류 시 구체적인 수정 가이드 제공
- Rollback 메커니즘 (설정 변경 실패 시 복구)

## 활용 시나리오

### 개발 환경 셋업

새로운 개발 환경에서 필요한 MCP 서버를 빠르게 구성합니다.

### 트러블슈팅

서버 연결 문제 발생 시 빠르게 원인을 파악하고 해결합니다.

### 리소스 디스커버리

사용 가능한 MCP 리소스를 탐색하고, 프로젝트에 활용할 도구를 찾습니다.

### 팀 협업

팀원들이 동일한 MCP 서버 설정을 공유하고 동기화합니다.

## 확장 아이디어

- **Health Check 자동화**: 주기적으로 서버 상태 모니터링
- **Performance Metrics**: 서버별 응답 시간, 호출 횟수 통계
- **Configuration Templates**: 자주 사용하는 서버 설정 템플릿 제공
- **Server Marketplace**: 유용한 MCP 서버 추천 및 자동 설치

## 파일 위치

| 구분 | 경로 |
|------|------|
| 스킬 정의 | `/assets/downloads/skills/mcp-server-manager/SKILL.md` |
| 설치 위치 | `~/.claude/skills/mcp-server-manager/` |

## 관련 게시글

- [skill-creator](/posts/skill-creator/) - 스킬 생성 가이드