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
# Contains: topic-selector, topic-researcher, storyboard-creator, post-writer, post-reviewer
AGENTS_CONFIG_JSON = os.environ.get("BLOG_AGENTS_CONFIG")
AGENTS = {}
if AGENTS_CONFIG_JSON:
    try:
        AGENTS = json.loads(AGENTS_CONFIG_JSON)
    except json.JSONDecodeError:
        print("Warning: Failed to parse BLOG_AGENTS_CONFIG. Agents might be missing.")

def get_agent_prompt(agent_name):
    """Retrieve prompt from loaded JSON config."""
    prompt = AGENTS.get(agent_name)
    if not prompt:
        print(f"Warning: Agent '{agent_name}' not found in configuration.")
        return f"You are acting as {agent_name}."
    return prompt

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
    base_delay = 2  # Short delay for Pro plan

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            return response
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                delay = base_delay * (1.5 ** attempt) + random.uniform(0, 1)
                print(f"Rate limited (429). Retrying in {delay:.2f}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
            else:
                raise e
    raise Exception("Max retries exceeded for Gemini API.")

# --- Pipeline Steps ---

def step_1_select_topic(client, existing_topics):
    print(">>> Step 1: Selecting Topic (topic-selector)")
    agent_prompt = get_agent_prompt("topic-selector")
    
    prompt = f"""
    {agent_prompt}
    
    Task: Use your expertise to Suggest ONE unique, specific technical blog post topic.
    
    Context:
    - Target Audience: Backend Engineers, Game Developers.
    - Existing Topics (Avoid these): {existing_topics[-30:]}
    
    Output Format: ONLY the topic title in Korean.
    """
    
    response = safe_generate_content(client, 'gemini-2.0-flash-exp', prompt)
    topic = response.text.strip()
    print(f"Selected Topic: {topic}")
    return topic

def step_2_research_topic(client, topic):
    print(">>> Step 2: Researching Topic (topic-researcher)")
    agent_prompt = get_agent_prompt("topic-researcher")
    
    prompt = f"""
    {agent_prompt}
    
    Task: Conduct deep research on the topic: "{topic}".
    
    Output Format:
    - Key Technical Concepts
    - Pros/Cons or Trade-offs
    - Best Practices
    - Code Snippet Ideas (Python/C#/Go)
    
    Provide comprehensive research notes usable by a writer.
    """
    
    response = safe_generate_content(client, 'gemini-2.0-flash-exp', prompt)
    research_notes = response.text
    return research_notes

def step_3_create_storyboard(client, topic, research_notes):
    print(">>> Step 3: Creating Storyboard (storyboard-creator)")
    agent_prompt = get_agent_prompt("storyboard-creator")
    
    prompt = f"""
    {agent_prompt}
    
    Task: Create a content outline (storyboard) for the topic: "{topic}".
    
    Input Research:
    {research_notes}
    
    Output Requirements:
    - Define clear section headers
    - Design 1 main image prompt (high quality)
    - Outline flow: Hook -> Problem -> Solution -> Deep Dive -> Conclusion
    """
    
    response = safe_generate_content(client, 'gemini-2.0-flash-exp', prompt)
    storyboard = response.text
    return storyboard

def step_4_write_post(client, topic, storyboard):
    print(">>> Step 4: Writing Post (post-writer)")
    agent_prompt = get_agent_prompt("post-writer")
    
    prompt = f"""
    {agent_prompt}
    
    Task: Write the full technical blog post for: "{topic}".
    
    Directives:
    - Use the provided Storyboard as a guide.
    - Tone: Professional, Knowledge-dense. No fluff.
    - Format: Markdown.
    - Include Code examples where planned.
    - Include the Main Image Placeholder defined in the storyboard.
    
    Storyboard:
    {storyboard}
    """
    
    response = safe_generate_content(client, 'gemini-2.0-flash-exp', prompt)
    draft_content = response.text
    return draft_content

def step_5_review_post(client, draft_content):
    print(">>> Step 5: Reviewing Post (post-reviewer)")
    agent_prompt = get_agent_prompt("post-reviewer")
    
    prompt = f"""
    {agent_prompt}
    
    Task: Review the following technical post.
    
    Critique Criteria:
    1. Is it technically accurate?
    2. Is it free of fluff/filler?
    3. Are code examples valid?
    4. Is the tone appropriate?
    
    If the post is Good (Score > 80), output the consolidated final markdown content (with minor fixes if needed).
    If the post is Bad, output "REJECTED: [Reason]".
    
    Draft Content:
    {draft_content}
    """
    
    response = safe_generate_content(client, 'gemini-2.0-flash-exp', prompt)
    review_result = response.text
    
    if "REJECTED" in review_result:
        raise Exception(f"Post Rejected by Reviewer: {review_result}")
        
    return review_result

def normalize_filename(title):
    clean = re.sub(r'[^\w\s-]', '', title).strip().lower()
    return re.sub(r'[\s]+', '-', clean)

def main():
    print("Starting Daily Blog Automation (Full Pipeline)...")
    client = get_client()
    
    # 1. Topic Selection
    existing = get_existing_topics()
    topic = step_1_select_topic(client, existing)
    time.sleep(5)
    
    # 2. Research
    research_notes = step_2_research_topic(client, topic)
    time.sleep(5)
    
    # 3. Storyboard
    storyboard = step_3_create_storyboard(client, topic, research_notes)
    time.sleep(5)
    
    # 4. Drafting
    draft_content = step_4_write_post(client, topic, storyboard)
    time.sleep(5)
    
    # 5. Review & Finalize
    final_content = step_5_review_post(client, draft_content)
    print(">>> Pipeline Completed Successfully.")
    
    # 6. Save File and Assets
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.datetime.now(kst)
    date_str = today.strftime("%Y-%m-%d")
    time_str = today.strftime("%H:%M:%S +0900")
    
    filename_slug = normalize_filename(topic)
    if not filename_slug:
        filename_slug = f"daily-tech-post-{int(time.time())}"
        
    filename = f"{date_str}-{filename_slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)
    
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
    
    # Ensure Final Front Matter
    # (The reviewer might output raw markdown, so we wrap it with Jekyll front matter if missing)
    if not final_content.startswith("---"):
        final_content = f"""---
layout: post
title: "{topic}"
date: {date_str} {time_str}
categories: [Automation, AI]
tags: [Gemini, AutoBlog, Pipeline]
image:
  path: {image_path}
  alt: {topic} Main Image
---

{final_content}

*(This post was automatically generated by AI Agent Pipeline)*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"Successfully created post: {filepath}")

if __name__ == "__main__":
    main()
