---
layout: post
title: "Slack GIF Creator - Slack용 GIF 생성 스킬"
date: 2026-01-23 10:10:00 +0900
categories: [AI, Skill]
tags: [claude-code, skill, gif, slack, animation]
---

## 개요

Slack GIF Creator는 Slack에 최적화된 애니메이션 GIF를 생성하기 위한 지식과 유틸리티를 제공하는 스킬입니다.

## Slack 요구사항

| 유형 | 크기 | 파라미터 |
|------|------|----------|
| 이모지 GIF | 128x128 | FPS 10-30, 3초 이하 |
| 메시지 GIF | 480x480 | 색상 48-128 |

## 핵심 워크플로우

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. 빌더 생성
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. 프레임 생성
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)
    # PIL로 애니메이션 그리기
    builder.add_frame(frame)

# 3. 최적화하여 저장
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## 애니메이션 컨셉

| 애니메이션 | 구현 방법 |
|-----------|----------|
| 흔들기/진동 | math.sin()/cos()로 위치 오프셋 |
| 펄스/하트비트 | 사인파로 크기 조절 (0.8-1.2) |
| 바운스 | ease_out 이징으로 착지 |
| 회전 | image.rotate() 사용 |
| 페이드 | RGBA 알파 채널 조정 |
| 슬라이드 | ease_out으로 부드러운 정지 |
| 폭발/파티클 | 랜덤 각도/속도로 입자 생성 |

## 사용 가능 유틸리티

| 모듈 | 기능 |
|------|------|
| GIFBuilder | 프레임 조립 및 Slack 최적화 |
| validators | GIF가 Slack 요구사항 충족 확인 |
| easing | 부드러운 모션 (linear, ease_in/out, bounce, elastic) |
| frame_composer | 블랭크 프레임, 그라디언트, 도형 헬퍼 |

## 최적화 전략

- **프레임 감소**: 낮은 FPS (20 대신 10)
- **색상 감소**: num_colors=48
- **크기 축소**: 128x128
- **중복 제거**: remove_duplicates=True

## 첨부 파일

> [slack-gif-creator SKILL.md](/assets/downloads/skills/slack-gif-creator/SKILL.md)

## 관련 스킬

- [algorithmic-art](/posts/algorithmic-art/) - 알고리즘 아트
- [canvas-design](/posts/canvas-design/) - 비주얼 아트
