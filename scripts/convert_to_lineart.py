from PIL import Image, ImageOps
import sys
src = sys.argv[1]
out = sys.argv[2]
img = Image.open(src).convert('L')
img = ImageOps.autocontrast(img)
# keep light line detail while removing most color residue
img = img.point(lambda p: 255 if p > 188 else 0)
img = img.convert('RGB')
img.save(out)
print(out)
