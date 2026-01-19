import os
import datetime
import glob
import random
import time
import re
import json
import google.generativeai as genai
import frontmatter
from pathlib import Path
import pytz
from dotenv import load_dotenv

# Load local .env file
load_dotenv()

# --- Configuration ---
BLOG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BLOG_DIR, "_posts")
IMAGE_DIR = os.path.join(BLOG_DIR, "assets", "img", "posts")
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Model Fallback List (Will try in order until one works)
# Updated based on actual API listing
MODEL_CANDIDATES = [
    "models/gemini-2.0-flash",
    "models/gemini-flash-latest",
    "models/gemini-pro-latest",
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash-exp",
]
WORKING_MODEL = None  # Will be set after first successful call

# Load Agents Configuration (Priority: Env Var > Local File)
AGENTS = {}

def load_agents_config():
    global AGENTS
    # 1. Try Environment Variable
    if os.environ.get("BLOG_AGENTS_CONFIG"):
        try:
            AGENTS = json.loads(os.environ.get("BLOG_AGENTS_CONFIG"))
            print("Loaded agents from Environment Variable.", flush=True)
            return
        except json.JSONDecodeError:
            print("Warning: Failed to parse BLOG_AGENTS_CONFIG env var.", flush=True)

    # 2. Try Local File
    local_json_path = os.path.join(BLOG_DIR, ".agent", "agents_prompts.json")
    if os.path.exists(local_json_path):
        try:
            with open(local_json_path, 'r', encoding='utf-8') as f:
                AGENTS = json.load(f)
            print(f"Loaded agents from local file: {local_json_path}", flush=True)
            return
        except Exception as e:
            print(f"Warning: Failed to load local agents file: {e}", flush=True)

    print("Warning: No agents configuration found. Using empty defaults.", flush=True)

def get_agent_prompt(agent_name):
    """Retrieve prompt from loaded JSON config."""
    prompt = AGENTS.get(agent_name)
    if not prompt:
        print(f"Warning: Agent '{agent_name}' not found in configuration.", flush=True)
        return f"You are acting as {agent_name}."
    return prompt

def configure_genai():
    if not GENAI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is missing. Check .env file or GitHub Secrets.")
    genai.configure(api_key=GENAI_API_KEY)
    
    # Debug: List available models
    print("\n[Debug] Available Gemini Models:", flush=True)
    try:
        found_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - {m.name}", flush=True)
                found_models.append(m.name)
        print("", flush=True)
        return found_models
    except Exception as e:
        print(f"Failed to list models: {e}", flush=True)
        return []

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

def safe_generate_content(contents):
    """
    Generation wrapper with model fallback and retry logic.
    Tries multiple model names until one works.
    """
    global WORKING_MODEL
    max_retries = 3
    base_delay = 2

    # If we already found a working model, use it directly
    models_to_try = [WORKING_MODEL] if WORKING_MODEL else MODEL_CANDIDATES

    for model_name in models_to_try:
        print(f"  [AI] Trying model '{model_name}' with input length: {len(contents)} chars...", flush=True)
        
        try:
            model = genai.GenerativeModel(model_name)
        except Exception as e:
            print(f"  [AI] Failed to initialize model '{model_name}': {e}", flush=True)
            continue

        for attempt in range(max_retries):
            try:
                start_time = time.time()
                response = model.generate_content(contents)
                elapsed = time.time() - start_time
                print(f"  [AI] Success with '{model_name}' in {elapsed:.2f}s", flush=True)
                
                # Remember this model for future calls
                WORKING_MODEL = model_name
                return response
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"  [AI] Rate limited (429). Retrying in {delay:.2f}s... (Attempt {attempt+1}/{max_retries})", flush=True)
                    time.sleep(delay)
                elif "404" in error_str or "NOT_FOUND" in error_str:
                    print(f"  [AI] Model '{model_name}' not found (404). Trying next model...", flush=True)
                    break  # Break inner retry loop, try next model
                else:
                    print(f"  [AI] Unexpected error: {e}", flush=True)
                    break  # Try next model
    
    raise Exception(f"All model candidates failed. Tried: {models_to_try}")

# --- Pipeline Steps ---

def step_1_select_topic(existing_topics):
    print(">>> Step 1: Selecting Topic (topic-selector)", flush=True)
    agent_prompt = get_agent_prompt("topic-selector")
    
    prompt = f"""
    {agent_prompt}
    
    Task: Use your expertise to Suggest ONE unique, specific technical blog post topic.
    
    Context:
    - Target Audience: Backend Engineers, Game Developers.
    - Existing Topics (Avoid these): {existing_topics[-30:]}
    
    Output Format: ONLY the topic title in Korean.
    """
    
    response = safe_generate_content(prompt)
    topic = response.text.strip()
    print(f"Selected Topic: {topic}", flush=True)
    return topic

def step_2_research_topic(topic):
    print(">>> Step 2: Researching Topic (topic-researcher)", flush=True)
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
    
    response = safe_generate_content(prompt)
    research_notes = response.text
    return research_notes

def step_3_create_storyboard(topic, research_notes):
    print(">>> Step 3: Creating Storyboard (storyboard-creator)", flush=True)
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
    
    response = safe_generate_content(prompt)
    storyboard = response.text
    return storyboard

def step_4_write_post(topic, storyboard):
    print(">>> Step 4: Writing Post (post-writer)", flush=True)
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
    
    response = safe_generate_content(prompt)
    draft_content = response.text
    return draft_content

def step_5_review_post(draft_content):
    print(">>> Step 5: Reviewing Post (post-reviewer)", flush=True)
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
    
    response = safe_generate_content(prompt)
    review_result = response.text
    
    if "REJECTED" in review_result:
        raise Exception(f"Post Rejected by Reviewer: {review_result}")
        
    return review_result

def normalize_filename(title):
    clean = re.sub(r'[^\w\s-]', '', title).strip().lower()
    return re.sub(r'[\s]+', '-', clean)

def main():
    print("=" * 60, flush=True)
    print("Starting Daily Blog Automation (Full Pipeline)...", flush=True)
    print("=" * 60, flush=True)
    
    load_agents_config()
    available_models = configure_genai()
    
    # 1. Topic Selection
    existing = get_existing_topics()
    print(f"Found {len(existing)} existing posts.", flush=True)
    topic = step_1_select_topic(existing)
    time.sleep(2)
    
    # 2. Research
    research_notes = step_2_research_topic(topic)
    time.sleep(2)
    
    # 3. Storyboard
    storyboard = step_3_create_storyboard(topic, research_notes)
    time.sleep(2)
    
    # 4. Drafting
    draft_content = step_4_write_post(topic, storyboard)
    time.sleep(2)
    
    # 5. Review & Finalize
    final_content = step_5_review_post(draft_content)
    print(">>> Pipeline Completed Successfully.", flush=True)
    
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
        print(f"Copied default background image.", flush=True)
    
    # Ensure Final Front Matter
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
        
    print(f"Successfully created post: {filepath}", flush=True)
    print("=" * 60, flush=True)

if __name__ == "__main__":
    main()
