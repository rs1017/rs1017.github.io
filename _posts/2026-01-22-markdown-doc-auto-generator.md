-
---
layout: post
title: "마크다운 문서 자동 생성 스킬"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [documentation, markdown, automation, api-docs, readme]
---

## 개요

프로젝트를 진행하다 보면 문서화는 항상 뒷전으로 밀리기 마련입니다. 코드는 빠르게 변하는데 문서는 업데이트가 안 되고, 새로운 팀원이 합류하면 온보딩에 시간이 오래 걸리죠.

**Markdown Documentation Auto Generator**는 코드베이스를 자동으로 분석하여 프로젝트 문서를 마크다운 형식으로 생성하는 스킬입니다. README, API 레퍼런스, 아키텍처 가이드 등을 자동으로 만들어줍니다.

## 스킬 구조

```
.claude/skills/markdown-doc-auto-generator/
├── SKILL.md                    # 스킬 정의 및 사용 가이드
├── config.yml                  # 설정 파일
├── scripts/
│   ├── doc_generator.py        # 메인 문서 생성 로직
│   ├── tree_builder.py         # 디렉토리 트리 생성
│   ├── api_extractor.py        # API 엔드포인트 추출
│   └── template_renderer.py    # 템플릿 렌더링
├── assets/
│   └── templates/
│       ├── README.template.md
│       ├── API.template.md
│       ├── ARCHITECTURE.template.md
│       └── CONTRIBUTING.template.md
└── references/
    └── supported-languages.md
```

## 주요 기능

### 1. 프로젝트 구조 자동 분석

코드베이스를 스캔하여 다음을 자동으로 파악합니다:
- 디렉토리 구조 (트리 형식)
- 사용 언어 및 프레임워크
- 의존성 정보 (package.json, requirements.txt 등)
- 주요 진입점 파일

### 2. 코드 기반 문서 추출

코드에서 직접 정보를 추출합니다:
- 함수/클래스 docstring
- API 엔드포인트 (Flask, FastAPI, Express 등)
- 환경 변수 및 설정 옵션
- 타입 힌트 및 인터페이스

### 3. 다양한 문서 템플릿

프로젝트 성격에 맞는 문서를 생성합니다:
- **README.md**: 프로젝트 개요, 설치, 사용법
- **API.md**: RESTful API 레퍼런스
- **ARCHITECTURE.md**: 시스템 아키텍처 설명
- **CONTRIBUTING.md**: 기여 가이드

## 사용 방법

### 설치

1. 스킬 파일을 `.claude/skills/` 디렉토리에 복사:

```bash
# 다운로드한 압축 파일 해제
mkdir -p ~/.claude/skills/markdown-doc-auto-generator
# SKILL.md 복사
```

2. Python 의존성 설치:

```bash
pip install -r .claude/skills/markdown-doc-auto-generator/requirements.txt
```

### 기본 사용

Claude Code에서 다음과 같이 요청하세요:

```
프로젝트 README를 자동 생성해줘
```

또는 특정 문서 타입 지정:

```
API 문서를 생성해줘
```

### 명령어 옵션

```bash
# README 생성
/markdown-doc-auto-generator --type readme

# API 문서 생성
/markdown-doc-auto-generator --type api

# 아키텍처 문서 생성
/markdown-doc-auto-generator --type architecture

# 모든 문서 한번에 생성
/markdown-doc-auto-generator --type all

# 출력 경로 지정
/markdown-doc-auto-generator --type readme --output ./docs/README.md
```

## 실제 사용 예시

### Python Flask 프로젝트

**입력 코드:**

```python
# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    모든 사용자 목록을 반환합니다.
    
    Returns:
        JSON: 사용자 목록 배열
    """
    return jsonify([
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    특정 사용자 정보를 반환합니다.
    
    Args:
        user_id (int): 사용자 ID
        
    Returns:
        JSON: 사용자 정보
    """
    user = {"id": user_id, "name": "Alice", "email": "alice@example.com"}
    return jsonify(user)
```

**자동 생성된 API.md:**

```markdown
# API Reference

## Endpoints

### GET /api/users

모든 사용자 목록을 반환합니다.

**Method:** `GET`

**Returns:**
- JSON: 사용자 목록 배열

**Example Response:**
```json
[
  {"id": 1, "name": "Alice", "email": "alice@example.com"},
  {"id": 2, "name": "Bob", "email": "bob@example.com"}
]
```

---

### GET /api/users/:user_id

특정 사용자 정보를 반환합니다.

**Method:** `GET`

**Parameters:**
- `user_id` (int): 사용자 ID

**Returns:**
- JSON: 사용자 정보

**Example Response:**
```json
{"id": 1, "name": "Alice", "email": "alice@example.com"}
```
```

### TypeScript Express 프로젝트

**입력 코드:**

```typescript
// routes/users.ts
import express from 'express';

const router = express.Router();

/**
 * Get all users
 * @route GET /api/users
 * @returns {Array} List of users
 */
router.get('/', (req, res) => {
  res.json([{ id: 1, name: 'Alice' }]);
});

/**
 * Create a new user
 * @route POST /api/users
 * @param {string} name - User name
 * @returns {Object} Created user
 */
router.post('/', (req, res) => {
  const { name } = req.body;
  res.json({ id: 2, name });
});

export default router;
```

**자동 생성된 문서:**

```markdown
### GET /api/users

Get all users

**Returns:** List of users

---

### POST /api/users

Create a new user

**Parameters:**
- `name` (string): User name

**Returns:** Created user
```

## 설정 커스터마이징

`.claude/skills/markdown-doc-auto-generator/config.yml`:

```yaml
# 문서 생성 옵션
templates_dir: ./assets/templates
output_dir: ./docs

# 스캔 대상
include_patterns:
  - "*.py"
  - "*.js"
  - "*.ts"
  - "*.java"
  - "*.go"

exclude_patterns:
  - "node_modules/**"
  - "venv/**"
  - "*.test.*"
  - "__pycache__/**"

# README 옵션
readme:
  include_badges: true        # GitHub badges 포함
  include_toc: true           # 목차 생성
  include_tree: true          # 디렉토리 트리 포함
  include_installation: true  # 설치 가이드 포함

# API 문서 옵션
api:
  format: markdown            # markdown | openapi
  include_examples: true      # 예제 코드 포함
  group_by: path             # path | method | tag

# 아키텍처 문서 옵션
architecture:
  include_diagrams: true      # Mermaid 다이어그램 생성
  include_dependencies: true  # 의존성 그래프 포함
```

## 지원 언어 및 프레임워크

### 백엔드
- Python: Flask, FastAPI, Django
- JavaScript/TypeScript: Express, NestJS, Koa
- Java: Spring Boot
- Go: Gin, Echo
- Ruby: Rails, Sinatra

### 프론트엔드
- React, Vue, Angular (컴포넌트 문서)
- Next.js, Nuxt.js (페이지 라우팅)

## 전체 코드

### SKILL.md

```markdown
---
name: markdown-doc-auto-generator
description: 코드베이스를 분석하여 프로젝트 문서를 자동 생성하는 스킬. README, API 문서, 아키텍처 가이드 등을 마크다운 형식으로 출력합니다.
version: 1.0.0
author: AI Skill Factory
---

(전체 내용은 다운로드 파일 참조)
```

### scripts/doc_generator.py

```python
import os
import ast
import yaml
from pathlib import Path
from typing import Dict, List, Any

class DocumentationGenerator:
    """코드베이스를 분석하여 마크다운 문서를 생성하는 클래스"""
    
    def __init__(self, config_path: str = "config.yml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.codebase_info = {}
    
    def analyze_codebase(self, root_path: str) -> Dict[str, Any]:
        """
        코드베이스 구조를 분석합니다.
        
        Args:
            root_path: 분석할 루트 디렉토리
            
        Returns:
            분석 결과 딕셔너리
        """
        info = {
            'structure': self._build_tree(root_path),
            'languages': self._detect_languages(root_path),
            'dependencies': self._extract_dependencies(root_path),
            'entry_points': self._find_entry_points(root_path)
        }
        self.codebase_info = info
        return info
    
    def generate_readme(self, output_path: str = "README.md"):
        """README.md 파일을 생성합니다."""
        template = self._load_template('README.template.md')
        content = self._render_template(template, self.codebase_info)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ README.md 생성 완료: {output_path}")
    
    def generate_api_docs(self, output_path: str = "API.md"):
        """API 문서를 생성합니다."""
        api_info = self._extract_api_endpoints()
        template = self._load_template('API.template.md')
        content = self._render_template(template, api_info)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ API.md 생성 완료: {output_path}")
    
    def _extract_api_endpoints(self) -> List[Dict]:
        """코드에서 API 엔드포인트를 추출합니다."""
        # Flask, FastAPI, Express 등에서 라우팅 정보 추출
        endpoints = []
        # 구현 로직...
        return endpoints
    
    def _build_tree(self, path: str) -> str:
        """디렉토리 트리를 문자열로 생성합니다."""
        # tree 구조 생성 로직
        pass
    
    def _detect_languages(self, path: str) -> Dict[str, int]:
        """사용 언어 통계를 수집합니다."""
        # 언어별 파일 수 카운트
        pass
    
    def _extract_dependencies(self, path: str) -> Dict:
        """의존성 정보를 추출합니다."""
        # package.json, requirements.txt 등 파싱
        pass
    
    def _load_template(self, template_name: str) -> str:
        """템플릿 파일을 로드합니다."""
        template_path = os.path.join(
            self.config['templates_dir'],
            template_name
        )
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _render_template(self, template: str, data: Dict) -> str:
        """템플릿에 데이터를 렌더링합니다."""
        # Jinja2 또는 간단한 치환 로직
        pass

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['readme', 'api', 'architecture', 'all'], required=True)
    parser.add_argument('--path', default='.')
    parser.add_argument('--output', default=None)
    
    args = parser.parse_args()
    
    generator = DocumentationGenerator()
    generator.analyze_codebase(args.path)
    
    if args.type == 'readme' or args.type == 'all':
        output = args.output or 'README.md'
        generator.generate_readme(output)
    
    if args.type == 'api' or args.type == 'all':
        output = args.output or 'API.md'
        generator.generate_api_docs(output)
```

## 다운로드

> [SKILL.md 보기](/assets/downloads/skills/markdown-doc-auto-generator/SKILL.md)

위 파일을 참고하여 `.claude/skills/markdown-doc-auto-generator/` 폴더에 구성하세요.

## 관련 스킬

- **[code-review-assistant](/posts/code-review-assistant/)**: AI 기반 코드 리뷰
- **[api-response-parser](/posts/api-response-parser/)**: API 응답 파싱

## 마무리

문서화는 귀찮지만 중요한 작업입니다. 이 스킬을 사용하면 코드베이스에서 자동으로 문서를 추출하여 시간을 절약할 수 있습니다. 특히 API 문서는 코드 변경 시 자동으로 업데이트할 수 있어 유용합니다.