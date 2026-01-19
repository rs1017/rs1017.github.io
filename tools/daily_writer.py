#!/usr/bin/env python3
"""
Daily Blog Writer - AI 블로그 자동화 시스템
역할: 파이프라인 흐름 제어 및 도구 실행 (이미지 생성 등)
모든 판단과 창작은 _agents/*.md 에 정의된 에이전트에게 위임
"""

import os
import datetime
import glob
import random
import time
import re
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
AGENTS_DIR = os.path.join(BLOG_DIR, "_agents")
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Model Fallback List (Will be updated dynamically)
# 1.5-flash-latest might be safer alias
MODEL_CANDIDATES = [
    "models/gemini-1.5-flash-latest",
    "models/gemini-2.0-flash-exp", 
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro-latest",
]
WORKING_MODEL = None


def load_agent_prompt(agent_name: str) -> str:
    """Load agent prompt from _agents/{agent_name}.md file."""
    # Also load concept.md to append to every agent
    concept_file = os.path.join(AGENTS_DIR, "concept.md")
    concept_content = ""
    if os.path.exists(concept_file):
        with open(concept_file, 'r', encoding='utf-8') as f:
            concept_content = f.read()

    agent_file = os.path.join(AGENTS_DIR, f"{agent_name}.md")
    if not os.path.exists(agent_file):
        print(f"Warning: Agent file not found: {agent_file}", flush=True)
        return f"You are acting as {agent_name}."
    
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove Front Matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        
        # Append concept for context
        return f"{content}\n\n---\n{concept_content}"
    except Exception as e:
        print(f"Error loading agent prompt: {e}", flush=True)
        return f"You are acting as {agent_name}."


def configure_genai():
    if not GENAI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
    genai.configure(api_key=GENAI_API_KEY)
    
    # Dynamically find available models
    print("[Init] Listing available models:", flush=True)
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - {m.name}", flush=True)
                available_models.append(m.name)
    except Exception as e:
        print(f"  Failed to list models: {e}", flush=True)

    if available_models:
        global MODEL_CANDIDATES
        # Prioritize known good models if they exist in the available list
        preferred = [
            "models/gemini-1.5-flash", 
            "models/gemini-1.5-flash-latest",
            "models/gemini-2.0-flash-exp",
            "models/gemini-1.5-pro",
            "models/gemini-1.0-pro"  # Fallback for old libraries
        ]
        
        # Filter preferred models that are actually available
        valid_preferred = [m for m in preferred if m in available_models]
        
        # Add any other available models that aren't in preferred list
        others = [m for m in available_models if m not in preferred]
        
        # New candidate list: Valid preferred first, then others
        MODEL_CANDIDATES = valid_preferred + others
        
        print(f"[Init] Selected Model Candidates: {MODEL_CANDIDATES}", flush=True)
    else:
        print("[Init] Warning: Could not verify available models. Using defaults.", flush=True)


def get_existing_topics() -> list:
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


def safe_generate_content(contents: str) -> str:
    global WORKING_MODEL
    max_retries = 5  # retries 증가
    base_delay = 10  # 기본 대기 시간 증가
    
    models_to_try = [WORKING_MODEL] + [m for m in MODEL_CANDIDATES if m != WORKING_MODEL] if WORKING_MODEL else MODEL_CANDIDATES

    last_error = None

    for model_name in models_to_try:
        if not model_name: continue
        
        print(f"  [AI] Trying {model_name}...", flush=True)
        try:
            model = genai.GenerativeModel(model_name)
            for attempt in range(max_retries):
                try:
                    response = model.generate_content(contents)
                    if not response.text:
                        raise Exception("Empty response text")
                    
                    WORKING_MODEL = model_name
                    print(f"  [AI] Success with {model_name}", flush=True)
                    return response.text
                except Exception as e:
                    last_error = e
                    error_str = str(e)
                    
                    # Rate Limit Handling
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        # Extract suggested wait time if available (e.g., from logs)
                        # Default aggressive backoff
                        sleep_time = base_delay * (2 ** attempt) + random.uniform(5, 10)
                        print(f"    - Rate limited (Attempt {attempt+1}). Sleeping {sleep_time:.1f}s...", flush=True)
                        time.sleep(sleep_time)
                    
                    # Model Not Found Handling -> Break to try next model
                    elif "404" in error_str or "not found" in error_str.lower():
                        print(f"    - Model {model_name} not found. Switching...", flush=True)
                        break
                    
                    # 500 Server Error -> Retry same model
                    elif "500" in error_str or "internal" in error_str.lower():
                        print(f"    - Internal error. Retrying...", flush=True)
                        time.sleep(base_delay)
                    
                    else:
                        print(f"    - Error: {error_str}", flush=True)
                        # Unknown error, maybe break to try next model?
                        # For now, retry a bit
                        time.sleep(base_delay)
                        
        except Exception as e:
            print(f"  [AI] Failed to init {model_name}: {e}", flush=True)
            continue
            
    raise Exception(f"All models failed. Last error: {last_error}")


# === Pipeline Steps ===

def step_1_select_topic(existing_topics: list) -> str:
    print("\n>>> Step 1: Selecting Topic", flush=True)
    prompt = f"""
{load_agent_prompt("topic-selector")}

Existing Topics: {existing_topics[-30:]}

Output ONLY the topic title.
"""
    result = safe_generate_content(prompt)
    return result.strip().replace('"', '').replace("'", '').strip()


def step_2_research_topic(topic: str) -> str:
    print("\n>>> Step 2: Researching Topic", flush=True)
    prompt = f"""
{load_agent_prompt("topic-researcher")}

Topic: "{topic}"
"""
    return safe_generate_content(prompt)


def step_3_create_storyboard(topic: str, research_notes: str) -> str:
    print("\n>>> Step 3: Creating Storyboard", flush=True)
    prompt = f"""
{load_agent_prompt("storyboard-creator")}

Topic: "{topic}"
Research: {research_notes}
"""
    return safe_generate_content(prompt)


def step_4_write_post(topic: str, storyboard: str, date_str: str, filename_slug: str) -> str:
    print("\n>>> Step 4: Writing Post", flush=True)
    
    # Provide context for Front Matter generation
    context = f"""
Current Date: {date_str}
Filename Slug: {filename_slug}
Expected Image Path format: /assets/img/posts/{date_str}-{filename_slug}/main.jpg
"""
    
    prompt = f"""
{load_agent_prompt("post-writer")}

Topic: "{topic}"
Context: 
{context}

Storyboard:
{storyboard}
"""
    return safe_generate_content(prompt)


def step_5_review_post(draft_content: str) -> str:
    print("\n>>> Step 5: Reviewing Post", flush=True)
    prompt = f"""
{load_agent_prompt("post-reviewer")}

Draft Content:
{draft_content}
"""
    result = safe_generate_content(prompt)
    if "REJECTED" in result:
        raise Exception(f"Post rejected: {result}")
    
    # Clean up review meta text if any remains
    skip = ['Score:', 'APPROVE', 'Editor Review', '점수:']
    return '\n'.join([l for l in result.split('\n') if not any(s in l for s in skip)]).strip()


def step_6_generate_images(content: str, asset_dir_path: str, asset_dir_name: str) -> str:
    print("\n>>> Step 6: Generating Images", flush=True)
    pattern = r'\[IMAGE_DESC:\s*([^\]]+)\]'
    matches = re.findall(pattern, content)
    
    print(f"  Found {len(matches)} images", flush=True)
    image_agent_prompt = load_agent_prompt("image-generator")
    
    # Image model usually needs specific name
    # We will try to find a valid one
    image_model_name = "models/gemini-2.0-flash-exp" # Often supports image gen
    # Or specifically
    # image_model_name = "models/gemini-1.5-pro-latest" 
    
    for idx, desc in enumerate(matches):
        filename = f"image_{idx+1}.jpg"
        full_path = os.path.join(asset_dir_path, filename)
        web_path = f"/assets/img/posts/{asset_dir_name}/{filename}"
        
        # Optimize prompt using agent guidelines
        prompt = f"""
{image_agent_prompt}

Generate an image for: {desc}
"""
        try:
            # Try with current working model first if it supports images?
            # Actually standard generate_content creates text. 
            # We need a model that supports image generation.
            # safe_generate_content returns text. We need a separate function.
            if generate_single_image(prompt, full_path):
                # Replace placeholder with markdown image
                alt = desc[:50].replace('"', "'")
                content = content.replace(f"[IMAGE_DESC: {desc}]", f"![{alt}]({web_path})")
            else:
                 if os.path.exists(full_path):
                     alt = desc[:50].replace('"', "'")
                     content = content.replace(f"[IMAGE_DESC: {desc}]", f"![{alt}]({web_path})")
                 else:
                     print(f"  Skipping image {idx+1}", flush=True)
        except Exception as e:
             print(f"  Image generation error: {e}", flush=True)
             
        time.sleep(5) 
        
    return content


def generate_single_image(prompt: str, output_path: str) -> bool:
    print(f"  [IMG] Generating...", flush=True)
    
    # Candidates for image generation
    # Not all models support image generation. 
    # Usually gemini-pro-vision (input) or specific imagen models (output).
    # Gemini 2.0 Flash Exp reportedly supports image generation.
    image_models = [
        "models/gemini-2.0-flash-exp", 
        "models/gemini-1.5-pro-latest"
    ]
    
    for model_name in image_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt, generation_config=genai.GenerationConfig(response_mime_type="image/jpeg"))
            if response.parts:
                import base64
                if hasattr(response.parts[0], 'inline_data'):
                    with open(output_path, 'wb') as f:
                        f.write(base64.b64decode(response.parts[0].inline_data.data))
                    return True
        except Exception as e:
            # print(f"  [IMG] Failed with {model_name}: {e}")
            pass
            
    return False


def normalize_filename(title: str) -> str:
    return re.sub(r'[\s]+', '-', re.sub(r'[^\w\s-]', '', title).strip().lower())


def main():
    print("=== Daily Blog Writer Agent ===", flush=True)
    try:
        configure_genai()
        
        # 1. Topic
        existing = get_existing_topics()
        topic = step_1_select_topic(existing)
        
        # 2. Research
        research = step_2_research_topic(topic)
        
        # 3. Storyboard
        storyboard = step_3_create_storyboard(topic, research)
        
        # Prepare paths
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.datetime.now(kst)
        date_str = now.strftime("%Y-%m-%d")
        slug = normalize_filename(topic) or f"post-{int(time.time())}"
        asset_dir_name = f"{date_str}-{slug}"
        full_asset_path = os.path.join(IMAGE_DIR, asset_dir_name)
        os.makedirs(full_asset_path, exist_ok=True)
        
        # 4. Write
        draft = step_4_write_post(topic, storyboard, date_str, slug)
        
        # 5. Review
        final = step_5_review_post(draft)
        
        # 6. Images
        final = step_6_generate_images(final, full_asset_path, asset_dir_name)
        
        # 7. Header Image
        print("\n>>> Step 7: Header Image", flush=True)
        header_prompt = f"Blog header image for topic: {topic}"
        generate_single_image(header_prompt, os.path.join(full_asset_path, "main.jpg"))
        
        # 8. Save
        filename = f"{date_str}-{slug}.md"
        filepath = os.path.join(POSTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final)
            
        print(f"\n✅ Created: {filepath}", flush=True)
        
    except Exception as e:
        print(f"\n❌ Pipeline Failed: {e}", flush=True)
        raise

if __name__ == "__main__":
    main()
