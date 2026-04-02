from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / 'assets' / 'img' / 'playroom' / 'comfy-src' / 'english-basic'
OUT_DIR = REPO_ROOT / 'assets' / 'img' / 'playroom' / 'english-comfy-basic'
POST_PATH = REPO_ROOT / '_posts' / '2026-06-07-english-animal.md'
PAGE_W, PAGE_H = 1240, 1754
INK = (18, 18, 18)
GRAY = (186, 186, 186)
LIGHT = (230, 230, 230)
WORDS = [
    ('apple', 'A', 'a'),
    ('balloon', 'B', 'b'),
    ('cat', 'C', 'c'),
    ('dog', 'D', 'd'),
    ('fish', 'F', 'f'),
    ('flower', 'F', 'f'),
    ('grapes', 'G', 'g'),
    ('ice cream', 'I', 'i'),
    ('jam', 'J', 'j'),
    ('duck', 'D', 'd'),
]


def font(size: int):
    for candidate in ['C:/Windows/Fonts/malgun.ttf', 'C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/arial.ttf']:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_TITLE = font(56)
FONT_SUB = font(28)
FONT_BODY = font(28)
FONT_SMALL = font(22)
FONT_TRACE = font(40)
FONT_LETTER = font(84)


def center_text(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], used_font, fill=INK):
    bbox = draw.textbbox((0, 0), text, font=used_font)
    x = xy[0] - (bbox[2] - bbox[0]) / 2
    y = xy[1] - (bbox[3] - bbox[1]) / 2
    draw.text((x, y), text, font=used_font, fill=fill)


def rounded(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], width: int = 4, radius: int = 22, outline=INK):
    draw.rounded_rectangle(rect, radius=radius, outline=outline, width=width)


def load_source(word_key: str) -> Image.Image:
    file_key = word_key.replace(' ', '')
    image = Image.open(SRC_DIR / f'{file_key}.png').convert('RGBA')
    alpha = Image.new('L', image.size, 255)
    image.putalpha(alpha)
    return image


def fit_image(image: Image.Image, max_w: int, max_h: int) -> Image.Image:
    scale = min(max_w / image.width, max_h / image.height)
    new_size = (max(1, int(image.width * scale)), max(1, int(image.height * scale)))
    return image.resize(new_size, Image.Resampling.LANCZOS)


def paste_center(base: Image.Image, image: Image.Image, box: tuple[int, int, int, int]):
    fitted = fit_image(image, box[2] - box[0], box[3] - box[1])
    x = box[0] + (box[2] - box[0] - fitted.width) // 2
    y = box[1] + (box[3] - box[1] - fitted.height) // 2
    base.alpha_composite(fitted, (x, y))


def trace_text(draw: ImageDraw.ImageDraw, text: str, rect_box: tuple[int, int, int, int], repeat: int = 3):
    rounded(draw, rect_box, width=3, radius=16)
    x1, y1, x2, y2 = rect_box
    gap = (y2 - y1) // (repeat + 1)
    for index in range(repeat):
        y = y1 + gap * (index + 1) - 12
        draw.line((x1 + 20, y + 44, x2 - 20, y + 44), fill=LIGHT, width=2)
        draw.text((x1 + 24, y), text, font=FONT_TRACE, fill=GRAY)


def letter_boxes(draw: ImageDraw.ImageDraw, upper: str, lower: str, rect_box: tuple[int, int, int, int]):
    rounded(draw, rect_box, width=3, radius=16)
    x1, y1, x2, y2 = rect_box
    mid = (x1 + x2) // 2
    draw.line((mid, y1 + 10, mid, y2 - 10), fill=INK, width=3)
    center_text(draw, upper, ((x1 + mid) // 2, (y1 + y2) // 2), FONT_LETTER)
    center_text(draw, lower, ((mid + x2) // 2, (y1 + y2) // 2), FONT_LETTER)


def choice_row(draw: ImageDraw.ImageDraw, labels: list[str], rect_box: tuple[int, int, int, int]):
    rounded(draw, rect_box, width=3, radius=16)
    x1, y1, x2, y2 = rect_box
    slot_w = (x2 - x1 - 20) // len(labels)
    for idx, label in enumerate(labels):
        sx1 = x1 + 10 + idx * slot_w
        sx2 = sx1 + slot_w - 10
        rounded(draw, (sx1, y1 + 12, sx2, y2 - 12), width=2, radius=14)
        center_text(draw, label, ((sx1 + sx2) // 2, (y1 + y2) // 2), FONT_BODY)


def build_page(index: int):
    word, upper, lower = WORDS[index]
    page = Image.new('RGBA', (PAGE_W, PAGE_H), 'white')
    draw = ImageDraw.Draw(page)
    rounded(draw, (24, 24, PAGE_W - 24, PAGE_H - 24), width=4, radius=24)
    rounded(draw, (48, 44, PAGE_W - 48, 156), width=4, radius=24)
    center_text(draw, f'{word.upper()} worksheet', (PAGE_W // 2, 78), FONT_TITLE)
    center_text(draw, 'picture · trace · match · sentence', (PAGE_W // 2, 120), FONT_SUB, fill=(80, 80, 80))
    rounded(draw, (56, 180, 620, 840), width=3, radius=24)
    center_text(draw, 'big picture', (338, 216), FONT_BODY)
    paste_center(page, load_source(word), (100, 250, 576, 796))
    trace_text(draw, word, (654, 180, 1184, 418), repeat=3)
    letter_boxes(draw, upper, lower, (654, 438, 1184, 598))
    distractors = [WORDS[(index + 1) % 10][0], WORDS[(index + 2) % 10][0]]
    choice_row(draw, [word, *distractors], (654, 618, 1184, 778))
    rounded(draw, (56, 870, 1184, 1248), width=3, radius=24)
    center_text(draw, 'picture to word match', (620, 906), FONT_BODY)
    option_words = [word, WORDS[(index + 3) % 10][0], WORDS[(index + 5) % 10][0], WORDS[(index + 7) % 10][0]]
    for idx, opt in enumerate(option_words):
        cx = 150 + idx * 260
        rounded(draw, (cx - 92, 950, cx + 92, 1160), width=2, radius=18)
        paste_center(page, load_source(opt), (cx - 70, 980, cx + 70, 1100))
        center_text(draw, opt, (cx, 1202), FONT_SMALL)
    rounded(draw, (56, 1288, 1184, 1678), width=3, radius=24)
    center_text(draw, 'beginning sound and sentence', (620, 1324), FONT_BODY)
    letters = [upper, chr(((ord(upper) - 65 + 4) % 26) + 65), chr(((ord(upper) - 65 + 8) % 26) + 65)]
    choice_row(draw, letters, (86, 1372, 520, 1504))
    trace_text(draw, f'This is a {word}.', (548, 1360, 1154, 1612), repeat=2)
    center_text(draw, 'circle the beginning sound, then trace the sentence', (620, 1650), FONT_SMALL)
    return page.convert('RGB')


def write_post():
    lines = ['---', 'title: 기초 영어 단어 학습지', 'date: 2026-04-02 15:00:00 +0900', 'categories: [프린터블, 영어]', 'tags: [영어, 단어, tracing]', 'description: "ComfyUI 그림과 학습지 레이아웃을 결합한 영어 단어 학습지 세트."', 'image:', '  path: /assets/img/playroom/english-comfy-basic/01.png', '---', '', '<section class="post-gallery">']
    for index, (word, _, _) in enumerate(WORDS, start=1):
        lines.append(f'  <figure class="post-image"><img src="/assets/img/playroom/english-comfy-basic/{index:02d}.png" alt="{word}" decoding="async" width="{PAGE_W}" height="{PAGE_H}" loading="lazy" fetchpriority="low" /><figcaption>{word}</figcaption></figure>')
    lines.append('</section>')
    POST_PATH.write_text('\n'.join(lines), encoding='utf-8')


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for index in range(10):
        build_page(index).save(OUT_DIR / f'{index + 1:02d}.png')
    write_post()


if __name__ == '__main__':
    main()
