# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Skill Factory - Jekyll 기반 Claude Code 스킬 자동 생성 플랫폼. Anthropic Claude API를 사용하여 Workflow, Agent, Skill 카테고리의 스킬을 자동 생성하고 GitHub Pages에 배포합니다.

## Common Commands

### Development
```bash
bundle exec jekyll serve          # Dev server at http://localhost:4000
npx gulp dev                      # Watch and compile JavaScript
```

### Building
```bash
bundle exec jekyll b              # Standard build
JEKYLL_ENV=production bundle exec jekyll b  # Production build
npx gulp                          # Minify JavaScript
```

### Testing
```bash
bundle exec htmlproofer _site --disable-external --check-html --allow_hash_href
```

### Skill Generation
```bash
cd generator
pip install -r requirements.txt
python generate.py                        # Auto strategy
python generate.py --strategy keyword     # Keyword combination
python generate.py --strategy trend       # Trend-based
python generate.py --topic "Git 커밋 분석 스킬"  # Specific topic
```

## Architecture

### Skill Generation Pipeline

`generator/generate.py` orchestrates a 6-step pipeline:

```
1. Topic Selection → 2. Skill Design → 3. Code Generation → 4. Post Writing → 5. Validation → 6. Save Files
```

### Directory Structure

```
generator/
├── generate.py              # Main entry point
├── prompts/                 # Agent prompts
│   ├── concept.md          # Platform identity
│   ├── skill-topic-selector.md
│   ├── skill-designer.md
│   ├── code-generator.md
│   ├── post-writer.md
│   └── validator.md
├── agents/                  # Python agent modules
├── clients/                 # API clients (Anthropic)
├── sources/                 # Topic sources (trends, requests)
└── utils/                   # Utilities

skills/                      # Generated skills
└── {skill-name}/
    ├── SKILL.md            # Skill documentation
    └── example.py          # Executable example

_posts/                      # Generated blog posts
_data/skill_registry.yml     # Skill registry
```

### Jekyll Layout Hierarchy

```
compress.html (HTML minification)
    └── default.html (base structure)
            ├── home.html (post list)
            ├── post.html (content, TOC)
            └── page.html (static pages)
```

### CI/CD Workflow

`.github/workflows/auto_generate.yml`:
- **Triggers**: Daily 00:00 UTC, manual dispatch, issue labeled `skill-request`
- **Jobs**: Generate Skill → Build Jekyll → Deploy to GitHub Pages

## Platform Constraints

### Categories (3 only)
- **Workflow**: 개발 워크플로우 자동화 (CI/CD, 코드 리뷰, 문서 생성)
- **Agent**: AI 에이전트 설계/구현 (멀티에이전트, MCP, 도구 사용)
- **Skill**: 특정 작업 수행 (API 통합, 데이터 처리, 파일 변환)

### Difficulty Levels
- `beginner`: 10분 내 이해 가능
- `intermediate`: 30분 내 적용 가능
- `advanced`: 아키텍처 레벨

### Content Rules
- Images: Minimum 3 per post (`[IMAGE_DESC: ...]` placeholders)
- Code: Must be executable, use Anthropic SDK
- Prohibited: "자동 생성", "AI Pipeline" in content/tags

### GitHub Secrets Required
- `ANTHROPIC_API_KEY`: Claude API key for skill generation

## Creation Guidelines

콘텐츠 생성 시 반드시 아래 도구를 사용하세요:

| 생성 대상 | 사용할 도구 |
|----------|------------|
| Skill 생성 | `skill-creator` |
| Agent/Subagent 생성 | `subagent-creator` |
| Hook 생성 | `hook-creator` |
| Slash Command 생성 | `slash-command-creator` |

---

## Blog Post Guidelines

### 필수 첨부 파일 구조

블로그 게시글 작성 시 실제 사용 가능한 코드/설정 파일을 `_data/templates/` 폴더에 저장하고 링크합니다.

```
_data/templates/
├── agents/                     # Agent 정의 파일
│   └── {agent-name}.md
│
├── skills/                     # Skill 패키지
│   └── {skill-name}/
│       ├── SKILL.md           # 스킬 문서
│       ├── reference/         # 참조 문서
│       │   └── ref.md
│       └── scripts/           # 실행 스크립트
│           └── main.py
│
├── commands/                   # Slash Command 정의
│   └── {command-name}.md
│
└── hooks/                      # Hook 정의
    └── {hook-name}.py (또는 .md)
```

### 게시글 작성 규칙

1. **폴더 구조 시각화** - 반드시 트리 구조로 표현
   ```
   project/
   ├── src/
   │   └── main.py
   └── README.md
   ```

2. **순서도/흐름도** - Mermaid 또는 ASCII 아트 사용
   ```
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │  Input  │───▶│ Process │───▶│ Output  │
   └─────────┘    └─────────┘    └─────────┘
   ```

3. **단계별 설명** - 번호와 아이콘으로 가독성 향상
   ```markdown
   ### 🔧 Step 1: 환경 설정
   ### 📝 Step 2: 코드 작성
   ### ▶️ Step 3: 실행
   ### ✅ Step 4: 검증
   ```

4. **첨부 파일 링크** - 템플릿 파일 참조
   ```markdown
   > 📎 **첨부 파일**: [agent-config.md](/data/templates/agents/my-agent.md)
   ```

5. **코드 블록** - 언어 명시 및 주석 포함
   ```python
   # 📌 주요 로직 설명
   def main():
       pass
   ```

### 게시글 구조 템플릿

```markdown
## 🎯 개요
(문제 정의 및 해결 목표)

## 📁 폴더 구조
(트리 다이어그램)

## 🔄 동작 흐름
(순서도/플로우차트)

## 🛠️ 구현
### Step 1: ...
### Step 2: ...

## 💻 전체 코드
(실행 가능한 코드)

## 📎 첨부 파일
(템플릿 링크)

## ✅ 실행 결과
(스크린샷 또는 출력 예시)

## 🔗 관련 스킬
(연관 스킬 링크)
```
