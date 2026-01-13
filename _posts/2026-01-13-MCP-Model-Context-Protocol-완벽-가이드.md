---
title: MCP(Model Context Protocol) 완벽 가이드 - AI 에이전트의 새로운 표준
author: naksupapa
date: 2026-01-13 13:00:00 +0900
categories: [AI, Protocol]
tags: [mcp, model-context-protocol, anthropic, ai-agent, claude, openai]
---

# MCP(Model Context Protocol) 완벽 가이드

> "작은 오픈소스 실험이 12개월도 안 되어 사실상의 표준이 되었다는 것을 상상하기 어렵습니다."

MCP는 AI 에이전트 생태계에서 **가장 빠르게 채택된 표준**이 되었습니다.

## MCP란?

**Model Context Protocol (MCP)**은 2024년 11월 Anthropic이 공개한 오픈 표준으로, AI 시스템(특히 LLM)이 외부 도구, 시스템, 데이터 소스와 **표준화된 방식으로 통합**할 수 있게 합니다.

### 핵심 기능

```
MCP가 제공하는 기능:
- 파일 읽기 (File Reading)
- 함수 실행 (Function Execution)
- 컨텍스트 프롬프트 처리 (Contextual Prompts)
- 범용 인터페이스 (Universal Interface)
```

### MCP 이전 vs 이후

| 항목 | MCP 이전 | MCP 이후 |
|------|----------|----------|
| 통합 방식 | 각 도구별 커스텀 구현 | 표준화된 프로토콜 |
| 개발 비용 | 높음 | 낮음 |
| 호환성 | 제한적 | 범용적 |
| 에이전트 능력 | 텍스트 생성 중심 | 실제 행동 가능 |

## 주요 발전 과정 (타임라인)

### 2024년 11월 - 출시
Anthropic이 MCP를 오픈소스로 공개

### 2025년 3월 - OpenAI 채택
OpenAI가 공식적으로 MCP를 채택하고 ChatGPT 데스크톱 앱을 포함한 전 제품에 통합

### 2025년 5월 - Microsoft & GitHub 참여
Build 2025 컨퍼런스에서 GitHub과 Microsoft가 MCP 운영위원회 합류 발표. Windows 11의 MCP 지원 프리뷰 공개

### 2025년 11월 - 1주년 스펙 릴리스
1주년을 맞아 새로운 MCP 사양 버전 출시

### 2025년 12월 - Linux Foundation 이관
Anthropic이 MCP를 **Agentic AI Foundation (AAIF)**에 기부

## Linux Foundation 이관

MCP는 현재 Linux Foundation 산하 **Agentic AI Foundation**에서 관리됩니다.

### 공동 설립 기업

| 창립 멤버 | 지원 기업 |
|-----------|-----------|
| Anthropic | Google |
| Block | Microsoft |
| OpenAI | AWS |
|  | Cloudflare |
|  | Bloomberg |

### AAIF의 다른 프로젝트

- **goose** (Block): AI 에이전트 프레임워크
- **AGENTS.md** (OpenAI): 에이전트 명세 표준

## 2025년 11월 스펙 주요 기능

1주년 릴리스에서 추가된 기능들:

### 새로운 기능

| 기능 | 설명 |
|------|------|
| **비동기 작업** | 장기 실행 작업 지원 |
| **상태 비저장** | Stateless 아키텍처 |
| **서버 ID** | 서버 식별 및 인증 |
| **공식 확장** | 표준화된 확장 메커니즘 |

## 생태계 현황

### SDK 및 다운로드

| 지표 | 수치 |
|------|------|
| 월간 SDK 다운로드 (Python + TypeScript) | **9,700만+** |
| Claude 공식 커넥터 | 75개+ |
| 활성 MCP 서버 수 | 수천 개 |

### 지원 언어

공식 SDK가 모든 주요 프로그래밍 언어에서 제공됩니다:

- Python
- TypeScript/JavaScript
- Go
- Rust
- Java
- 등

## MCP 아키텍처

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│  MCP Server │────▶│   Tools/    │
│  (Claude,   │◀────│             │◀────│   Data      │
│   GPT 등)   │     │             │     │   Sources   │
└─────────────┘     └─────────────┘     └─────────────┘
      │                    │
      │    MCP Protocol    │
      └────────────────────┘
```

### 구성 요소

1. **Client**: AI 모델 (Claude, GPT 등)
2. **MCP Server**: 프로토콜 처리 및 도구 연결
3. **Tools/Data Sources**: 실제 기능 제공 (파일 시스템, API, DB 등)

## 간단한 MCP 서버 예시

```python
from mcp import Server, Tool

server = Server("my-mcp-server")

@server.tool("read_file")
async def read_file(path: str) -> str:
    """파일 내용을 읽습니다."""
    with open(path, 'r') as f:
        return f.read()

@server.tool("search_web")
async def search_web(query: str) -> list:
    """웹 검색을 수행합니다."""
    # 검색 로직 구현
    return results

if __name__ == "__main__":
    server.run()
```

## 보안 고려사항

2025년 4월 보안 연구자들이 MCP의 여러 보안 이슈를 발표했습니다:

### 주요 보안 위험

| 위험 | 설명 |
|------|------|
| **프롬프트 인젝션** | 악의적 프롬프트를 통한 공격 |
| **도구 권한** | 도구 조합 시 파일 유출 가능성 |
| **유사 도구** | 신뢰된 도구를 가장한 악성 도구 |

### 권장 보안 대책

```
1. 도구 권한 최소화 원칙 적용
2. 입력 값 검증 철저히
3. 신뢰할 수 있는 MCP 서버만 사용
4. 정기적인 보안 감사
```

## MCP vs 다른 프로토콜

| 프로토콜 | 개발사 | 초점 |
|----------|--------|------|
| **MCP** | Anthropic | 에이전트 ↔ 도구 |
| **A2A** | Google | 에이전트 ↔ 에이전트 |
| **OpenAPI** | 커뮤니티 | API 명세 |

## 시작하기

### 1. SDK 설치

```bash
# Python
pip install mcp

# TypeScript
npm install @modelcontextprotocol/sdk
```

### 2. 공식 리소스

- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [Anthropic MCP 강좌](https://anthropic.skilljar.com/introduction-to-model-context-protocol)
- [GitHub 저장소](https://github.com/modelcontextprotocol)

## 결론

MCP는 AI 에이전트 생태계의 **USB**와 같은 역할을 합니다. 마치 USB가 다양한 장치를 컴퓨터에 연결하는 표준이 된 것처럼, MCP는 AI 모델과 외부 세계를 연결하는 표준이 되어가고 있습니다.

### 핵심 포인트

1. **업계 표준으로 자리매김**: OpenAI, Google, Microsoft 모두 채택
2. **오픈소스 & 중립적 관리**: Linux Foundation 산하
3. **활발한 생태계**: 수천 개의 MCP 서버, 수천만 SDK 다운로드
4. **보안 주의 필요**: 알려진 취약점에 대한 대응 필요

AI 에이전트를 개발하거나 활용할 계획이라면, MCP는 반드시 알아야 할 핵심 기술입니다.

---

## 참고 자료

- [Anthropic - Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [MCP 공식 사양](https://modelcontextprotocol.io/specification/2025-11-25)
- [Wikipedia - Model Context Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- [The New Stack - Why the Model Context Protocol Won](https://thenewstack.io/why-the-model-context-protocol-won/)
