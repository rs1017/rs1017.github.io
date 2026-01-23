-
---
layout: post
title: "CSV to JSON 변환 스킬 - 표 데이터를 구조화된 JSON으로"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [csv, json, data-conversion, parsing, transformation]
---

## 개요

CSV 파일을 JSON 형식으로 변환하는 것은 데이터 처리 작업에서 자주 발생하는 요구사항입니다. 특히 API 응답 형식으로 변환하거나, 웹 애플리케이션에서 사용하기 위해 구조화된 데이터가 필요할 때 유용합니다.

이 스킬은 Claude Code를 통해 CSV 파일을 다양한 형식의 JSON으로 변환할 수 있게 해주며, 컬럼 필터링, 데이터 타입 자동 추론, 커스텀 키 매핑 등 유연한 변환 옵션을 제공합니다.

## 스킬 구조

```
.claude/skills/csv-to-json-converter/
├── SKILL.md              # 스킬 정의 및 사용 지침
└── scripts/
    └── convert.py        # CSV to JSON 변환 스크립트
```

## 주요 기능

### 1. 다양한 출력 형식
- **Array of Objects**: 가장 일반적인 형식 (각 행이 객체)
- **Nested Structure**: 계층 구조 JSON
- **Key-Value Object**: 특정 컬럼을 키로 사용

### 2. 데이터 처리
- 자동 데이터 타입 추론 (문자열, 숫자, 불린)
- 헤더 행 자동 감지
- UTF-8 및 다양한 인코딩 지원
- 대용량 파일 스트리밍 처리

### 3. 커스터마이징
- 특정 컬럼만 포함/제외
- 컬럼명 매핑
- Pretty print 옵션
- 커스텀 구분자 지원

## 사용 방법

### 설치

1. 스킬 파일을 다운로드하여 압축 해제
2. `.claude/skills/csv-to-json-converter/` 디렉토리에 배치

### 실행

Claude Code에서 다음과 같이 요청:

```
"customers.csv 파일을 JSON으로 변환해줘"
```

고급 옵션 사용:
```
"데이터.csv를 JSON으로 변환하는데, name과 email 컬럼만 포함하고 pretty print로 출력해줘"
```

## 변환 예시

### 기본 변환

**입력 (data.csv)**:
```csv
name,age,email,active
Alice,30,alice@example.com,true
Bob,25,bob@example.com,false
Charlie,35,charlie@example.com,true
```

**출력 (data.json)**:
```json
[
  {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "active": true
  },
  {
    "name": "Bob",
    "age": 25,
    "email": "bob@example.com",
    "active": false
  },
  {
    "name": "Charlie",
    "age": 35,
    "email": "charlie@example.com",
    "active": true
  }
]
```

### 키-값 객체 형식

**설정**: `key_column: "name"`

**출력**:
```json
{
  "Alice": {
    "age": 30,
    "email": "alice@example.com",
    "active": true
  },
  "Bob": {
    "age": 25,
    "email": "bob@example.com",
    "active": false
  },
  "Charlie": {
    "age": 35,
    "email": "charlie@example.com",
    "active": true
  }
}
```

## 전체 코드

### SKILL.md

프론트매터와 사용 지침은 위 CONTENT 섹션 참조.

### scripts/convert.py

```python
#!/usr/bin/env python3
"""
CSV to JSON Converter Script
Converts CSV files to JSON with flexible formatting options.
"""

import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def infer_type(value: str) -> Any:
    """Infer and convert data type from string."""
    value = value.strip()
    
    # Boolean
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    
    # None/Null
    if value.lower() in ('none', 'null', ''):
        return None
    
    # Number (int or float)
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        pass
    
    # String (default)
    return value


def convert_csv_to_json(
    csv_path: str,
    output_format: str = "array",
    include_columns: Optional[List[str]] = None,
    exclude_columns: Optional[List[str]] = None,
    key_column: Optional[str] = None,
    type_inference: bool = True,
    pretty_print: bool = True,
    encoding: str = "utf-8"
) -> Dict[str, Any]:
    """
    Convert CSV file to JSON.
    
    Args:
        csv_path: Path to CSV file
        output_format: "array", "object", or "nested"
        include_columns: List of columns to include (None = all)
        exclude_columns: List of columns to exclude
        key_column: Column to use as key for object format
        type_inference: Auto-convert data types
        pretty_print: Format JSON with indentation
        encoding: File encoding
    
    Returns:
        Dict with 'success', 'data', 'message'
    """
    try:
        csv_file = Path(csv_path)
        if not csv_file.exists():
            return {
                "success": False,
                "message": f"File not found: {csv_path}"
            }
        
        # Read CSV
        with open(csv_file, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if not rows:
            return {
                "success": False,
                "message": "CSV file is empty"
            }
        
        # Filter columns
        headers = list(rows[0].keys())
        
        if include_columns:
            headers = [h for h in headers if h in include_columns]
        
        if exclude_columns:
            headers = [h for h in headers if h not in exclude_columns]
        
        # Process rows
        processed_rows = []
        for row in rows:
            processed_row = {}
            for header in headers:
                value = row.get(header, '')
                if type_inference:
                    value = infer_type(value)
                processed_row[header] = value
            processed_rows.append(processed_row)
        
        # Format output
        if output_format == "array":
            result = processed_rows
        
        elif output_format == "object":
            if not key_column:
                return {
                    "success": False,
                    "message": "key_column required for object format"
                }
            
            if key_column not in headers:
                return {
                    "success": False,
                    "message": f"key_column '{key_column}' not found in CSV"
                }
            
            result = {}
            for row in processed_rows:
                key = str(row.pop(key_column))
                result[key] = row
        
        else:
            return {
                "success": False,
                "message": f"Unknown output_format: {output_format}"
            }
        
        # Generate output filename
        output_path = csv_file.with_suffix('.json')
        
        # Write JSON
        indent = 2 if pretty_print else None
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=indent, ensure_ascii=False)
        
        return {
            "success": True,
            "data": result,
            "output_file": str(output_path),
            "message": f"Successfully converted {len(processed_rows)} rows",
            "row_count": len(processed_rows),
            "column_count": len(headers)
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python convert.py <csv_file> [options]")
        print("\nOptions:")
        print("  --format array|object")
        print("  --key-column COLUMN_NAME")
        print("  --include COL1,COL2")
        print("  --exclude COL1,COL2")
        print("  --no-type-inference")
        print("  --no-pretty")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    # Parse options
    options = {
        "output_format": "array",
        "type_inference": True,
        "pretty_print": True
    }
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--format" and i + 1 < len(sys.argv):
            options["output_format"] = sys.argv[i + 1]
            i += 2
        elif arg == "--key-column" and i + 1 < len(sys.argv):
            options["key_column"] = sys.argv[i + 1]
            i += 2
        elif arg == "--include" and i + 1 < len(sys.argv):
            options["include_columns"] = sys.argv[i + 1].split(',')
            i += 2
        elif arg == "--exclude" and i + 1 < len(sys.argv):
            options["exclude_columns"] = sys.argv[i + 1].split(',')
            i += 2
        elif arg == "--no-type-inference":
            options["type_inference"] = False
            i += 1
        elif arg == "--no-pretty":
            options["pretty_print"] = False
            i += 1
        else:
            i += 1
    
    # Convert
    result = convert_csv_to_json(csv_path, **options)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        print(f"  Rows: {result['row_count']}")
        print(f"  Columns: {result['column_count']}")
        print(f"  Output: {result['output_file']}")
    else:
        print(f"✗ {result['message']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## 파일 위치

| 구분 | 경로 |
|------|------|
| 정의 파일 | `/assets/downloads/skills/csv-to-json-converter/SKILL.md` |
| 스크립트 | `/assets/downloads/skills/csv-to-json-converter/scripts/convert.py` |
| 설치 위치 | `~/.claude/skills/csv-to-json-converter/` |

## 다운로드

> [csv-to-json-converter.zip](/assets/downloads/skills/csv-to-json-converter.zip)

## 활용 사례

1. **API 응답 데이터 생성**: 테스트용 JSON 데이터 생성
2. **데이터 마이그레이션**: 레거시 CSV를 모던 JSON API로 변환
3. **설정 파일 변환**: CSV 형식의 설정을 JSON config로 변환
4. **웹 앱 데이터 준비**: 프론트엔드에서 사용할 데이터 포맷팅

## 관련 스킬

- `json-to-csv-converter`: 역방향 변환 스킬
- `data-validator`: JSON 스키마 검증
- `api-response-formatter`: API 응답 포맷팅