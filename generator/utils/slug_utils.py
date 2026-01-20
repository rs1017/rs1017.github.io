"""
Slug and filename utilities for AI Skill Factory.
"""

import re
import unicodedata


def normalize_filename(text: str) -> str:
    """
    Normalize text to a valid filename/slug.
    Handles Korean and special characters.
    """
    # Normalize unicode
    text = unicodedata.normalize("NFC", text)

    # Convert to lowercase
    text = text.lower()

    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)

    # Remove special characters except hyphens and alphanumeric (including Korean)
    text = re.sub(r"[^\w가-힣-]", "", text)

    # Remove consecutive hyphens
    text = re.sub(r"-+", "-", text)

    # Strip leading/trailing hyphens
    text = text.strip("-")

    # Limit length
    if len(text) > 50:
        text = text[:50].rstrip("-")

    return text or "untitled"


def to_kebab_case(text: str) -> str:
    """
    Convert text to kebab-case (lowercase with hyphens).
    """
    # Handle camelCase and PascalCase
    text = re.sub(r"([a-z])([A-Z])", r"\1-\2", text)

    # Handle consecutive uppercase letters
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", text)

    # Convert to lowercase
    text = text.lower()

    # Replace non-alphanumeric with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text)

    # Remove consecutive hyphens
    text = re.sub(r"-+", "-", text)

    # Strip leading/trailing hyphens
    return text.strip("-")


def sanitize_tag(tag: str) -> str:
    """
    Sanitize a tag for use in front matter.
    """
    # Remove leading/trailing whitespace
    tag = tag.strip()

    # Replace problematic characters
    tag = re.sub(r"[:\[\]{}#]", "", tag)

    return tag
