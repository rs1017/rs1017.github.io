"""
File utilities for AI Skill Factory.
"""

import datetime
from pathlib import Path
from typing import Any, Dict

import yaml


def save_skill(
    skills_dir: Path,
    skill_name: str,
    skill_md: str,
    code: str,
) -> Path:
    """
    Save skill files to the skills directory.

    Returns the skill directory path.
    """
    skill_dir = skills_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Save SKILL.md
    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md, encoding="utf-8")

    # Save index.md (copy of SKILL.md for Jekyll routing)
    index_path = skill_dir / "index.md"
    index_path.write_text(skill_md, encoding="utf-8")

    # Save example.py
    example_path = skill_dir / "example.py"
    example_path.write_text(code, encoding="utf-8")

    return skill_dir


def save_post(
    posts_dir: Path,
    date_str: str,
    slug: str,
    content: str,
) -> Path:
    """
    Save a blog post to the _posts directory.

    Returns the post file path.
    """
    posts_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{date_str}-{slug}.md"
    post_path = posts_dir / filename
    post_path.write_text(content, encoding="utf-8")

    return post_path


def update_registry(
    registry_path: Path,
    topic_info: Dict[str, Any],
    skill_name: str,
    date_str: str,
) -> None:
    """
    Update the skill registry with new skill information.
    """
    # Load existing registry or create new
    if registry_path.exists():
        content = registry_path.read_text(encoding="utf-8")
        registry = yaml.safe_load(content) or {}
    else:
        registry = {
            "last_updated": None,
            "total_skills": 0,
            "categories": {
                "Workflow": {"count": 0, "skills": []},
                "Agent": {"count": 0, "skills": []},
                "Skill": {"count": 0, "skills": []},
            },
            "skills": [],
            "statistics": {
                "by_difficulty": {"beginner": 0, "intermediate": 0, "advanced": 0},
                "by_month": {},
            },
        }

    # Update timestamp
    registry["last_updated"] = datetime.datetime.now().isoformat()

    # Get skill info
    category = topic_info.get("category", "Skill")
    difficulty = topic_info.get("difficulty", "intermediate")
    tags = topic_info.get("tags", [])

    # Create skill entry
    skill_entry = {
        "name": skill_name,
        "title": topic_info.get("topic", skill_name),
        "category": category,
        "difficulty": difficulty,
        "tags": tags,
        "created_at": date_str,
        "post_path": f"/posts/{skill_name}/",
        "skill_path": f"/skills/{skill_name}/",
    }

    # Add to skills list
    if "skills" not in registry:
        registry["skills"] = []
    registry["skills"].append(skill_entry)

    # Update category count
    if category in registry.get("categories", {}):
        registry["categories"][category]["count"] += 1
        registry["categories"][category]["skills"].append({
            "name": skill_name,
            "difficulty": difficulty,
            "created_at": date_str,
        })

    # Update total count
    registry["total_skills"] = len(registry["skills"])

    # Update statistics
    if "statistics" not in registry:
        registry["statistics"] = {
            "by_difficulty": {"beginner": 0, "intermediate": 0, "advanced": 0},
            "by_month": {},
        }

    if difficulty in registry["statistics"]["by_difficulty"]:
        registry["statistics"]["by_difficulty"][difficulty] += 1

    # Update monthly stats
    month_key = date_str[:7]  # YYYY-MM
    if month_key not in registry["statistics"]["by_month"]:
        registry["statistics"]["by_month"][month_key] = {
            "total": 0,
            "breakdown": {"Workflow": 0, "Agent": 0, "Skill": 0},
        }
    registry["statistics"]["by_month"][month_key]["total"] += 1
    registry["statistics"]["by_month"][month_key]["breakdown"][category] += 1

    # Ensure parent directory exists
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    # Save registry
    with open(registry_path, "w", encoding="utf-8") as f:
        yaml.dump(registry, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
