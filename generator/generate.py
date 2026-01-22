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
    print("\n>>> Step 1: Topic Selection", flush=True)

    agent_prompt = load_agent("topic-selector")
    rules = load_rules()
    existing = get_existing_skills()
    existing_str = ", ".join(existing) if existing else "없음"

    if user_topic:
        topic_instruction = f'사용자 요청 주제: "{user_topic}"'
    else:
        topic_instruction = "키워드 풀과 트렌드를 참고하여 새로운 주제를 선정하세요."

    prompt = f"""## 규칙
{rules}

## 기존 스킬 (중복 방지)
{existing_str}

## 작업
{topic_instruction}

위 규칙과 에이전트 지침을 따라 주제를 선정하고 작업 계획을 출력하세요.
"""

    response = call_claude(prompt, system=agent_prompt)

    # Parse topic selection response
    topic_info = parse_topic_response(response)

    print(f"  선정된 주제: {topic_info.get('name', 'unknown')}", flush=True)
    print(f"  제목: {topic_info.get('title', 'unknown')}", flush=True)

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
    print("\n>>> Step 2: Development", flush=True)

    agent_prompt = load_agent("developer")

    prompt = f"""## 주제 정보
name: {topic_info['name']}
title: {topic_info['title']}
category: {topic_info['category']}
difficulty: {topic_info['difficulty']}
tags: {topic_info['tags']}
description: {topic_info['description']}

## 작업 계획
{topic_info.get('work_plan', '기본 스킬 생성')}

위 정보를 바탕으로 SKILL.md와 블로그 포스트를 작성하세요.
에이전트 지침의 Output Format을 따르세요.
"""

    response = call_claude(prompt, system=agent_prompt)

    # Parse developer response
    skill_md, post_content = parse_developer_response(response)

    print(f"  SKILL.md: {len(skill_md)} chars", flush=True)
    print(f"  POST: {len(post_content)} chars", flush=True)

    return skill_md, post_content


def parse_developer_response(response: str) -> Tuple[str, str]:
    """Parse Developer response into skill_md and post_content."""
    parts = {}
    current_section = None
    current_content = []

    for line in response.split('\n'):
        stripped = line.strip()

        if stripped == '---SKILL.md---':
            if current_section:
                parts[current_section] = '\n'.join(current_content).strip()
            current_section = 'skill'
            current_content = []
        elif stripped == '---POST---':
            if current_section:
                parts[current_section] = '\n'.join(current_content).strip()
            current_section = 'post'
            current_content = []
        elif stripped == '---FILES---':
            if current_section:
                parts[current_section] = '\n'.join(current_content).strip()
            current_section = 'files'
            current_content = []
        else:
            current_content.append(line)

    if current_section:
        parts[current_section] = '\n'.join(current_content).strip()

    skill_md = parts.get('skill', '')
    post_content = parts.get('post', '')

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
    print("\n>>> Step 3: Review", flush=True)

    agent_prompt = load_agent("reviewer")

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

    response = call_claude(prompt, system=agent_prompt)

    # Parse review result
    approved, final_skill, final_post = parse_reviewer_response(
        response, skill_md, post_content
    )

    status = "APPROVED" if approved else "NEEDS_REVISION"
    print(f"  검토 결과: {status}", flush=True)

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
    if "---FIXED_SKILL---" in response or "---SKILL.md---" in response:
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
# │  File Operations                                             │
# └─────────────────────────────────────────────────────────────┘

def save_skill(name: str, category: str, skill_md: str) -> Path:
    """Save skill files to appropriate .claude/ directory."""
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

def generate_skill(user_topic: Optional[str] = None) -> Tuple[str, str, str, str]:
    """
    Generate a skill using agent-based pipeline.

    Returns:
        (name, title, skill_md, post_content)
    """
    # Step 1: Topic Selection
    topic_info = run_topic_selector(user_topic)

    # Step 2: Development
    skill_md, post_content = run_developer(topic_info)

    # Step 3: Review
    approved, skill_md, post_content = run_reviewer(topic_info, skill_md, post_content)

    if not approved:
        print("  [WARNING] 리뷰어가 수정을 권장했습니다. 수정된 버전을 사용합니다.", flush=True)

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

    print("=" * 60)
    print("AI Skill Factory - Agent-based Generator")
    print("=" * 60)

    try:
        # Generate skill
        name, title, skill_md, post_content = generate_skill(args.topic)

        print(f"\n>>> 결과")
        print(f"  Name: {name}")
        print(f"  Title: {title}")

        # Determine category from skill_md or default
        category = "Skill"
        for line in skill_md.split('\n')[:10]:
            if line.startswith('category:'):
                category = line.split(':', 1)[1].strip()
                break

        # Save files
        print("\n>>> 파일 저장")
        skill_dir = save_skill(name, category, skill_md)
        print(f"  Skill: {skill_dir}")

        post_file = save_post(name, post_content)
        print(f"  Post: {post_file}")

        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)

        return 0

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
