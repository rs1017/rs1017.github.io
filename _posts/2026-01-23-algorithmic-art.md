---
layout: post
title: "Algorithmic Art - p5.js 기반 생성 예술 스킬"
date: 2026-01-23 10:00:00 +0900
categories: [AI, Skill]
tags: [claude-code, skill, generative-art, p5js, creative-coding]
---

## 개요

Algorithmic Art는 p5.js를 사용하여 시드 기반 랜덤성과 인터랙티브 파라미터 탐색을 통해 알고리즘 예술을 생성하는 스킬입니다.

## 주요 기능

1. **알고리즘 철학 생성** - 계산적 미학 운동을 정의하는 마니페스토 작성
2. **p5.js 구현** - 생성 예술을 코드로 표현
3. **시드 기반 재현성** - 동일한 시드로 동일한 결과 보장
4. **인터랙티브 파라미터** - 실시간 파라미터 조정 UI

## 워크플로우

```
┌─────────────────┐    ┌─────────────────┐
│ 1. 철학 생성     │───▶│ 2. p5.js 구현   │
│ (.md 파일)      │    │ (.html 파일)    │
└─────────────────┘    └─────────────────┘
```

## 철학 예시

| 운동 이름 | 설명 |
|----------|------|
| Organic Turbulence | 자연 법칙에 의해 제약된 카오스 |
| Quantum Harmonics | 파동 간섭 패턴을 보이는 개별 입자 |
| Recursive Whispers | 유한 공간에서의 무한 깊이 |
| Field Dynamics | 물질에 대한 효과로 가시화된 보이지 않는 힘 |

## 기술 요구사항

```javascript
// 시드 기반 랜덤성
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);

// 파라미터 구조
let params = {
  seed: 12345,
  // 커스텀 파라미터들
};
```

## 출력 형식

- **철학 문서** (.md) - 생성적 미학을 설명하는 마크다운
- **HTML 아티팩트** - p5.js, 알고리즘, UI를 모두 포함한 단일 파일

## 첨부 파일

> [algorithmic-art SKILL.md](/assets/downloads/skills/algorithmic-art/SKILL.md)

## 관련 스킬

- [canvas-design](/posts/canvas-design/) - 정적 비주얼 아트
- [frontend-design](/posts/frontend-design/) - 프론트엔드 인터페이스
