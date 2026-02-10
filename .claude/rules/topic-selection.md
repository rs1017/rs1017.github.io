# 블로그 주제 선택 규칙

낙현아빠의 개발 블로그 포스트 주제를 선정할 때 따라야 하는 규칙입니다.

## 카테고리

| 카테고리 | 설명 | 예시 주제 |
|----------|------|----------|
| **Server** | 게임 서버 아키텍처, 네트워크, 동시성 | MMORPG 서버 구조, 소켓 프로그래밍 |
| **AI** | LLM, 프롬프트 엔지니어링, AI 도구 활용 | Claude Code 활용, RAG 구현 |
| **Database** | Redis, MySQL, MongoDB, 쿼리 최적화 | Redis Cluster, 인덱스 최적화 |
| **DevOps** | CI/CD, Docker, Kubernetes, 모니터링 | Jenkins 파이프라인, Grafana |
| **Architecture** | 설계 패턴, MSA, 분산 시스템 | 이벤트 소싱, CQRS |
| **Career** | 개발자 성장, 팀 관리, 커리어 | 코드 리뷰 문화, 기술 면접 |
| **Claude Code** | Claude Code 스킬, 에이전트, 훅, 커맨드 | MCP 서버, Hook 설정 |

## 난이도 레벨

| 레벨 | 기준 |
|------|------|
| **beginner** | 10분 내 이해 가능 |
| **intermediate** | 30분 내 적용 가능 |
| **advanced** | 아키텍처 레벨 |

## 주제 선정 전략

### 1. 실무 경험 기반
16년차 게임 서버 개발자의 실무 경험에서 주제를 도출

### 2. 트렌드 기반
트렌드 토픽 섹션 참조

### 3. 키워드 조합
키워드 풀에서 조합하여 새로운 주제 생성

### 4. 시리즈 확장
기존 포스트의 후속편이나 심화 내용

## 키워드 풀

### 게임 서버
MMORPG, 실시간, 동시접속, 매칭, 로비, 채팅, 인벤토리, 전투, 랭킹, 세션, 패킷, 직렬화, 프로토콜, 소켓, TCP, UDP, 게임 루프, 틱레이트

### 서버 아키텍처
마이크로서비스, 모놀리식, 이벤트 소싱, CQRS, 메시지 큐, RPC, gRPC, REST, GraphQL, 로드 밸런싱, 오토스케일링, 서비스 메시

### 데이터베이스
Redis, MySQL, MongoDB, PostgreSQL, 인덱스, 쿼리 최적화, 샤딩, 레플리카, 캐싱, 트랜잭션, 락, 데드락

### AI/LLM
Claude, GPT, 프롬프트, RAG, 임베딩, 벡터DB, 파인튜닝, 에이전트, MCP, Function Calling, 토큰, 컨텍스트

### DevOps/인프라
Docker, Kubernetes, Jenkins, GitHub Actions, Terraform, AWS, GCP, 모니터링, 로깅, Grafana, Prometheus, ELK

### 프로그래밍
C++, C#, Python, Go, Rust, 디자인 패턴, SOLID, 리팩토링, 테스트, TDD, 코드 리뷰, 성능 최적화, 메모리 관리

### 개발 문화
애자일, 스크럼, 코드 리뷰, 기술 면접, 팀 빌딩, 온보딩, 회고, 기술 부채, 레거시

## 트렌드 토픽

### Hot (높은 관련성)
- AI/LLM을 게임 서버에 활용하기
- Claude Code로 개발 생산성 높이기
- Redis 최신 기능 활용 (Redis Stack, Search)
- 서버리스 게임 백엔드
- 실시간 데이터 파이프라인

### Rising (떠오르는)
- AI 에이전트 시스템
- 벡터 데이터베이스
- WebSocket vs gRPC 스트리밍
- 옵저버빌리티 (Observability)
- Platform Engineering

## 제외 조건

다음 주제는 선정하지 않습니다:

1. 이미 존재하는 포스트와 80% 이상 유사
2. 실행 불가능하거나 검증 어려운 내용
3. 특정 유료 서비스에만 의존 (범용적이지 않은 경우)
4. 금지어 포함: "자동 생성", "AI Pipeline"

## 출력 형식

```yaml
title: "한글 블로그 포스트 제목"
category: Server | AI | Database | DevOps | Architecture | Career | Claude Code
difficulty: beginner | intermediate | advanced
tags:
  - tag1
  - tag2
description: "한 줄 설명"
```
