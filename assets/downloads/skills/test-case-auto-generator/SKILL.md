---
name: test-case-auto-generator
description: 코드를 분석하여 테스트 케이스를 자동 생성하는 스킬
version: 1.0.0
author: AI Skill Factory
---

# Test Case Auto Generator

코드를 분석하여 누락된 테스트 케이스를 자동으로 생성하는 스킬입니다.

## 사용 시점

다음과 같은 상황에서 이 스킬을 활성화합니다:

- "이 함수에 대한 테스트 케이스 생성해줘"
- "테스트 커버리지를 높이고 싶어"
- "엣지 케이스 테스트 추가해줘"
- "단위 테스트 자동 생성"
- "이 클래스 테스트 코드 만들어줘"

## 작동 방식

1. **코드 분석**
   - 대상 함수/클래스/모듈 읽기
   - 파라미터, 리턴 타입, 예외 처리 파악
   - 기존 테스트 파일 존재 여부 확인

2. **테스트 시나리오 생성**
   - 정상 케이스 (Happy Path)
   - 경계값 테스트 (Boundary Cases)
   - 예외 처리 테스트 (Error Cases)
   - 엣지 케이스 (Edge Cases)

3. **테스트 코드 작성**
   - 프로젝트의 테스트 프레임워크 감지 (pytest, unittest, jest, etc.)
   - 기존 테스트 스타일 학습
   - 테스트 코드 자동 생성

4. **검증 및 제안**
   - 생성된 테스트 실행
   - 커버리지 리포트 생성
   - 추가 개선 사항 제안

## 지원 언어 및 프레임워크

### Python
- pytest
- unittest
- nose2

### JavaScript/TypeScript
- Jest
- Mocha
- Jasmine
- Vitest

### Java
- JUnit 4/5
- TestNG

### Go
- testing package

## 사용 예시

### 예시 1: 함수 테스트 생성

**입력:**
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
    
    def test_small_discount(self):
        """엣지 케이스: 매우 작은 할인율"""
        result = calculate_discount(100, 0.001)
        assert result == pytest.approx(99.9)
```

### 예시 2: 클래스 테스트 생성

**사용자 요청:**
"UserManager 클래스에 대한 테스트 케이스 생성해줘"

**스킬 실행:**
1. UserManager 클래스 코드 읽기
2. 모든 public 메서드 파악
3. 각 메서드별 테스트 시나리오 생성
4. 통합 테스트 시나리오 추가
5. Mock 객체 필요 여부 판단 및 생성

## 구성 옵션

```yaml
# .claude/skills/test-case-auto-generator/config.yml
coverage_target: 80  # 목표 커버리지 (%)
include_edge_cases: true
include_integration_tests: false
mock_external_dependencies: true
test_framework: auto  # 또는 pytest, jest 등 명시
```

## 참고 사항

- 생성된 테스트는 반드시 검토 후 사용
- 복잡한 비즈니스 로직은 수동 보완 필요
- 외부 의존성(DB, API)은 mock 처리
- 기존 테스트 파일이 있으면 추가 모드로 동작

## 제한 사항

- 100% 커버리지를 보장하지 않음
- 복잡한 상태 머신 테스트는 부분적 지원
- Private 메서드는 간접 테스트로 처리
- UI/E2E 테스트는 미지원