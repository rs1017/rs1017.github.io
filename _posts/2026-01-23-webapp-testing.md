---
layout: post
title: "WebApp Testing - Playwright 기반 웹앱 테스트 스킬"
date: 2026-01-23 10:12:00 +0900
categories: [AI, Skill]
tags: [claude-code, skill, testing, playwright, automation]
---

## 개요

WebApp Testing은 Playwright를 사용하여 로컬 웹 애플리케이션과 상호작용하고 테스트하는 툴킷입니다. 프론트엔드 기능 검증, UI 동작 디버깅, 브라우저 스크린샷 캡처, 브라우저 로그 확인을 지원합니다.

## 결정 트리

```
사용자 작업 → 정적 HTML인가?
    ├─ Yes → HTML 파일 직접 읽어 셀렉터 식별
    │         → Playwright 스크립트 작성
    │
    └─ No (동적 웹앱) → 서버 실행 중인가?
        ├─ No → scripts/with_server.py 사용
        │
        └─ Yes → 정찰 후 행동:
            1. 네비게이션 및 networkidle 대기
            2. 스크린샷 또는 DOM 검사
            3. 렌더링된 상태에서 셀렉터 식별
            4. 발견된 셀렉터로 액션 실행
```

## with_server.py 사용 예시

### 단일 서버

```bash
python scripts/with_server.py \
  --server "npm run dev" \
  --port 5173 \
  -- python your_automation.py
```

### 다중 서버 (백엔드 + 프론트엔드)

```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

## 자동화 스크립트 예시

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # 중요!
    # ... 자동화 로직
    browser.close()
```

## 정찰-후-행동 패턴

1. **렌더된 DOM 검사**
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **셀렉터 식별** - 검사 결과에서
3. **액션 실행** - 발견된 셀렉터 사용

## 주의사항

- 동적 앱에서 `networkidle` 대기 전 DOM 검사 금지
- `sync_playwright()` 사용
- 완료 후 브라우저 닫기
- 명확한 셀렉터 사용: `text=`, `role=`, CSS, ID

## 첨부 파일

> [webapp-testing SKILL.md](/assets/downloads/skills/webapp-testing/SKILL.md)

## 관련 스킬

- [frontend-design](/posts/frontend-design/) - 프론트엔드 디자인
- [web-artifacts-builder](/posts/web-artifacts-builder/) - 웹 아티팩트 빌더
