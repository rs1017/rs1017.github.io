from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 768
BG = 'white'
INK = '#121212'
LINE = 6
THIN = 4
REPO_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = REPO_ROOT / 'assets' / 'img' / 'playroom'
POST_ROOT = REPO_ROOT / '_posts'


def font(size: int):
    candidates = [
        'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/segoeui.ttf',
        'C:/Windows/Fonts/malgun.ttf',
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


BIG_FONT = font(88)
MID_FONT = font(40)


def canvas():
    image = Image.new('RGB', (WIDTH, HEIGHT), BG)
    return image, ImageDraw.Draw(image)


def line(draw, points, width=LINE):
    draw.line(points, fill=INK, width=width, joint='curve')


def circle(draw, x, y, r, width=LINE):
    draw.ellipse((x - r, y - r, x + r, y + r), outline=INK, width=width)


def ellipse(draw, x, y, rx, ry, width=LINE):
    draw.ellipse((x - rx, y - ry, x + rx, y + ry), outline=INK, width=width)


def rect(draw, x1, y1, x2, y2, width=LINE, radius=0):
    draw.rounded_rectangle((x1, y1, x2, y2), radius=radius, outline=INK, width=width)


def poly(draw, points, width=LINE):
    draw.polygon(points, outline=INK, fill=BG)
    if width > 1:
        line(draw, points + [points[0]], width=width)


def arc(draw, box, start, end, width=LINE):
    draw.arc(box, start, end, fill=INK, width=width)


def dot_path(draw, points, step=22, radius=5):
    for start, end in zip(points, points[1:]):
        x1, y1 = start
        x2, y2 = end
        dist = max(1, int(math.hypot(x2 - x1, y2 - y1)))
        count = max(1, dist // step)
        for i in range(count + 1):
            t = i / count
            cx = x1 + (x2 - x1) * t
            cy = y1 + (y2 - y1) * t
            circle(draw, cx, cy, radius, width=2)


def dashed_rect(draw, box, dash=18):
    x1, y1, x2, y2 = box
    edges = [
        ((x1, y1), (x2, y1)),
        ((x2, y1), (x2, y2)),
        ((x2, y2), (x1, y2)),
        ((x1, y2), (x1, y1)),
    ]
    for (sx, sy), (ex, ey) in edges:
        dist = int(math.hypot(ex - sx, ey - sy))
        for i in range(0, dist, dash * 2):
            t1 = i / dist
            t2 = min(dist, i + dash) / dist
            ax = sx + (ex - sx) * t1
            ay = sy + (ey - sy) * t1
            bx = sx + (ex - sx) * t2
            by = sy + (ey - sy) * t2
            line(draw, [(ax, ay), (bx, by)], width=THIN)


def flower(draw, x, y, s=1.0):
    for angle in range(0, 360, 72):
        px = x + math.cos(math.radians(angle)) * 24 * s
        py = y + math.sin(math.radians(angle)) * 24 * s
        circle(draw, px, py, 18 * s)
    circle(draw, x, y, 14 * s)
    line(draw, [(x, y + 22 * s), (x, y + 120 * s)])
    line(draw, [(x, y + 66 * s), (x - 28 * s, y + 40 * s)], width=THIN)
    line(draw, [(x, y + 88 * s), (x + 28 * s, y + 62 * s)], width=THIN)


def tulip(draw, x, y, s=1.0):
    line(draw, [(x, y + 28 * s), (x, y + 124 * s)])
    line(draw, [(x, y + 78 * s), (x - 22 * s, y + 52 * s)], width=THIN)
    line(draw, [(x, y + 92 * s), (x + 22 * s, y + 66 * s)], width=THIN)
    petal = [(x - 34 * s, y + 30 * s), (x - 18 * s, y - 18 * s), (x, y + 4 * s), (x + 18 * s, y - 18 * s), (x + 34 * s, y + 30 * s)]
    poly(draw, petal)


def butterfly(draw, x, y, s=1.0):
    ellipse(draw, x - 26 * s, y - 10 * s, 30 * s, 40 * s)
    ellipse(draw, x - 26 * s, y + 30 * s, 24 * s, 30 * s)
    ellipse(draw, x + 26 * s, y - 10 * s, 30 * s, 40 * s)
    ellipse(draw, x + 26 * s, y + 30 * s, 24 * s, 30 * s)
    line(draw, [(x, y - 34 * s), (x, y + 64 * s)])
    line(draw, [(x, y - 34 * s), (x - 28 * s, y - 74 * s)], width=THIN)
    line(draw, [(x, y - 34 * s), (x + 28 * s, y - 74 * s)], width=THIN)


def rabbit(draw, x, y, s=1.0):
    ellipse(draw, x - 10 * s, y + 70 * s, 110 * s, 84 * s)
    circle(draw, x + 100 * s, y + 6 * s, 56 * s)
    ellipse(draw, x + 72 * s, y - 92 * s, 20 * s, 70 * s)
    ellipse(draw, x + 122 * s, y - 98 * s, 20 * s, 78 * s)
    circle(draw, x + 82 * s, y - 2 * s, 4 * s, width=2)
    circle(draw, x + 118 * s, y - 2 * s, 4 * s, width=2)
    circle(draw, x + 100 * s, y + 18 * s, 6 * s)
    arc(draw, (x + 84 * s, y + 18 * s, x + 116 * s, y + 44 * s), 10, 170, width=THIN)
    line(draw, [(x + 130 * s, y + 66 * s), (x + 188 * s, y + 96 * s)])
    line(draw, [(x - 58 * s, y + 144 * s), (x - 36 * s, y + 180 * s)])
    line(draw, [(x + 8 * s, y + 144 * s), (x + 30 * s, y + 180 * s)])
    circle(draw, x - 84 * s, y + 20 * s, 18 * s)


def tree(draw, x, y, s=1.0):
    rect(draw, x - 18 * s, y + 8 * s, x + 18 * s, y + 124 * s, radius=6)
    circle(draw, x - 38 * s, y - 4 * s, 48 * s)
    circle(draw, x + 18 * s, y - 44 * s, 58 * s)
    circle(draw, x + 74 * s, y - 4 * s, 48 * s)
    circle(draw, x + 18 * s, y + 16 * s, 66 * s)


def fish(draw, x, y, s=1.0):
    ellipse(draw, x, y, 88 * s, 52 * s)
    poly(draw, [(x + 86 * s, y), (x + 148 * s, y - 46 * s), (x + 148 * s, y + 46 * s)])
    circle(draw, x - 40 * s, y - 10 * s, 4 * s, width=2)
    arc(draw, (x - 56 * s, y + 4 * s, x - 24 * s, y + 28 * s), 15, 165, width=THIN)
    poly(draw, [(x - 8 * s, y - 44 * s), (x + 20 * s, y - 82 * s), (x + 46 * s, y - 40 * s)])


def shell(draw, x, y, s=1.0):
    poly(draw, [(x - 86 * s, y + 92 * s), (x, y - 86 * s), (x + 86 * s, y + 92 * s)])
    line(draw, [(x - 56 * s, y + 90 * s), (x - 24 * s, y - 4 * s)], width=THIN)
    line(draw, [(x - 18 * s, y + 90 * s), (x - 6 * s, y - 24 * s)], width=THIN)
    line(draw, [(x + 18 * s, y + 90 * s), (x + 6 * s, y - 24 * s)], width=THIN)
    line(draw, [(x + 56 * s, y + 90 * s), (x + 24 * s, y - 4 * s)], width=THIN)


def star(draw, x, y, s=1.0):
    points = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        radius = (82 if i % 2 == 0 else 34) * s
        points.append((x + math.cos(angle) * radius, y + math.sin(angle) * radius))
    poly(draw, points)


def whale(draw, x, y, s=1.0):
    body = [
        (x - 148 * s, y + 18 * s), (x - 120 * s, y - 84 * s), (x + 32 * s, y - 88 * s),
        (x + 132 * s, y - 24 * s), (x + 202 * s, y + 12 * s), (x + 166 * s, y + 78 * s),
        (x + 88 * s, y + 38 * s), (x + 24 * s, y + 118 * s), (x - 112 * s, y + 102 * s)
    ]
    poly(draw, body)
    poly(draw, [(x - 146 * s, y + 10 * s), (x - 206 * s, y - 34 * s), (x - 188 * s, y + 12 * s), (x - 206 * s, y + 58 * s)])
    circle(draw, x + 78 * s, y - 4 * s, 4 * s, width=2)
    arc(draw, (x + 18 * s, y, x + 64 * s, y + 34 * s), 10, 170, width=THIN)
    line(draw, [(x + 36 * s, y - 18 * s), (x + 46 * s, y - 82 * s)])


def octopus(draw, x, y, s=1.0):
    ellipse(draw, x, y, 84 * s, 72 * s)
    circle(draw, x - 24 * s, y - 14 * s, 4 * s, width=2)
    circle(draw, x + 24 * s, y - 14 * s, 4 * s, width=2)
    arc(draw, (x - 16 * s, y + 12 * s, x + 16 * s, y + 34 * s), 10, 170, width=THIN)
    for offset in [-58, -28, 0, 28, 58]:
        line(draw, [(x + offset * s, y + 42 * s), (x + (offset - 18) * s, y + 106 * s), (x + offset * s, y + 158 * s), (x + (offset - 14) * s, y + 220 * s)])


def submarine(draw, x, y, s=1.0):
    rect(draw, x - 132 * s, y - 28 * s, x + 132 * s, y + 84 * s, radius=int(56 * s))
    rect(draw, x - 28 * s, y - 78 * s, x + 64 * s, y - 26 * s, radius=int(18 * s))
    circle(draw, x - 54 * s, y + 28 * s, 24 * s)
    circle(draw, x, y + 28 * s, 24 * s)
    circle(draw, x + 54 * s, y + 28 * s, 24 * s)
    line(draw, [(x + 80 * s, y - 82 * s), (x + 80 * s, y - 116 * s)])
    line(draw, [(x + 64 * s, y - 82 * s), (x + 96 * s, y - 82 * s)])


def apple(draw, x, y, s=1.0):
    poly(draw, [(x, y - 22 * s), (x - 68 * s, y - 88 * s), (x - 92 * s, y + 4 * s), (x - 60 * s, y + 90 * s), (x, y + 118 * s), (x + 60 * s, y + 90 * s), (x + 92 * s, y + 4 * s), (x + 68 * s, y - 88 * s)])
    line(draw, [(x, y - 34 * s), (x - 8 * s, y - 104 * s)])
    line(draw, [(x + 4 * s, y - 92 * s), (x + 46 * s, y - 112 * s)], width=THIN)


def balloon(draw, x, y, s=1.0):
    ellipse(draw, x, y - 10 * s, 68 * s, 92 * s)
    poly(draw, [(x - 10 * s, y + 76 * s), (x + 10 * s, y + 76 * s), (x, y + 96 * s)])
    line(draw, [(x, y + 96 * s), (x - 6 * s, y + 156 * s), (x + 22 * s, y + 214 * s)])


def cat(draw, x, y, s=1.0):
    ellipse(draw, x, y + 70 * s, 92 * s, 78 * s)
    circle(draw, x, y - 10 * s, 56 * s)
    poly(draw, [(x - 34 * s, y - 42 * s), (x - 60 * s, y - 88 * s), (x - 8 * s, y - 62 * s)])
    poly(draw, [(x + 34 * s, y - 42 * s), (x + 60 * s, y - 88 * s), (x + 8 * s, y - 62 * s)])
    circle(draw, x - 18 * s, y - 10 * s, 4 * s, width=2)
    circle(draw, x + 18 * s, y - 10 * s, 4 * s, width=2)
    circle(draw, x, y + 10 * s, 6 * s)
    arc(draw, (x - 18 * s, y + 12 * s, x + 18 * s, y + 34 * s), 10, 170, width=THIN)
    line(draw, [(x + 86 * s, y + 46 * s), (x + 154 * s, y + 38 * s), (x + 134 * s, y + 100 * s)])


def duck(draw, x, y, s=1.0):
    ellipse(draw, x, y + 40 * s, 92 * s, 68 * s)
    circle(draw, x + 88 * s, y - 8 * s, 34 * s)
    poly(draw, [(x + 110 * s, y - 6 * s), (x + 150 * s, y + 10 * s), (x + 104 * s, y + 26 * s)])
    circle(draw, x + 98 * s, y - 12 * s, 4 * s, width=2)
    line(draw, [(x - 10 * s, y + 104 * s), (x - 10 * s, y + 148 * s)])
    line(draw, [(x + 30 * s, y + 104 * s), (x + 30 * s, y + 148 * s)])
    line(draw, [(x - 28 * s, y + 152 * s), (x + 8 * s, y + 152 * s)], width=THIN)
    line(draw, [(x + 12 * s, y + 152 * s), (x + 48 * s, y + 152 * s)], width=THIN)


def egg(draw, x, y, s=1.0):
    ellipse(draw, x, y, 72 * s, 96 * s)


def grapes(draw, x, y, s=1.0):
    for ox, oy in [(-24, 0), (12, 0), (-42, 36), (-6, 36), (30, 36), (-24, 72), (12, 72), (-6, 108)]:
        circle(draw, x + ox * s, y + oy * s, 24 * s)
    line(draw, [(x, y - 46 * s), (x + 48 * s, y - 92 * s)])
    line(draw, [(x + 14 * s, y - 78 * s), (x - 44 * s, y - 86 * s)], width=THIN)


def hat(draw, x, y, s=1.0):
    rect(draw, x - 56 * s, y - 10 * s, x + 56 * s, y + 84 * s, radius=int(10 * s))
    line(draw, [(x - 110 * s, y + 94 * s), (x + 110 * s, y + 94 * s)])
    line(draw, [(x - 24 * s, y + 22 * s), (x + 24 * s, y + 22 * s)], width=THIN)


def icecream(draw, x, y, s=1.0):
    circle(draw, x, y - 46 * s, 42 * s)
    circle(draw, x - 34 * s, y - 8 * s, 34 * s)
    circle(draw, x + 34 * s, y - 8 * s, 34 * s)
    poly(draw, [(x - 34 * s, y + 18 * s), (x, y + 146 * s), (x + 34 * s, y + 18 * s)])
    line(draw, [(x - 16 * s, y + 52 * s), (x + 16 * s, y + 112 * s)], width=THIN)
    line(draw, [(x + 16 * s, y + 52 * s), (x - 16 * s, y + 112 * s)], width=THIN)


def jam(draw, x, y, s=1.0):
    rect(draw, x - 66 * s, y - 24 * s, x + 66 * s, y + 96 * s, radius=int(18 * s))
    rect(draw, x - 78 * s, y - 54 * s, x + 78 * s, y - 22 * s, radius=int(12 * s))
    arc(draw, (x - 40 * s, y + 6 * s, x + 40 * s, y + 54 * s), 180, 360, width=THIN)
    arc(draw, (x - 40 * s, y + 34 * s, x + 40 * s, y + 82 * s), 0, 180, width=THIN)


DRAWERS = {
    'flower': flower,
    'tulip': tulip,
    'butterfly': butterfly,
    'rabbit': rabbit,
    'tree': tree,
    'fish': fish,
    'shell': shell,
    'star': star,
    'whale': whale,
    'octopus': octopus,
    'submarine': submarine,
    'apple': apple,
    'balloon': balloon,
    'cat': cat,
    'duck': duck,
    'egg': egg,
    'grapes': grapes,
    'hat': hat,
    'icecream': icecream,
    'jam': jam,
}


def draw_sun(draw, x, y, s=1.0):
    for angle in range(0, 360, 45):
        x1 = x + math.cos(math.radians(angle)) * 48 * s
        y1 = y + math.sin(math.radians(angle)) * 48 * s
        x2 = x + math.cos(math.radians(angle)) * 76 * s
        y2 = y + math.sin(math.radians(angle)) * 76 * s
        line(draw, [(x1, y1), (x2, y2)])
    circle(draw, x, y, 38 * s)


def draw_cloud(draw, x, y, s=1.0):
    ellipse(draw, x, y, 48 * s, 28 * s)
    ellipse(draw, x + 40 * s, y - 10 * s, 38 * s, 24 * s)
    ellipse(draw, x + 80 * s, y, 44 * s, 28 * s)


def draw_ground(draw):
    points = [(64, 650), (256, 624), (448, 650), (640, 624), (960, 650)]
    line(draw, points)


def coloring_page(title, idx):
    image, draw = canvas()
    draw_ground(draw)
    draw_cloud(draw, 140, 120, 0.9)
    draw_cloud(draw, 760, 120, 0.8)
    draw_sun(draw, 900, 122, 0.7)
    if idx == 0:
        tulip(draw, 210, 520, 1.3)
        tulip(draw, 760, 532, 1.2)
        rabbit(draw, 450, 320, 1.0)
        flower(draw, 150, 560, 0.9)
        flower(draw, 850, 560, 0.9)
    elif idx == 1:
        rect(draw, 390, 292, 640, 516, radius=18)
        poly(draw, [(356, 308), (516, 190), (674, 308)])
        rect(draw, 478, 394, 546, 516, radius=12)
        tulip(draw, 250, 540, 1.4)
        tulip(draw, 788, 546, 1.4)
        butterfly(draw, 790, 250, 0.8)
    elif idx == 2:
        tree(draw, 420, 260, 1.4)
        butterfly(draw, 720, 238, 1.0)
        butterfly(draw, 820, 320, 0.8)
        butterfly(draw, 210, 278, 0.75)
        flower(draw, 178, 570, 0.8)
        flower(draw, 856, 576, 0.8)
    elif idx == 3:
        ellipse(draw, 520, 470, 150, 96)
        line(draw, [(420, 440), (520, 330), (620, 440)])
        flower(draw, 430, 292, 0.8)
        flower(draw, 510, 258, 0.8)
        flower(draw, 590, 292, 0.8)
        tulip(draw, 360, 320, 0.7)
        tulip(draw, 648, 320, 0.7)
    elif idx == 4:
        for x in [150, 280, 420, 570, 730, 860]:
            flower(draw, x, 560 + (x % 3) * 8, 0.8)
        butterfly(draw, 512, 284, 1.1)
    elif idx == 5:
        draw_cloud(draw, 300, 210, 1.15)
        draw_cloud(draw, 676, 226, 1.15)
        line(draw, [(492, 214), (492, 398)])
        line(draw, [(540, 214), (540, 398)])
        line(draw, [(438, 402), (592, 402)])
        rabbit(draw, 486, 430, 0.72)
    elif idx == 6:
        rect(draw, 390, 312, 630, 514, radius=16)
        poly(draw, [(356, 328), (510, 190), (662, 328)])
        line(draw, [(508, 170), (484, 118), (434, 90)])
        line(draw, [(510, 170), (540, 118), (602, 92)])
        flower(draw, 274, 570, 0.9)
        flower(draw, 754, 570, 0.9)
    elif idx == 7:
        line(draw, [(420, 620), (460, 520), (540, 430), (620, 336), (656, 220)])
        tree(draw, 690, 250, 1.05)
        butterfly(draw, 320, 300, 0.8)
        for px, py in [(360, 180), (410, 210), (468, 176), (536, 230), (600, 188)]:
            circle(draw, px, py, 9)
    elif idx == 8:
        ellipse(draw, 512, 510, 246, 96)
        ellipse(draw, 512, 510, 120, 38, width=THIN)
        ellipse(draw, 512, 400, 76, 58)
        circle(draw, 478, 356, 18)
        circle(draw, 546, 356, 18)
        circle(draw, 478, 356, 4, width=2)
        circle(draw, 546, 356, 4, width=2)
        arc(draw, (490, 396, 534, 424), 10, 170, width=THIN)
        flower(draw, 270, 540, 0.8)
        flower(draw, 758, 540, 0.8)
    else:
        tree(draw, 240, 280, 1.0)
        tree(draw, 748, 290, 0.95)
        rabbit(draw, 470, 438, 0.82)
        flower(draw, 320, 570, 0.72)
        flower(draw, 706, 570, 0.72)
    return image


def hidden_page(title, idx):
    image, draw = canvas()
    rect(draw, 82, 74, 942, 618, radius=30)
    draw_cloud(draw, 138, 120, 0.72)
    draw_cloud(draw, 794, 126, 0.68)
    for y in [430, 470, 510, 550]:
        line(draw, [(140, y), (320, y)], width=THIN)
    tree(draw, 700, 250, 1.0)
    flower(draw, 206, 560, 0.7)
    flower(draw, 850, 560, 0.7)
    if idx % 2 == 0:
        rect(draw, 362, 350, 468, 522, radius=12)
        poly(draw, [(348, 370), (416, 308), (482, 370)])
        ellipse(draw, 660, 520, 146, 50)
    else:
        rect(draw, 366, 340, 470, 502, radius=14)
        circle(draw, 418, 408, 20)
        line(draw, [(418, 430), (418, 502)])
        ellipse(draw, 680, 520, 150, 58)
    targets = [
        ['flower', 'apple', 'butterfly', 'shell'],
        ['butterfly', 'flower', 'fish', 'apple'],
        ['flower', 'shell', 'fish', 'apple'],
        ['butterfly', 'flower', 'apple', 'fish'],
        ['apple', 'flower', 'shell', 'fish'],
        ['apple', 'butterfly', 'flower', 'shell'],
        ['flower', 'fish', 'shell', 'apple'],
        ['apple', 'flower', 'fish', 'butterfly'],
        ['flower', 'butterfly', 'fish', 'shell'],
        ['apple', 'flower', 'shell', 'butterfly'],
    ][idx]
    hidden_positions = [(178, 380), (290, 240), (430, 360), (610, 520), (770, 220), (842, 560)]
    for pos, name in zip(hidden_positions, (targets + targets)[:6]):
        DRAWERS[name](draw, pos[0], pos[1], 0.22)
    rect(draw, 184, 632, 840, 742, radius=24)
    for box_idx, icon_name in enumerate(targets):
        box_x = 248 + box_idx * 148
        rect(draw, box_x - 54, 644, box_x + 54, 730, radius=18)
        DRAWERS[icon_name](draw, box_x, 688, 0.24)
    return image


def generate_maze(cols, rows, seed):
    random.seed(seed)
    grid = [[set() for _ in range(cols)] for _ in range(rows)]
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    stack = [(0, 0)]
    visited[0][0] = True
    dirs = [(1, 0, 'E', 'W'), (-1, 0, 'W', 'E'), (0, 1, 'S', 'N'), (0, -1, 'N', 'S')]
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy, here, there in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                neighbors.append((nx, ny, here, there))
        if not neighbors:
            stack.pop()
            continue
        nx, ny, here, there = random.choice(neighbors)
        grid[y][x].add(here)
        grid[ny][nx].add(there)
        visited[ny][nx] = True
        stack.append((nx, ny))
    return grid


def maze_page(title, idx):
    image, draw = canvas()
    rect(draw, 72, 102, 952, 698, radius=32)
    cell = 70
    left = 92
    top = 120
    cols, rows = 12, 8
    grid = generate_maze(cols, rows, 700 + idx)
    for y in range(rows):
        for x in range(cols):
            x1 = left + x * cell
            y1 = top + y * cell
            x2 = x1 + cell
            y2 = y1 + cell
            if 'N' not in grid[y][x]:
                line(draw, [(x1, y1), (x2, y1)])
            if 'W' not in grid[y][x]:
                line(draw, [(x1, y1), (x1, y2)])
            if y == rows - 1 and 'S' not in grid[y][x]:
                line(draw, [(x1, y2), (x2, y2)])
            if x == cols - 1 and 'E' not in grid[y][x]:
                line(draw, [(x2, y1), (x2, y2)])
    circle(draw, left + 22, top + 36, 18)
    circle(draw, left + cols * cell - 22, top + rows * cell - 36, 18)
    return image


def english_page(title, idx):
    image, draw = canvas()
    rect(draw, 88, 78, 936, 690, radius=36)
    letter, word, drawer_name = [
        ('A', 'APPLE', 'apple'),
        ('B', 'BALLOON', 'balloon'),
        ('C', 'CAT', 'cat'),
        ('D', 'DUCK', 'duck'),
        ('E', 'EGG', 'egg'),
        ('F', 'FISH', 'fish'),
        ('G', 'GRAPES', 'grapes'),
        ('H', 'HAT', 'hat'),
        ('I', 'ICE CREAM', 'icecream'),
        ('J', 'JAM', 'jam'),
    ][idx]
    draw.text((104, 74), f'{letter} {letter.lower()}', fill=INK, font=BIG_FONT)
    for row in range(3):
        y = 248 + row * 74
        dot_path(draw, [(132, y + 26), (892, y + 26)], step=20, radius=3)
        draw.text((146, y - 8), word, fill=INK, font=MID_FONT)
    DRAWERS[drawer_name](draw, 512, 556, 0.7)
    return image


def tracing_page(title, idx):
    image, draw = canvas()
    rect(draw, 92, 84, 932, 684, radius=34)
    paths = [
        [(150, 560), (280, 360), (420, 300), (512, 410), (618, 536), (748, 476), (874, 236)],
        [(150, 560), (220, 260), (420, 170), (620, 300), (760, 400), (874, 214)],
        [(144, 560), (300, 300), (512, 530), (702, 360), (884, 236)],
        [(144, 560), (230, 444), (250, 280), (404, 250), (642, 530), (880, 228)],
        [(160, 562), (262, 486), (338, 276), (498, 346), (720, 572), (870, 230)],
        [(160, 552), (314, 628), (392, 248), (548, 314), (746, 612), (870, 232)],
        [(146, 562), (296, 328), (426, 608), (562, 356), (742, 216), (878, 236)],
        [(154, 558), (248, 248), (418, 270), (534, 534), (744, 468), (882, 234)],
        [(158, 566), (236, 376), (324, 520), (452, 312), (702, 196), (872, 232)],
        [(142, 556), (314, 246), (438, 566), (584, 326), (760, 178), (876, 230)],
    ]
    dot_path(draw, paths[idx], step=16, radius=4)
    circle(draw, paths[idx][0][0], paths[idx][0][1], 20)
    circle(draw, paths[idx][-1][0], paths[idx][-1][1], 20)
    return image


def cut_paste_page(title, idx):
    image, draw = canvas()
    rect(draw, 74, 78, 950, 456, radius=30)
    line(draw, [(120, 424), (260, 374), (400, 420), (562, 380), (724, 422), (908, 424)])
    combos = [
        ['whale', 'fish', 'shell'],
        ['fish', 'shell', 'star'],
        ['octopus', 'fish', 'shell'],
        ['fish', 'shell', 'whale'],
        ['fish', 'star', 'shell'],
        ['submarine', 'fish', 'shell'],
        ['shell', 'star', 'fish'],
        ['star', 'fish', 'shell'],
        ['fish', 'shell', 'star'],
        ['whale', 'octopus', 'fish'],
    ][idx]
    slot_positions = [(250, 258), (512, 230), (772, 280)]
    piece_positions = [(216, 640), (512, 640), (808, 640)]
    for (x, y), icon_name in zip(slot_positions, combos):
        dashed_rect(draw, (x - 86, y - 86, x + 86, y + 86))
        DRAWERS[icon_name](draw, x, y + 10, 0.3)
    line(draw, [(92, 520), (932, 520)], width=THIN)
    for (x, y), icon_name in zip(piece_positions, combos):
        dashed_rect(draw, (x - 118, y - 86, x + 118, y + 86))
        DRAWERS[icon_name](draw, x, y, 0.34)
    return image


SETS = [
    {
        'filename': '2026-03-30-spring-coloring-pack.md',
        'date': '2026-04-01 09:00:00 +0900',
        'title': '봄 색칠놀이',
        'description': '봄 장면을 따라 색칠하는 흑백 유아용 색칠 활동지 세트.',
        'categories': ['프린터블', '색칠'],
        'tags': ['색칠', '봄', '유아'],
        'folder': 'coloring-spring',
        'items': ['꽃 토끼', '튤립 집', '나비 나무', '꽃 바구니', '봄 들판', '구름 그네', '새싹 집', '꽃비 길', '봄 연못', '숲 낮잠'],
        'renderer': coloring_page,
    },
    {
        'filename': '2026-03-30-garden-hidden-picture.md',
        'date': '2026-04-01 10:00:00 +0900',
        'title': '정원 숨은그림',
        'description': '정원 장면에서 물건을 찾는 흑백 유아용 숨은그림 활동지 세트.',
        'categories': ['프린터블', '숨은그림'],
        'tags': ['숨은그림', '찾기', '유아'],
        'folder': 'hidden-garden',
        'items': ['정원 문', '새집 길', '화분 코너', '나비 울타리', '씨앗 상자', '사과 나무', '연못 모서리', '벤치 자리', '꽃길 찾기', '나무 그늘'],
        'renderer': hidden_page,
    },
    {
        'filename': '2026-03-31-rainy-day-maze.md',
        'date': '2026-04-01 11:00:00 +0900',
        'title': '비 오는 날 미로',
        'description': '길을 따라 도착점을 찾는 흑백 유아용 미로 활동지 세트.',
        'categories': ['프린터블', '미로'],
        'tags': ['미로', '길찾기', '유아'],
        'folder': 'maze-rainy',
        'items': ['무지개 길', '토끼 길', '조개 길', '풍선 길', '과일 길', '별 길', '공룡 길', '연 길', '기차 길', '사탕 길'],
        'renderer': maze_page,
    },
    {
        'filename': '2026-03-30-ocean-cut-paste.md',
        'date': '2026-04-01 12:00:00 +0900',
        'title': '바다 오려붙이기',
        'description': '오리고 붙여서 장면을 완성하는 흑백 유아용 오려붙이기 활동지 세트.',
        'categories': ['프린터블', '오려붙이기'],
        'tags': ['오리기', '붙이기', '유아'],
        'folder': 'cut-paste-ocean',
        'items': ['고래 바다', '물고기 산호', '문어 동굴', '거북 산책', '별불가사리', '잠수함 바다', '조개 해변', '산호 바닥', '파도 조각', '바다 친구'],
        'renderer': cut_paste_page,
    },
    {
        'filename': '2026-04-01-animal-english-words.md',
        'date': '2026-04-01 13:00:00 +0900',
        'title': '영어 단어 놀이',
        'description': '알파벳과 단어를 따라 읽고 쓰는 유아용 영어 학습 활동지 세트.',
        'categories': ['프린터블', '영어'],
        'tags': ['영어', '알파벳', '유아'],
        'folder': 'english-words',
        'items': ['사과 영어', '풍선 영어', '고양이 영어', '오리 영어', '달걀 영어', '물고기 영어', '포도 영어', '모자 영어', '아이스크림 영어', '잼 영어'],
        'renderer': english_page,
    },
    {
        'filename': '2026-04-01-basic-line-tracing.md',
        'date': '2026-04-01 14:00:00 +0900',
        'title': '기초 선긋기',
        'description': '점선 길을 따라 손 움직임을 연습하는 유아용 선긋기 활동지 세트.',
        'categories': ['프린터블', '선긋기'],
        'tags': ['선긋기', '따라쓰기', '유아'],
        'folder': 'line-tracing',
        'items': ['꽃 길', '구름 길', '토끼 길', '별 길', '나비 길', '물고기 길', '오리 길', '사과 길', '모자 길', '고래 길'],
        'renderer': tracing_page,
    },
]


def post_markdown(meta):
    figures = []
    for index, title in enumerate(meta['items'], start=1):
        name = f'{index:02d}'
        figures.append(
            f'  <figure class="post-image"><img src="/assets/img/playroom/{meta["folder"]}/{name}.png" alt="{title}" decoding="async" width="{WIDTH}" height="{HEIGHT}" loading="lazy" fetchpriority="low" /><figcaption>{title}</figcaption></figure>'
        )
    categories = ', '.join(meta['categories'])
    tags = ', '.join(meta['tags'])
    return (
        f'---\n'
        f'title: {meta["title"]}\n'
        f'date: {meta["date"]}\n'
        f'categories: [{categories}]\n'
        f'tags: [{tags}]\n'
        f'description: "{meta["description"]}"\n'
        f'image:\n'
        f'  path: /assets/img/playroom/{meta["folder"]}/01.png\n'
        f'---\n\n'
        f'<section class="post-gallery">\n'
        + '\n'.join(figures)
        + '\n</section>\n'
    )


def main():
    for meta in SETS:
        folder = ASSET_ROOT / meta['folder']
        folder.mkdir(parents=True, exist_ok=True)
        for index, title in enumerate(meta['items'], start=1):
            image = meta['renderer'](title, index - 1)
            image.save(folder / f'{index:02d}.png')
        (POST_ROOT / meta['filename']).write_text(post_markdown(meta), encoding='utf-8')


if __name__ == '__main__':
    main()
