#!/usr/bin/env python3
"""
AI Skill Factory - Main Generator Script
Orchestrates the skill generation pipeline using Anthropic Claude API.
"""

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import pytz
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generator.clients.gemini_client import GeminiClient
from generator.clients.claude_code_client import ClaudeCodeClient
from generator.agents.topic_selector import TopicSelectorAgent
from generator.agents.skill_designer import SkillDesignerAgent
from generator.agents.code_generator import CodeGeneratorAgent
from generator.agents.post_writer import PostWriterAgent
from generator.agents.validator import ValidatorAgent
from generator.utils.file_utils import save_skill, save_post, update_registry
from generator.utils.slug_utils import normalize_filename
from generator.utils.git_utils import commit_and_push, has_changes

load_dotenv()

# Configuration
BLOG_DIR = Path(__file__).parent.parent
SKILLS_DIR = BLOG_DIR / ".claude" / "skills"
POSTS_DIR = BLOG_DIR / "_posts"
DATA_DIR = BLOG_DIR / "_data"
PROMPTS_DIR = Path(__file__).parent / "prompts"
SOURCES_DIR = Path(__file__).parent / "sources"


class SkillFactoryPipeline:
    """Main pipeline orchestrator for AI Skill Factory."""

    def __init__(self, use_claude_cli: bool = False) -> None:
        """Initialize the pipeline.

        Args:
            use_claude_cli: If True, use Claude Code CLI instead of Gemini API
        """
        if use_claude_cli:
            self.client = ClaudeCodeClient()
        else:
            self.client = GeminiClient()
        self.topic_selector = TopicSelectorAgent(self.client, PROMPTS_DIR)
        self.skill_designer = SkillDesignerAgent(self.client, PROMPTS_DIR)
        self.code_generator = CodeGeneratorAgent(self.client, PROMPTS_DIR)
        self.post_writer = PostWriterAgent(self.client, PROMPTS_DIR)
        self.validator = ValidatorAgent(self.client, PROMPTS_DIR)

        self.kst = pytz.timezone("Asia/Seoul")

    def run(
        self, strategy: str = "auto", user_topic: Optional[str] = None,
        skip_validation: bool = False
    ) -> bool:
        """Execute the full 6-step pipeline."""
        print("=" * 60)
        print("AI Skill Factory - Generation Pipeline")
        print("=" * 60)

        try:
            # Step 1: Topic Selection
            topic_info = self._step_1_select_topic(strategy, user_topic)

            # Step 2: Skill Design
            skill_md = self._step_2_design_skill(topic_info)

            # Step 3: Code Generation
            example_code = self._step_3_generate_code(topic_info, skill_md)

            # Step 4: Post Writing
            date_str, slug, post_content = self._step_4_write_post(
                topic_info, skill_md, example_code
            )

            # Step 5: Validation
            if skip_validation:
                print("\n>>> Step 5: Validation (SKIPPED)")
                validation_result = {"approved": True, "score": 0, "warnings": ["Validation skipped"]}
            else:
                validation_result = self._step_5_validate(
                    skill_md, example_code, post_content
                )

                if not validation_result["approved"]:
                    print(f"\n[REJECTED] {validation_result['reason']}")
                    print("Errors:")
                    for error in validation_result.get("errors", []):
                        print(f"  - {error}")
                    return False

            # Step 6: Save Files
            self._step_6_save_files(
                topic_info, skill_md, example_code, post_content, date_str, slug
            )

            print("\n" + "=" * 60)
            print("SUCCESS: Skill generated successfully!")
            print(f"  Skill: skills/{slug}/")
            print(f"  Post: _posts/{date_str}-{slug}.md")
            print("=" * 60)
            return True

        except Exception as e:
            print(f"\n[ERROR] Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _step_1_select_topic(
        self, strategy: str, user_topic: Optional[str]
    ) -> Dict[str, Any]:
        """Step 1: Select topic using specified strategy."""
        print("\n>>> Step 1: Selecting Topic")

        existing_skills = self._get_existing_skills()
        sources = self._load_sources()

        topic_info = self.topic_selector.select(
            strategy=strategy,
            user_topic=user_topic,
            existing_skills=existing_skills,
            sources=sources,
        )

        print(f"  Topic: {topic_info.get('topic', 'Unknown')}")
        print(f"  Category: {topic_info.get('category', 'Unknown')}")
        print(f"  Difficulty: {topic_info.get('difficulty', 'Unknown')}")
        print(f"  Strategy: {topic_info.get('strategy_used', 'Unknown')}")

        return topic_info

    def _step_2_design_skill(self, topic_info: Dict[str, Any]) -> str:
        """Step 2: Design SKILL.md structure."""
        print("\n>>> Step 2: Designing Skill")

        skill_md = self.skill_designer.design(topic_info)
        print(f"  SKILL.md generated ({len(skill_md)} chars)")

        return skill_md

    def _step_3_generate_code(
        self, topic_info: Dict[str, Any], skill_md: str
    ) -> str:
        """Step 3: Generate executable example code."""
        print("\n>>> Step 3: Generating Code")

        code = self.code_generator.generate(topic_info, skill_md)
        print(f"  example.py generated ({len(code)} chars)")

        return code

    def _step_4_write_post(
        self, topic_info: Dict[str, Any], skill_md: str, code: str
    ) -> tuple[str, str, str]:
        """Step 4: Write blog post."""
        print("\n>>> Step 4: Writing Post")

        now = datetime.datetime.now(self.kst)
        date_str = now.strftime("%Y-%m-%d")
        slug = normalize_filename(topic_info.get("topic", "unknown-skill"))

        post_content = self.post_writer.write(
            topic_info=topic_info,
            skill_md=skill_md,
            code=code,
            date_str=date_str,
            slug=slug,
        )

        print(f"  Post generated ({len(post_content)} chars)")
        print(f"  Date: {date_str}")
        print(f"  Slug: {slug}")

        return date_str, slug, post_content

    def _step_5_validate(
        self, skill_md: str, code: str, post: str
    ) -> Dict[str, Any]:
        """Step 5: Validate all generated content."""
        print("\n>>> Step 5: Validating")

        result = self.validator.validate(skill_md, code, post)

        status = "APPROVED" if result["approved"] else "REJECTED"
        print(f"  Status: {status}")
        print(f"  Score: {result['score']}/100")

        if result.get("warnings"):
            print("  Warnings:")
            for warning in result["warnings"]:
                print(f"    - {warning}")

        return result

    def _step_6_save_files(
        self,
        topic_info: Dict[str, Any],
        skill_md: str,
        code: str,
        post: str,
        date_str: str,
        slug: str,
    ) -> None:
        """Step 6: Save all generated files."""
        print("\n>>> Step 6: Saving Files")

        # Save skill files
        skill_dir = save_skill(SKILLS_DIR, slug, skill_md, code)
        print(f"  Saved: {skill_dir.relative_to(BLOG_DIR)}/SKILL.md")
        print(f"  Saved: {skill_dir.relative_to(BLOG_DIR)}/example.py")

        # Save post
        post_path = save_post(POSTS_DIR, date_str, slug, post)
        print(f"  Saved: {post_path.relative_to(BLOG_DIR)}")

        # Update registry
        registry_path = DATA_DIR / "skill_registry.yml"
        update_registry(registry_path, topic_info, slug, date_str)
        print(f"  Updated: {registry_path.relative_to(BLOG_DIR)}")

    def _get_existing_skills(self) -> list[str]:
        """Get list of existing skill names."""
        if not SKILLS_DIR.exists():
            return []
        return [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]

    def _load_sources(self) -> Dict[str, Any]:
        """Load topic sources (trends, requests)."""
        sources: Dict[str, Any] = {}

        trending_path = SOURCES_DIR / "trending_topics.json"
        if trending_path.exists():
            sources["trending"] = json.loads(
                trending_path.read_text(encoding="utf-8")
            )

        requests_path = SOURCES_DIR / "user_requests.json"
        if requests_path.exists():
            sources["requests"] = json.loads(
                requests_path.read_text(encoding="utf-8")
            )

        return sources


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AI Skill Factory Generator")
    parser.add_argument(
        "--strategy",
        choices=["auto", "keyword", "trend", "request", "extend"],
        default="auto",
        help="Topic selection strategy",
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="Specific topic to generate (overrides strategy)",
    )
    parser.add_argument(
        "--use-claude-cli",
        action="store_true",
        help="Use Claude Code CLI instead of Gemini API",
    )
    parser.add_argument(
        "--auto-git",
        action="store_true",
        help="Automatically commit and push changes after generation",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip content validation (for testing)",
    )
    args = parser.parse_args()

    pipeline = SkillFactoryPipeline(use_claude_cli=args.use_claude_cli)
    success = pipeline.run(
        strategy=args.strategy,
        user_topic=args.topic,
        skip_validation=args.skip_validation,
    )

    # Handle auto-git if requested and generation succeeded
    if success and args.auto_git:
        print("\n>>> Auto Git: Committing and pushing changes")
        if has_changes(BLOG_DIR):
            git_success, git_msg = commit_and_push(BLOG_DIR)
            if git_success:
                print(f"  {git_msg}")
            else:
                print(f"  [ERROR] {git_msg}")
                success = False
        else:
            print("  No changes to commit")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
