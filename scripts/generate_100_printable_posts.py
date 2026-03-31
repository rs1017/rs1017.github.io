from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import random

from PIL import Image, ImageDraw

from build_comfyui_final_printables import (
    ASSET_ROOT,
    WIDTH,
    HEIGHT,
    BIG_FONT,
    MID_FONT,
    SMALL_FONT,
    INK,
    blank_page,
    load_icon,
    paste_center,
    line,
    circle,
    rect,
    cloud,
    sun,
    flower_simple,
    house,
    tree,
    pond,
    basket,
    kite,
    train,
    candy,
    generate_maze,
    load_scene,
    fit_box,
)

POST_ROOT = Path(__file__).resolve().parents[1] / '_posts'


def render_symbol(base: Image.Image, draw: ImageDraw.ImageDraw, name: str, cx: int, cy: int, max_w: int, max_h: int, opacity: int = 255, flip: bool = False):
    code_symbols = {'flower', 'cloud', 'sun', 'basket', 'house', 'tree', 'pond', 'kite', 'train', 'candy', 'balloon'}
    if name in code_symbols:
        scale = min(max_w, max_h) / 160
        if name == 'flower':
            flower_simple(draw, cx, cy, scale)
        elif name == 'cloud':
            cloud(draw, cx - 40 * scale, cy - 10 * scale, scale)
        elif name == 'sun':
            sun(draw, cx, cy, int(30 * scale))
        elif name == 'basket':
            basket(draw, cx, cy, scale)
        elif name == 'house':
            house(draw, cx, cy, scale)
        elif name == 'tree':
            tree(draw, cx, cy, scale)
        elif name == 'pond':
            pond(draw, cx, cy, scale)
        elif name == 'kite':
            kite(draw, cx, cy, scale)
        elif name == 'train':
            train(draw, cx, cy, scale)
        elif name == 'candy':
            candy(draw, cx, cy, scale)
        elif name == 'balloon':
            draw.ellipse((cx - 36 * scale, cy - 58 * scale, cx + 36 * scale, cy + 26 * scale), outline=INK, width=4)
            line(draw, [(cx, cy + 26 * scale), (cx - 4 * scale, cy + 78 * scale), (cx + 18 * scale, cy + 124 * scale)], width=3)
        return
    try:
        paste_center(base, load_icon(name), cx, cy, max_w, max_h, opacity=opacity, flip=flip)
    except FileNotFoundError:
        rect(draw, (cx - 40, cy - 40, cx + 40, cy + 40), width=3, radius=12)



COLORING_THEMES = [
    ('2026-03-30-spring-coloring-pack.md', 'coloring-spring', '봄 색칠놀이', 'rabbit', 'tulip', 'butterfly'),
    ('auto', 'coloring-rabbit', '토끼 색칠놀이', 'rabbit', 'flower', 'cloud'),
    ('auto', 'coloring-cat', '고양이 색칠놀이', 'cat', 'flower', 'cloud'),
    ('auto', 'coloring-duck', '오리 색칠놀이', 'duck', 'pond', 'flower'),
    ('auto', 'coloring-fish', '물고기 색칠놀이', 'fish', 'shell', 'starfish'),
    ('auto', 'coloring-whale', '고래 색칠놀이', 'whale', 'cloud', 'sun'),
    ('auto', 'coloring-octopus', '문어 색칠놀이', 'octopus', 'shell', 'fish'),
    ('auto', 'coloring-submarine', '잠수함 색칠놀이', 'submarine', 'fish', 'shell'),
    ('auto', 'coloring-apple', '사과 색칠놀이', 'apple', 'flower', 'cloud'),
    ('auto', 'coloring-balloon', '풍선 색칠놀이', 'balloon', 'cloud', 'sun'),
    ('auto', 'coloring-grapes', '포도 색칠놀이', 'grapes', 'basket', 'flower'),
    ('auto', 'coloring-hat', '모자 색칠놀이', 'hat', 'flower', 'cloud'),
    ('auto', 'coloring-jam', '잼 병 색칠놀이', 'jam', 'basket', 'flower'),
    ('auto', 'coloring-tulip', '튤립 색칠놀이', 'tulip', 'rabbit', 'flower'),
    ('auto', 'coloring-butterfly', '나비 색칠놀이', 'butterfly', 'flower', 'cloud'),
    ('auto', 'coloring-shell', '조개 색칠놀이', 'shell', 'starfish', 'fish'),
    ('auto', 'coloring-starfish', '불가사리 색칠놀이', 'starfish', 'shell', 'fish'),
    ('auto', 'coloring-sun', '해님 색칠놀이', 'sun', 'cloud', 'flower'),
    ('auto', 'coloring-cloud', '구름 색칠놀이', 'cloud', 'sun', 'balloon'),
    ('auto', 'coloring-basket', '바구니 색칠놀이', 'basket', 'apple', 'flower'),
]

HIDDEN_THEMES = [
    ('2026-03-30-garden-hidden-picture.md', 'hidden-garden', '정원 숨은그림', 'garden', ['flower', 'apple', 'butterfly', 'bee', 'rabbit', 'tulip']),
    ('auto', 'hidden-picnic', '소풍 숨은그림', 'picnic', ['basket', 'apple', 'balloon', 'hat', 'jam', 'flower']),
    ('auto', 'hidden-classroom', '교실 숨은그림', 'indoor', ['apple', 'balloon', 'hat', 'cat', 'duck', 'flower']),
    ('auto', 'hidden-kitchen', '주방 숨은그림', 'indoor', ['apple', 'jam', 'egg', 'basket', 'grapes', 'hat']),
    ('auto', 'hidden-forest', '숲 숨은그림', 'forest', ['rabbit', 'butterfly', 'flower', 'shell', 'apple', 'duck']),
    ('auto', 'hidden-beach', '해변 숨은그림', 'beach', ['shell', 'starfish', 'fish', 'balloon', 'apple', 'whale']),
    ('auto', 'hidden-bedroom', '방 숨은그림', 'indoor', ['hat', 'cat', 'balloon', 'apple', 'jam', 'flower']),
    ('auto', 'hidden-bakery', '빵집 숨은그림', 'market', ['basket', 'jam', 'apple', 'grapes', 'hat', 'balloon']),
    ('auto', 'hidden-camping', '캠핑 숨은그림', 'forest', ['cloud', 'sun', 'basket', 'apple', 'rabbit', 'hat']),
    ('auto', 'hidden-party', '파티 숨은그림', 'picnic', ['balloon', 'hat', 'candy', 'apple', 'jam', 'flower']),
    ('auto', 'hidden-market', '시장 숨은그림', 'market', ['apple', 'grapes', 'basket', 'balloon', 'hat', 'flower']),
    ('auto', 'hidden-playground', '놀이터 숨은그림', 'playground', ['balloon', 'rabbit', 'flower', 'kite', 'apple', 'duck']),
    ('auto', 'hidden-zoo', '동물 숨은그림', 'forest', ['cat', 'duck', 'rabbit', 'fish', 'apple', 'butterfly']),
    ('auto', 'hidden-farm', '농장 숨은그림', 'farm', ['duck', 'egg', 'apple', 'basket', 'flower', 'rabbit']),
    ('auto', 'hidden-toyroom', '장난감 숨은그림', 'indoor', ['balloon', 'train', 'kite', 'cat', 'apple', 'hat']),
    ('auto', 'hidden-rainy', '비 오는 날 숨은그림', 'rainy', ['cloud', 'sun', 'duck', 'fish', 'flower', 'balloon']),
    ('auto', 'hidden-garden-2', '꽃길 숨은그림', 'garden', ['flower', 'butterfly', 'apple', 'bee', 'basket', 'tulip']),
    ('auto', 'hidden-ocean', '바다 숨은그림', 'beach', ['fish', 'shell', 'starfish', 'whale', 'submarine', 'octopus']),
    ('auto', 'hidden-spring', '봄 숨은그림', 'garden', ['rabbit', 'tulip', 'butterfly', 'flower', 'cloud', 'sun']),
    ('auto', 'hidden-home', '집 숨은그림', 'indoor', ['house', 'apple', 'flower', 'cat', 'hat', 'basket']),
]

MAZE_THEMES = [
    ('2026-03-31-rainy-day-maze.md', 'maze-rainy', '비 오는 날 미로', 'cloud', 'sun'),
    ('auto', 'maze-rabbit', '토끼 미로', 'rabbit', 'tulip'),
    ('auto', 'maze-shell', '조개 미로', 'shell', 'starfish'),
    ('auto', 'maze-balloon', '풍선 미로', 'balloon', 'flower'),
    ('auto', 'maze-apple', '사과 미로', 'apple', 'basket'),
    ('auto', 'maze-starfish', '별 미로', 'starfish', 'sun'),
    ('auto', 'maze-dinosaur', '공룡 미로', 'cat', 'flower'),
    ('auto', 'maze-kite', '연 미로', 'kite', 'cloud'),
    ('auto', 'maze-train', '기차 미로', 'train', 'house'),
    ('auto', 'maze-candy', '사탕 미로', 'candy', 'flower'),
    ('auto', 'maze-fish', '물고기 미로', 'fish', 'shell'),
    ('auto', 'maze-duck', '오리 미로', 'duck', 'pond'),
    ('auto', 'maze-whale', '고래 미로', 'whale', 'cloud'),
    ('auto', 'maze-submarine', '잠수함 미로', 'submarine', 'fish'),
    ('auto', 'maze-hat', '모자 미로', 'hat', 'basket'),
    ('auto', 'maze-jam', '잼 미로', 'jam', 'apple'),
    ('auto', 'maze-cloud', '구름 미로', 'cloud', 'sun'),
    ('auto', 'maze-butterfly', '나비 미로', 'butterfly', 'flower'),
    ('auto', 'maze-grapes', '포도 미로', 'grapes', 'basket'),
    ('auto', 'maze-octopus', '문어 미로', 'octopus', 'fish'),
]

CUTPASTE_THEMES = [
    ('2026-03-30-ocean-cut-paste.md', 'cut-paste-ocean', '바다 오려붙이기', ['whale', 'fish', 'shell', 'submarine', 'octopus']),
    ('auto', 'cut-paste-farm', '농장 오려붙이기', ['duck', 'egg', 'rabbit', 'apple', 'basket']),
    ('auto', 'cut-paste-fruit', '과일 오려붙이기', ['apple', 'grapes', 'basket', 'jam', 'balloon']),
    ('auto', 'cut-paste-spring', '봄 오려붙이기', ['rabbit', 'tulip', 'butterfly', 'flower', 'basket']),
    ('auto', 'cut-paste-weather', '날씨 오려붙이기', ['cloud', 'sun', 'balloon', 'kite', 'flower']),
    ('auto', 'cut-paste-pets', '반려동물 오려붙이기', ['cat', 'rabbit', 'duck', 'basket', 'flower']),
    ('auto', 'cut-paste-picnic', '소풍 오려붙이기', ['basket', 'apple', 'balloon', 'hat', 'jam']),
    ('auto', 'cut-paste-ride', '탈것 오려붙이기', ['submarine', 'train', 'kite', 'balloon', 'fish']),
    ('auto', 'cut-paste-style', '꾸미기 오려붙이기', ['hat', 'flower', 'butterfly', 'jam', 'balloon']),
    ('auto', 'cut-paste-snack', '간식 오려붙이기', ['jam', 'apple', 'icecream', 'grapes', 'basket']),
]

TRACING_THEMES = [
    ('2026-04-01-basic-line-tracing.md', 'line-tracing', '기초 선긋기', [('tulip', 'tulip'), ('cloud', 'sun'), ('rabbit', 'tulip'), ('starfish', 'balloon'), ('butterfly', 'flower'), ('fish', 'shell'), ('duck', 'pond'), ('apple', 'basket'), ('hat', 'jam'), ('whale', 'starfish')]),
    ('auto', 'curve-tracing', '곡선 선긋기', [('cloud', 'sun'), ('balloon', 'flower'), ('rabbit', 'flower'), ('fish', 'shell'), ('apple', 'basket'), ('duck', 'pond'), ('hat', 'jam'), ('whale', 'cloud'), ('butterfly', 'tulip'), ('grapes', 'basket')]),
    ('auto', 'zigzag-tracing', '지그재그 선긋기', [('tulip', 'balloon'), ('fish', 'starfish'), ('apple', 'flower'), ('cloud', 'sun'), ('rabbit', 'basket'), ('hat', 'jam'), ('duck', 'pond'), ('grapes', 'basket'), ('whale', 'shell'), ('cat', 'flower')]),
    ('auto', 'animal-tracing', '동물 선긋기', [('rabbit', 'cat'), ('duck', 'rabbit'), ('fish', 'whale'), ('cat', 'duck'), ('whale', 'fish'), ('octopus', 'fish'), ('rabbit', 'flower'), ('duck', 'pond'), ('cat', 'basket'), ('whale', 'cloud')]),
    ('auto', 'spring-tracing', '봄길 선긋기', [('tulip', 'flower'), ('butterfly', 'flower'), ('rabbit', 'tulip'), ('cloud', 'sun'), ('basket', 'flower'), ('apple', 'flower'), ('duck', 'flower'), ('grapes', 'flower'), ('hat', 'flower'), ('rabbit', 'cloud')]),
    ('auto', 'ocean-tracing', '바다길 선긋기', [('fish', 'shell'), ('whale', 'shell'), ('octopus', 'fish'), ('submarine', 'fish'), ('starfish', 'shell'), ('fish', 'starfish'), ('whale', 'starfish'), ('octopus', 'shell'), ('submarine', 'shell'), ('fish', 'whale')]),
    ('auto', 'weather-tracing', '날씨 선긋기', [('cloud', 'sun'), ('balloon', 'cloud'), ('kite', 'sun'), ('cloud', 'flower'), ('sun', 'basket'), ('balloon', 'sun'), ('kite', 'cloud'), ('sun', 'flower'), ('cloud', 'basket'), ('balloon', 'kite')]),
    ('auto', 'food-tracing', '간식 선긋기', [('apple', 'jam'), ('grapes', 'basket'), ('jam', 'basket'), ('apple', 'grapes'), ('icecream', 'jam'), ('apple', 'basket'), ('grapes', 'jam'), ('icecream', 'apple'), ('basket', 'jam'), ('apple', 'icecream')]),
    ('auto', 'toy-tracing', '놀이 선긋기', [('balloon', 'kite'), ('train', 'balloon'), ('kite', 'train'), ('hat', 'balloon'), ('basket', 'kite'), ('balloon', 'hat'), ('train', 'basket'), ('kite', 'hat'), ('balloon', 'basket'), ('train', 'kite')]),
    ('auto', 'travel-tracing', '이동 선긋기', [('train', 'house'), ('submarine', 'fish'), ('kite', 'cloud'), ('balloon', 'sun'), ('train', 'basket'), ('submarine', 'shell'), ('kite', 'flower'), ('train', 'cloud'), ('submarine', 'starfish'), ('balloon', 'house')]),
]

COUNTING_THEMES = [
    ('auto', 'count-rabbit', '토끼 숫자 세기', 'rabbit'),
    ('auto', 'count-apple', '사과 숫자 세기', 'apple'),
    ('auto', 'count-fish', '물고기 숫자 세기', 'fish'),
    ('auto', 'count-flower', '꽃 숫자 세기', 'flower'),
    ('auto', 'count-balloon', '풍선 숫자 세기', 'balloon'),
    ('auto', 'count-cat', '고양이 숫자 세기', 'cat'),
    ('auto', 'count-duck', '오리 숫자 세기', 'duck'),
    ('auto', 'count-shell', '조개 숫자 세기', 'shell'),
    ('auto', 'count-star', '별 숫자 세기', 'starfish'),
    ('auto', 'count-grapes', '포도 숫자 세기', 'grapes'),
]

ENGLISH_THEMES = [
    ('2026-04-01-animal-english-words.md', 'english-words', '영어 단어 놀이', [('A', 'APPLE', 'apple'), ('B', 'BALLOON', 'balloon'), ('C', 'CAT', 'cat'), ('D', 'DUCK', 'duck'), ('E', 'EGG', 'egg'), ('F', 'FISH', 'fish'), ('G', 'GRAPES', 'grapes'), ('H', 'HAT', 'hat'), ('I', 'ICE CREAM', 'icecream'), ('J', 'JAM', 'jam')]),
    ('auto', 'english-animal', '동물 영어 놀이', [('C', 'CAT', 'cat'), ('D', 'DUCK', 'duck'), ('F', 'FISH', 'fish'), ('R', 'RABBIT', 'rabbit'), ('W', 'WHALE', 'whale'), ('O', 'OCTOPUS', 'octopus'), ('B', 'BEE', 'bee'), ('S', 'SHELL', 'shell'), ('S', 'STARFISH', 'starfish'), ('B', 'BUTTERFLY', 'butterfly')]),
    ('auto', 'english-fruit', '과일 영어 놀이', [('A', 'APPLE', 'apple'), ('G', 'GRAPES', 'grapes'), ('J', 'JAM', 'jam'), ('A', 'APPLE', 'apple'), ('G', 'GRAPES', 'grapes'), ('J', 'JAM', 'jam'), ('A', 'APPLE', 'apple'), ('G', 'GRAPES', 'grapes'), ('J', 'JAM', 'jam'), ('A', 'APPLE', 'apple')]),
    ('auto', 'english-ocean', '바다 영어 놀이', [('F', 'FISH', 'fish'), ('S', 'SHELL', 'shell'), ('W', 'WHALE', 'whale'), ('O', 'OCTOPUS', 'octopus'), ('S', 'STARFISH', 'starfish'), ('S', 'SUBMARINE', 'submarine'), ('F', 'FISH', 'fish'), ('W', 'WHALE', 'whale'), ('S', 'SHELL', 'shell'), ('O', 'OCTOPUS', 'octopus')]),
    ('auto', 'english-spring', '봄 영어 놀이', [('F', 'FLOWER', 'flower'), ('T', 'TULIP', 'tulip'), ('B', 'BUTTERFLY', 'butterfly'), ('R', 'RABBIT', 'rabbit'), ('C', 'CLOUD', 'cloud'), ('S', 'SUN', 'sun'), ('B', 'BASKET', 'basket'), ('F', 'FLOWER', 'flower'), ('T', 'TULIP', 'tulip'), ('R', 'RABBIT', 'rabbit')]),
    ('auto', 'english-weather', '날씨 영어 놀이', [('C', 'CLOUD', 'cloud'), ('S', 'SUN', 'sun'), ('B', 'BALLOON', 'balloon'), ('K', 'KITE', 'kite'), ('C', 'CLOUD', 'cloud'), ('S', 'SUN', 'sun'), ('B', 'BALLOON', 'balloon'), ('K', 'KITE', 'kite'), ('C', 'CLOUD', 'cloud'), ('S', 'SUN', 'sun')]),
    ('auto', 'english-home', '집 영어 놀이', [('H', 'HOUSE', 'house'), ('B', 'BASKET', 'basket'), ('H', 'HAT', 'hat'), ('J', 'JAM', 'jam'), ('A', 'APPLE', 'apple'), ('C', 'CLOUD', 'cloud'), ('S', 'SUN', 'sun'), ('H', 'HOUSE', 'house'), ('B', 'BASKET', 'basket'), ('H', 'HAT', 'hat')]),
    ('auto', 'english-play', '놀이 영어 놀이', [('B', 'BALLOON', 'balloon'), ('K', 'KITE', 'kite'), ('T', 'TRAIN', 'train'), ('H', 'HAT', 'hat'), ('C', 'CANDY', 'candy'), ('B', 'BALLOON', 'balloon'), ('K', 'KITE', 'kite'), ('T', 'TRAIN', 'train'), ('H', 'HAT', 'hat'), ('C', 'CANDY', 'candy')]),
    ('auto', 'english-travel', '이동 영어 놀이', [('T', 'TRAIN', 'train'), ('S', 'SUBMARINE', 'submarine'), ('B', 'BALLOON', 'balloon'), ('K', 'KITE', 'kite'), ('H', 'HOUSE', 'house'), ('T', 'TRAIN', 'train'), ('S', 'SUBMARINE', 'submarine'), ('B', 'BALLOON', 'balloon'), ('K', 'KITE', 'kite'), ('H', 'HOUSE', 'house')]),
    ('auto', 'english-mixed', '기초 영어 놀이', [('A', 'APPLE', 'apple'), ('R', 'RABBIT', 'rabbit'), ('S', 'SUN', 'sun'), ('F', 'FISH', 'fish'), ('H', 'HAT', 'hat'), ('B', 'BALLOON', 'balloon'), ('J', 'JAM', 'jam'), ('T', 'TULIP', 'tulip'), ('C', 'CAT', 'cat'), ('W', 'WHALE', 'whale')]),
]


def build_filename(date: datetime, slug: str) -> str:
    return f"{date:%Y-%m-%d}-{slug}.md"


def post_markdown(title: str, date: datetime, categories: list[str], tags: list[str], description: str, folder: str, captions: list[str]) -> str:
    figures = []
    for i, caption in enumerate(captions, start=1):
        figures.append(f'  <figure class="post-image"><img src="/assets/img/playroom/{folder}/{i:02d}.png" alt="{caption}" decoding="async" width="1024" height="768" loading="lazy" fetchpriority="low" /><figcaption>{caption}</figcaption></figure>')
    return (
        '---\n'
        f'title: {title}\n'
        f'date: {date:%Y-%m-%d %H:%M:%S} +0900\n'
        f'categories: [{", ".join(categories)}]\n'
        f'tags: [{", ".join(tags)}]\n'
        f'description: "{description}"\n'
        'image:\n'
        f'  path: /assets/img/playroom/{folder}/01.png\n'
        '---\n\n'
        '<section class="post-gallery">\n' + '\n'.join(figures) + '\n</section>\n'
    )


def make_coloring(main: str, secondary: str, accent: str, idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    draw = ImageDraw.Draw(base)
    cloud(draw, 132, 118, 1.0)
    cloud(draw, 770, 126, 0.92)
    sun(draw, 894, 110, 30)
    line(draw, [(64, 650), (242, 622), (438, 650), (652, 618), (956, 650)], width=4)
    variant = idx % 5
    if variant == 0:
        render_symbol(base, draw, main, 512, 420, 600, 520)
        render_symbol(base, draw, secondary, 196, 514, 240, 260)
        render_symbol(base, draw, secondary, 836, 514, 240, 260, flip=True)
        render_symbol(base, draw, accent, 300, 246, 180, 150)
        render_symbol(base, draw, accent, 724, 228, 180, 150, flip=True)
    elif variant == 1:
        house(draw, 514, 344, 1.22)
        render_symbol(base, draw, secondary, 274, 520, 220, 240)
        render_symbol(base, draw, secondary, 770, 520, 220, 240, flip=True)
        render_symbol(base, draw, main, 768, 316, 260, 230)
        render_symbol(base, draw, accent, 256, 232, 180, 150)
    elif variant == 2:
        tree(draw, 228, 286, 1.12)
        tree(draw, 748, 302, 1.0)
        render_symbol(base, draw, main, 520, 500, 420, 360)
        render_symbol(base, draw, accent, 316, 238, 190, 150)
        render_symbol(base, draw, accent, 708, 226, 190, 150, flip=True)
        render_symbol(base, draw, secondary, 844, 556, 180, 180)
    elif variant == 3:
        basket(draw, 512, 500, 1.35)
        render_symbol(base, draw, secondary, 328, 382, 190, 220)
        render_symbol(base, draw, secondary, 696, 382, 190, 220, flip=True)
        render_symbol(base, draw, accent, 512, 220, 220, 170)
        render_symbol(base, draw, main, 804, 550, 200, 180)
    else:
        pond(draw, 512, 558, 1.05)
        render_symbol(base, draw, main, 354, 438, 280, 230)
        render_symbol(base, draw, main, 670, 420, 300, 240, flip=True)
        render_symbol(base, draw, accent, 520, 228, 200, 150)
        render_symbol(base, draw, secondary, 224, 586, 170, 170)
        render_symbol(base, draw, secondary, 826, 590, 170, 170, flip=True)
    return base.convert('RGB')


def hidden_scene(draw: ImageDraw.ImageDraw, scene: str):
    if scene == 'garden':
        house(draw, 540, 288, 0.95)
        tree(draw, 180, 210, 0.9)
        tree(draw, 806, 214, 0.9)
        line(draw, [(400, 530), (512, 410), (636, 530)], width=4)
    elif scene == 'indoor':
        rect(draw, (130, 150, 894, 530), width=4, radius=18)
        line(draw, [(182, 218), (842, 218)], width=3)
        line(draw, [(182, 316), (842, 316)], width=3)
        line(draw, [(182, 414), (842, 414)], width=3)
    elif scene == 'picnic':
        line(draw, [(70, 610), (950, 610)], width=4)
        rect(draw, (300, 360, 724, 560), width=4, radius=18)
        cloud(draw, 178, 128, 0.82)
        sun(draw, 886, 120, 28)
    elif scene == 'beach':
        line(draw, [(80, 520), (320, 468), (520, 494), (742, 462), (940, 500)], width=4)
        line(draw, [(90, 596), (292, 552), (520, 584), (726, 546), (942, 588)], width=4)
        sun(draw, 860, 118, 28)
    elif scene == 'forest':
        tree(draw, 180, 206, 1.0)
        tree(draw, 732, 192, 1.15)
        tree(draw, 470, 236, 0.86)
        line(draw, [(64, 610), (250, 572), (474, 616), (690, 568), (954, 610)], width=4)
    elif scene == 'market':
        rect(draw, (144, 224, 360, 520), width=4, radius=14)
        rect(draw, (412, 184, 620, 520), width=4, radius=14)
        rect(draw, (680, 224, 880, 520), width=4, radius=14)
        line(draw, [(64, 610), (954, 610)], width=4)
    elif scene == 'playground':
        line(draw, [(70, 610), (950, 610)], width=4)
        line(draw, [(240, 200), (240, 500)], width=4)
        line(draw, [(240, 200), (392, 200)], width=4)
        line(draw, [(272, 232), (272, 420)], width=4)
        line(draw, [(360, 232), (360, 420)], width=4)
        line(draw, [(272, 420), (360, 420)], width=4)
    elif scene == 'farm':
        house(draw, 548, 294, 0.9)
        line(draw, [(70, 610), (950, 610)], width=4)
        line(draw, [(160, 520), (160, 336), (332, 336)], width=4)
        line(draw, [(332, 336), (332, 520)], width=4)
        line(draw, [(130, 520), (362, 520)], width=4)
    else:  # rainy
        cloud(draw, 160, 110, 0.85)
        cloud(draw, 760, 118, 0.85)
        line(draw, [(92, 610), (950, 610)], width=4)
        pond(draw, 538, 520, 0.8)


def make_hidden(pool: list[str], scene: str, idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    draw = ImageDraw.Draw(base)
    scene_img = fit_box(load_scene('hidden-garden', (idx % 10) + 1), 900, 500)
    base.alpha_composite(scene_img, (62 + (900 - scene_img.width) // 2, 68 + (500 - scene_img.height) // 2))
    hidden_scene(draw, scene)
    items = [pool[(idx + shift) % len(pool)] for shift in range(4)]
    hero_positions = [
        [(166, 210), (338, 300), (686, 248), (846, 210)],
        [(182, 388), (346, 470), (686, 404), (840, 486)],
        [(200, 244), (438, 184), (646, 486), (836, 394)],
        [(210, 452), (420, 320), (612, 220), (828, 540)],
        [(174, 224), (374, 514), (700, 214), (842, 430)],
    ][idx % 5]
    for (x, y), name in zip(hero_positions, items):
        render_symbol(base, draw, name, x, y, 104, 104)
    distractors = [pool[(idx + 2 + off) % len(pool)] for off in range(6)]
    distract_positions = [(244, 154), (540, 146), (792, 170), (222, 556), (532, 564), (806, 560)]
    for (x, y), name in zip(distract_positions, distractors):
        render_symbol(base, draw, name, x, y, 56, 56, opacity=160)
    rect(draw, (158, 620, 866, 736), width=4, radius=24)
    for slot, name in enumerate(items):
        cx = 246 + slot * 154
        rect(draw, (cx - 54, 642, cx + 54, 714), width=4, radius=18)
        render_symbol(base, draw, name, cx, 678, 74, 74)
    return base.convert('RGB')


def make_maze(start_symbol: str, end_symbol: str, idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    draw = ImageDraw.Draw(base)
    left, top, cell, cols, rows = 92, 120, 68, 12, 8
    rect(draw, (72, 98, 952, 700), width=4, radius=28)
    grid = generate_maze(cols, rows, 1800 + idx)
    for y in range(rows):
        for x in range(cols):
            x1, y1 = left + x * cell, top + y * cell
            x2, y2 = x1 + cell, y1 + cell
            if 'N' not in grid[y][x]:
                line(draw, [(x1, y1), (x2, y1)], width=5)
            if 'W' not in grid[y][x]:
                line(draw, [(x1, y1), (x1, y2)], width=5)
            if y == rows - 1 and 'S' not in grid[y][x]:
                line(draw, [(x1, y2), (x2, y2)], width=5)
            if x == cols - 1 and 'E' not in grid[y][x]:
                line(draw, [(x2, y1), (x2, y2)], width=5)
    circle(draw, left + 18, top + 34, 16, width=4)
    circle(draw, left + cols * cell - 18, top + rows * cell - 34, 16, width=4)
    render_symbol(base, draw, start_symbol, 120, 84, 92, 92)
    render_symbol(base, draw, end_symbol, 916, 676, 92, 92)
    return base.convert('RGB')


def make_cutpaste(pool: list[str], idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    draw = ImageDraw.Draw(base)
    items = [pool[(idx + shift) % len(pool)] for shift in range(3)]
    draw.arc((84, 394, 944, 468), 0, 180, fill=INK, width=4)
    slot_centers = [(220, 258), (512, 230), (804, 268)]
    piece_centers = [(220, 640), (512, 640), (804, 640)]
    for (cx, cy), name in zip(slot_centers, items):
        rect(draw, (cx - 104, cy - 92, cx + 104, cy + 92), width=3, radius=22)
        render_symbol(base, draw, name, cx, cy, 170, 150, opacity=80)
    line(draw, [(86, 518), (938, 518)], width=2)
    for (cx, cy), name in zip(piece_centers, items):
        x1, y1, x2, y2 = cx - 118, cy - 86, cx + 118, cy + 86
        for seg in range(x1, x2, 22):
            line(draw, [(seg, y1), (min(seg + 12, x2), y1)], width=2)
            line(draw, [(seg, y2), (min(seg + 12, x2), y2)], width=2)
        for seg in range(y1, y2, 22):
            line(draw, [(x1, seg), (x1, min(seg + 12, y2))], width=2)
            line(draw, [(x2, seg), (x2, min(seg + 12, y2))], width=2)
        render_symbol(base, draw, name, cx, cy, 170, 160)
    return base.convert('RGB')


def make_english(words: list[tuple[str, str, str]], idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    draw = ImageDraw.Draw(base)
    letter, word, icon = words[idx]
    draw.text((86, 78), f'{letter} {letter.lower()}', fill=INK, font=BIG_FONT)
    render_symbol(base, draw, icon, 824, 176, 180, 160)
    for row in range(3):
        y = 238 + row * 126
        line(draw, [(92, y + 70), (934, y + 70)], width=2)
        line(draw, [(92, y + 28), (934, y + 28)], width=1)
        draw.text((112, y - 12), word, fill=INK, font=MID_FONT)
        for x in range(300, 924, 20):
            circle(draw, x, y + 28, 2, width=1)
    render_symbol(base, draw, icon, 512, 602, 260, 220)
    return base.convert('RGB')


def make_tracing(pairs: list[tuple[str, str]], idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    draw = ImageDraw.Draw(base)
    start_symbol, end_symbol = pairs[idx]
    paths = [
        [(144, 584), (268, 438), (396, 310), (512, 368), (652, 512), (880, 238)],
        [(144, 584), (250, 372), (420, 196), (626, 286), (744, 508), (886, 224)],
        [(144, 582), (286, 338), (480, 536), (664, 368), (884, 236)],
        [(144, 584), (290, 472), (312, 274), (526, 272), (720, 540), (880, 228)],
        [(146, 586), (266, 502), (364, 296), (530, 360), (736, 574), (884, 232)],
        [(144, 584), (302, 630), (408, 266), (560, 338), (744, 604), (886, 230)],
        [(146, 586), (310, 360), (460, 582), (606, 326), (770, 202), (886, 228)],
        [(146, 582), (272, 264), (454, 294), (570, 530), (762, 462), (888, 224)],
        [(148, 588), (250, 402), (332, 540), (476, 312), (726, 192), (886, 230)],
        [(148, 580), (332, 274), (446, 560), (596, 330), (754, 182), (886, 230)],
    ]
    path = paths[idx]
    for start, end in zip(path, path[1:]):
        sx, sy = start
        ex, ey = end
        dist = max(1, int(((ex - sx) ** 2 + (ey - sy) ** 2) ** 0.5))
        count = max(1, dist // 18)
        for i in range(count + 1):
            t = i / count
            circle(draw, sx + (ex - sx) * t, sy + (ey - sy) * t, 3, width=2)
    circle(draw, path[0][0], path[0][1], 18, width=4)
    circle(draw, path[-1][0], path[-1][1], 18, width=4)
    render_symbol(base, draw, start_symbol, 138, 582, 150, 130)
    render_symbol(base, draw, end_symbol, 886, 214, 150, 130)
    return base.convert('RGB')


def make_counting(symbol: str, idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    draw = ImageDraw.Draw(base)
    count = idx + 1
    draw.text((88, 68), str(count), fill=INK, font=BIG_FONT)
    draw.text((184, 102), 'COUNT', fill=INK, font=SMALL_FONT)
    cols = 5
    spacing_x = 152
    spacing_y = 164
    start_x = 220
    start_y = 246
    for n in range(count):
        row = n // cols
        col = n % cols
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        render_symbol(base, draw, symbol, x, y, 156, 136)
    for x in range(152, 918, 150):
        line(draw, [(x, 620), (x + 74, 620)], width=2)
    return base.convert('RGB')


def make_matching(pool: list[str], idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    draw = ImageDraw.Draw(base)
    items = [pool[(idx + shift) % len(pool)] for shift in range(3)]
    shuffled = [items[2], items[0], items[1]]
    left_x = 252
    right_x = 772
    ys = [204, 388, 572]
    for i, (left, right, y) in enumerate(zip(items, shuffled, ys), start=1):
        rect(draw, (118, y - 70, 386, y + 70), width=3, radius=22)
        rect(draw, (638, y - 70, 906, y + 70), width=3, radius=22)
        draw.text((96, y - 18), str(i), fill=INK, font=MID_FONT)
        draw.text((922, y - 18), chr(64 + i), fill=INK, font=MID_FONT)
        render_symbol(base, draw, left, left_x, y, 136, 120)
        render_symbol(base, draw, right, right_x, y, 136, 120)
    return base.convert('RGB')


def make_same_different(pool: list[str], idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    draw = ImageDraw.Draw(base)
    main = pool[idx % len(pool)]
    other = pool[(idx + 2) % len(pool)]
    centers = [(250, 250), (772, 250), (250, 560), (772, 560)]
    picks = [main, main, other, main]
    for (cx, cy), name in zip(centers, picks):
        rect(draw, (cx - 140, cy - 106, cx + 140, cy + 106), width=3, radius=22)
        render_symbol(base, draw, name, cx, cy, 170, 150)
    draw.text((372, 80), 'DIFFERENT', fill=INK, font=MID_FONT)
    return base.convert('RGB')


def save_post(filename: str, folder: str, title: str, categories: list[str], tags: list[str], description: str, captions: list[str], renderer):
    out_dir = ASSET_ROOT / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(10):
        img = renderer(idx)
        img.save(out_dir / f'{idx + 1:02d}.png', optimize=True)
    (POST_ROOT / filename).write_text(post_markdown(title, CURRENT_DATE, categories, tags, description, folder, captions), encoding='utf-8')


CURRENT_DATE = datetime(2026, 4, 1, 9, 0)
extra_offset = 1


def next_filename(slug: str) -> str:
    global extra_offset
    date = datetime(2026, 4, 2) + timedelta(days=extra_offset - 1)
    extra_offset += 1
    return build_filename(date, slug)


all_posts = []

for filename, folder, title, main, secondary, accent in COLORING_THEMES:
    file_name = filename if filename != 'auto' else next_filename(folder)
    captions = [f'{title.split()[0]} {i}' for i in range(1, 11)]
    all_posts.append((file_name, folder, title, ['프린터블', '색칠'], ['색칠', '유아'], f'{title} 흑백 출력 활동지 세트.', captions, lambda idx, m=main, s=secondary, a=accent: make_coloring(m, s, a, idx)))

for filename, folder, title, scene, pool in HIDDEN_THEMES:
    file_name = filename if filename != 'auto' else next_filename(folder)
    captions = [f'찾기 {i}' for i in range(1, 11)]
    all_posts.append((file_name, folder, title, ['프린터블', '숨은그림'], ['숨은그림', '찾기', '유아'], f'{title} 흑백 출력 활동지 세트.', captions, lambda idx, p=pool, s=scene: make_hidden(p, s, idx)))

for filename, folder, title, start_symbol, end_symbol in MAZE_THEMES:
    file_name = filename if filename != 'auto' else next_filename(folder)
    captions = [f'길 {i}' for i in range(1, 11)]
    all_posts.append((file_name, folder, title, ['프린터블', '미로'], ['미로', '길찾기', '유아'], f'{title} 흑백 출력 활동지 세트.', captions, lambda idx, a=start_symbol, b=end_symbol: make_maze(a, b, idx)))

for filename, folder, title, pool in CUTPASTE_THEMES:
    file_name = filename if filename != 'auto' else next_filename(folder)
    captions = [f'조각 {i}' for i in range(1, 11)]
    all_posts.append((file_name, folder, title, ['프린터블', '오려붙이기'], ['오리기', '붙이기', '유아'], f'{title} 흑백 출력 활동지 세트.', captions, lambda idx, p=pool: make_cutpaste(p, idx)))

for filename, folder, title, words in ENGLISH_THEMES:
    file_name = filename if filename != 'auto' else next_filename(folder)
    captions = [word[1] for word in words]
    all_posts.append((file_name, folder, title, ['프린터블', '영어'], ['영어', '알파벳', '유아'], f'{title} 출력 활동지 세트.', captions, lambda idx, w=words: make_english(w, idx)))

for filename, folder, title, pairs in TRACING_THEMES:
    file_name = filename if filename != 'auto' else next_filename(folder)
    captions = [f'따라 {i}' for i in range(1, 11)]
    all_posts.append((file_name, folder, title, ['프린터블', '선긋기'], ['선긋기', '따라쓰기', '유아'], f'{title} 출력 활동지 세트.', captions, lambda idx, p=pairs: make_tracing(p, idx)))

for filename, folder, title, symbol in COUNTING_THEMES:
    file_name = filename if filename != 'auto' else next_filename(folder)
    captions = [f'{i}개 세기' for i in range(1, 11)]
    all_posts.append((file_name, folder, title, ['프린터블', '숫자'], ['숫자', '세기', '유아'], f'{title} 출력 활동지 세트.', captions, lambda idx, s=symbol: make_counting(s, idx)))

MATCH_POOLS = []

SAME_POOLS = []

assert len(all_posts) == 100, len(all_posts)

for filename, folder, title, categories, tags, description, captions, renderer in all_posts:
    out_dir = ASSET_ROOT / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(10):
        img = renderer(idx)
        img.save(out_dir / f'{idx + 1:02d}.png', optimize=True)
    post_date = datetime(2026, 4, 1, 9, 0)
    (POST_ROOT / filename).write_text(post_markdown(title, post_date, categories, tags, description, folder, captions), encoding='utf-8')

print(f'POSTS_GENERATED={len(all_posts)}')





