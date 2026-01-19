import os
import datetime
import glob
import random
import time
import re
import json
import argparse
from google import genai
from google.genai import types
import frontmatter
from pathlib import Path
import pytz

# --- Configuration ---
BLOG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BLOG_DIR, "_posts")
IMAGE_DIR = os.path.join(BLOG_DIR, "assets", "img", "posts")
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Load Agents Configuration (JSON Secret)
# This contains specific prompts for: topic-selector, post-writer, etc.
AGENTS_CONFIG_JSON = os.environ.get("BLOG_AGENTS_CONFIG")
AGENTS = {}
if AGENTS_CONFIG_JSON:
    try:
        AGENTS = json.loads(AGENTS_CONFIG_JSON)
    except json.JSONDecodeError:
        print("Warning: Failed to parse BLOG_AGENTS_CONFIG. Using defaults.")

# Fallback Prompts if JSON is missing
DEFAULT_WRITER_PROMPT = """
Role: Expert Game Server Developer.
Task: Write a technical blog post.
Language: Korean.
Focus on: Game Server Architecture, Backend Systems, AI/ML.
"""

def get_agent_prompt(agent_name, fallback):
    """Retrieve prompt from loaded JSON config or use fallback."""
    return AGENTS.get(agent_name, fallback)

def get_client():
    if not GENAI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
    return genai.Client(api_key=GENAI_API_KEY)

def get_existing_topics():
    topics = []
    files = glob.glob(os.path.join(POSTS_DIR, "*.md"))
    for f in files:
        try:
            post = frontmatter.load(f)
            title = post.get('title', '')
            if title:
                topics.append(title)
        except:
            continue
    return topics

def safe_generate_content(client, model, contents):
    """Citron-wrapped generation with retry for 429 errors."""
    max_retries = 5
    base_delay = 10

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            return response
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                delay = base_delay * (2 ** attempt) + random.uniform(0, 5)
                print(f"Rate limited (429). Retrying in {delay:.2f}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
            else:
                raise e
    raise Exception("Max retries exceeded for Gemini API.")

def generate_topic(existing_topics):
    client = get_client()
    model_name = 'gemini-1.5-flash'
    
    # Use topic-selector agent if available
    agent_prompt = get_agent_prompt("topic-selector", DEFAULT_WRITER_PROMPT)
    
    prompt = f"""
    {agent_prompt}
    
    Task: Suggest ONE unique, specific technical blog post topic.
    
    Constraints:
    1. Must be related to Game Development, Backend, or AI Agents.
    2. Must NOT be one of the following existing topics:
    {existing_topics[-20:]} (Recent 20 topics)
    3. Output ONLY the topic title in Korean. No explanations.
    """
    
    response = safe_generate_content(client, model_name, prompt)
    
    if not response or not response.text:
       raise Exception("Failed to generate topic")
    
    return response.text.strip()

def generate_post_content(topic):
    client = get_client()
    model_name = 'gemini-1.5-flash'
    
    # Use post-writer agent if available
    agent_prompt = get_agent_prompt("post-writer", DEFAULT_WRITER_PROMPT)
    
    prompt = f"""
    {agent_prompt}
    
    Task: Write a technical blog post about "{topic}".
    
    Rules:
    1. **Structure**: Introduction, Key Concepts, Code/Examples, Conclusion.
    2. **Content**: Knowledge-first, no fluff.
    3. **Images**: Include placeholders like `[IMAGE_DESC: ...]`.
    4. **Format**: Markdown. No front matter.
    
    Write the post now.
    """
    
    response = safe_generate_content(client, model_name, prompt)
    return response.text

def normalize_filename(title):
    clean = re.sub(r'[^\w\s-]', '', title).strip().lower()
    return re.sub(r'[\s]+', '-', clean)

def main():
    print("Starting Daily Blog Automation...")
    get_client()
    
    # 1. Get Topics
    existing = get_existing_topics()
    print(f"Found {len(existing)} existing posts.")
    
    # 2. Generate New Topic
    new_topic = generate_topic(existing)
    print(f"Goal Topic: {new_topic}")
    
    time.sleep(5)
    
    # 3. Write Content
    content_body = generate_post_content(new_topic)
    print("Content generated.")
    
    # 4. Prepare Metadata
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.datetime.now(kst)
    date_str = today.strftime("%Y-%m-%d")
    time_str = today.strftime("%H:%M:%S +0900")
    
    filename_slug = normalize_filename(new_topic)
    if not filename_slug:
        filename_slug = f"daily-tech-post-{int(time.time())}"
        
    filename = f"{date_str}-{filename_slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)
    
    # 5. Asset Management
    asset_dir_name = f"{date_str}-{filename_slug}"
    full_asset_path = os.path.join(IMAGE_DIR, asset_dir_name)
    os.makedirs(full_asset_path, exist_ok=True)
    
    image_path = f"/assets/img/posts/{asset_dir_name}/main.jpg"
    
    default_bg = os.path.join(IMAGE_DIR, "../../background.jpg")
    if os.path.exists(default_bg):
        import shutil
        target_image_path = os.path.join(BLOG_DIR, image_path.lstrip("/"))
        parent_dir = os.path.dirname(target_image_path)
        os.makedirs(parent_dir, exist_ok=True)
        shutil.copy(default_bg, target_image_path)
        print(f"Copied default background to {target_image_path}")
    
    # 6. Assemble Post
    post_content = f"""---
layout: post
title: "{new_topic}"
date: {date_str} {time_str}
categories: [Automation, AI]
tags: [Gemini, AutoBlog, Daily]
image:
  path: {image_path}
  alt: {new_topic} Main Image
---

{content_body}

*(This post was automatically generated by AI Agent)*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(post_content)
        
    print(f"Successfully created post: {filepath}")

if __name__ == "__main__":
    main()
