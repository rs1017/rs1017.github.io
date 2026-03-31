from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

WIDTH = 1024
HEIGHT = 768
INK = (18, 18, 18)
REPO_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = REPO_ROOT / 'assets' / 'img' / 'playroom'
SRC_ROOT = ASSET_ROOT / 'comfy-src'


def font(size: int):
    for name in ['C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/malgun.ttf']:
        path = Path(name)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


BIG_FONT = font(86)
MID_FONT = font(44)
SMALL_FONT = font(24)
ICON_CACHE: dict[str, Image.Image] = {}
SCENE_CACHE: dict[str, Image.Image] = {}


def blank_page():
    image = Image.new('RGB', (WIDTH, HEIGHT), 'white')
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((34, 34, WIDTH - 34, HEIGHT - 34), radius=28, outline=INK, width=4)
    return image, draw


def fit_box(image: Image.Image, max_w: int, max_h: int) -> Image.Image:
    scale = min(max_w / image.width, max_h / image.height)
    return image.resize((max(1, int(image.width * scale)), max(1, int(image.height * scale))), Image.Resampling.LANCZOS)


def paste_center(base: Image.Image, asset: Image.Image, cx: int, cy: int, max_w: int, max_h: int, opacity: int = 255, flip: bool = False):
    layer = asset.copy()
    if flip:
        layer = ImageOps.mirror(layer)
    layer = fit_box(layer, max_w, max_h)
    if opacity < 255:
        alpha = layer.getchannel('A').point(lambda p: p * opacity // 255)
        layer.putalpha(alpha)
    x = int(cx - layer.width / 2)
    y = int(cy - layer.height / 2)
    base.alpha_composite(layer, (x, y))


def load_icon(name: str) -> Image.Image:
    if name in ICON_CACHE:
        return ICON_CACHE[name]
    path = SRC_ROOT / 'icons' / f'{name}.png'
    gray = Image.open(path).convert('L')
    gray = ImageOps.autocontrast(gray)
    alpha = ImageOps.invert(gray)
    alpha = alpha.point(lambda p: 0 if p < 24 else min(255, int((p - 24) * 1.8)))
    rgba = Image.new('RGBA', gray.size, (*INK, 0))
    rgba.putalpha(alpha)
    bbox = rgba.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    ICON_CACHE[name] = rgba
    return rgba


def load_scene(group: str, idx: int) -> Image.Image:
    key = f'{group}:{idx}'
    if key in SCENE_CACHE:
        return SCENE_CACHE[key]
    path = SRC_ROOT / group / f'{idx:02d}.png'
    gray = Image.open(path).convert('L')
    gray = ImageOps.autocontrast(gray)
    gray = gray.point(lambda p: 255 if p > 244 else min(255, int(p * 1.06)))
    img = Image.merge('RGBA', (gray, gray, gray, Image.new('L', gray.size, 255)))
    SCENE_CACHE[key] = img
    return img


def line(draw, points, width=5):
    draw.line(points, fill=INK, width=width, joint='curve')


def circle(draw, x, y, r, width=4):
    draw.ellipse((x - r, y - r, x + r, y + r), outline=INK, width=width)


def rect(draw, box, width=4, radius=18):
    draw.rounded_rectangle(box, outline=INK, width=width, radius=radius)


def cloud(draw, x, y, s=1.0):
    draw.ellipse((x - 58 * s, y - 26 * s, x + 4 * s, y + 26 * s), outline=INK, width=4)
    draw.ellipse((x - 8 * s, y - 42 * s, x + 66 * s, y + 24 * s), outline=INK, width=4)
    draw.ellipse((x + 46 * s, y - 26 * s, x + 116 * s, y + 26 * s), outline=INK, width=4)


def sun(draw, x, y, r=34):
    circle(draw, x, y, r, width=4)
    for angle in range(0, 360, 45):
        x1 = x + math.cos(math.radians(angle)) * (r + 6)
        y1 = y + math.sin(math.radians(angle)) * (r + 6)
        x2 = x + math.cos(math.radians(angle)) * (r + 26)
        y2 = y + math.sin(math.radians(angle)) * (r + 26)
        line(draw, [(x1, y1), (x2, y2)], width=4)


def flower_simple(draw, x, y, s=1.0):
    for angle in range(0, 360, 72):
        px = x + math.cos(math.radians(angle)) * 18 * s
        py = y + math.sin(math.radians(angle)) * 18 * s
        circle(draw, px, py, 15 * s, width=4)
    circle(draw, x, y, 10 * s, width=4)
    line(draw, [(x, y + 16 * s), (x, y + 86 * s)], width=4)


def house(draw, x, y, s=1.0):
    rect(draw, (x - 90 * s, y - 6 * s, x + 90 * s, y + 130 * s), radius=int(14 * s))
    line(draw, [(x - 112 * s, y + 8 * s), (x, y - 84 * s), (x + 112 * s, y + 8 * s)], width=5)
    rect(draw, (x - 28 * s, y + 54 * s, x + 28 * s, y + 130 * s), radius=int(8 * s))
    rect(draw, (x - 72 * s, y + 38 * s, x - 24 * s, y + 82 * s), radius=int(8 * s))
    rect(draw, (x + 24 * s, y + 38 * s, x + 72 * s, y + 82 * s), radius=int(8 * s))


def tree(draw, x, y, s=1.0):
    rect(draw, (x - 12 * s, y + 38 * s, x + 12 * s, y + 138 * s), radius=int(5 * s))
    circle(draw, x - 42 * s, y + 20 * s, 40 * s, width=4)
    circle(draw, x + 20 * s, y - 8 * s, 48 * s, width=4)
    circle(draw, x + 64 * s, y + 24 * s, 38 * s, width=4)


def pond(draw, x, y, s=1.0):
    draw.ellipse((x - 150 * s, y - 40 * s, x + 150 * s, y + 40 * s), outline=INK, width=4)
    draw.arc((x - 96 * s, y - 18 * s, x - 20 * s, y + 18 * s), 10, 170, fill=INK, width=3)
    draw.arc((x + 10 * s, y - 18 * s, x + 86 * s, y + 18 * s), 10, 170, fill=INK, width=3)


def basket(draw, x, y, s=1.0):
    line(draw, [(x - 70 * s, y + 40 * s), (x - 48 * s, y - 18 * s), (x + 48 * s, y - 18 * s), (x + 70 * s, y + 40 * s)], width=4)
    line(draw, [(x - 40 * s, y - 18 * s), (x, y - 62 * s), (x + 40 * s, y - 18 * s)], width=4)
    for off in [-40, -12, 16, 44]:
        line(draw, [(x + off * s, y - 6 * s), (x + off * s, y + 28 * s)], width=3)
    for off in [-34, 0, 34]:
        line(draw, [(x - 56 * s, y + off * 0.7 * s), (x + 56 * s, y + off * 0.7 * s)], width=3)


def kite(draw, x, y, s=1.0):
    line(draw, [(x, y - 52 * s), (x + 42 * s, y), (x, y + 52 * s), (x - 42 * s, y), (x, y - 52 * s)], width=4)
    line(draw, [(x, y + 52 * s), (x + 34 * s, y + 102 * s), (x - 6 * s, y + 136 * s), (x + 26 * s, y + 168 * s)], width=3)


def train(draw, x, y, s=1.0):
    rect(draw, (x - 90 * s, y - 10 * s, x + 40 * s, y + 56 * s), radius=int(10 * s))
    rect(draw, (x + 10 * s, y - 46 * s, x + 56 * s, y + 10 * s), radius=int(8 * s))
    circle(draw, x - 52 * s, y + 64 * s, 18 * s, width=4)
    circle(draw, x + 8 * s, y + 64 * s, 18 * s, width=4)
    line(draw, [(x + 48 * s, y - 52 * s), (x + 48 * s, y - 82 * s)], width=4)


def candy(draw, x, y, s=1.0):
    rect(draw, (x - 42 * s, y - 28 * s, x + 42 * s, y + 28 * s), radius=int(16 * s))
    line(draw, [(x - 42 * s, y - 28 * s), (x - 86 * s, y - 8 * s), (x - 42 * s, y + 28 * s)], width=4)
    line(draw, [(x + 42 * s, y - 28 * s), (x + 86 * s, y - 8 * s), (x + 42 * s, y + 28 * s)], width=4)


def paste_scene(base: Image.Image, group: str, idx: int, box: tuple[int, int, int, int]):
    scene = load_scene(group, idx)
    scene = fit_box(scene, box[2] - box[0], box[3] - box[1])
    x = box[0] + (box[2] - box[0] - scene.width) // 2
    y = box[1] + (box[3] - box[1] - scene.height) // 2
    base.alpha_composite(scene, (x, y))


def coloring_page(idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    if idx in {1, 2, 4, 6, 7, 8, 9}:
        paste_scene(base, 'coloring-spring', idx + 1, (68, 68, 956, 700))
    else:
        cloud(draw, 150, 118, 0.95)
        cloud(draw, 790, 126, 0.85)
        sun(draw, 900, 112, 30)
        line(draw, [(70, 646), (250, 620), (450, 650), (660, 620), (950, 650)], width=4)
        if idx == 0:
            paste_center(base, load_icon('rabbit'), 520, 420, 420, 420)
            paste_center(base, load_icon('tulip'), 180, 520, 160, 230)
            paste_center(base, load_icon('tulip'), 850, 520, 160, 230, flip=True)
            flower_simple(draw, 286, 604, 1.0)
            flower_simple(draw, 740, 604, 1.0)
        elif idx == 3:
            basket(draw, 512, 478, 1.25)
            paste_center(base, load_icon('tulip'), 332, 400, 150, 190)
            paste_center(base, load_icon('tulip'), 692, 400, 150, 190, flip=True)
            paste_center(base, load_icon('butterfly'), 512, 220, 180, 140)
            flower_simple(draw, 250, 592, 0.8)
            flower_simple(draw, 770, 592, 0.8)
        elif idx == 5:
            line(draw, [(422, 164), (422, 322)], width=4)
            line(draw, [(600, 164), (600, 322)], width=4)
            line(draw, [(390, 164), (632, 164)], width=4)
            line(draw, [(390, 322), (632, 322)], width=4)
            paste_center(base, load_icon('rabbit'), 512, 456, 360, 360)
            paste_center(base, load_icon('cloud'), 352, 170, 220, 110)
            paste_center(base, load_icon('cloud'), 668, 178, 220, 110, flip=True)
        else:
            tree(draw, 238, 326, 1.1)
            tree(draw, 748, 336, 1.0)
            paste_center(base, load_icon('rabbit'), 512, 482, 340, 340)
            paste_center(base, load_icon('butterfly'), 310, 236, 150, 120)
            paste_center(base, load_icon('butterfly'), 734, 226, 150, 120, flip=True)
    return base.convert('RGB')


def hidden_page(idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    paste_scene(base, 'hidden-garden', idx + 1, (64, 64, 960, 588))
    hidden_sets = [
        ['flower', 'apple', 'butterfly', 'bee'],
        ['butterfly', 'flower', 'fish', 'apple'],
        ['flower', 'shell', 'fish', 'apple'],
        ['butterfly', 'flower', 'apple', 'fish'],
        ['apple', 'flower', 'shell', 'fish'],
        ['apple', 'butterfly', 'flower', 'shell'],
        ['flower', 'fish', 'shell', 'apple'],
        ['apple', 'flower', 'fish', 'butterfly'],
        ['flower', 'butterfly', 'fish', 'shell'],
        ['apple', 'flower', 'shell', 'butterfly'],
    ]
    positions = [
        [(170, 230), (354, 184), (680, 188), (848, 226)],
        [(220, 252), (402, 382), (722, 240), (854, 474)],
        [(190, 200), (352, 464), (652, 246), (808, 420)],
        [(218, 226), (380, 500), (690, 276), (834, 378)],
        [(172, 236), (350, 354), (640, 228), (856, 450)],
        [(182, 194), (372, 430), (652, 212), (838, 512)],
        [(228, 214), (404, 514), (702, 250), (844, 420)],
        [(168, 250), (396, 462), (680, 240), (860, 390)],
        [(210, 212), (386, 430), (670, 260), (852, 502)],
        [(172, 236), (412, 490), (700, 214), (850, 404)],
    ]
    icons = hidden_sets[idx]
    for (x, y), name in zip(positions[idx], icons):
        paste_center(base, load_icon(name), x, y, 82, 82)
    rect(draw, (162, 620, 862, 736), width=4, radius=26)
    for box_idx, name in enumerate(icons):
        cx = 246 + box_idx * 154
        rect(draw, (cx - 54, 642, cx + 54, 714), width=4, radius=18)
        paste_center(base, load_icon(name), cx, 678, 74, 74)
    return base.convert('RGB')


def generate_maze(cols: int, rows: int, seed: int):
    random.seed(seed)
    grid = [[set() for _ in range(cols)] for _ in range(rows)]
    seen = [[False] * cols for _ in range(rows)]
    stack = [(0, 0)]
    seen[0][0] = True
    dirs = [(1, 0, 'E', 'W'), (-1, 0, 'W', 'E'), (0, 1, 'S', 'N'), (0, -1, 'N', 'S')]
    while stack:
        x, y = stack[-1]
        opts = []
        for dx, dy, a, b in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not seen[ny][nx]:
                opts.append((nx, ny, a, b))
        if not opts:
            stack.pop()
            continue
        nx, ny, a, b = random.choice(opts)
        grid[y][x].add(a)
        grid[ny][nx].add(b)
        seen[ny][nx] = True
        stack.append((nx, ny))
    return grid


def maze_page(idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    left, top, cell, cols, rows = 92, 120, 68, 12, 8
    rect(draw, (72, 98, 952, 700), width=4, radius=28)
    grid = generate_maze(cols, rows, 1200 + idx)
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
    start_assets = ['cloud', 'rabbit', 'shell', 'balloon', 'apple', 'starfish', None, None, None, None]
    end_assets = ['sun', 'tulip', 'starfish', 'flower', 'basket', 'sun', None, None, None, None]
    if start_assets[idx]:
        paste_center(base, load_icon(start_assets[idx]), 120, 86, 108, 90)
    if end_assets[idx] == 'flower':
        flower_simple(draw, 918, 676, 0.8)
    elif end_assets[idx] == 'basket':
        basket(draw, 900, 676, 0.6)
    elif end_assets[idx]:
        paste_center(base, load_icon(end_assets[idx]), 916, 676, 90, 90)
    else:
        if idx == 6:
            # dino
            ellipse = draw.ellipse
            ellipse((864, 640, 928, 686), outline=INK, width=4)
            ellipse((914, 624, 956, 654), outline=INK, width=4)
            line(draw, [(848, 664), (820, 676), (834, 694)], width=4)
            line(draw, [(886, 684), (878, 716)], width=4)
            line(draw, [(912, 684), (924, 716)], width=4)
        elif idx == 7:
            kite(draw, 916, 676, 0.7)
        elif idx == 8:
            train(draw, 900, 668, 0.55)
        else:
            candy(draw, 916, 676, 0.6)
    return base.convert('RGB')


def english_page(idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    letter, word, icon = [
        ('A', 'APPLE', 'apple'), ('B', 'BALLOON', 'balloon'), ('C', 'CAT', 'cat'), ('D', 'DUCK', 'duck'),
        ('E', 'EGG', 'egg'), ('F', 'FISH', 'fish'), ('G', 'GRAPES', 'grapes'), ('H', 'HAT', 'hat'),
        ('I', 'ICE CREAM', 'icecream'), ('J', 'JAM', 'jam')
    ][idx]
    draw.text((86, 78), f'{letter} {letter.lower()}', fill=INK, font=BIG_FONT)
    paste_center(base, load_icon(icon), 824, 176, 180, 160)
    for row in range(3):
        y = 238 + row * 126
        line(draw, [(92, y + 70), (934, y + 70)], width=2)
        line(draw, [(92, y + 28), (934, y + 28)], width=1)
        draw.text((112, y - 12), word, fill=INK, font=MID_FONT)
        for x in range(300, 924, 20):
            circle(draw, x, y + 28, 2, width=1)
    paste_center(base, load_icon(icon), 512, 602, 280, 220)
    return base.convert('RGB')


def tracing_page(idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    pairs = [
        ('tulip', 'tulip'), ('cloud', 'sun'), ('rabbit', 'tulip'), ('starfish', 'balloon'), ('butterfly', 'flower'),
        ('fish', 'shell'), ('duck', None), ('apple', None), ('hat', 'jam'), ('whale', 'starfish')
    ]
    start_name, end_name = pairs[idx]
    paths = [
        [(144, 584), (268, 438), (396, 310), (512, 368), (652, 512), (880, 238)],
        [(144, 584), (248, 360), (412, 196), (612, 260), (740, 486), (884, 210)],
        [(144, 582), (286, 338), (480, 536), (664, 368), (884, 224)],
        [(144, 584), (290, 472), (312, 274), (526, 272), (720, 540), (884, 226)],
        [(146, 586), (266, 502), (364, 296), (530, 360), (736, 574), (884, 232)],
        [(144, 584), (302, 630), (408, 266), (560, 338), (744, 604), (886, 230)],
        [(146, 586), (310, 360), (460, 582), (606, 326), (770, 202), (886, 228)],
        [(146, 582), (272, 264), (454, 294), (570, 530), (762, 462), (888, 224)],
        [(148, 588), (250, 402), (332, 540), (476, 312), (726, 192), (886, 230)],
        [(148, 580), (332, 274), (446, 560), (596, 330), (754, 182), (886, 230)],
    ]
    for start, end in zip(paths[idx], paths[idx][1:]):
        sx, sy = start
        ex, ey = end
        dist = max(1, int(math.hypot(ex - sx, ey - sy)))
        count = max(1, dist // 18)
        for i in range(count + 1):
            t = i / count
            circle(draw, sx + (ex - sx) * t, sy + (ey - sy) * t, 3, width=2)
    circle(draw, paths[idx][0][0], paths[idx][0][1], 18, width=4)
    circle(draw, paths[idx][-1][0], paths[idx][-1][1], 18, width=4)
    if start_name == 'cloud':
        cloud(draw, 138, 582, 0.8)
    else:
        paste_center(base, load_icon(start_name), 138, 582, 160, 140)
    if end_name == 'sun':
        sun(draw, 886, 214, 28)
    elif end_name == 'flower':
        flower_simple(draw, 886, 214, 0.8)
    elif end_name is None:
        if idx == 6:
            pond(draw, 886, 214, 0.5)
        else:
            basket(draw, 886, 214, 0.5)
    else:
        paste_center(base, load_icon(end_name), 886, 214, 150, 130)
    return base.convert('RGB')


def cut_paste_page(idx: int):
    base, draw = blank_page()
    base = base.convert('RGBA')
    combos = [
        ['whale', 'fish', 'shell'], ['fish', 'shell', 'starfish'], ['octopus', 'fish', 'shell'], ['whale', 'shell', 'fish'],
        ['starfish', 'fish', 'shell'], ['submarine', 'fish', 'shell'], ['shell', 'starfish', 'fish'], ['fish', 'shell', 'whale'],
        ['balloon', 'fish', 'starfish'], ['whale', 'octopus', 'fish']
    ][idx]
    draw.arc((84, 390, 944, 470), 0, 180, fill=INK, width=4)
    slot_centers = [(220, 260), (512, 228), (804, 268)]
    piece_centers = [(220, 640), (512, 640), (804, 640)]
    for (cx, cy), name in zip(slot_centers, combos):
        rect(draw, (cx - 104, cy - 92, cx + 104, cy + 92), width=3, radius=22)
        if name == 'balloon':
            paste_center(base, load_icon('balloon'), cx, cy, 150, 150, opacity=80)
        else:
            paste_center(base, load_icon(name), cx, cy, 160, 150, opacity=80)
    line(draw, [(86, 518), (938, 518)], width=2)
    for (cx, cy), name in zip(piece_centers, combos):
        box = (cx - 118, cy - 86, cx + 118, cy + 86)
        # dashed box
        x1, y1, x2, y2 = box
        for seg in range(x1, x2, 22):
            line(draw, [(seg, y1), (min(seg + 12, x2), y1)], width=2)
            line(draw, [(seg, y2), (min(seg + 12, x2), y2)], width=2)
        for seg in range(y1, y2, 22):
            line(draw, [(x1, seg), (x1, min(seg + 12, y2))], width=2)
            line(draw, [(x2, seg), (x2, min(seg + 12, y2))], width=2)
        paste_center(base, load_icon(name if name != 'balloon' else 'balloon'), cx, cy, 170, 160)
    return base.convert('RGB')


def save_all():
    targets = [
        ('coloring-spring', coloring_page),
        ('hidden-garden', hidden_page),
        ('maze-rainy', maze_page),
        ('cut-paste-ocean', cut_paste_page),
        ('english-words', english_page),
        ('line-tracing', tracing_page),
    ]
    for folder, renderer in targets:
        out_dir = ASSET_ROOT / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        for idx in range(10):
            img = renderer(idx)
            img.save(out_dir / f'{idx + 1:02d}.png')
            print(f'CREATED {out_dir / (f"{idx + 1:02d}.png")}')


if __name__ == '__main__':
    save_all()
