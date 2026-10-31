# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
assets = root / 'assets'
assets.mkdir(exist_ok=True)
image = Image.new('RGBA', (256, 256))
d = ImageDraw.Draw(image)
d.rounded_rectangle((8, 8, 248, 248), radius=54, fill='#176BEE')
d.rounded_rectangle((61, 38, 192, 217), radius=15, fill='white')
d.polygon([(154, 38), (192, 76), (154, 76)], fill='#B5D4FF')
d.rounded_rectangle((82, 109, 174, 184), radius=7, fill='#DDEBFF')
d.ellipse((143, 119, 160, 136), fill='#176BEE')
d.polygon([(85, 174), (112, 137), (136, 165), (150, 148), (172, 174)], fill='#176BEE')
image.save(assets / 'app.png')
image.save(assets / 'app.ico', sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
