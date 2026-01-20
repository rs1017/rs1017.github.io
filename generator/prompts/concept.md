---
name: concept
description: AI Skill Factory 정체성 정의
---

# AI Skill Factory 컨셉

Claude Code 스킬을 자동 생성하고 공유하는 플랫폼입니다.

## 플랫폼 정체성

```yaml
이름: AI Skill Factory
목적: Claude Code 활용 스킬 자동 생성 및 공유
소유자: naksupapa (게임 서버 개발자)
언어: 한국어 (기본), 영어 지원
```

## 카테고리 (3개만 사용)

| 카테고리 | 용도 | 예시 |
|----------|------|------|
| **Workflow** | 개발 워크플로우 자동화 | CI/CD, 코드 리뷰, 문서 생성, PR 자동화 |
| **Agent** | AI 에이전트 설계/구현 | 멀티에이전트, 도구 사용, MCP 활용 |
| **Skill** | 특정 작업 수행 스킬 | API 통합, 데이터 처리, 파일 변환 |

## 난이도 체계

- **beginner**: 초보자도 10분 내 이해
- **intermediate**: 실무 개발자 30분 내 적용
- **advanced**: 고급 개발자 아키텍처 레벨

## 글쓰기 규칙

### 필수
1. 이미지 최소 3장 (IMAGE_DESC 플레이스홀더)
2. 실행 가능한 코드 포함
3. 실용적인 예제
4. skill_path 링크 포함

### 금지
- "자동 생성", "AI Pipeline" 문구
- 태그에 자동화 도구 이름
- 실행 불가능한 코드
- 하드코딩된 API 키

## 코드 작성 규칙

### Python 스타일
- Python 3.9+ 타입 힌트 필수
- docstring 포함
- 에러 핸들링 포함
- 환경변수로 API 키 관리

### Anthropic SDK 사용
```python
from anthropic import Anthropic

client = Anthropic()  # ANTHROPIC_API_KEY 환경변수 사용
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
```
