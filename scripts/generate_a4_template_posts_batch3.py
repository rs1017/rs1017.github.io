from __future__ import annotations

import random
import sys
from pathlib import Path

from PIL import ImageDraw
sys.path.append(str(Path(__file__).resolve().parent))
import generate_a4_template_posts as base

POST_ROOT = base.POST_ROOT
ASSET_ROOT = base.ASSET_ROOT
A4P = base.A4P
A4L = base.A4L
DRAWERS = base.DRAWERS
NUMBER_WORDS = base.NUMBER_WORDS
ENGLISH_WORDS = ['apple', 'hat', 'jam', 'balloon', 'cat', 'dog', 'duck', 'fish', 'grapes', 'icecream']
COUNT_OBJECTS = [('물고기', 'fish'), ('조개', 'shell'), ('별', 'star'), ('풍선', 'balloon'), ('오리', 'duck'), ('토끼', 'rabbit'), ('사과', 'apple'), ('꽃', 'flower'), ('포도', 'grapes'), ('물고기', 'fish')]


def counting_page(index):
    img, d = base.page(A4P)
    count = index + 1
    obj_name, obj_key = COUNT_OBJECTS[index]
    base.header(d, A4P, f'{count} 바다 숫자 학습지', 'scene · trace · more or less')
    base.box(d, (56, 180, 760, 930))
    base.center(d, f'{obj_name}을 세고 숫자를 고르세요', (408, 214), base.BODY)
    placed = 0
    for row in range(3):
        for col in range(4):
            if placed >= count: break
            DRAWERS[obj_key](d, 170 + col * 150, 330 + row * 150, 0.72)
            placed += 1
    base.trace_text(d, str(count), (800, 180, 1168, 418), 2)
    base.trace_text(d, NUMBER_WORDS[index], (800, 438, 1168, 676), 2)
    base.ten_frame(d, (800, 696, 1168, 934), count)
    base.choices(d, [str(max(1, count - 1)), str(count), str(min(10, count + 1))], (56, 976, 590, 1120))
    base.choices(d, ['적다', '같다', '많다'], (616, 976, 1168, 1120))
    base.box(d, (56, 1148, 1168, 1678))
    base.center(d, 'draw more to make 10', (612, 1184), base.BODY)
    for i in range(5):
        base.circle(d, 200 + i * 170, 1390, 40, width=3)
        if i < min(5, count):
            DRAWERS[obj_key](d, 200 + i * 170, 1390, 0.28)
    for i in range(5):
        base.circle(d, 200 + i * 170, 1546, 40, width=3)
    base.center(d, '위 칸을 세고 아래 빈 칸에 더 그려 10을 만드세요', (612, 1646), base.SMALL)
    return img


def english_page(index):
    img, d = base.page(A4P)
    word = ENGLISH_WORDS[index]
    base.header(d, A4P, f'{word.upper()} worksheet', 'picture · trace · match · sentence')
    base.box(d, (56, 180, 620, 840))
    base.center(d, 'big picture', (338, 216), base.BODY)
    DRAWERS[word if word in DRAWERS else 'cat'](d, 338, 500, 1.15)
    base.trace_text(d, word, (654, 180, 1184, 418), 3)
    base.letter_boxes(d, (word[0].upper(), word[0].lower()), (654, 438, 1184, 598))
    base.choices(d, [word, ENGLISH_WORDS[(index + 1) % 10], ENGLISH_WORDS[(index + 2) % 10]], (654, 618, 1184, 778))
    base.box(d, (56, 870, 1184, 1248))
    base.center(d, 'picture to word match', (620, 906), base.BODY)
    for cx, opt in zip([210, 460, 710, 960], [word, ENGLISH_WORDS[(index + 3) % 10], ENGLISH_WORDS[(index + 5) % 10], ENGLISH_WORDS[(index + 7) % 10]]):
        base.box(d, (cx - 90, 950, cx + 90, 1160), width=2, radius=18)
        DRAWERS[opt if opt in DRAWERS else 'cat'](d, cx, 1040, 0.42)
        base.center(d, opt, (cx, 1200), base.SMALL)
    base.box(d, (56, 1288, 1184, 1678))
    base.center(d, 'beginning sound and sentence', (620, 1324), base.BODY)
    base.choices(d, [word[0].upper(), chr(((ord(word[0].upper()) - 65 + 4) % 26) + 65), chr(((ord(word[0].upper()) - 65 + 9) % 26) + 65)], (86, 1372, 520, 1504))
    base.trace_text(d, f'This is a {word}.', (548, 1360, 1154, 1612), 2)
    base.center(d, 'circle the beginning sound, then trace the sentence', (620, 1650), base.SMALL)
    return img


def tracing_page(index):
    img, d = base.page(A4P)
    base.header(d, A4P, '동물 선긋기 학습지', 'animal lines · loops · picture finish')
    base.box(d, (56, 180, 1184, 530))
    base.center(d, 'curve warm-up', (620, 216), base.BODY)
    for row, pattern in enumerate([
        [(120, 290), (260, 250), (400, 330), (540, 250), (680, 330), (820, 250), (1120, 290)],
        [(120, 380), (240, 450), (360, 330), (480, 450), (600, 330), (720, 450), (840, 330), (1120, 380)],
        [(120, 470), (240, 390), (360, 470), (480, 390), (600, 470), (720, 390), (840, 470), (1120, 430)],
    ]):
        base.dot_path(d, pattern, step=16, radius=4)
    base.box(d, (56, 560, 1184, 1060))
    base.center(d, 'loops and turns', (620, 596), base.BODY)
    for path in [
        [(170, 740), (240, 680), (310, 740), (380, 680), (450, 740), (520, 680), (590, 740)],
        [(700, 700), (760, 780), (820, 700), (880, 780), (940, 700), (1000, 780), (1060, 700)],
        [(180, 930), (300, 860), (420, 930), (540, 860), (660, 930), (780, 860), (900, 930), (1080, 880)],
    ]:
        base.dot_path(d, path, step=16, radius=4)
    base.box(d, (56, 1090, 1184, 1678))
    base.center(d, 'finish the picture', (620, 1126), base.BODY)
    DRAWERS['flower'](d, 250, 1360, 1.2)
    base.dot_path(d, [(250, 1374), (250, 1600)], step=18, radius=4)
    DRAWERS['balloon'](d, 620, 1360, 0.9)
    base.dot_path(d, [(620, 1408), (590, 1490), (640, 1560), (600, 1640)], step=18, radius=4)
    DRAWERS['star'](d, 980, 1360, 0.95)
    base.dot_path(d, [(980, 1448), (980, 1640)], step=18, radius=4)
    return img


def maze_page(index):
    img = base.maze_page(index + 20)
    d = ImageDraw.Draw(img)
    d.rectangle((40, 36, A4P[0]-40, 166), fill='white')
    base.header(d, A4P, '공룡 하드 미로', 'dinosaur routes · more dead ends')
    return img


def cut_paste_page(index):
    img = base.cut_paste_page((index + 3) % 10)
    d = ImageDraw.Draw(img)
    d.rectangle((40, 36, A4P[0]-40, 166), fill='white')
    base.header(d, A4P, '오려붙이기 코스튬 인형', 'dress-up · costume · build')
    return img


def hidden_page(index):
    img = base.hidden_page(index + 14)
    d = ImageDraw.Draw(img)
    d.rectangle((40, 36, A4L[0]-40, 166), fill='white')
    base.header(d, A4L, '시장 숨은 캐릭터 찾기', 'dense classroom search')
    return img


def save_set(folder_name, generator):
    folder = ASSET_ROOT / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    for i in range(10):
        generator(i).save(folder / f'{i+1:02d}.png')


def write_post(path, title, description, folder_name, labels, size):
    width, height = size
    lines = ['---', f'title: {title}', 'date: 2026-04-02 12:00:00 +0900', 'categories: [프린터블]', 'tags: [학습지, 유아]', f'description: "{description}"', 'image:', f'  path: /assets/img/playroom/{folder_name}/01.png', '---', '', '<section class="post-gallery">']
    for i, label in enumerate(labels, start=1):
        lines.append(f'  <figure class="post-image"><img src="/assets/img/playroom/{folder_name}/{i:02d}.png" alt="{label}" decoding="async" width="{width}" height="{height}" loading="lazy" fetchpriority="low" /><figcaption>{label}</figcaption></figure>')
    lines.append('</section>')
    path.write_text('\n'.join(lines), encoding='utf-8')


def main():
    sets = [
        ('count-ocean-a4', counting_page, POST_ROOT / '2026-06-27-count-fish.md', '바다 숫자 학습지', '세기, trace, ten-frame, draw-more를 묶은 바다 숫자 학습지 세트.', [f'바다 숫자 {i}' for i in range(1, 11)], A4P),
        ('english-home-a4', english_page, POST_ROOT / '2026-06-08-english-fruit.md', '기초 영어 홈 단어 학습지', '큰 그림, tracing, matching, sentence를 묶은 생활 영어 학습지 세트.', [f'생활 영어 {i}' for i in range(1, 11)], A4P),
        ('tracing-animals-a4', tracing_page, POST_ROOT / '2026-06-18-animal-tracing.md', '동물 선긋기 학습지', '동물 모양과 finish-the-picture를 묶은 선긋기 세트.', [f'동물 선긋기 {i}' for i in range(1, 11)], A4P),
        ('maze-dino-a4', maze_page, POST_ROOT / '2026-05-15-maze-dinosaur.md', '공룡 하드 미로', '공룡 테마 branch형 공룡 미로 세트.', [f'공룡 미로 {i}' for i in range(1, 11)], A4P),
        ('cut-paste-costume-a4', cut_paste_page, POST_ROOT / '2026-05-30-cut-paste-fruit.md', '오려붙이기 코스튬 인형', 'dress-up과 character assembly를 묶은 오려붙이기 세트.', [f'코스튬 인형 {i}' for i in range(1, 11)], A4P),
        ('hidden-wally-market-a4', hidden_page, POST_ROOT / '2026-04-23-hidden-kitchen.md', '시장 숨은 캐릭터 찾기', 'target strip과 dense scene으로 만든 시장 탐색 세트.', [f'시장 탐색 {i}' for i in range(1, 11)], A4L),
    ]
    for folder_name, generator, post, title, description, labels, size in sets:
        save_set(folder_name, generator)
        write_post(post, title, description, folder_name, labels, size)


if __name__ == '__main__':
    main()
