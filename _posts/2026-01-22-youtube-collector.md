---
layout: post
title: "YouTube Collector - 유튜브 채널 수집 및 요약"
date: 2026-01-22 10:40:00 +0900
categories: [AI, Skill]
tags: [youtube, collector, transcript, summary, automation]
---

## 개요

YouTube Collector는 등록된 유튜브 채널의 새 컨텐츠를 수집하고 자막 기반 요약을 생성하는 스킬입니다.

## 사전 요구사항

```bash
pip install google-api-python-client youtube-transcript-api pyyaml
```

## API 키 설정

```bash
# 대화형 설정
python3 scripts/setup_api_key.py

# 직접 지정
python3 scripts/setup_api_key.py --api-key YOUR_API_KEY

# 현재 설정 확인
python3 scripts/setup_api_key.py --show
```

## 워크플로우

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 1. 채널 등록    │───▶│ 2. 컨텐츠 수집  │───▶│ 3. 요약 생성    │
│ register_channel│    │ collect_videos  │    │ Claude 분석     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1. 채널 등록

```bash
# 핸들로 등록
python3 scripts/register_channel.py --channel-handle @channelname --output-dir .reference/

# URL로 등록
python3 scripts/register_channel.py --channel-url "https://youtube.com/@channelname" --output-dir .reference/
```

### 2. 컨텐츠 수집

```bash
# 특정 채널 수집
python3 scripts/collect_videos.py --channel-handle @channelname --output-dir .reference/ --max-results 10

# 모든 채널 수집
python3 scripts/collect_videos.py --all --output-dir .reference/
```

### 3. 요약 생성

자막 또는 설명을 기반으로 요약 생성:

```yaml
summary:
  source: "transcript"  # 또는 "description"
  content: |
    ## 서론
    - 문제 제기 또는 주제 소개

    ## 본론
    - 핵심 내용 상세 설명

    ## 결론
    - 핵심 요약
```

## 데이터 구조

```
.reference/
├── channels.yaml           # 등록된 채널 목록
└── contents/
    └── @channelname/
        ├── video_id_1.yaml
        └── video_id_2.yaml
```

### 영상 데이터 예시

```yaml
video_id: "abc123"
title: "영상 제목"
published_at: "2025-12-10T10:00:00Z"
url: "https://youtube.com/watch?v=abc123"
thumbnail: "https://..."
description: "영상 설명..."
duration: "PT10M30S"
collected_at: "2025-12-13T15:00:00Z"
transcript:
  available: true
  language: "ko"
  text: "자막 전체..."
```

## 스크립트 옵션

### register_channel.py

| 옵션 | 설명 |
|------|------|
| `--channel-handle` | 채널 핸들 (@username) |
| `--channel-url` | 채널 URL |
| `--channel-id` | 채널 ID (UC...) |
| `--output-dir` | 저장 디렉토리 |

### collect_videos.py

| 옵션 | 설명 |
|------|------|
| `--channel-handle` | 특정 채널 핸들 |
| `--all` | 모든 채널 처리 |
| `--max-results` | 최대 수집 개수 (기본: 10) |
| `--language` | 자막 우선 언어 (기본: ko) |

## 에러 처리

| 상황 | 안내 |
|------|------|
| API 키 미설정 | `python3 scripts/setup_api_key.py`로 설정 |
| 채널 미등록 | 먼저 채널 등록 필요 |
| API 할당량 초과 | 내일 다시 시도 |

## 첨부 파일

> [youtube-collector SKILL.md](/assets/downloads/skills/youtube-collector/SKILL.md)

## 관련 스킬

- [skill-creator](/posts/skill-creator/) - Skill 생성 가이드
