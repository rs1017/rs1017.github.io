from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Iterable

import requests

USER_AGENT = 'rs1017-preschool-reference-bot/1.0 (https://rs1017.github.io/)'
WIKI_API = 'https://en.wikipedia.org/w/api.php'
JIKAN_API = 'https://api.jikan.moe/v4/anime'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Build anime/game reference caches from anime DB + Wikipedia.')
    parser.add_argument('--anime-limit', type=int, default=500)
    parser.add_argument('--game-limit', type=int, default=120)
    parser.add_argument('--output-dir', type=Path, default=Path('reference/character_cache'))
    return parser.parse_args()


def new_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    return session


def request_json(session: requests.Session, url: str, *, params: dict, timeout: int = 30, retries: int = 6) -> dict:
    for attempt in range(retries):
        response = session.get(url, params=params, timeout=timeout)
        if response.status_code == 429:
            wait_seconds = min(10, 2 + attempt * 2)
            time.sleep(wait_seconds)
            continue
        response.raise_for_status()
        return response.json()
    response.raise_for_status()
    return {}


def slugify(text: str, max_length: int = 72) -> str:
    value = re.sub(r'[^a-zA-Z0-9]+', '-', text.strip().lower()).strip('-')
    value = value[:max_length].rstrip('-')
    return value or 'item'


def clean_title(text: str) -> str:
    text = re.sub(r'\[[^\]]+\]', '', text)
    text = re.sub(r'\([^\)]*\)$', '', text).strip()
    return re.sub(r'\s+', ' ', text)


def fetch_category_members(session: requests.Session, category: str, limit: int) -> list[str]:
    titles: list[str] = []
    continuation: dict[str, str] = {}
    while len(titles) < limit:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'categorymembers',
            'cmtitle': category,
            'cmlimit': min(500, limit - len(titles)),
            'cmnamespace': 0,
        }
        params.update(continuation)
        payload = request_json(session, WIKI_API, params=params)
        for member in payload.get('query', {}).get('categorymembers', []):
            title = clean_title(member['title'])
            if title and title not in titles:
                titles.append(title)
        if 'continue' not in payload:
            break
        continuation = {'cmcontinue': payload['continue']['cmcontinue']}
        time.sleep(0.05)
    return titles[:limit]


def collect_anime_titles(session: requests.Session, limit: int) -> list[str]:
    titles: list[str] = []
    page = 1
    while len(titles) < limit:
        payload = request_json(session, JIKAN_API, params={'type': 'movie', 'page': page})
        for item in payload.get('data', []):
            title = clean_title(item.get('title') or item.get('title_english') or '')
            if title and title not in titles:
                titles.append(title)
            if len(titles) >= limit:
                break
        pagination = payload.get('pagination', {})
        if not pagination.get('has_next_page'):
            break
        page += 1
        time.sleep(1.0)
    return titles[:limit]


def collect_game_titles(session: requests.Session, limit: int) -> list[str]:
    candidates = fetch_category_members(session, 'Category:Video game franchises', limit * 3)
    results: list[str] = []
    for title in candidates:
        lowered = title.lower()
        if lowered.startswith('list of'):
            continue
        if any(flag in lowered for flag in ('amusement rides', 'timeline of')):
            continue
        if title not in results:
            results.append(title)
        if len(results) >= limit:
            break
    return results


def wiki_search(session: requests.Session, query: str, limit: int = 5) -> list[str]:
    payload = request_json(
        session,
        WIKI_API,
        params={
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': limit,
        },
    )
    return [item['title'] for item in payload.get('query', {}).get('search', [])]


def fetch_extract(session: requests.Session, title: str, chars: int = 3000) -> str:
    if not title:
        return ''
    payload = request_json(
        session,
        WIKI_API,
        params={
            'action': 'query',
            'format': 'json',
            'prop': 'extracts',
            'titles': title,
            'explaintext': 1,
            'exchars': chars,
            'redirects': 1,
        },
    )
    pages = payload.get('query', {}).get('pages', {})
    for page in pages.values():
        extract = page.get('extract', '').strip()
        if extract:
            return extract
    return ''


def find_main_wiki_page(session: requests.Session, title: str) -> str | None:
    candidates = wiki_search(session, f'"{title}"', limit=5)
    for candidate in candidates:
        lowered = candidate.lower()
        if any(flag in lowered for flag in ('character', 'cast', 'episode', 'discography')):
            continue
        return candidate
    return None


def find_character_page(session: requests.Session, title: str) -> str | None:
    queries = [
        f'"{title}" characters',
        f'"List of {title} characters"',
        f'"{title}" cast',
        f'"Characters of {title}"',
    ]
    for query in queries:
        for candidate in wiki_search(session, query):
            lowered = candidate.lower()
            if any(key in lowered for key in ('character', 'cast', 'list of')):
                return candidate
    return None


def build_records(session: requests.Session, titles: Iterable[str], kind: str, out_dir: Path) -> list[dict]:
    records: list[dict] = []
    cache_dir = out_dir / 'wiki'
    cache_dir.mkdir(parents=True, exist_ok=True)
    for index, title in enumerate(titles, start=1):
        main_page_title = find_main_wiki_page(session, title) or title
        main_extract = fetch_extract(session, main_page_title, chars=2400)
        character_page = find_character_page(session, title)
        character_extract = fetch_extract(session, character_page, chars=5000) if character_page else ''
        record = {
            'kind': kind,
            'title': title,
            'main_page_title': main_page_title,
            'main_page_extract': main_extract,
            'character_page_title': character_page,
            'character_page_extract': character_extract,
        }
        records.append(record)
        slug = slugify(f'{kind}-{index:04d}-{title}')
        (cache_dir / f'{slug}.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
        time.sleep(0.05)
    return records


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def main() -> None:
    args = parse_args()
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    session = new_session()

    anime_titles = collect_anime_titles(session, args.anime_limit)
    game_titles = collect_game_titles(session, args.game_limit)

    anime_records = build_records(session, anime_titles, 'anime-film', out_dir / 'anime-films')
    game_records = build_records(session, game_titles, 'game', out_dir / 'games')

    summary = {
        'anime_film_count': len(anime_records),
        'game_count': len(game_records),
        'anime_titles': anime_titles,
        'game_titles': game_titles,
    }
    write_json(out_dir / 'summary.json', summary)

    lines = [
        '# Character Reference Cache',
        '',
        f'- Anime films: {len(anime_records)}',
        f'- Games: {len(game_records)}',
        '',
        '## Anime Film Source Sample',
    ]
    lines.extend([f'- {title}' for title in anime_titles[:50]])
    lines.append('')
    lines.append('## Game Source Sample')
    lines.extend([f'- {title}' for title in game_titles[:50]])
    (out_dir / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
