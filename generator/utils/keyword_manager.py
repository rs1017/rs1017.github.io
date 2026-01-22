"""
Keyword Manager for AI Skill Factory.
Manages keywords from various sources including GitHub trending.
"""

import json
import random
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class KeywordManager:
    """Manages keywords for topic selection."""

    def __init__(self, sources_dir: Optional[Path] = None):
        if sources_dir is None:
            sources_dir = Path(__file__).parent.parent / "sources"
        self.sources_dir = sources_dir
        self.keywords_file = sources_dir / "keywords.json"
        self.data = self._load_keywords()

    def _load_keywords(self) -> dict:
        """Load keywords from JSON file."""
        if self.keywords_file.exists():
            with open(self.keywords_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"categories": {}, "trending": [], "github_topics": []}

    def _save_keywords(self) -> None:
        """Save keywords to JSON file."""
        self.data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        with open(self.keywords_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get_all_keywords(self) -> List[str]:
        """Get all keywords from all categories."""
        keywords = []
        for category_keywords in self.data.get("categories", {}).values():
            keywords.extend(category_keywords)
        keywords.extend(self.data.get("trending", []))
        keywords.extend(self.data.get("github_topics", []))
        return list(set(keywords))

    def get_random_keywords(self, count: int = 5) -> List[str]:
        """Get random keywords for topic generation."""
        all_keywords = self.get_all_keywords()
        return random.sample(all_keywords, min(count, len(all_keywords)))

    def get_category_keywords(self, category: str) -> List[str]:
        """Get keywords for a specific category."""
        return self.data.get("categories", {}).get(category, [])

    def get_mixed_keywords(self, count: int = 5) -> List[str]:
        """Get keywords from different categories for diversity."""
        categories = list(self.data.get("categories", {}).keys())
        selected = []

        # Pick at least one from each category if possible
        for cat in random.sample(categories, min(count, len(categories))):
            cat_keywords = self.get_category_keywords(cat)
            if cat_keywords:
                selected.append(random.choice(cat_keywords))

        # Fill remaining with random keywords
        all_keywords = self.get_all_keywords()
        remaining = [k for k in all_keywords if k not in selected]
        while len(selected) < count and remaining:
            kw = random.choice(remaining)
            selected.append(kw)
            remaining.remove(kw)

        return selected

    def update_github_trending(self) -> List[str]:
        """Fetch trending topics from GitHub using gh CLI."""
        try:
            # Search GitHub for trending AI/Claude related repos
            queries = [
                "claude code language:python stars:>10",
                "mcp server language:python stars:>5",
                "ai automation language:python stars:>50",
                "llm tools language:python stars:>20"
            ]

            topics = set()
            for query in queries:
                try:
                    result = subprocess.run(
                        ["gh", "search", "repos", query, "--limit", "5", "--json", "name,description"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0 and result.stdout:
                        repos = json.loads(result.stdout)
                        for repo in repos:
                            # Extract keywords from name and description
                            name = repo.get("name", "")
                            desc = repo.get("description", "") or ""

                            # Add meaningful words
                            for word in name.replace("-", " ").replace("_", " ").split():
                                if len(word) > 2 and word.lower() not in ["the", "and", "for", "with"]:
                                    topics.add(word)

                            # Extract key terms from description
                            for word in desc.split():
                                if len(word) > 3 and word.isalpha():
                                    topics.add(word)
                except Exception:
                    continue

            # Filter and limit
            filtered_topics = list(topics)[:30]
            self.data["github_topics"] = filtered_topics
            self._save_keywords()

            return filtered_topics

        except Exception as e:
            print(f"  Warning: Failed to fetch GitHub trending: {e}")
            return []

    def add_keyword(self, keyword: str, category: str = "trending") -> None:
        """Add a new keyword."""
        if category == "trending":
            if keyword not in self.data["trending"]:
                self.data["trending"].append(keyword)
        elif category in self.data["categories"]:
            if keyword not in self.data["categories"][category]:
                self.data["categories"][category].append(keyword)
        self._save_keywords()

    def refresh_trending(self) -> None:
        """Refresh trending keywords from all sources."""
        print("  Refreshing GitHub trending keywords...")
        github_topics = self.update_github_trending()
        print(f"  Found {len(github_topics)} GitHub topics")
