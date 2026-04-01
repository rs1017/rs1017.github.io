from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


def dhash(image: Image.Image, size: int = 8) -> int:
    gray = image.convert("L").resize((size + 1, size), Image.Resampling.LANCZOS)
    pixels = list(gray.getdata())
    width, height = gray.size
    bits = 0
    for y in range(height):
        for x in range(width - 1):
            left = pixels[y * width + x]
            right = pixels[y * width + x + 1]
            bits = (bits << 1) | (1 if left > right else 0)
    return bits


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_image_similarity.py <candidate> <folder>")
        return 1

    candidate_path = Path(sys.argv[1])
    folder = Path(sys.argv[2])
    if not candidate_path.exists() or not folder.exists():
        print("missing path")
        return 1

    candidate_hash = dhash(Image.open(candidate_path))
    best_name = ""
    best_distance = 999

    for existing in sorted(folder.glob("*.png")):
        if existing.resolve() == candidate_path.resolve():
            continue
        distance = hamming(candidate_hash, dhash(Image.open(existing)))
        if distance < best_distance:
            best_distance = distance
            best_name = existing.name

    print(f"closest={best_name or 'none'}")
    print(f"distance={best_distance if best_name else -1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
