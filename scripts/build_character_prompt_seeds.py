from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path('reference/character_cache')
OUT = BASE / 'prompt_seeds.json'
SAMPLE = BASE / 'prompt_seed_samples.md'


def first_sentences(text: str, limit: int = 2) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return ''
    parts = re.split(r'(?<=[.!?])\s+', text)
    return ' '.join(parts[:limit]).strip()

seeds = []
for kind_dir, kind_name in [(BASE / 'anime-films' / 'wiki', 'anime-film'), (BASE / 'games' / 'wiki', 'game')]:
    for path in sorted(kind_dir.glob('*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        if not data.get('character_page_extract'):
            continue
        main_summary = first_sentences(data.get('main_page_extract', ''), 2)
        character_summary = first_sentences(data.get('character_page_extract', ''), 3)
        if not character_summary:
            continue
        seeds.append({
            'kind': kind_name,
            'title': data.get('title', ''),
            'main_page_title': data.get('main_page_title', ''),
            'character_page_title': data.get('character_page_title', ''),
            'main_summary': main_summary,
            'character_summary': character_summary,
            'prompt_basis': f"{main_summary} {character_summary}".strip(),
        })

OUT.write_text(json.dumps(seeds, ensure_ascii=False, indent=2), encoding='utf-8')

lines = ['# Prompt Seed Samples', '']
for item in seeds[:40]:
    lines.append(f"## {item['title']}")
    lines.append(f"- kind: {item['kind']}")
    lines.append(f"- main: {item['main_summary']}")
    lines.append(f"- characters: {item['character_summary']}")
    lines.append('')
SAMPLE.write_text('\n'.join(lines), encoding='utf-8')
print(f'seeds={len(seeds)}')
