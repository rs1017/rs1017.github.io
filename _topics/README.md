# 주제 관리 폴더 구조

블로그 포스트 자동화 파이프라인을 위한 주제 관리 시스템입니다.

## 폴더 구조

```
.claude/topics/
├── pending/      # 수집된 주제 (선정 대기)
├── selected/     # 선정 완료 (리서치 대기)
├── researched/   # 리서치 완료 (콘티 작성 대기)
├── drafting/     # 콘티/작성 진행 중
└── review/       # 리뷰 대기
```

## 주제 파일 형식

각 주제는 YAML 파일로 관리됩니다: `{topic-id}.yml`

```yaml
# 주제 메타데이터
id: topic-id
title: 주제 제목
proposed_by: user | agent
proposed_date: 2026-01-19
status: pending | selected | researched | drafting | review | published | rejected

# 주제 상세
description: 주제에 대한 설명
keywords:
  - 키워드1
  - 키워드2
target_category:
  - 카테고리1
  - 카테고리2
estimated_difficulty: easy | medium | hard

# 리서치 결과 (리서치 에이전트가 작성)
research:
  completed_date: 2026-01-20
  sources:
    - url: https://example.com
      title: 참고 자료 제목
      key_points:
        - 핵심 내용 1
        - 핵심 내용 2
  outline:
    - section: 섹션 제목
      points:
        - 내용 1
        - 내용 2

# 콘티 정보 (콘티 에이전트가 작성)
storyboard:
  created_date: 2026-01-21
  structure:
    - type: intro
      content: 도입부 내용 설명
    - type: section
      title: 섹션 제목
      content: 내용 설명
      media:
        - type: image
          prompt: 이미지 생성 프롬프트
          status: pending | generated
          path: /assets/img/posts/...
    - type: conclusion
      content: 결론 내용

# 리뷰 결과 (리뷰 에이전트가 작성)
review:
  date: 2026-01-22
  score: 85
  status: approved | rejected
  feedback:
    - type: critical | suggestion
      content: 피드백 내용

# 최종 게시글 정보
post:
  path: _posts/2026-01-22-topic-id.md
  published_date: 2026-01-22
```

## 워크플로우

1. **pending** → 사용자가 주제 제안 또는 topic-selector 에이전트가 수집
2. **selected** → 사용자 승인 후 topic-researcher 에이전트가 리서치 시작
3. **researched** → 리서치 완료, storyboard-creator 에이전트가 콘티 작성
4. **drafting** → post-writer 에이전트가 게시글 작성
5. **review** → post-reviewer 에이전트가 품질 검토
   - 승인 → 배포
   - 반려 → selected로 되돌아가 재리서치
