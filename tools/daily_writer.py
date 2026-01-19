import os
import datetime
import glob
import random
import time
import re
import argparse
import google.generativeai as genai
import frontmatter
from pathlib import Path
import pytz

# --- Configuration ---
BLOG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BLOG_DIR, "_posts")
IMAGE_DIR = os.path.join(BLOG_DIR, "assets", "img", "posts")
# Set your Gemini API Key in environment variables
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Blog Identity for Context
BLOG_CONTEXT = """
Role: Expert Game Server Developer & Backend Engineer.
Topics: Game Server Architecture, Backend Systems (Redis, DB, Networks), AI/ML (LLMs, Agents), Productivity.
Tone: Professional, Insightful, "Knowledge-first" (No fluff, no thesis-style boring text).
Language: Korean.
"""

def setup_gemini():
    if not GENAI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
    genai.configure(api_key=GENAI_API_KEY)

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

def generate_topic(existing_topics):
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    {BLOG_CONTEXT}
    
    Task: Suggest ONE unique, specific technical blog post topic.
    
    Constraints:
    1. Must be related to Game Development, Backend, or AI Agents.
    2. Must NOT be one of the following existing topics:
    {existing_topics[-20:]} (Recent 20 topics)
    3. Output ONLY the topic title in Korean. No explanations.
    """
    
    response = model.generate_content(prompt)
    if not response or not response.text:
       raise Exception("Failed to generate topic")
    
    return response.text.strip()

def generate_post_content(topic):
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    {BLOG_CONTEXT}
    
    Task: Write a technical blog post about "{topic}".
    
    Rules:
    1. **Structure**: 
       - Introduction (Hook)
       - Key Concept 1 (Technical Detail)
       - Key Concept 2 (Practical Application/Code example)
       - Conclusion
    2. **Content**: Focus strictly on transferring knowledge. Avoid fillers like "Hello everyone".
    3. **Images**: You MUST include text description placeholders for images where appropriate, like `[IMAGE_DESC: A diagram showing X...]`.
    4. **Format**: Markdown.
    5. **Front Matter**: DO NOT include Jekyll front matter (I will add it programmatically). Just the body.
    
    Write the post now.
    """
    
    response = model.generate_content(prompt)
    return response.text

def normalize_filename(title):
    # Remove special chars, spaces to hyphens
    clean = re.sub(r'[^\w\s-]', '', title).strip().lower()
    return re.sub(r'[\s]+', '-', clean)

def main():
    print("Starting Daily Blog Automation...")
    setup_gemini()
    
    # 1. Get Topics
    existing = get_existing_topics()
    print(f"Found {len(existing)} existing posts.")
    
    # 2. Generate New Topic
    new_topic = generate_topic(existing)
    print(f"Goal Topic: {new_topic}")
    
    # 3. Write Content
    content_body = generate_post_content(new_topic)
    print("Content generated.")
    
    # 4. Prepare Metadata
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.datetime.now(kst)
    date_str = today.strftime("%Y-%m-%d")
    time_str = today.strftime("%H:%M:%S +0900")
    
    filename_slug = normalize_filename(new_topic)
    # Fallback if slug is empty (Korean titles often become empty with simple regex)
    if not filename_slug:
        filename_slug = f"daily-tech-post-{int(time.time())}"
        
    filename = f"{date_str}-{filename_slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)
    
    # 5. Asset Management (Images)
    # Note: Real Gemini Image Gen requires different model/API handling. 
    # For automation stability, we will use a placeholder/Unsplash approach 
    # OR you can implement the specific 'imagen-3' call here if you have access.
    # For now, we use a reliable curated placeholder based on keywords.
    
    asset_dir_name = f"{date_str}-{filename_slug}"
    full_asset_path = os.path.join(IMAGE_DIR, asset_dir_name)
    os.makedirs(full_asset_path, exist_ok=True)
    
    # Minimal validation/logic for "Odin" style images could go here.
    # We will simply point to a placeholder in the markdown for now, 
    # or use a generic tech image.
    image_path = f"/assets/img/posts/{asset_dir_name}/main.jpg"
    
    # Create a dummy image or copy one (GitHub Action should have a default)
    # In a real scenario, call `genai.generate_images` here if available.
    default_bg = os.path.join(IMAGE_DIR, "../../background.jpg") # assets/img/background.jpg
    if os.path.exists(default_bg):
        import shutil
        target_image_path = os.path.join(BLOG_DIR, image_path.lstrip("/"))
        parent_dir = os.path.dirname(target_image_path)
        os.makedirs(parent_dir, exist_ok=True)
        shutil.copy(default_bg, target_image_path)
        print(f"Copied default background to {target_image_path}")
    else:
        print("Warning: Default background image not found.")
    
    
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
