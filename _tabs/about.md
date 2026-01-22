---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

# AI Skill Factory

> Claude Code 스킬 자동 생성 플랫폼

---

## 프로젝트 목표

**개발자의 반복 작업을 AI로 자동화하여 생산성을 극대화한다.**

이 블로그는 Claude Code를 활용한 실용적인 스킬들을 자동 생성하고 공유하는 플랫폼입니다.

---

## 주제 키포인트

| 카테고리 | 설명 |
|---------|------|
| **Workflow** | CI/CD, 코드 리뷰, 문서 생성 등 개발 워크플로우 자동화 |
| **Agent** | 멀티에이전트 설계, MCP 서버, 도구 사용 패턴 |
| **Skill** | API 통합, 데이터 처리, 파일 변환 등 특정 작업 수행 |

---

## 에이전트 기반 생성 파이프라인

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Topic Selector  │───▶│    Developer    │───▶│    Reviewer     │
│  주제 선정 +     │    │  스킬/포스트     │    │  검토 + QA      │
│  작업 계획       │    │  작성           │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1. Topic Selector
- `.claude/rules/topic-selection.md` 규칙 준수
- 키워드 풀 + 트렌드 기반 주제 선정
- 중복 방지를 위한 기존 스킬 확인
- 작업 계획 수립

### 2. Developer
- SKILL.md 및 블로그 포스트 작성
- 카테고리별 적절한 위치에 파일 생성
- 실행 가능한 예제 코드 포함

### 3. Reviewer
- 품질 검증 체크리스트 적용
- 이름 규칙, 코드 품질, 보안 검토
- 필요시 자동 수정 및 피드백

---

## 폴더 구조 (Single Source of Truth)

```
.claude/                     # 실제 사용 가능한 파일들
├── agents/                  # 에이전트 정의
│   ├── topic-selector.md
│   ├── developer.md
│   └── reviewer.md
├── skills/                  # 스킬 패키지
│   └── {skill-name}/
│       └── SKILL.md
├── commands/                # Slash Command
├── hooks/                   # Claude Code Hook
├── scripts/                 # 공용 스크립트
├── workflows/               # 워크플로우 정의
└── rules/                   # 생성 규칙
    └── topic-selection.md

assets/downloads/            # 블로그 배포용 복사본
└── {skills, agents, ...}

_posts/                      # 블로그 포스트
```

---

## 스케줄

| 요일 | 생성 개수 | 시작 시간 |
|------|----------|----------|
| 월-금 | 5개 | 12:00 |
| 토-일 | 50개 | 12:00 |

- Windows Task Scheduler로 자동 실행
- 모든 생성 완료 후 일괄 commit & push
- GitHub Actions로 Jekyll 빌드 및 배포

---

## AI 자동화 성장 목표

1. **에이전트 기반 자동화**: 주제 선정 → 개발 → 리뷰 파이프라인
2. **품질 검증 자동화**: Reviewer 에이전트의 자동 QA
3. **지식 축적**: 실무에서 바로 사용 가능한 스킬 라이브러리 구축
4. **커뮤니티 성장**: 스킬 요청 및 피드백을 통한 지속적 개선

---

## 제작자

**최진호 (Jinho Choi)**

- 16년차 게임 서버 개발자
- 덱사스튜디오
- MMORPG-ProjectR 서버 개발

---

## Contact

- **GitHub**: [github.com/rs1017](https://github.com/rs1017)
- **Blog**: [rs1017.github.io](https://rs1017.github.io)
