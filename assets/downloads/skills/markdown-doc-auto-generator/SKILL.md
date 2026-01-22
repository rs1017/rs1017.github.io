
# Markdown Documentation Auto Generator

코드베이스를 자동으로 분석하여 프로젝트 문서를 마크다운 형식으로 생성하는 스킬입니다.

## 사용 시점

다음과 같은 상황에서 이 스킬을 사용하세요:

- 프로젝트 README.md를 자동 생성하고 싶을 때
- API 문서를 코드베이스에서 추출하고 싶을 때
- 아키텍처 개요 문서가 필요할 때
- 기존 문서를 업데이트해야 할 때
- 새로운 팀원을 위한 온보딩 문서가 필요할 때

## 주요 기능

### 1. 프로젝트 구조 분석
- 디렉토리 트리 자동 생성
- 주요 파일 및 폴더 식별
- 언어별 통계 및 의존성 분석

### 2. 코드 기반 문서 생성
- 함수/클래스 docstring 추출
- API 엔드포인트 자동 탐지
- 설정 파일 분석 (package.json, requirements.txt 등)

### 3. 템플릿 기반 출력
- README.md (프로젝트 개요)
- API.md (API 레퍼런스)
- ARCHITECTURE.md (시스템 구조)
- CONTRIBUTING.md (기여 가이드)

## 사용 방법

### 기본 사용

```bash
# 현재 디렉토리의 README.md 생성
/markdown-doc-auto-generator --type readme

# API 문서 생성
/markdown-doc-auto-generator --type api

# 아키텍처 문서 생성
/markdown-doc-auto-generator --type architecture

# 모든 문서 생성
/markdown-doc-auto-generator --type all
```

### 고급 옵션

```bash
# 특정 경로 지정
/markdown-doc-auto-generator --type readme --path ./src

# 출력 파일 지정
/markdown-doc-auto-generator --type api --output docs/API.md

# 템플릿 커스터마이징
/markdown-doc-auto-generator --type readme --template custom-template.md
```

## 생성 문서 예시

### README.md 구조
```markdown
# 프로젝트명

## 개요
(프로젝트 설명)

## 설치 방법
(의존성 및 설치 가이드)

## 사용 방법
(기본 사용 예제)

## 프로젝트 구조
(디렉토리 트리)

## 기여 방법
(컨트리뷰션 가이드)

## 라이센스
(라이센스 정보)
```

### API.md 구조
```markdown
# API Reference

## Endpoints

### GET /api/users
(설명, 파라미터, 응답 예시)

### POST /api/users
(설명, 파라미터, 응답 예시)
```

## 지원 언어

- Python (.py)
- JavaScript/TypeScript (.js, .ts)
- Java (.java)
- Go (.go)
- Ruby (.rb)
- PHP (.php)
- Rust (.rs)

## 설정 파일

`.claude/skills/markdown-doc-auto-generator/config.yml`에서 설정을 커스터마이징할 수 있습니다:

```yaml
# 문서 생성 설정
templates_dir: ./assets/templates
output_dir: ./docs

# 포함/제외 패턴
include_patterns:
  - "*.py"
  - "*.js"
  - "*.ts"
exclude_patterns:
  - "node_modules/**"
  - "venv/**"
  - "*.test.js"

# 문서 구조 옵션
readme:
  include_badges: true
  include_toc: true
  include_tree: true

api:
  format: openapi
  include_examples: true
```

## 스크립트 세부사항

### scripts/doc_generator.py

메인 문서 생성 로직을 담당합니다.

**주요 함수:**
- `analyze_codebase()`: 코드베이스 구조 분석
- `extract_docstrings()`: 함수/클래스 문서 추출
- `generate_readme()`: README.md 생성
- `generate_api_docs()`: API 문서 생성
- `generate_architecture()`: 아키텍처 문서 생성

### scripts/tree_builder.py

디렉토리 트리를 마크다운 형식으로 생성합니다.

### scripts/api_extractor.py

코드에서 API 엔드포인트를 자동 탐지하고 문서화합니다.

## 제한사항

- 매우 큰 프로젝트(1000+ 파일)는 처리 시간이 오래 걸릴 수 있습니다
- 코드 주석이 없는 경우 자동 생성 문서의 품질이 낮을 수 있습니다
- 일부 프레임워크 특화 패턴은 수동 설정이 필요합니다

## 예제

### Python Flask API 프로젝트

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    모든 사용자 목록을 반환합니다.
    
    Returns:
        JSON: 사용자 목록
    """
    return jsonify([{"id": 1, "name": "Alice"}])
```

위 코드에서 자동 생성되는 API 문서:

```markdown
### GET /api/users

모든 사용자 목록을 반환합니다.

**Method:** GET

**Returns:**
- JSON: 사용자 목록

**Example Response:**
```json
[{"id": 1, "name": "Alice"}]
```
```

## 관련 스킬

- `code-documentation-checker`: 문서 품질 검증
- `api-spec-validator`: API 스펙 검증
- `readme-enhancer`: README 개선 제안
