-
---
layout: post
title: "환경 변수 관리 자동화 스킬 - .env 파일 검증과 보안 체크"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [env, dotenv, security, configuration, environment-variables, devops]
---

## 개요

프로젝트를 운영하다 보면 환경 변수 관리가 점점 복잡해집니다. 새로운 팀원이 합류할 때마다 "이 환경 변수가 뭐죠?"라는 질문을 받고, 프로덕션 배포 전에는 "혹시 환경 변수 빠뜨린 거 없나?" 걱정하게 됩니다.

더 심각한 문제는 보안입니다. `.env` 파일을 실수로 git에 커밋하거나, API 키를 코드에 하드코딩하는 실수는 생각보다 자주 발생합니다.

**Environment Variable Manager** 스킬은 이런 문제를 자동으로 해결합니다:
- 코드에서 사용 중인 환경 변수 자동 탐지
- `.env` 파일과 실제 사용 변수 비교하여 누락/미사용 변수 리포트
- `.env.example` 템플릿 자동 생성
- 민감 정보 하드코딩 및 보안 위험 탐지

## 스킬 구조

```
.claude/skills/env-variable-manager/
└── SKILL.md              # 스킬 정의 및 사용 가이드
```

단일 파일로 구성된 심플한 스킬이지만, 강력한 환경 변수 관리 기능을 제공합니다.

## 주요 기능

### 1. 환경 변수 검증

코드베이스를 스캔하여 실제 사용 중인 환경 변수를 찾아냅니다:

```javascript
// JavaScript/TypeScript
process.env.API_KEY
process.env['DATABASE_URL']
import.meta.env.VITE_APP_URL
```

```python
# Python
os.getenv('SECRET_KEY')
os.environ['DATABASE_URL']
```

그리고 `.env` 파일과 비교하여:
- **누락된 변수**: 코드에서 사용하지만 `.env`에 없는 변수
- **미사용 변수**: `.env`에 있지만 코드에서 사용하지 않는 변수

를 리포트합니다.

### 2. .env.example 자동 생성

현재 `.env` 파일을 기반으로 템플릿을 생성합니다:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys (Required)
API_KEY=your_api_key_here
JWT_SECRET=your_jwt_secret_here

# Redis Cache (Optional)
REDIS_URL=redis://localhost:6379
```

- 실제 값은 안전한 placeholder로 대체
- 각 변수에 설명 주석 추가
- 필수/선택 변수 구분

### 3. 보안 검사

다음 항목을 자동으로 체크합니다:

✅ **통과 항목**:
- `.env` 파일이 `.gitignore`에 포함되어 있는지
- 민감 정보가 코드에 하드코딩되지 않았는지

⚠️ **경고**:
- API 키가 코드에 직접 입력된 경우 (파일명과 라인 번호 제공)
- `.env.production` 같은 파일이 git에 커밋된 경우

### 4. 환경별 설정 비교

개발/스테이징/프로덕션 환경의 `.env` 파일을 비교하여:
- 환경별 차이점 시각화
- 프로덕션에 누락된 변수 경고
- 일관성 없는 설정 탐지

## 사용 방법

### 설치

1. `.claude/skills/` 폴더에 `env-variable-manager` 디렉토리 생성
2. `SKILL.md` 파일을 해당 폴더에 저장

### 사용 예시

#### 예시 1: 프로젝트 초기 설정

```
User: "이 프로젝트에 필요한 환경 변수를 분석해줘"

Claude: 
코드베이스를 스캔한 결과, 다음 환경 변수가 필요합니다:

필수 변수 (5개):
- DATABASE_URL
- API_KEY
- JWT_SECRET
- REDIS_URL
- SMTP_PASSWORD

.env.example 파일을 생성했습니다.
```

#### 예시 2: 환경 변수 누락 탐지

```
User: "환경 변수 설정이 제대로 되어 있는지 확인해줘"

Claude:
❌ .env에 누락된 변수 (2개):
- REDIS_URL
  - 사용 위치: src/cache/redis.js:12
  - 권장값: redis://localhost:6379

- SMTP_PASSWORD
  - 사용 위치: src/email/mailer.js:28
  - 권장값: <your-smtp-password>
```

#### 예시 3: 보안 검사

```
User: "환경 변수 보안 문제 체크"

Claude:
🔒 보안 검사 결과:
✅ .env가 .gitignore에 포함됨
⚠️ API_KEY가 config.js:42에 하드코딩되어 있음
⚠️ .env.local 파일이 git에 추적되고 있음

수정이 필요합니다.
```

## 지원 언어 및 프레임워크

### JavaScript/TypeScript
- Node.js (process.env)
- Vite (import.meta.env)
- Next.js (process.env, NEXT_PUBLIC_)
- React (REACT_APP_)

### Python
- os.getenv, os.environ
- django-environ
- python-dotenv

### PHP
- $_ENV, getenv()

### Ruby
- ENV[], ENV.fetch()

### Go
- os.Getenv()

## 트리거 조건

다음 키워드를 포함한 요청 시 자동 활성화:
- "환경 변수", "env", "dotenv", ".env"
- "API 키", "secret", "credential"
- "설정 파일", "configuration"
- "환경별 설정", "development/staging/production"

## 출력 예시

### 환경 변수 검증 리포트

```markdown
## 환경 변수 분석 결과

### 📋 사용 중인 변수 (10개)
- DATABASE_URL (3 references)
  - src/db/connection.js:15
  - src/db/migrations.js:8
  - src/config/database.js:22

- API_KEY (5 references)
  - src/api/client.js:12
  - src/services/payment.js:45
  ...

### ❌ .env에 누락된 변수 (2개)
- REDIS_URL
  - 사용 위치: src/cache/redis.js:12
  - 권장값: redis://localhost:6379

- SMTP_PASSWORD
  - 사용 위치: src/email/mailer.js:28
  - 권장값: <your-smtp-password>

### ⚠️ .env에 있지만 미사용 (1개)
- OLD_API_ENDPOINT
  - .env.example에서 제거 권장

### 🔒 보안 검사
✅ .env가 .gitignore에 포함됨
✅ 민감 정보 하드코딩 없음
⚠️ .env.local 파일이 git에 추적되고 있음
```

## 작업 흐름

```
1. 프로젝트 구조 파악
   ↓
2. 환경 변수 파일 탐색 (.env, .env.*)
   ↓
3. 코드베이스에서 환경 변수 사용 패턴 검색
   ↓
4. 사용 변수 목록 추출 및 분류
   ↓
5. .env 파일과 비교 분석
   ↓
6. 보안 검사 수행
   ↓
7. 리포트 생성 및 권장사항 제시
```

## 전체 코드

### SKILL.md

```markdown
---
name: env-variable-manager
description: 프로젝트의 환경 변수를 안전하게 관리하고 검증하는 스킬. .env 파일 생성, 누락된 변수 탐지, 민감 정보 보호, 환경별 설정 비교 기능 제공
version: 1.0.0
author: AI Skill Factory
---

# Environment Variable Manager

프로젝트의 환경 변수를 체계적으로 관리하고 검증하는 Claude Code 스킬입니다.

[전체 내용은 위 SKILL.md 섹션 참조]
```

## 보안 주의사항

### 스킬이 자동으로 체크하는 항목

1. **.gitignore 검증**: .env 파일들이 git에서 제외되었는지 확인
2. **하드코딩 탐지**: API 키, 비밀번호 등이 코드에 직접 입력되었는지 검사
3. **민감 정보 패턴**: `password`, `secret`, `key`, `token` 등 키워드 포함 변수 특별 관리
4. **공개 저장소 경고**: .env 파일이 실수로 커밋되었는지 git history 검사

## 제한사항

- 동적으로 생성되는 환경 변수명은 탐지 불가 (예: `process.env[variableName]`)
- 암호화된 환경 변수 파일은 분석 불가
- 외부 secret 관리 시스템(AWS Secrets Manager, HashiCorp Vault 등)은 별도 처리 필요

## 다운로드

> [SKILL.md 보기](/assets/downloads/skills/env-variable-manager/SKILL.md)

위 파일을 참고하여 `.claude/skills/env-variable-manager/` 폴더에 구성하세요.

## 관련 스킬

- **[code-review-assistant](/posts/code-review-assistant/)**: AI 기반 코드 리뷰
- **[test-case-auto-generator](/posts/test-case-auto-generator/)**: 테스트 케이스 자동 생성

## 활용 팁

### 1. CI/CD 파이프라인 통합

배포 전 환경 변수 검증을 자동화하세요:

```yaml
# .github/workflows/deploy.yml
- name: Validate Environment Variables
  run: |
    claude "환경 변수 검증해줘"
    # 누락된 변수가 있으면 실패
```

### 2. 팀 온보딩

새로운 팀원이 합류할 때:

```
User: "개발 환경 설정에 필요한 환경 변수 알려줘"
→ .env.example 기반으로 단계별 가이드 제공
```

### 3. 정기 보안 점검

월 1회 정기적으로:

```
User: "환경 변수 보안 검사"
→ 민감 정보 노출 위험 체크
```

---

환경 변수 관리가 번거로웠다면, 이제 Claude Code에게 맡기세요!