#!/usr/bin/env python3
"""
AI Skill Factory - Skill Generator (Agent-based)

에이전트 기반 스킬 생성기입니다.
1. Topic Selector: 주제 선정 및 작업 계획
2. Developer: 스킬 및 포스트 작성
3. Reviewer: 검토 및 QA

사용법:
    python generate.py
    python generate.py --topic "PDF 요약 스킬"
"""

import argparse
import datetime
import subprocess
import sys
import shutil
import re
from pathlib import Path
from typing import Optional, Tuple, Dict

import pytz

# Configuration
REPO_DIR = Path(__file__).parent.parent
CLAUDE_DIR = REPO_DIR / ".claude"
RULES_DIR = CLAUDE_DIR / "rules"
AGENTS_DIR = CLAUDE_DIR / "agents"
SKILLS_DIR = CLAUDE_DIR / "skills"
POSTS_DIR = REPO_DIR / "_posts"
DATA_DIR = REPO_DIR / "_data"
LOG_DIR = REPO_DIR / "logs"


def log(message: str, level: str = "INFO") -> None:
    """로그 출력 (콘솔 + 파일)"""
    from datetime import datetime as dt
    timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"

    # 콘솔 출력 (인코딩 에러 무시)
    try:
        print(log_line, flush=True)
    except UnicodeEncodeError:
        # 이모지 등 출력 불가 문자 제거
        safe_line = log_line.encode('ascii', 'ignore').decode('ascii')
        print(safe_line, flush=True)

    # 파일에도 기록 (UTF-8)
    LOG_DIR.mkdir(exist_ok=True)
    today = dt.now().strftime("%Y-%m-%d")
    log_file = LOG_DIR / f"generator_{today}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")


def find_claude_cli() -> str:
    """Find claude executable."""
    claude_path = shutil.which("claude")
    if claude_path:
        return claude_path
    if sys.platform == "win32":
        claude_cmd = shutil.which("claude.cmd")
        if claude_cmd:
            return claude_cmd
    return "claude"


def call_claude(prompt: str, system: Optional[str] = None) -> str:
    """Call Claude CLI and return response."""
    claude_exe = find_claude_cli()

    cmd = [claude_exe, "-p", "--model", "sonnet", "--output-format", "text"]
    if system:
        cmd.extend(["--system-prompt", system])

    print("  [Claude CLI] 호출 중...", flush=True)

    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=300,
        encoding="utf-8",
        shell=(sys.platform == "win32"),
    )

    if result.returncode != 0:
        raise RuntimeError(f"Claude CLI 실패: {result.stderr}")

    response = result.stdout.strip()
    if not response:
        raise RuntimeError("Claude CLI 빈 응답")

    print("  [Claude CLI] 완료", flush=True)
    return response


def load_agent(agent_name: str) -> str:
    """Load agent prompt from .claude/agents/."""
    agent_file = AGENTS_DIR / f"{agent_name}.md"
    if agent_file.exists():
        return agent_file.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Agent not found: {agent_file}")


def load_rules() -> str:
    """Load topic selection rules from .claude/rules/."""
    rules_file = RULES_DIR / "topic-selection.md"
    if rules_file.exists():
        return rules_file.read_text(encoding="utf-8")
    return ""


def get_existing_skills() -> list:
    """Get list of existing skill names."""
    skills = []

    # Check skills directory
    if SKILLS_DIR.exists():
        skills.extend([d.name for d in SKILLS_DIR.iterdir() if d.is_dir()])

    # Check agents directory
    agents_dir = CLAUDE_DIR / "agents"
    if agents_dir.exists():
        skills.extend([f.stem for f in agents_dir.glob("*.md")])

    return skills


# ┌─────────────────────────────────────────────────────────────┐
# │  Step 1: Topic Selection                                     │
# └─────────────────────────────────────────────────────────────┘

def run_topic_selector(user_topic: Optional[str] = None) -> Dict[str, str]:
    """
    Run Topic Selector agent to choose topic and create work plan.

    Returns:
        dict with keys: name, title, category, difficulty, tags, description, work_plan
    """
    log("=== Topic Selector 에이전트 시작 ===")

    agent_prompt = load_agent("topic-selector")
    log("topic-selector 프롬프트 로드 완료")

    rules = load_rules()
    existing = get_existing_skills()
    existing_str = ", ".join(existing) if existing else "없음"
    log(f"기존 스킬: {len(existing)}개")

    if user_topic:
        topic_instruction = f'사용자 요청 주제: "{user_topic}"'
        log(f"사용자 지정 주제: {user_topic}")
    else:
        topic_instruction = "키워드 풀과 트렌드를 참고하여 새로운 주제를 선정하세요."
        log("자동 주제 선정 모드")

    prompt = f"""## 규칙
{rules}

## 기존 스킬 (중복 방지)
{existing_str}

## 작업
{topic_instruction}

위 규칙과 에이전트 지침을 따라 주제를 선정하고 작업 계획을 출력하세요.
"""

    log("Claude CLI 호출 중...")
    response = call_claude(prompt, system=agent_prompt)
    log("Claude CLI 응답 수신")

    # Parse topic selection response
    topic_info = parse_topic_response(response)

    log(f"=== Topic Selector 완료 ===")
    log(f"  선정된 주제: {topic_info.get('name', 'unknown')}")
    log(f"  제목: {topic_info.get('title', 'unknown')}")
    log(f"  → Developer 에이전트로 전달")

    return topic_info


def parse_topic_response(response: str) -> Dict[str, str]:
    """Parse Topic Selector response."""
    result = {
        "name": "",
        "title": "",
        "category": "Skill",
        "difficulty": "intermediate",
        "tags": "",
        "description": "",
        "work_plan": "",
    }

    current_section = None
    content_lines = []

    for line in response.split('\n'):
        stripped = line.strip()

        if stripped == '---TOPIC---':
            if current_section and content_lines:
                result[current_section] = '\n'.join(content_lines).strip()
            current_section = 'topic'
            content_lines = []
        elif stripped == '---WORK_PLAN---':
            if current_section == 'topic':
                # Parse topic metadata
                topic_text = '\n'.join(content_lines)
                for topic_line in topic_text.split('\n'):
                    if topic_line.startswith('name:'):
                        result['name'] = topic_line.split(':', 1)[1].strip()
                    elif topic_line.startswith('title:'):
                        result['title'] = topic_line.split(':', 1)[1].strip()
                    elif topic_line.startswith('category:'):
                        result['category'] = topic_line.split(':', 1)[1].strip()
                    elif topic_line.startswith('difficulty:'):
                        result['difficulty'] = topic_line.split(':', 1)[1].strip()
                    elif topic_line.startswith('tags:'):
                        result['tags'] = topic_line.split(':', 1)[1].strip()
                    elif topic_line.startswith('description:'):
                        result['description'] = topic_line.split(':', 1)[1].strip()
            current_section = 'work_plan'
            content_lines = []
        elif stripped == '---NOTES---':
            if current_section and content_lines:
                result[current_section] = '\n'.join(content_lines).strip()
            current_section = 'notes'
            content_lines = []
        else:
            content_lines.append(line)

    if current_section and content_lines:
        result[current_section] = '\n'.join(content_lines).strip()

    # Fallback: try to extract from response if parsing failed
    if not result['name']:
        for line in response.split('\n'):
            if 'name:' in line.lower():
                result['name'] = line.split(':', 1)[1].strip()
                break

    if not result['name']:
        result['name'] = 'generated-skill'
    if not result['title']:
        result['title'] = result['name']

    return result


# ┌─────────────────────────────────────────────────────────────┐
# │  Step 2: Development                                         │
# └─────────────────────────────────────────────────────────────┘

def run_developer(topic_info: Dict[str, str]) -> Tuple[str, str]:
    """
    Run Developer agent to create skill and post.

    Returns:
        (skill_md, post_content)
    """
    log("=== Developer 에이전트 시작 ===")
    log(f"  주제: {topic_info['name']}")

    agent_prompt = load_agent("developer")
    log("developer 프롬프트 로드 완료")

    prompt = f"""## 중요 지시사항
- 도구를 사용하지 마세요. 권한 요청을 하지 마세요.
- 바로 아래 Output Format에 맞춰 텍스트를 출력하세요.
- ---CONTENT--- 로 시작해서 콘텐츠를 출력하세요.

## 주제 정보
name: {topic_info['name']}
title: {topic_info['title']}
category: {topic_info['category']}
difficulty: {topic_info['difficulty']}
tags: {topic_info['tags']}
description: {topic_info['description']}

## 작업 계획
{topic_info.get('work_plan', '기본 스킬 생성')}

## Output Format (정확히 따르세요!)

⚠️ 콘텐츠 파일에는 YAML frontmatter를 넣지 마세요!
⚠️ 블로그 포스트에만 YAML frontmatter를 넣으세요.

---CONTENT---
# 제목
(콘텐츠 내용 - YAML frontmatter 없이!)

---POST---
---
layout: post
title: "한글 제목"
date: 2026-01-22 12:00:00 +0900
categories: [AI, {topic_info['category']}]
tags: [태그들]
---

## 개요
(이하 내용...)

## 파일 위치
| 구분 | 경로 |
|------|------|
| 정의 파일 | /assets/downloads/... |
| 설치 위치 | ~/.claude/... |

---FILES---
(생성될 파일 경로 목록)

지금 바로 ---CONTENT--- 부터 시작하여 콘텐츠를 출력하세요.
"""
    log("Claude CLI 호출 중...")

    response = call_claude(prompt, system=agent_prompt)
    log("Claude CLI 응답 수신")

    # 디버그: 응답 저장
    debug_file = LOG_DIR / f"developer_response_{topic_info['name']}.txt"
    debug_file.write_text(response, encoding="utf-8")
    log(f"  응답 저장: {debug_file}")

    # Parse developer response
    skill_md, post_content = parse_developer_response(response)

    log(f"=== Developer 완료 ===")
    log(f"  SKILL.md: {len(skill_md)} chars")
    log(f"  POST: {len(post_content)} chars")
    log(f"  → Reviewer 에이전트로 전달")

    return skill_md, post_content


def parse_developer_response(response: str) -> Tuple[str, str]:
    """Parse Developer response into skill_md and post_content."""
    log("  응답 파싱 시작...")

    # 정확한 구분자로 분리 (첫 번째만 사용)
    skill_md = ""
    post_content = ""

    # ---CONTENT--- 또는 ---SKILL.md--- 와 ---POST--- 구분자 찾기
    skill_start = response.find('---CONTENT---')
    delimiter_len = 13  # len('---CONTENT---')
    if skill_start == -1:
        skill_start = response.find('---SKILL.md---')
        delimiter_len = 14  # len('---SKILL.md---')
    if skill_start == -1:
        skill_start = response.find('---SKILL---')
        delimiter_len = 11  # len('---SKILL---')

    post_start = response.find('---POST---')
    if post_start == -1:
        post_start = response.find('---BLOG---')

    files_start = response.find('---FILES---')
    if files_start == -1:
        files_start = len(response)

    # CONTENT/SKILL 추출
    if skill_start != -1:
        skill_end = post_start if post_start > skill_start else files_start
        skill_md = response[skill_start + delimiter_len:skill_end].strip()
        if skill_md.startswith('---'):
            skill_md = skill_md[skill_md.find('---', 3):]  # SKILL--- 제거

    # POST 추출
    if post_start != -1:
        post_end = files_start if files_start > post_start else len(response)
        post_content = response[post_start + 9:post_end].strip()  # len('---POST---') = 9

    # 파싱 실패 시 응답 전체 로깅
    if not skill_md and not post_content:
        log("  [경고] 파싱 실패! 응답 미리보기:", "WARN")
        preview = response[:500].replace('\n', '\\n')
        log(f"  {preview}...", "WARN")

    log(f"  파싱 결과: SKILL={len(skill_md)}chars, POST={len(post_content)}chars")
    return skill_md, post_content


# ┌─────────────────────────────────────────────────────────────┐
# │  Step 3: Review                                              │
# └─────────────────────────────────────────────────────────────┘

def run_reviewer(topic_info: Dict[str, str], skill_md: str, post_content: str) -> Tuple[bool, str, str]:
    """
    Run Reviewer agent to validate and QA.

    Returns:
        (approved, final_skill_md, final_post_content)
    """
    log("=== Reviewer 에이전트 시작 ===")
    log(f"  주제: {topic_info['name']}")

    agent_prompt = load_agent("reviewer")
    log("reviewer 프롬프트 로드 완료")

    prompt = f"""## 검토 대상

### 주제 정보
name: {topic_info['name']}
title: {topic_info['title']}
category: {topic_info['category']}

### SKILL.md
```markdown
{skill_md}
```

### 블로그 포스트
```markdown
{post_content}
```

위 내용을 검토하고 결과를 출력하세요.
문제가 있으면 직접 수정한 버전도 함께 출력하세요.
"""

    log("Claude CLI 호출 중...")
    response = call_claude(prompt, system=agent_prompt)
    log("Claude CLI 응답 수신")

    # Parse review result
    approved, final_skill, final_post = parse_reviewer_response(
        response, skill_md, post_content
    )

    status = "APPROVED" if approved else "NEEDS_REVISION"
    log(f"=== Reviewer 완료 ===")
    log(f"  검토 결과: {status}")

    return approved, final_skill, final_post


def parse_reviewer_response(
    response: str, original_skill: str, original_post: str
) -> Tuple[bool, str, str]:
    """Parse Reviewer response."""
    approved = "APPROVED" in response and "NEEDS_REVISION" not in response

    # Check if reviewer provided fixed versions
    fixed_skill = original_skill
    fixed_post = original_post

    # Try to extract fixed content if provided
    if "---FIXED_SKILL---" in response or "---SKILL.md---" in response or "---CONTENT---" in response:
        # Try ---CONTENT--- first, then ---SKILL.md---
        if "---CONTENT---" in response:
            parts = response.split("---CONTENT---")
        else:
            parts = response.split("---SKILL.md---")
        if len(parts) > 1:
            skill_part = parts[1].split("---")[0].strip()
            if skill_part:
                fixed_skill = skill_part

    if "---FIXED_POST---" in response or "---POST---" in response:
        parts = response.split("---POST---")
        if len(parts) > 1:
            post_part = parts[1].split("---")[0].strip()
            if post_part:
                fixed_post = post_part

    return approved, fixed_skill, fixed_post


# ┌─────────────────────────────────────────────────────────────┐
# │  YAML Validation                                             │
# └─────────────────────────────────────────────────────────────┘

def remove_yaml_frontmatter(content: str) -> str:
    """
    YAML frontmatter 제거 (콘텐츠 파일용)
    Jekyll이 HTML로 변환하지 않도록 frontmatter를 제거합니다.
    """
    lines = content.strip().split('\n')

    # frontmatter가 없으면 그대로 반환
    if not lines or lines[0].strip() != '---':
        return content

    # 닫는 --- 찾기
    closing_idx = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            closing_idx = i
            break

    # 닫는 ---가 없으면 그대로 반환
    if closing_idx == -1:
        return content

    # frontmatter 제거하고 나머지 반환
    remaining = '\n'.join(lines[closing_idx + 1:]).strip()
    return remaining


def validate_yaml_frontmatter(content: str, name: str) -> Tuple[bool, str]:
    """
    YAML frontmatter 유효성 검증

    Returns:
        (is_valid, fixed_content)
    """
    import yaml

    lines = content.strip().split('\n')

    # Check if starts with ---
    if not lines or lines[0].strip() != '---':
        log(f"[YAML FIX] {name}: frontmatter 시작 --- 누락, 추가", "WARN")
        # Add frontmatter
        fixed = f"""---
name: {name}
description: {name} 스킬
version: 1.0.0
author: AI Skill Factory
---

{content}"""
        return False, fixed

    # Find closing ---
    closing_idx = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            closing_idx = i
            break

    if closing_idx == -1:
        log(f"[YAML FIX] {name}: frontmatter 닫는 --- 누락, 수정", "WARN")
        # Find where content starts (first non-empty line after ---)
        content_start = 1
        for i, line in enumerate(lines[1:], 1):
            if line.strip() and not line.strip().startswith('#') and ':' not in line:
                content_start = i
                break

        # Insert closing --- and add missing fields
        fixed_lines = ['---']
        fixed_lines.append(f'name: {name}')
        fixed_lines.append(f'description: {name} 스킬')
        fixed_lines.append('version: 1.0.0')
        fixed_lines.append('author: AI Skill Factory')
        fixed_lines.append('---')
        fixed_lines.append('')
        fixed_lines.extend(lines[content_start:])
        return False, '\n'.join(fixed_lines)

    # Extract frontmatter content
    frontmatter_lines = lines[1:closing_idx]
    frontmatter_str = '\n'.join(frontmatter_lines)

    # Check if frontmatter is empty or invalid
    if not frontmatter_str.strip():
        log(f"[YAML FIX] {name}: frontmatter 내용 없음, 추가", "WARN")
        fixed_lines = ['---']
        fixed_lines.append(f'name: {name}')
        fixed_lines.append(f'description: {name} 스킬')
        fixed_lines.append('version: 1.0.0')
        fixed_lines.append('author: AI Skill Factory')
        fixed_lines.append('---')
        fixed_lines.extend(lines[closing_idx + 1:])
        return False, '\n'.join(fixed_lines)

    # Try to parse YAML
    try:
        data = yaml.safe_load(frontmatter_str)
        if data is None:
            raise ValueError("Empty YAML")

        # Check required fields for SKILL.md
        if 'name' not in data:
            log(f"[YAML FIX] {name}: name 필드 누락, 추가", "WARN")
            frontmatter_lines.insert(0, f'name: {name}')
        if 'description' not in data:
            log(f"[YAML FIX] {name}: description 필드 누락, 추가", "WARN")
            frontmatter_lines.append(f'description: {name} 스킬')

        # Rebuild content
        fixed_lines = ['---']
        fixed_lines.extend(frontmatter_lines)
        fixed_lines.append('---')
        fixed_lines.extend(lines[closing_idx + 1:])
        return True, '\n'.join(fixed_lines)

    except Exception as e:
        log(f"[YAML FIX] {name}: YAML 파싱 실패 ({e}), 재생성", "WARN")
        fixed_lines = ['---']
        fixed_lines.append(f'name: {name}')
        fixed_lines.append(f'description: {name} 스킬')
        fixed_lines.append('version: 1.0.0')
        fixed_lines.append('author: AI Skill Factory')
        fixed_lines.append('---')
        fixed_lines.extend(lines[closing_idx + 1:])
        return False, '\n'.join(fixed_lines)


# ┌─────────────────────────────────────────────────────────────┐
# │  File Operations                                             │
# └─────────────────────────────────────────────────────────────┘

def save_skill(name: str, category: str, skill_md: str) -> Path:
    """Save skill files to appropriate .claude/ directory."""
    # YAML frontmatter 제거 (Jekyll이 HTML로 변환하지 않도록)
    skill_md = remove_yaml_frontmatter(skill_md)
    log(f"  콘텐츠 파일 저장 (frontmatter 없음): {name}")

    category_lower = category.lower()

    if category_lower == "skill":
        skill_dir = SKILLS_DIR / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
    elif category_lower == "agent":
        skill_dir = AGENTS_DIR
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / f"{name}.md"
    elif category_lower == "hook":
        skill_dir = CLAUDE_DIR / "hooks"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / f"{name}.md"
    elif category_lower == "command":
        skill_dir = CLAUDE_DIR / "commands"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / f"{name}.md"
    elif category_lower == "script":
        skill_dir = CLAUDE_DIR / "scripts"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / f"{name}.py"
    elif category_lower == "workflow":
        skill_dir = CLAUDE_DIR / "workflows"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / f"{name}.md"
    else:
        # Default to skills
        skill_dir = SKILLS_DIR / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"

    skill_file.write_text(skill_md, encoding="utf-8")

    return skill_dir


def save_post(name: str, post_content: str) -> Path:
    """Save blog post to _posts/."""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    kst = pytz.timezone("Asia/Seoul")
    today = datetime.datetime.now(kst).strftime("%Y-%m-%d")

    post_file = POSTS_DIR / f"{today}-{name}.md"
    post_file.write_text(post_content, encoding="utf-8")

    return post_file


# ┌─────────────────────────────────────────────────────────────┐
# │  Main Pipeline                                               │
# └─────────────────────────────────────────────────────────────┘

def generate_skill(user_topic: Optional[str] = None, max_retries: int = 3) -> Tuple[str, str, str, str]:
    """
    Generate a skill using agent-based pipeline.

    Args:
        user_topic: Optional topic from user
        max_retries: Maximum retry attempts when review fails

    Returns:
        (name, title, skill_md, post_content)
    """
    # Step 1: Topic Selection
    topic_info = run_topic_selector(user_topic)

    for attempt in range(max_retries):
        log(f"========== 시도 {attempt + 1}/{max_retries} ==========")

        # Step 2: Development
        skill_md, post_content = run_developer(topic_info)

        # Step 3: Review
        approved, skill_md, post_content = run_reviewer(topic_info, skill_md, post_content)

        if approved:
            log("[OK] 리뷰 승인됨!")
            log(f"  → 파일 저장 단계로 진행")
            break
        else:
            if attempt < max_retries - 1:
                log(f"[RETRY] 리뷰어가 반려함. Developer로 다시 전달합니다.", "WARN")
                # Reviewer의 피드백을 work_plan에 추가하여 Developer가 참고하도록 함
                topic_info['work_plan'] = f"이전 시도 수정 필요.\n{topic_info.get('work_plan', '')}"
            else:
                log("최대 재시도 횟수 도달. 마지막 버전을 사용합니다.", "WARN")

    return (
        topic_info['name'],
        topic_info['title'],
        skill_md,
        post_content,
    )


def main():
    parser = argparse.ArgumentParser(description="AI Skill Factory - Agent-based Generator")
    parser.add_argument("--topic", type=str, help="생성할 스킬 주제")
    parser.add_argument("--skip-review", action="store_true", help="리뷰 단계 건너뛰기")
    args = parser.parse_args()

    log("=" * 60)
    log("AI Skill Factory - Agent-based Generator")
    log("=" * 60)

    try:
        # Generate skill
        name, title, skill_md, post_content = generate_skill(args.topic)

        log("=== 결과 ===")
        log(f"  Name: {name}")
        log(f"  Title: {title}")

        # Determine category from skill_md or default
        category = "Skill"
        for line in skill_md.split('\n')[:10]:
            if line.startswith('category:'):
                category = line.split(':', 1)[1].strip()
                break

        # Save files
        log("=== 파일 저장 ===")
        skill_dir = save_skill(name, category, skill_md)
        log(f"  Skill: {skill_dir}")

        post_file = save_post(name, post_content)
        log(f"  Post: {post_file}")

        log("=" * 60)
        log("SUCCESS! 스킬 생성 완료!")
        log("=" * 60)

        return 0

    except Exception as e:
        log(f"오류 발생: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
