-
---
layout: post
title: "JSON Schema Generator - JSON 데이터로 스키마 자동 생성"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [json, schema, validation, api, automation, developer-tools]
---

## 개요

API 개발이나 데이터 구조 문서화 작업을 하다 보면 JSON Schema를 작성해야 하는 경우가 많습니다. 하지만 복잡한 중첩 구조를 가진 JSON 데이터의 스키마를 수동으로 작성하는 것은 시간이 오래 걸리고 실수하기 쉽습니다.

**JSON Schema Generator** 스킬은 실제 JSON 데이터 샘플로부터 JSON Schema Draft-07을 자동으로 생성하고, 생성된 스키마로 다른 JSON 데이터를 검증할 수 있는 도구입니다.

### 해결하는 문제

- ✅ API 응답 형식을 빠르게 문서화
- ✅ JSON 데이터 구조의 자동 검증
- ✅ 설정 파일 스키마 정의 자동화
- ✅ 데이터 구조 변경 감지

## 스킬 구조

```
.claude/skills/json-schema-generator/
├── SKILL.md                    # 스킬 문서
└── scripts/
    └── generate_schema.py      # 스키마 생성 스크립트
```

## 설치 방법

### 1. 스킬 파일 복사

`.claude/skills/json-schema-generator/` 디렉토리를 Claude Code 프로젝트의 `.claude/skills/` 경로에 복사합니다.

### 2. 의존성 설치

```bash
pip install jsonschema
```

## 사용 방법

### 기본 사용법

```bash
# JSON 파일로부터 스키마 생성
python .claude/skills/json-schema-generator/scripts/generate_schema.py sample.json

# 출력 파일명 지정
python .claude/skills/json-schema-generator/scripts/generate_schema.py sample.json -o my_schema.json

# 스키마 생성 후 다른 JSON 파일 검증
python .claude/skills/json-schema-generator/scripts/generate_schema.py sample.json -v data.json
```

### 실전 예제: API 응답 검증

**1단계: 샘플 API 응답으로 스키마 생성**

```json
// user_response.json
{
  "user": {
    "id": 12345,
    "name": "홍길동",
    "email": "hong@example.com",
    "roles": ["admin", "developer"],
    "metadata": {
      "created_at": "2024-01-15",
      "last_login": "2024-01-20"
    }
  },
  "status": "success"
}
```

```bash
python generate_schema.py user_response.json -o user_schema.json
```

**2단계: 생성된 스키마**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "roles": {
          "type": "array",
          "items": {"type": "string"}
        },
        "metadata": {
          "type": "object",
          "properties": {
            "created_at": {"type": "string"},
            "last_login": {"type": "string"}
          },
          "required": ["created_at", "last_login"]
        }
      },
      "required": ["id", "name", "email", "roles", "metadata"]
    },
    "status": {"type": "string"}
  },
  "required": ["user", "status"]
}
```

**3단계: 실제 API 응답 검증**

```bash
# API 호출 후 응답 검증
curl https://api.example.com/users/123 > test_response.json
python generate_schema.py user_response.json -v test_response.json
```

## 전체 코드

### generate_schema.py

```python
#!/usr/bin/env python3
"""
JSON Schema Generator
JSON 데이터로부터 JSON Schema Draft-07을 자동 생성하고 검증하는 도구
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
from jsonschema import validate, ValidationError, Draft7Validator


class JSONSchemaGenerator:
    """JSON 데이터로부터 JSON Schema를 생성하는 클래스"""
    
    SCHEMA_VERSION = "http://json-schema.org/draft-07/schema#"
    
    def __init__(self):
        pass
    
    def infer_type(self, value: Any) -> str:
        """값의 타입을 추론"""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "string"
    
    def generate_from_value(self, value: Any) -> Dict[str, Any]:
        """단일 값으로부터 스키마 생성"""
        value_type = self.infer_type(value)
        
        if value_type == "array":
            return self._generate_array_schema(value)
        elif value_type == "object":
            return self._generate_object_schema(value)
        else:
            return {"type": value_type}
    
    def _generate_array_schema(self, arr: List[Any]) -> Dict[str, Any]:
        """배열 스키마 생성"""
        schema = {"type": "array"}
        
        if arr:
            # 첫 번째 요소로부터 items 스키마 추론
            first_item = arr[0]
            schema["items"] = self.generate_from_value(first_item)
        
        return schema
    
    def _generate_object_schema(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """객체 스키마 생성"""
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for key, value in obj.items():
            schema["properties"][key] = self.generate_from_value(value)
            schema["required"].append(key)
        
        return schema
    
    def generate(self, data: Any) -> Dict[str, Any]:
        """JSON 데이터로부터 완전한 JSON Schema 생성"""
        schema = {
            "$schema": self.SCHEMA_VERSION
        }
        
        schema.update(self.generate_from_value(data))
        
        return schema
    
    def validate(self, data: Any, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """스키마로 데이터 검증"""
        validator = Draft7Validator(schema)
        errors = []
        
        for error in validator.iter_errors(data):
            error_path = ".".join(str(p) for p in error.path) if error.path else "root"
            errors.append(f"{error_path}: {error.message}")
        
        return len(errors) == 0, errors
    
    def save_schema(self, schema: Dict[str, Any], output_path: str, indent: int = 2):
        """스키마를 파일로 저장"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=indent, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="JSON 데이터로부터 JSON Schema를 생성하고 검증합니다."
    )
    parser.add_argument(
        "input_file",
        help="입력 JSON 파일 경로"
    )
    parser.add_argument(
        "-o", "--output",
        help="출력 스키마 파일 경로 (기본값: {입력파일명}_schema.json)"
    )
    parser.add_argument(
        "-v", "--validate",
        help="생성된 스키마로 검증할 JSON 파일 경로"
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON 출력 들여쓰기 (기본값: 2)"
    )
    
    args = parser.parse_args()
    
    # 입력 파일 읽기
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 오류: 파일을 찾을 수 없습니다: {args.input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
        sys.exit(1)
    
    # 스키마 생성
    generator = JSONSchemaGenerator()
    schema = generator.generate(input_data)
    
    # 출력 파일명 결정
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input_file)
        output_path = input_path.stem + "_schema.json"
    
    # 스키마 저장
    generator.save_schema(schema, output_path, indent=args.indent)
    print(f"✅ 스키마 생성 완료: {output_path}")
    
    # 검증 수행 (옵션)
    if args.validate:
        try:
            with open(args.validate, 'r', encoding='utf-8') as f:
                validate_data = json.load(f)
            
            is_valid, errors = generator.validate(validate_data, schema)
            
            if is_valid:
                print(f"✅ 검증 성공: {args.validate}")
            else:
                print(f"❌ 검증 실패: {args.validate}")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
        
        except FileNotFoundError:
            print(f"❌ 검증 파일을 찾을 수 없습니다: {args.validate}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ 검증 파일 JSON 파싱 오류: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
```

## 활용 사례

### 1. REST API 문서화

```bash
# Swagger/OpenAPI 대신 JSON Schema로 빠르게 문서화
curl https://api.example.com/products/1 > sample_product.json
python generate_schema.py sample_product.json -o product_schema.json
```

### 2. CI/CD 파이프라인 검증

```yaml
# .github/workflows/validate-api.yml
- name: Validate API Response
  run: |
    curl ${{ secrets.API_URL }}/endpoint > response.json
    python generate_schema.py expected_schema.json -v response.json
```

### 3. 설정 파일 검증

```bash
# 프로덕션 배포 전 설정 검증
python generate_schema.py config.dev.json -v config.prod.json
```

## 다운로드

> [json-schema-generator.zip](/assets/downloads/skills/json-schema-generator.zip)

ZIP 파일을 다운로드하여 압축 해제 후, `.claude/skills/` 디렉토리에 복사하세요.

## 관련 스킬

- **api-response-validator**: API 응답 자동 검증
- **config-file-manager**: JSON 설정 파일 관리
- **data-structure-analyzer**: 복잡한 데이터 구조 분석