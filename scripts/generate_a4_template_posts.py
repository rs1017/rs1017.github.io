from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.append(str(Path(__file__).resolve().parent))
from generate_printable_png_sets import DRAWERS, dot_path, line, circle, rect, poly

REPO_ROOT = Path(__file__).resolve().parents[1]
POST_ROOT = REPO_ROOT / '_posts'
ASSET_ROOT = REPO_ROOT / 'assets' / 'img' / 'playroom'
A4P = (1240, 1754)
A4L = (1754, 1240)
INK = '#121212'
GRAY = '#b0b0b0'
LIGHT = '#e2e2e2'

def font(size):
    for candidate in ['C:/Windows/Fonts/malgun.ttf', 'C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/arial.ttf']:
        p = Path(candidate)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()

TITLE = font(60)
SUB = font(32)
BODY = font(28)
SMALL = font(22)
TRACE = font(38)


def page(size):
    img = Image.new('RGB', size, 'white')
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((24, 24, size[0]-24, size[1]-24), radius=24, outline=INK, width=4)
    return img, d


def center(draw, text, xy, used_font, fill=INK):
    box = draw.textbbox((0, 0), text, font=used_font)
    draw.text((xy[0] - (box[2]-box[0])/2, xy[1] - (box[3]-box[1])/2), text, font=used_font, fill=fill)


def header(draw, size, title, subtitle):
    draw.rounded_rectangle((48, 44, size[0]-48, 156), radius=24, outline=INK, width=4)
    center(draw, title, (size[0]//2, 82), TITLE)
    center(draw, subtitle, (size[0]//2, 122), SUB, fill='#555555')


def box(draw, xy, width=3, radius=18, outline=INK):
    draw.rounded_rectangle(xy, radius=radius, outline=outline, width=width)


def trace_text(draw, text, xy, repeat=3):
    box(draw, xy)
    x1, y1, x2, y2 = xy
    gap = (y2-y1)//(repeat+1)
    for i in range(repeat):
        y = y1 + gap*(i+1) - 12
        draw.line((x1+18, y+42, x2-18, y+42), fill=LIGHT, width=2)
        draw.text((x1+24, y), text, font=TRACE, fill=GRAY)


def letter_boxes(draw, letters, xy):
    box(draw, xy)
    x1, y1, x2, y2 = xy
    mid = (x1+x2)//2
    draw.line((mid, y1+10, mid, y2-10), fill=INK, width=3)
    center(draw, letters[0], ((x1+mid)//2, (y1+y2)//2), font(84))
    center(draw, letters[1], ((mid+x2)//2, (y1+y2)//2), font(84))


def choices(draw, options, xy):
    box(draw, xy)
    x1, y1, x2, y2 = xy
    width = (x2-x1-20)//len(options)
    for i, option in enumerate(options):
        ox1 = x1 + 10 + i*width
        ox2 = ox1 + width - 10
        box(draw, (ox1, y1+12, ox2, y2-12), width=2, radius=14)
        center(draw, option, ((ox1+ox2)//2, (y1+y2)//2), BODY)


def ten_frame(draw, xy, count):
    box(draw, xy)
    x1, y1, x2, y2 = xy
    cw = (x2-x1-40)//5
    ch = (y2-y1-40)//2
    for row in range(2):
        for col in range(5):
            cx = x1 + 20 + col*cw + cw//2
            cy = y1 + 20 + row*ch + ch//2
            draw.ellipse((cx-18, cy-18, cx+18, cy+18), outline=INK, width=3)
    for i in range(count):
        row = i // 5
        col = i % 5
        cx = x1 + 20 + col*cw + cw//2
        cy = y1 + 20 + row*ch + ch//2
        draw.ellipse((cx-10, cy-10, cx+10, cy+10), fill=INK)


def doll_base(draw, cx, cy):
    circle(draw, cx, cy-250, 70, width=4)
    line(draw, [(cx, cy-180), (cx, cy+120)], width=5)
    line(draw, [(cx-120, cy-70), (cx+120, cy-70)], width=5)
    line(draw, [(cx, cy+120), (cx-80, cy+300)], width=5)
    line(draw, [(cx, cy+120), (cx+80, cy+300)], width=5)
    line(draw, [(cx-120, cy-70), (cx-150, cy+100)], width=5)
    line(draw, [(cx+120, cy-70), (cx+150, cy+100)], width=5)
    box(draw, (cx-80, cy-160, cx+80, cy-30), width=2, radius=14, outline=GRAY)
    box(draw, (cx-100, cy-10, cx+100, cy+120), width=2, radius=14, outline=GRAY)
    box(draw, (cx-70, cy+290, cx-10, cy+350), width=2, radius=12, outline=GRAY)
    box(draw, (cx+10, cy+290, cx+70, cy+350), width=2, radius=12, outline=GRAY)


def mini_char(draw, cx, cy, hat, prop, pose, scale=1.0):
    circle(draw, cx, cy-26*scale, 10*scale, width=2)
    line(draw, [(cx, cy-16*scale), (cx, cy+10*scale)], width=2)
    if pose == 'arms_up':
        line(draw, [(cx, cy-6*scale), (cx-16*scale, cy-18*scale)], width=2)
        line(draw, [(cx, cy-6*scale), (cx+16*scale, cy-18*scale)], width=2)
    elif pose == 'wave':
        line(draw, [(cx, cy-6*scale), (cx-14*scale, cy+2*scale)], width=2)
        line(draw, [(cx, cy-6*scale), (cx+16*scale, cy-14*scale)], width=2)
    else:
        line(draw, [(cx, cy-6*scale), (cx-14*scale, cy+2*scale)], width=2)
        line(draw, [(cx, cy-6*scale), (cx+14*scale, cy+2*scale)], width=2)
    line(draw, [(cx, cy+10*scale), (cx-10*scale, cy+28*scale)], width=2)
    line(draw, [(cx, cy+10*scale), (cx+10*scale, cy+28*scale)], width=2)
    if hat == 'bow':
        line(draw, [(cx-12*scale, cy-40*scale), (cx, cy-30*scale), (cx+12*scale, cy-40*scale)], width=2)
    elif hat == 'cap':
        line(draw, [(cx-12*scale, cy-38*scale), (cx+8*scale, cy-38*scale)], width=2)
    elif hat == 'wizard':
        line(draw, [(cx-10*scale, cy-34*scale), (cx, cy-52*scale), (cx+10*scale, cy-34*scale)], width=2)
    elif hat == 'bonnet':
        draw.arc((cx-16*scale, cy-46*scale, cx+16*scale, cy-20*scale), 180, 360, fill=INK, width=2)
    if prop == 'balloon':
        circle(draw, cx+18*scale, cy-4*scale, 8*scale, width=2)
        line(draw, [(cx+18*scale, cy+4*scale), (cx+10*scale, cy+18*scale)], width=2)
    elif prop == 'book':
        box(draw, (int(cx+8*scale), int(cy-2*scale), int(cx+24*scale), int(cy+10*scale)), width=2, radius=4)
    elif prop == 'umbrella':
        line(draw, [(cx+14*scale, cy-16*scale), (cx+14*scale, cy+16*scale)], width=2)
        line(draw, [(cx, cy-16*scale), (cx+28*scale, cy-16*scale)], width=2)
    elif prop == 'basket':
        box(draw, (int(cx+6*scale), int(cy+2*scale), int(cx+24*scale), int(cy+12*scale)), width=2, radius=4)
    elif prop == 'wand':
        line(draw, [(cx+12*scale, cy-8*scale), (cx+24*scale, cy-18*scale)], width=2)
        DRAWERS['star'](draw, cx+28*scale, cy-22*scale, 0.18*scale)
    elif prop == 'watering':
        box(draw, (int(cx+6*scale), int(cy+2*scale), int(cx+18*scale), int(cy+12*scale)), width=2, radius=2)
        line(draw, [(cx+18*scale, cy+4*scale), (cx+26*scale, cy)], width=2)
COUNT_OBJECTS = [('토끼', 'rabbit'), ('당근', 'tulip'), ('사과', 'apple'), ('별', 'star'), ('꽃', 'flower'), ('오리', 'duck'), ('물고기', 'fish'), ('조개', 'shell'), ('풍선', 'balloon'), ('포도', 'grapes')]
NUMBER_WORDS = ['하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉', '열']
ENGLISH_WORDS = ['apple', 'balloon', 'cat', 'duck', 'egg', 'fish', 'grapes', 'hat', 'icecream', 'jam']


def counting_page(index):
    img, d = page(A4P)
    count = index + 1
    obj_name, obj_key = COUNT_OBJECTS[index]
    header(d, A4P, f'{count} 숫자 학습지', '세기 · trace · matching')
    box(d, (56, 180, 760, 930))
    center(d, f'{obj_name}을 세어 보세요', (408, 214), BODY)
    cols = 3 if count <= 6 else 4
    placed = 0
    for row in range(3):
        for col in range(cols):
            if placed >= count:
                break
            x = 180 + col * 160
            y = 330 + row * 160
            DRAWERS[obj_key](d, x, y, 0.8)
            placed += 1
    trace_text(d, str(count), (800, 180, 1168, 418), 2)
    trace_text(d, NUMBER_WORDS[index], (800, 438, 1168, 676), 2)
    ten_frame(d, (800, 696, 1168, 934), count)
    choices(d, [str(max(1, count - 1)), str(count), str(min(10, count + 1))], (56, 976, 590, 1120))
    choices(d, [NUMBER_WORDS[index], NUMBER_WORDS[max(0, index - 1)], NUMBER_WORDS[min(9, index + 1)]], (616, 976, 1168, 1120))
    box(d, (56, 1148, 1168, 1676))
    center(d, 'count and color review', (612, 1184), BODY)
    review_key = COUNT_OBJECTS[(index + 3) % len(COUNT_OBJECTS)][1]
    for i in range(5):
        DRAWERS[review_key](d, 190 + i * 210, 1390, 0.68)
    for i, value in enumerate([count, max(1, count - 2), min(10, count + 2)]):
        cx = 360 + i * 220
        circle(d, cx, 1578, 36, width=3)
        center(d, str(value), (cx, 1578), BODY)
    center(d, '숫자와 단어를 함께 익혀 보세요', (612, 1652), SMALL)
    return img


def english_page(index):
    img, d = page(A4P)
    word = ENGLISH_WORDS[index]
    header(d, A4P, word.upper(), 'picture · trace · sound')
    box(d, (56, 180, 620, 880))
    center(d, 'hero picture', (338, 216), BODY)
    DRAWERS[word if word in DRAWERS else 'cat'](d, 338, 540, 1.2)
    trace_text(d, word, (654, 180, 1184, 418), 3)
    letter_boxes(d, (word[0].upper(), word[0].lower()), (654, 438, 1184, 598))
    choices(d, [word, ENGLISH_WORDS[(index + 1) % 10], ENGLISH_WORDS[(index + 2) % 10]], (654, 618, 1184, 778))
    box(d, (56, 910, 1184, 1298))
    center(d, 'match the picture', (620, 946), BODY)
    opts = [word, ENGLISH_WORDS[(index + 3) % 10], ENGLISH_WORDS[(index + 5) % 10]]
    for cx, opt in zip([210, 460, 710], opts):
        box(d, (cx - 100, 980, cx + 100, 1210), width=2, radius=18)
        DRAWERS[opt if opt in DRAWERS else 'cat'](d, cx, 1096, 0.45)
        center(d, opt, (cx, 1240), SMALL)
    box(d, (56, 1332, 1184, 1678))
    center(d, 'beginning sound and sentence', (620, 1368), BODY)
    letters = [word[0].upper(), chr(((ord(word[0].upper()) - 65 + 3) % 26) + 65), chr(((ord(word[0].upper()) - 65 + 7) % 26) + 65)]
    choices(d, letters, (86, 1414, 560, 1544))
    trace_text(d, f'I see a {word}.', (586, 1400, 1154, 1640), 2)
    center(d, 'circle the first sound and trace the sentence', (620, 1660), SMALL)
    return img


def house(draw, x, y, s=1.0):
    box(draw, (int(x - 90 * s), int(y - 6 * s), int(x + 90 * s), int(y + 130 * s)), width=4, radius=int(14 * s))
    line(draw, [(x - 112 * s, y + 8 * s), (x, y - 84 * s), (x + 112 * s, y + 8 * s)], width=5)


def tracing_page(index):
    img, d = page(A4P)
    titles = ['straight and curve', 'zigzag and wave', 'loops and hills', 'shapes and turns', 'road path tracing', 'rain to umbrella', 'trace the balloon strings', 'finish the flower', 'finish the fish pond', 'mixed review tracing']
    header(d, A4P, '선긋기 학습지', titles[index])
    box(d, (56, 180, 1184, 558))
    center(d, 'warm-up strips', (620, 216), BODY)
    y = 280
    for pattern in [
        [(120, y), (1120, y)],
        [(120, y + 70), (380, y + 70), (380, y + 120), (620, y + 120), (620, y + 70), (1120, y + 70)],
        [(120, y + 150), (260, y + 110), (400, y + 190), (540, y + 110), (680, y + 190), (820, y + 110), (960, y + 190), (1120, y + 150)],
        [(120, y + 240), (240, y + 200), (360, y + 240), (480, y + 280), (600, y + 240), (720, y + 200), (840, y + 240), (960, y + 280), (1120, y + 240)],
    ]:
        dot_path(d, pattern, step=18, radius=4)
    box(d, (56, 586, 1184, 1120))
    center(d, 'main tracing blocks', (620, 622), BODY)
    for shape in [
        [(200, 760), (300, 760), (300, 860), (200, 860), (200, 760)],
        [(450, 760), (540, 700), (630, 760), (630, 870), (450, 870), (450, 760)],
        [(820, 710), (900, 880), (740, 880), (820, 710)],
    ]:
        dot_path(d, shape, step=18, radius=4)
    dot_path(d, [(170, 980), (340, 980), (430, 1040), (600, 980), (760, 980)], step=18, radius=4)
    dot_path(d, [(760, 980), (840, 930), (930, 1030), (1030, 930), (1110, 980)], step=18, radius=4)
    box(d, (56, 1148, 1184, 1678))
    center(d, 'finish the picture', (620, 1184), BODY)
    if index % 3 == 0:
        DRAWERS['balloon'](d, 330, 1380, 0.9)
        dot_path(d, [(330, 1428), (300, 1500), (340, 1570), (300, 1640)], step=18, radius=4)
        house(d, 860, 1450, 1.0)
    elif index % 3 == 1:
        DRAWERS['flower'](d, 330, 1380, 1.0)
        dot_path(d, [(330, 1400), (330, 1640)], step=18, radius=4)
        d.ellipse((710, 1450, 1010, 1518), outline=INK, width=4)
        dot_path(d, [(760, 1500), (820, 1440), (900, 1520), (980, 1440), (1050, 1510)], step=18, radius=4)
    else:
        DRAWERS['rabbit'](d, 330, 1450, 0.9)
        dot_path(d, [(280, 1290), (300, 1220), (330, 1290), (360, 1220), (380, 1290)], step=18, radius=4)
        DRAWERS['star'](d, 900, 1400, 0.8)
        dot_path(d, [(900, 1490), (900, 1638)], step=18, radius=4)
    return img

def generate_maze(cols, rows, seed):
    random.seed(seed)
    visited = [[False] * cols for _ in range(rows)]
    walls = [[[True, True, True, True] for _ in range(cols)] for _ in range(rows)]
    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        x, y = stack[-1]
        neighbors = []
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                neighbors.append((nx, ny))
        if not neighbors:
            stack.pop()
            continue
        nx, ny = random.choice(neighbors)
        if nx == x - 1:
            walls[y][x][3] = False; walls[ny][nx][1] = False
        elif nx == x + 1:
            walls[y][x][1] = False; walls[ny][nx][3] = False
        elif ny == y - 1:
            walls[y][x][0] = False; walls[ny][nx][2] = False
        else:
            walls[y][x][2] = False; walls[ny][nx][0] = False
        visited[ny][nx] = True
        stack.append((nx, ny))
    return walls


def maze_page(index):
    img, d = page(A4P)
    header(d, A4P, '하드 미로 학습지', 'branch · dead end · checkpoint')
    maze_box = (74, 180, 1166, 1580)
    box(d, maze_box)
    cols, rows = 18, 24
    cell_w = (maze_box[2] - maze_box[0] - 40) / cols
    cell_h = (maze_box[3] - maze_box[1] - 40) / rows
    walls = generate_maze(cols, rows, 800 + index * 17)
    x0 = maze_box[0] + 20
    y0 = maze_box[1] + 20
    for y in range(rows):
        for x in range(cols):
            wx = x0 + x * cell_w
            wy = y0 + y * cell_h
            top, right, bottom, left = walls[y][x]
            if top: line(d, [(wx, wy), (wx + cell_w, wy)], width=5)
            if right: line(d, [(wx + cell_w, wy), (wx + cell_w, wy + cell_h)], width=5)
            if bottom: line(d, [(wx, wy + cell_h), (wx + cell_w, wy + cell_h)], width=5)
            if left: line(d, [(wx, wy), (wx, wy + cell_h)], width=5)
    line(d, [(x0, y0 + 2), (x0, y0 + cell_h - 2)], width=8)
    line(d, [(x0 + cols * cell_w, y0 + (rows - 1) * cell_h + 2), (x0 + cols * cell_w, y0 + rows * cell_h - 2)], width=8)
    d.text((88, 146), 'START', font=BODY, fill=INK)
    d.text((1030, 1588), 'GOAL', font=BODY, fill=INK)
    for offset in (6, 12, 18):
        DRAWERS['star'](d, x0 + offset * cell_w, y0 + (offset * cell_h * 0.9), 0.14)
    center(d, '길을 따라가며 별 3개도 지나가 보세요', (620, 1650), SMALL)
    return img


def cut_paste_page(index):
    img, d = page(A4P)
    themes = ['raincoat doll', 'chef puppet', 'astronaut doll', 'gardener doll', 'pirate puppet', 'princess doll', 'doctor doll', 'explorer doll', 'winter doll', 'animal costume doll']
    header(d, A4P, '오려 붙이기 인형', themes[index])
    box(d, (56, 180, 640, 1678))
    center(d, 'base body', (348, 214), BODY)
    doll_base(d, 350, 980)
    box(d, (680, 180, 1184, 1678))
    center(d, 'cut pieces', (932, 214), BODY)
    pieces = [(720, 260, 1144, 480), (720, 500, 1144, 740), (720, 760, 1144, 1010), (720, 1030, 1144, 1270), (720, 1290, 1144, 1540)]
    labels = ['hat', 'top', 'bottom', 'accessory', 'shoes']
    for piece_box, label in zip(pieces, labels):
        box(d, piece_box, width=2, radius=18)
        center(d, label, ((piece_box[0] + piece_box[2]) // 2, piece_box[1] + 24), SMALL)
    shape_index = index % 5
    if shape_index == 0:
        poly(d, [(932, 294), (874, 388), (990, 388)], width=4)
    elif shape_index == 1:
        poly(d, [(860, 356), (932, 292), (1004, 356), (980, 412), (884, 412)], width=4)
    elif shape_index == 2:
        circle(d, 932, 350, 60, width=4)
    elif shape_index == 3:
        poly(d, [(860, 392), (900, 292), (964, 292), (1004, 392)], width=4)
    else:
        poly(d, [(850, 392), (1014, 392), (980, 330), (884, 330)], width=4)
    d.rounded_rectangle((840, 548, 1024, 714), outline=INK, width=4, radius=18)
    if index % 2 == 0:
        poly(d, [(840, 960), (1024, 960), (980, 822), (884, 822)], width=4)
    else:
        d.ellipse((844, 832, 1020, 960), outline=INK, width=4)
    if index in {0, 3, 8}:
        line(d, [(870, 1148), (988, 1148)], width=4)
        line(d, [(932, 1148), (932, 1230)], width=4)
    elif index in {1, 6}:
        box(d, (862, 1100, 1002, 1224), width=4, radius=14)
    else:
        DRAWERS['star'](d, 932, 1168, 0.18)
    box(d, (840, 1370, 920, 1488), width=4, radius=16)
    box(d, (944, 1370, 1024, 1488), width=4, radius=16)
    center(d, 'cut, then glue onto the body', (932, 1626), SMALL)
    return img


def hidden_page(index):
    img, d = page(A4L)
    header(d, A4L, '월리형 숨은 캐릭터 찾기', 'dense scene search')
    scene_box = (56, 180, 1698, 980)
    target_box = (56, 1010, 1698, 1180)
    box(d, scene_box)
    box(d, target_box)
    hats = ['bow', 'cap', 'wizard', 'bonnet', 'none']
    props = ['balloon', 'book', 'umbrella', 'basket', 'wand', 'watering', 'none']
    poses = ['stand', 'wave', 'arms_up']
    random.seed(2000 + index)
    targets = [('wizard', 'wand', 'stand'), ('bow', 'balloon', 'wave'), ('bonnet', 'basket', 'stand'), ('cap', 'book', 'arms_up'), ('none', 'umbrella', 'stand'), ('bow', 'watering', 'wave')]
    positions = []
    for row in range(7):
        for col in range(11):
            positions.append((96 + col * 142 + random.randint(-16, 16), 248 + row * 96 + random.randint(-16, 16)))
    random.shuffle(positions)
    for combo, (x, y) in zip(targets, positions[:len(targets)]):
        mini_char(d, x, y, combo[0], combo[1], combo[2], 1.4)
    for x, y in positions[len(targets):]:
        mini_char(d, x, y, random.choice(hats), random.choice(props), random.choice(poses), 1.4)
    center(d, '아래 캐릭터 6명을 장면에서 찾아보세요', (878, 1046), BODY)
    for idx2, combo in enumerate(targets):
        x1 = 100 + idx2 * 270
        x2 = x1 + 220
        box(d, (x1, 1074, x2, 1152), width=2, radius=16)
        mini_char(d, x1 + 58, 1120, combo[0], combo[1], combo[2], 1.4)
    return img


def save_images(folder, generator, count):
    folder.mkdir(parents=True, exist_ok=True)
    for i in range(count):
        generator(i).save(folder / f'{i+1:02d}.png')


def write_post(path, title, description, folder_name, labels, size):
    width, height = size
    lines = ['---', f'title: {title}', 'date: 2026-04-02 09:00:00 +0900', 'categories: [프린터블]', 'tags: [학습지, 유아]', f'description: "{description}"', 'image:', f'  path: /assets/img/playroom/{folder_name}/01.png', '---', '', '<section class="post-gallery">']
    for i, label in enumerate(labels, start=1):
        lines.append(f'  <figure class="post-image"><img src="/assets/img/playroom/{folder_name}/{i:02d}.png" alt="{label}" decoding="async" width="{width}" height="{height}" loading="lazy" fetchpriority="low" /><figcaption>{label}</figcaption></figure>')
    lines.append('</section>')
    path.write_text('\n'.join(lines), encoding='utf-8')


def main():
    sets = [
        ('count-bunny-a4', counting_page, POST_ROOT / '2026-06-25-count-rabbit.md', '토끼 숫자 학습지', '세기, trace, ten-frame, matching이 함께 들어간 숫자 학습지 세트.', [f'숫자 학습 {i}' for i in range(1, 11)], A4P),
        ('english-farm-a4', english_page, POST_ROOT / '2026-04-01-animal-english-words.md', '영어 단어 학습지', '큰 그림, tracing, sound, matching을 묶은 영어 학습지 세트.', [f'영어 학습 {i}' for i in range(1, 11)], A4P),
        ('tracing-mixed-a4', tracing_page, POST_ROOT / '2026-04-01-basic-line-tracing.md', '선긋기 기초 학습지', 'warm-up, shape tracing, path tracing을 묶은 선긋기 학습지 세트.', [f'선긋기 {i}' for i in range(1, 11)], A4P),
        ('maze-adventure-a4', maze_page, POST_ROOT / '2026-03-31-rainy-day-maze.md', '하드 미로 학습지', 'branch와 dead-end가 많은 A4 하드 미로 세트.', [f'하드 미로 {i}' for i in range(1, 11)], A4P),
        ('cut-paste-paper-dolls-a4', cut_paste_page, POST_ROOT / '2026-03-30-ocean-cut-paste.md', '오려붙이기 인형 만들기', 'base body와 cut pieces를 함께 담은 인형 만들기 세트.', [f'인형 만들기 {i}' for i in range(1, 11)], A4P),
        ('hidden-wally-park-a4', hidden_page, POST_ROOT / '2026-04-21-hidden-picnic.md', '월리형 숨은 캐릭터 찾기', 'crowded scene과 target strip으로 만든 dense search 세트.', [f'숨은 캐릭터 {i}' for i in range(1, 11)], A4L),
    ]
    for folder_name, generator, post, title, description, labels, size in sets:
        save_images(ASSET_ROOT / folder_name, generator, 10)
        write_post(post, title, description, folder_name, labels, size)


if __name__ == '__main__':
    main()
