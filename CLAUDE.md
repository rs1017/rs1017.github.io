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
