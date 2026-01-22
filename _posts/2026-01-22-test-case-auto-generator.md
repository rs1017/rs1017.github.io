-
---
title: "테스트 케이스 자동 생성 스킬 - 코드 커버리지를 높이는 지능형 도구"
categories: [Skill]
tags: [test, testing, unit-test, coverage, automation, pytest, jest]
---

## 개요

테스트 코드 작성은 개발자에게 필수적이지만 시간이 많이 소요되는 작업입니다. 특히 레거시 코드나 복잡한 비즈니스 로직에 대한 테스트 작성은 더욱 어렵습니다.

**Test Case Auto Generator** 스킬은 코드를 분석하여 다음을 자동으로 생성합니다:

- ✅ 정상 케이스 (Happy Path)
- ✅ 경계값 테스트 (Boundary Cases)
- ✅ 예외 처리 테스트 (Error Cases)
- ✅ 엣지 케이스 (Edge Cases)

Python(pytest, unittest), JavaScript(Jest, Mocha), Java(JUnit), Go 등 주요 언어와 테스트 프레임워크를 지원합니다.

## 스킬 구조

```
.claude/skills/test-case-auto-generator/
├── SKILL.md              # 스킬 정의 및 사용 지침
└── config.yml            # 커버리지 목표, 프레임워크 설정
```

## 사용 방법

### 1. 설치

스킬 폴더를 `.claude/skills/`에 배치합니다:

```bash
# 다운로드 후 압축 해제
unzip test-case-auto-generator.zip -d ~/.claude/skills/
```

### 2. 기본 사용

코드 파일을 열고 다음과 같이 요청합니다:

```
"이 함수에 대한 테스트 케이스 생성해줘"
"calculate_discount 함수 테스트 작성"
"UserManager 클래스 단위 테스트 추가"
```

### 3. 실행 예시

**대상 코드 (Python):**

```python
def calculate_discount(price: float, discount_rate: float) -> float:
    if price < 0:
        raise ValueError("Price cannot be negative")
    if discount_rate < 0 or discount_rate > 1:
        raise ValueError("Discount rate must be between 0 and 1")
    return price * (1 - discount_rate)
```

**생성된 테스트:**

```python
import pytest
from mymodule import calculate_discount

class TestCalculateDiscount:
    def test_normal_discount(self):
        """정상 케이스: 일반적인 할인 계산"""
        assert calculate_discount(100, 0.2) == 80.0
    
    def test_zero_discount(self):
        """경계값: 할인율 0%"""
        assert calculate_discount(100, 0) == 100.0
    
    def test_full_discount(self):
        """경계값: 할인율 100%"""
        assert calculate_discount(100, 1.0) == 0.0
    
    def test_negative_price(self):
        """예외: 음수 가격"""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_discount(-10, 0.1)
    
    def test_invalid_discount_rate_negative(self):
        """예외: 음수 할인율"""
        with pytest.raises(ValueError, match="Discount rate must be between 0 and 1"):
            calculate_discount(100, -0.1)
    
    def test_invalid_discount_rate_over_one(self):
        """예외: 1 초과 할인율"""
        with pytest.raises(ValueError, match="Discount rate must be between 0 and 1"):
            calculate_discount(100, 1.5)
    
    def test_zero_price(self):
        """엣지 케이스: 가격 0"""
        assert calculate_discount(0, 0.5) == 0.0
```

### 4. 고급 설정

`config.yml`을 통해 커스터마이징:

```yaml
coverage_target: 80  # 목표 커버리지
include_edge_cases: true
include_integration_tests: false
mock_external_dependencies: true
test_framework: auto  # 또는 pytest, jest 등
```

## 작동 원리

### 1단계: 코드 분석
- 함수/클래스 시그니처 파악
- 파라미터 타입, 리턴 타입 추출
- 예외 처리 로직 식별

### 2단계: 시나리오 생성
- **정상 케이스**: 일반적인 입력값
- **경계값**: 0, 최대값, 최소값
- **예외 케이스**: None, 음수, 타입 불일치
- **엣지 케이스**: 빈 리스트, 매우 큰 값

### 3단계: 테스트 코드 작성
- 프로젝트의 기존 테스트 스타일 학습
- 프레임워크에 맞는 assert 문 생성
- Mock 객체 자동 생성 (필요 시)

### 4단계: 검증
- 생성된 테스트 실행
- 실패 케이스 분석 및 수정 제안

## 지원 환경

| 언어 | 프레임워크 |
|------|-----------|
| Python | pytest, unittest, nose2 |
| JavaScript/TypeScript | Jest, Mocha, Jasmine, Vitest |
| Java | JUnit 4/5, TestNG |
| Go | testing package |

## 활용 팁

### 1. 레거시 코드 테스트
기존 코드에 테스트가 없다면:
```
"src/legacy/payment.py의 모든 함수에 테스트 생성"
```

### 2. 커버리지 개선
현재 커버리지 확인 후:
```
"커버되지 않은 함수들에 테스트 추가"
```

### 3. 리팩토링 전 안전망
코드 변경 전:
```
"리팩토링 전에 현재 동작을 검증할 테스트 작성"
```

## 제한 사항

- 100% 커버리지를 보장하지 않음 (복잡한 로직은 수동 보완 필요)
- UI/E2E 테스트는 미지원
- 외부 의존성(DB, API)은 mock 처리
- 생성된 테스트는 반드시 검토 후 사용

## 전체 코드

### SKILL.md

```markdown
---
name: test-case-auto-generator
description: 코드 분석을 통해 테스트 케이스를 자동 생성하는 스킬. 사용자가 "테스트 케이스 생성", "단위 테스트 작성", "test coverage 개선" 등을 요청할 때 사용.
---

# Test Case Auto Generator

코드를 분석하여 누락된 테스트 케이스를 자동으로 생성하는 스킬입니다.

## 사용 시점

- "이 함수에 대한 테스트 케이스 생성해줘"
- "테스트 커버리지를 높이고 싶어"
- "엣지 케이스 테스트 추가해줘"

## 작동 방식

1. 코드 분석 (파라미터, 리턴 타입, 예외)
2. 테스트 시나리오 생성 (정상/경계/예외/엣지)
3. 테스트 코드 작성 (프레임워크 자동 감지)
4. 검증 및 커버리지 리포트

## 지원 언어

Python (pytest, unittest), JavaScript (Jest, Mocha), Java (JUnit), Go

## 참고 사항

- 생성된 테스트는 반드시 검토 후 사용
- 외부 의존성은 mock 처리
- 기존 테스트 파일이 있으면 추가 모드로 동작
```

### config.yml

```yaml
coverage_target: 80
include_edge_cases: true
include_integration_tests: false
mock_external_dependencies: true
test_framework: auto
```

## 다운로드

> [test-case-auto-generator.zip](/assets/downloads/skills/test-case-auto-generator.zip)

압축을 해제하여 `.claude/skills/` 폴더에 배치하면 바로 사용할 수 있습니다.

## 관련 스킬

- **code-reviewer**: 코드 리뷰 시 테스트 커버리지 체크
- **git-commit-analyzer**: 커밋 전 테스트 검증
- **pre-commit-lint**: 커밋 전 테스트 실행 자동화 (Hook)