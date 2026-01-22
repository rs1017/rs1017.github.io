---
name: env-variable-manager
description: 프로젝트의 환경 변수를 체계적으로 관리하고 검증하는 스킬
version: 1.0.0
author: AI Skill Factory
---

# Environment Variable Manager

프로젝트의 환경 변수를 체계적으로 관리하고 검증하는 Claude Code 스킬입니다.

## 주요 기능

### 1. 환경 변수 검증
- 코드에서 사용 중인 환경 변수 자동 탐지
- .env 파일과 실제 사용 변수 비교
- 누락되거나 미사용 변수 리포트

### 2. .env 템플릿 생성
- .env.example 자동 생성
- 민감 정보 마스킹
- 변수별 설명 주석 추가

### 3. 환경별 설정 관리
- development/staging/production 환경 비교
- 환경별 필수 변수 체크
- 설정 차이점 시각화

### 4. 보안 검사
- 민감 정보 하드코딩 탐지
- .gitignore에 .env 포함 여부 확인
- 환경 변수 노출 위험 경고

## 사용 시나리오

### 시나리오 1: 프로젝트 초기 설정
```
User: "이 프로젝트에 필요한 환경 변수를 분석해줘"
→ 코드 스캔 후 .env.example 생성
```

### 시나리오 2: 환경 변수 누락 탐지
```
User: "환경 변수 설정이 제대로 되어 있는지 확인해줘"
→ 누락/미사용 변수 리포트 제공
```

### 시나리오 3: 보안 검사
```
User: "환경 변수 보안 문제 체크"
→ 하드코딩, .gitignore 누락 등 검사
```

## 트리거 조건

다음 키워드를 포함한 요청 시 자동 활성화:
- "환경 변수", "env", "dotenv", ".env"
- "API 키", "secret", "credential"
- "설정 파일", "configuration"
- "환경별 설정", "development/staging/production"

## 사용 방법

### 1. 환경 변수 검증

스킬이 자동으로:
1. 프로젝트 루트에서 .env, .env.example 파일 탐색
2. 코드베이스에서 process.env, os.getenv 등 환경 변수 사용 패턴 검색
3. 사용 중인 변수 목록 추출
4. .env 파일과 비교하여 누락/미사용 변수 리포트

### 2. .env.example 생성

```markdown
현재 .env 파일 기반으로:
- 실제 값은 placeholder로 대체
- 각 변수에 설명 주석 추가
- 필수/선택 변수 구분
```

### 3. 보안 검사 리포트

```markdown
✅ 통과 항목:
- .env 파일이 .gitignore에 포함됨
- 민감 정보 하드코딩 없음

⚠️ 경고:
- API_KEY가 config.js에 하드코딩되어 있음 (line 42)
- .env.production 파일이 git에 커밋됨
```

## 분석 패턴

### JavaScript/TypeScript
```javascript
process.env.API_KEY
process.env['DATABASE_URL']
import.meta.env.VITE_APP_URL
```

### Python
```python
os.getenv('SECRET_KEY')
os.environ['DATABASE_URL']
os.environ.get('API_KEY', 'default')
```

### PHP
```php
$_ENV['DB_HOST']
getenv('API_KEY')
```

### Ruby
```ruby
ENV['RAILS_ENV']
ENV.fetch('SECRET_KEY')
```

### Go
```go
os.Getenv("PORT")
```

## 출력 예시

### 환경 변수 검증 리포트

```markdown
## 환경 변수 분석 결과

### 📋 사용 중인 변수 (10개)
- DATABASE_URL (3 references)
- API_KEY (5 references)
- JWT_SECRET (2 references)
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

### 생성된 .env.example

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys (Required)
API_KEY=your_api_key_here
JWT_SECRET=your_jwt_secret_here

# Redis Cache (Optional)
REDIS_URL=redis://localhost:6379

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_smtp_password

# Application Settings
NODE_ENV=development
PORT=3000
LOG_LEVEL=info
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

## 지원 파일 형식

- `.env` - 기본 환경 변수 파일
- `.env.local` - 로컬 개발 설정
- `.env.development` - 개발 환경
- `.env.staging` - 스테이징 환경
- `.env.production` - 프로덕션 환경
- `.env.example` - 템플릿 파일

## 보안 주의사항

### 스킬이 자동으로 체크하는 항목:

1. **.gitignore 검증**
   - .env 파일들이 git에서 제외되었는지 확인

2. **하드코딩 탐지**
   - API 키, 비밀번호 등이 코드에 직접 입력되었는지 검사

3. **민감 정보 패턴**
   - `password`, `secret`, `key`, `token` 등의 키워드 포함 변수 특별 관리

4. **공개 저장소 경고**
   - .env 파일이 실수로 커밋되었는지 git history 검사

## 제한사항

- 동적으로 생성되는 환경 변수명은 탐지 불가
- 암호화된 환경 변수 파일은 분석 불가
- 외부 secret 관리 시스템(AWS Secrets Manager 등)은 별도 처리 필요

## 관련 도구

- **dotenv**: Node.js 환경 변수 로더
- **python-dotenv**: Python 환경 변수 로더
- **direnv**: 디렉토리별 환경 변수 자동 로드
- **git-secrets**: Git 커밋 전 민감 정보 검사