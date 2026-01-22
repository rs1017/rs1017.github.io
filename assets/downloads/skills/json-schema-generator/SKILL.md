
# JSON Schema Generator

JSON 데이터 샘플로부터 JSON Schema를 자동으로 생성하고, 생성된 스키마로 다른 JSON 데이터를 검증하는 스킬입니다.

## 사용 시점

다음과 같은 상황에서 이 스킬을 사용하세요:

1. **API 문서화**: REST API 응답 형식을 JSON Schema로 문서화하고 싶을 때
2. **데이터 검증**: JSON 데이터의 구조와 타입을 자동으로 검증하고 싶을 때
3. **타입 정의**: 프로젝트에서 사용하는 JSON 설정 파일의 스키마를 정의하고 싶을 때
4. **문서 생성**: JSON 데이터 구조를 명확하게 문서화하고 싶을 때
5. **테스트 자동화**: API 응답이나 데이터 구조의 일관성을 자동으로 체크하고 싶을 때

## 주요 기능

- JSON 데이터로부터 JSON Schema Draft-07 자동 생성
- 중첩된 객체 및 배열 구조 완벽 지원
- 타입 추론 (string, number, integer, boolean, null, array, object)
- Required 필드 자동 감지
- 생성된 스키마로 다른 JSON 데이터 검증
- 검증 오류 상세 리포트

## 사용 방법

### 1. 기본 사용법

```bash
# JSON 파일로부터 스키마 생성
python generate_schema.py input.json

# 출력 파일명 지정
python generate_schema.py input.json -o schema.json

# 스키마 생성 후 다른 JSON 검증
python generate_schema.py sample.json -v data_to_validate.json
```

### 2. Python 코드에서 사용

```python
from generate_schema import JSONSchemaGenerator

# 스키마 생성
generator = JSONSchemaGenerator()
with open('sample.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

schema = generator.generate(data)

# 파일로 저장
generator.save_schema(schema, 'output_schema.json')

# 검증
is_valid, errors = generator.validate(data_to_check, schema)
if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

### 3. 예시

**입력 JSON (sample.json):**
```json
{
  "user": {
    "id": 12345,
    "name": "홍길동",
    "email": "hong@example.com",
    "age": 30,
    "active": true,
    "tags": ["developer", "python", "api"]
  },
  "settings": {
    "theme": "dark",
    "notifications": {
      "email": true,
      "push": false
    }
  }
}
```

**생성된 JSON Schema:**
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
        "age": {"type": "integer"},
        "active": {"type": "boolean"},
        "tags": {
          "type": "array",
          "items": {"type": "string"}
        }
      },
      "required": ["id", "name", "email", "age", "active", "tags"]
    },
    "settings": {
      "type": "object",
      "properties": {
        "theme": {"type": "string"},
        "notifications": {
          "type": "object",
          "properties": {
            "email": {"type": "boolean"},
            "push": {"type": "boolean"}
          },
          "required": ["email", "push"]
        }
      },
      "required": ["theme", "notifications"]
    }
  },
  "required": ["user", "settings"]
}
```

## 설치

스킬 디렉토리에서 필요한 패키지를 설치하세요:

```bash
pip install jsonschema
```

## 옵션

- `-o, --output`: 출력 스키마 파일 경로 (기본값: `{입력파일명}_schema.json`)
- `-v, --validate`: 생성된 스키마로 검증할 JSON 파일 경로
- `--indent`: JSON 출력 들여쓰기 (기본값: 2)

## 팁

1. **배열 처리**: 배열의 첫 번째 요소 타입으로 스키마를 생성합니다. 일관된 데이터 구조를 사용하세요.
2. **null 값**: null 값이 있는 필드는 "null" 타입으로 추론됩니다.
3. **혼합 타입**: 배열 내 여러 타입이 섞여있으면 첫 번째 요소 타입만 인식됩니다.
4. **필수 필드**: 모든 존재하는 키를 required로 설정합니다. 선택 필드는 수동으로 조정하세요.

## 활용 사례

### API 응답 검증
```bash
# 1. API 응답 샘플로 스키마 생성
curl https://api.example.com/users/1 > sample_response.json
python generate_schema.py sample_response.json -o user_schema.json

# 2. 실제 응답 검증
curl https://api.example.com/users/2 > test_response.json
python generate_schema.py sample_response.json -v test_response.json
```

### 설정 파일 검증
```bash
# config.json 스키마 생성
python generate_schema.py config.json -o config_schema.json

# 배포 전 설정 파일 검증
python generate_schema.py config.json -v production_config.json
```

## 제한사항

- Draft-07 스펙 기준 (최신 Draft 2020-12는 미지원)
- 복잡한 패턴이나 포맷 검증은 수동 추가 필요
- 배열 내 혼합 타입은 완벽하게 추론하지 못함

## 라이센스

MIT License
