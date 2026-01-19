# Blog Agents

블로그 자동화 파이프라인에서 사용하는 AI 에이전트 프롬프트 모음입니다.

## 에이전트 목록

| 에이전트 | 파일 | 역할 |
|----------|------|------|
| Topic Selector | `topic-selector.md` | 블로그 주제 선정 |
| Topic Researcher | `topic-researcher.md` | 주제 리서치 |
| Storyboard Creator | `storyboard-creator.md` | 콘티/스토리보드 작성 |
| Post Writer | `post-writer.md` | 게시글 작성 |
| Post Reviewer | `post-reviewer.md` | 품질 검토 |
| Image Generator | `image-generator.md` | 이미지 프롬프트 최적화 |

## 파이프라인 흐름

```
Step 1: Topic Selector    → 주제 선정
Step 2: Topic Researcher  → 주제 리서치
Step 3: Storyboard Creator → 콘티 작성
Step 4: Post Writer       → 게시글 작성
Step 5: Post Reviewer     → 품질 검토
Step 6: Image Generator   → 이미지 생성
Step 7: Header Image      → 헤더 이미지 생성
```

## 사용 방법

`tools/daily_writer.py`에서 각 에이전트 프롬프트를 자동으로 로드하여 사용합니다.

```python
# 에이전트 프롬프트 로드
prompt = load_agent_prompt("topic-selector")  # _agents/topic-selector.md 로드
```

## 블로그 정체성

- **소유자**: 게임 서버 개발자 아빠
- **가족**: 7살 남아(민준이), 6살 여아(서연이)
- **카테고리**: AI, Tech, Life (3개만 사용)

## 글쓰기 규칙

1. **이미지 최소 3장** 포함
2. **자연스러운 글쓰기** (AI 생성 티 안 나게)
3. **자동 생성 문구 금지** (Gemini, AutoBlog, Pipeline 등)
4. **태그에 자동화 도구 이름 사용 금지**
