# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based static blog using the **Chirpy theme** (jekyll-theme-chirpy v4.3.4), hosted on GitHub Pages at https://naksupapa.github.io. The blog language is Korean (`lang: ko`).

**Working Directory**: `rs1017.github.io/` - all Jekyll commands should be run from this directory.

## Common Commands

### Setup
```bash
bundle install                  # Install Ruby dependencies
```

### Development
```bash
bundle exec jekyll serve        # Start local dev server (http://localhost:4000)
bundle exec jekyll serve --drafts  # Include draft posts
```

### Build
```bash
bundle exec jekyll b                              # Build site to _site/
JEKYLL_ENV=production bundle exec jekyll b        # Production build (used in CI)
```

### Testing
```bash
bundle exec htmlproofer _site --disable-external --allow-hash-href
```

### JavaScript Build
```bash
npx gulp                        # Production build (minified bundles)
npx gulp dev                    # Development mode with watch
```

### Deployment
Deployment runs automatically via GitHub Actions (`.github/workflows/pages-deploy.yml`) on push to main branch.

## Architecture

### Content Structure
- `_posts/` - Published blog posts (Markdown with YAML front matter)
- `_drafts/` - Draft posts (not published)
- `_tabs/` - Navigation pages (About, Archives, Categories, Tags)
- `_data/` - YAML data files and localization

### Template System
- `_layouts/` - Jekyll page layout templates (override theme defaults)
- `_includes/` - Reusable HTML/Liquid template snippets
- `_sass/` - SCSS stylesheets

### Theme Customization
The Chirpy theme is installed as a gem (`jekyll-theme-chirpy`). To customize theme files:
- Use `bundle info --path jekyll-theme-chirpy` to find theme source location
- Copy files to local project to override (e.g., `_layouts/`, `_includes/`, `_sass/`)

> **IMPORTANT: DO NOT upgrade jekyll-theme-chirpy**
> - 현재 버전(v4.3.4)에 맞춰 `_includes/`, `_sass/` 등 커스터마이징이 많이 되어 있음
> - 테마 업그레이드 시 커스터마이징 파일과 충돌하여 사이트가 깨질 수 있음
> - `bundle update jekyll-theme-chirpy` 절대 실행 금지
> - Bootstrap 4 + jQuery 사용 중 (v5 이상 버전과 호환되지 않음)

### Key Configuration
- `_config.yml` - Main Jekyll configuration
- Post permalink format: `/posts/:title/`
- Theme mode: User-selectable (toggle in sidebar) - leave `theme_mode` empty in config
- Auto-generated TOC for posts

### Custom Plugin
- `_plugins/posts-lastmod-hook.rb` - Automatically sets post `last_modified_at` from git history (only if post has >1 commit)

## Writing Posts

Posts go in `_posts/` with filename format: `YYYY-MM-DD-title.md`

### Front Matter Template
```yaml
---
title: Post Title
author: naksupapa
date: YYYY-MM-DD HH:MM:SS +0900
categories: [Category1, Category2]
tags: [tag1, tag2, tag3]
---
```

- `future: true` is enabled in `_config.yml`, so future-dated posts will be published
- Posts automatically get TOC and comments enabled via defaults in `_config.yml`

### Optional Front Matter
```yaml
image:
  path: /assets/img/posts/YYYY-MM-DD-포스트명/thumbnail.jpg
  alt: 썸네일 설명
pin: true                       # Pin post to top of home page
math: true                      # Enable MathJax
mermaid: true                   # Enable Mermaid diagrams
```

## Image & Media Management

### Folder Structure
```
assets/img/
├── avatar.jpg              # 시스템용 (사이드바 프로필)
├── favicons/               # 시스템용 (파비콘)
├── common/                 # 공용 이미지 (여러 포스트에서 사용)
└── posts/                  # 포스트별 이미지
    └── YYYY-MM-DD-포스트명/   ← 포스트 파일명과 동일 (한글 가능)
        ├── 01-photo.jpg
        ├── 02-screenshot.png
        └── demo.mp4
```

### Naming Convention
- **이미지 폴더명 = 포스트 파일명** (확장자 제외)
- 한글 폴더명/파일명 사용 가능
- 예: `_posts/2026-01-13-판교-보배반점.md` → `assets/img/posts/2026-01-13-판교-보배반점/`

### Post Creation Workflow
1. `/new-post 제목` - 템플릿 파일 + 이미지 폴더 생성 (동일한 이름)
2. 이미지 폴더에 이미지 저장
3. `/write-post 제목` - 이미지 참조하여 내용 작성

### Image Syntax
마크다운 또는 HTML 모두 사용 가능 (lazy loading 비활성화됨):

```markdown
# 마크다운 방식
![설명](/assets/img/posts/YYYY-MM-DD-포스트명/image.jpg)
![설명](/assets/img/posts/YYYY-MM-DD-포스트명/image.jpg){: .shadow }

# HTML 방식
<img src="/assets/img/posts/YYYY-MM-DD-포스트명/image.jpg" alt="설명" class="shadow" />

# 캡션 추가
![설명](/assets/img/posts/YYYY-MM-DD-포스트명/image.jpg){: .shadow }
_이미지 캡션_

# 크기 조절
![설명](/assets/img/posts/YYYY-MM-DD-포스트명/image.jpg){: width="500" }
```

### Video Embedding
```markdown
# 로컬 비디오
{% include embed/video.html src='/assets/img/posts/YYYY-MM-DD-포스트명/video.mp4' %}

# YouTube
{% include embed/youtube.html id='유튜브ID' %}
```

### Image Notes
- Lazy loading 비활성화됨 (`_includes/refactor-content.html` 수정)
- 이미지가 바로 로드됨 (data-src 대신 src 사용)

## Troubleshooting

### 사이트가 빌드되지 않거나 빈 페이지가 나오는 경우

**증상**: 사이트 접속 시 빈 페이지, 404 에러, 또는 레이아웃이 깨짐

**원인**: `_layouts/` 파일에서 `{% include lang.html %}` 누락

**확인 방법**:
```bash
# 모든 레이아웃에서 lang.html include 확인
grep -r "include lang.html" _layouts/
```

**주의사항**:
- `_layouts/home.html`, `_layouts/page.html`, `_layouts/post.html` 등에서 `{% include lang.html %}` 필수
- 이 include가 없으면 `lang` 변수가 정의되지 않아 locale 데이터 조회 실패
- **절대로 `#{% include lang.html %}`처럼 주석 처리하면 안 됨**

**수정 예시**:
```liquid
---
layout: page
---

{% include lang.html %}  <!-- 이 줄 필수! -->

{% assign pinned = site.posts | where: "pin", "true" %}
...
```

### 레이아웃 파일 수정 시 체크리스트

1. `{% include lang.html %}` 포함 여부 확인
2. `site.data.locales[lang]` 사용하는 곳에서 lang 변수 정의 확인
3. 수정 후 로컬 빌드 테스트: `bundle exec jekyll build`

## Claude Code Slash Commands

블로그 작성 워크플로우용 슬래시 커맨드가 `.claude/skills/`에 정의되어 있습니다.

| 명령어 | 설명 |
|--------|------|
| `/new-post 제목` | 새 포스트 템플릿 + 이미지 폴더 생성 |
| `/write-post 제목` | 포스트 내용 작성 |
| `/draft-to-post publish 제목` | 초안 → 발행 변환 |
| `/seo-optimizer 제목` | SEO 점수 검사 |
| `/image-optimizer 제목` | 이미지 최적화 검사 |
| `/series-post` | 시리즈 포스트 관리 |
| `/related-posts 제목` | 관련 포스트 추천 |

전체 워크플로우는 `.claude/BLOG-WORKFLOW.md` 참조.

## 블로그 자동화 파이프라인

AI 에이전트를 활용한 블로그 포스트 자동 작성 시스템입니다.

### 에이전트 목록

| 에이전트 | 역할 | 파일 |
|----------|------|------|
| **topic-selector** | 사용자와 협업하여 주제 수집/선정 | `.claude/agents/topic-selector.md` |
| **topic-researcher** | 인터넷 서치로 자료 수집 | `.claude/agents/topic-researcher.md` |
| **storyboard-creator** | 콘티 작성, 이미지/영상 프롬프트 생성 | `.claude/agents/storyboard-creator.md` |
| **post-writer** | 실제 마크다운 게시글 작성 | `.claude/agents/post-writer.md` |
| **post-reviewer** | 품질 검토, 승인/반려, 배포 | `.claude/agents/post-reviewer.md` |

### 워크플로우

```
[topic-selector] → [topic-researcher] → [storyboard-creator] → [post-writer] → [post-reviewer]
       ↑                                                                              ↓
       └──────────────────────────── 반려 시 (60점 미만) ─────────────────────────────┘
```

### 주제 관리 폴더 (`_topics/`)

```
_topics/
├── pending/      # 수집된 주제 (선정 대기)
├── selected/     # 선정 완료 (리서치 대기)
├── researched/   # 리서치 완료 (콘티 대기)
├── drafting/     # 콘티/작성 진행 중
└── review/       # 리뷰 대기
```

> **Note**: `_topics/` 폴더는 Jekyll 빌드에서 제외됨 (`_config.yml` exclude)

### 주제 파일 상태 흐름

```
pending → selected → researched → drafting → review → published
                ↑                                ↓
                └────────────── rejected ────────┘
```

자세한 워크플로우는 `.claude/workflows/auto-blog-pipeline.md` 참조.

## MCP 서버 (미디어 생성)

Claude Desktop과 연동하여 이미지/영상을 자동 생성하는 MCP 서버입니다.

### 서버 목록

| 서버 | 용도 | API | 비용 |
|------|------|-----|------|
| **image-generator** | 이미지 생성 | Pollinations.ai | 무료 |
| **video-generator** | 영상 생성 | Hugging Face Space | 무료 |

### 설치 및 설정

```bash
# 패키지 설치
pip install mcp gradio_client

# Claude Desktop 설정 파일 위치
# Windows: %APPDATA%\Claude\claude_desktop_config.json
```

설정 예제: `.claude/mcp-servers/mcp-config.example.json`

### 사용 가능한 도구

**image-generator:**
- `generate_image` - 프롬프트로 이미지 생성
- `generate_image_variations` - 여러 이미지 변형 생성

**video-generator:**
- `generate_video` - 프롬프트로 영상 생성 (ltx-video, modelscope, animatediff)
- `generate_video_from_image` - 이미지 기반 영상 생성

자세한 내용은 `.claude/mcp-servers/README.md` 참조.
