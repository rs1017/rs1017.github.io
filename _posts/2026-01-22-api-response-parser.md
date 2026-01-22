-
---
title: "API 응답 파서 스킬 - JSON/XML 데이터 자동 추출"
date: 2024-01-22 12:00:00 +0900
categories: [Skill]
tags: [api, json, xml, parser, data, conversion, validation]
---

## 개요

API 응답 데이터를 효율적으로 파싱하고 변환하는 스킬입니다. 복잡한 JSON/XML 구조에서 필요한 필드만 추출하거나, 포맷을 변환하거나, 스키마를 검증할 수 있습니다.

### 해결하는 문제

- 복잡한 중첩 구조에서 특정 데이터 추출이 어려움
- JSON ↔ XML ↔ CSV 간 변환 작업의 반복
- API 응답 구조 검증 필요
- 페이지네이션 처리의 번거로움
- 데이터 정제 및 변환 작업 자동화

## 스킬 구조

```
.claude/skills/api-response-parser/
└── SKILL.md              # 스킬 정의 및 사용 가이드
```

## 주요 기능

### 1. 필드 추출

중첩된 JSON/XML에서 원하는 필드만 선택적으로 추출합니다.

**입력 예시:**
```json
{
  "data": {
    "users": [
      {"id": 1, "profile": {"name": "Alice", "email": "alice@example.com"}},
      {"id": 2, "profile": {"name": "Bob", "email": "bob@example.com"}}
    ]
  }
}
```

**요청:** "모든 이름과 이메일 추출"

**출력:**
```
Alice, alice@example.com
Bob, bob@example.com
```

### 2. 포맷 변환

JSON, XML, CSV, YAML 간 자유로운 변환을 지원합니다.

**JSON → CSV 예시:**
```json
[
  {"id": 101, "name": "Laptop", "price": 999},
  {"id": 102, "name": "Mouse", "price": 29}
]
```

**결과:**
```csv
id,name,price
101,Laptop,999
102,Mouse,29
```

### 3. 스키마 검증

API 응답이 예상한 구조와 일치하는지 확인합니다.

```
요청: "id, name, price 필드가 있는지 확인"
결과: ✓ 모든 필수 필드 존재
```

### 4. 데이터 변환

- 중첩 구조 평탄화
- 필드명 변경
- 조건부 필터링
- 값 집계 및 통계
- 정렬 및 그룹화

### 5. 페이지네이션 처리

여러 페이지의 데이터를 자동으로 결합합니다.

### 6. 에러 분석

API 에러 응답을 분석하고 원인을 설명합니다.

## 사용 방법

### 설치

```bash
# 스킬 다운로드 후 .claude/skills/ 디렉토리에 배치
cp -r api-response-parser ~/.claude/skills/
```

### 기본 사용법

Claude에게 원하는 작업을 자연어로 설명하면 됩니다:

```
"이 API 응답에서 사용자 이름과 이메일 추출해줘"
```

```
"JSON 응답을 CSV로 변환해줘"
```

```
"응답이 예상 스키마와 맞는지 확인해줘"
```

## 실전 예시

### 예시 1: 제품 정보 테이블 생성

**API 응답:**
```json
{
  "products": [
    {"id": 101, "details": {"name": "Laptop", "price": 999}},
    {"id": 102, "details": {"name": "Mouse", "price": 29}}
  ]
}
```

**요청:** "ID, 이름, 가격으로 테이블 만들어줘"

**결과:**
| ID  | 이름   | 가격  |
|-----|--------|-------|
| 101 | Laptop | $999  |
| 102 | Mouse  | $29   |

### 예시 2: 필터링 및 집계

**요청:** "가격이 100달러 이상인 제품만 추출하고 평균 가격 계산"

**결과:**
```
필터링된 제품: 1개
- Laptop ($999)

평균 가격: $999
```

### 예시 3: 복잡한 변환

**요청:** "사용자별로 주문 개수를 세고 내림차순 정렬"

**결과:**
```
Alice: 5건
Bob: 3건
Charlie: 1건
```

## 활용 팁

1. **전체 응답 제공**: 정확한 파싱을 위해 API 응답 전체를 제공하세요
2. **명확한 필드 지정**: 추출할 필드명을 정확히 명시하세요
3. **출력 포맷 명시**: 테이블, CSV, JSON 등 원하는 형식을 지정하세요
4. **필터 조건 제시**: 큰 응답의 경우 필터링 조건을 함께 제공하세요
5. **샘플 제공**: 복잡한 변환은 예상 출력 샘플을 제시하세요

## 전체 코드

### SKILL.md

```markdown
---
name: api-response-parser
description: Parse and transform API responses into structured formats. Use when you need to extract specific fields from JSON/XML responses, convert between formats, or validate API data structures.
---

# API Response Parser Skill

This skill helps you parse, transform, and validate API responses efficiently.

## When to Use

Use this skill when you need to:
- Extract specific fields from complex JSON/XML API responses
- Convert API responses between formats (JSON ↔ XML ↔ CSV)
- Validate response schemas and data types
- Transform nested structures into flat tables
- Handle pagination and extract data from multiple pages
- Debug API responses by pretty-printing or analyzing structure

## How to Use

Simply describe what you want to do with the API response:

```
Parse this API response and extract user names and emails
```

```
Convert this JSON response to CSV format
```

```
Validate if this response matches the expected schema
```

## Capabilities

### 1. Field Extraction
Extract specific fields from nested JSON/XML structures.

### 2. Format Conversion
Convert between JSON, XML, CSV, and YAML formats.

### 3. Schema Validation
Check if response matches expected structure and data types.

### 4. Data Transformation
- Flatten nested structures
- Rename fields
- Filter by conditions
- Aggregate values
- Sort and group data

### 5. Pagination Handling
Extract and combine data from paginated responses.

### 6. Error Analysis
Identify and explain API error responses.

## Tips

- Provide the full API response for accurate parsing
- Specify the exact fields you need
- Mention the desired output format (table, CSV, JSON, etc.)
- For large responses, specify filtering criteria
- Include sample expected output for complex transformations

## Related Skills

- `json-validator` - Validate JSON schemas
- `data-transformer` - Advanced data transformations
- `csv-converter` - CSV file operations
- `api-client` - Make API requests
```

## 다운로드

> [api-response-parser.zip](/assets/downloads/skills/api-response-parser.zip)

## 관련 스킬

- [json-validator](/posts/json-validator/) - JSON 스키마 검증
- [data-transformer](/posts/data-transformer/) - 고급 데이터 변환
- [csv-converter](/posts/csv-converter/) - CSV 파일 작업
- [api-client](/posts/api-client/) - API 요청 자동화