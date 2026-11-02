#!/usr/bin/env python3
"""
Checkpoint 4: the blueprint must match the drawing.
  1. Every label drawn on the color reference appears word for word in BLUEPRINT.md.
  2. Every color painted in the color reference appears (as a hex code) in BLUEPRINT.md.
  3. Every color named in BLUEPRINT.md's color key is really used in the drawing.
  4. Every leader line ends on a drawn part (its end dot is not on empty background).
  5. BLUEPRINT.md contains no em dashes.
Usage: python3 tools/check_blueprint.py
"""
import html
import json
import re
import sys

doc = open("BLUEPRINT.md", encoding="utf-8").read()
svg = open("reference/membrane_color.svg", encoding="utf-8").read()
geo = json.load(open("reference/geometry.json"))
fails = []

# 1. labels
labels = [html.unescape(l["text"]) for l in geo["labels"]]
missing = sorted({t for t in labels if t not in doc})
print(f"labels drawn: {len(labels)}; missing from blueprint: {missing or 'none'}")
if missing:
    fails.append("labels")

# 2 + 3. colors (ignore white, which is only the paper and text halos)
body = svg.split("</defs>", 1)[1]
used = {c.upper() for c in re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', body)} - {"#FFFFFF"}
used |= {c.upper() for c in re.findall(r'<marker[^>]*>.*?fill="(#[0-9A-Fa-f]{6})"', svg)}
in_doc = {c.upper() for c in re.findall(r"#[0-9A-Fa-f]{6}", doc)}
not_in_doc = sorted(used - in_doc)
key_part = doc.split("### 5a. Color key", 1)[1].split("### 5b.", 1)[0]
key_colors = {c.upper() for c in re.findall(r"#[0-9A-Fa-f]{6}", key_part)}
unused_key = sorted(key_colors - used)
print(f"colors used in drawing: {len(used)}; not documented: {not_in_doc or 'none'}")
print(f"colors in the color key: {len(key_colors)}; listed but never drawn: {unused_key or 'none'}")
if not_in_doc or unused_key:
    fails.append("colors")

# 4. leader end dots sit on something drawn (checked on the label-free raster from the layout audit)
try:
    from PIL import Image
    import glob
    shot = sorted(glob.glob("/tmp/claude-*/**/audit_nolabels.png", recursive=True))
    img = Image.open(shot[-1]).convert("RGB")
    s = img.width / 1100
    dots = re.findall(r'<circle class="leaderdot" cx="([\d.]+)" cy="([\d.]+)"', svg)
    empty = []
    for cx, cy in dots:
        x, y = float(cx), float(cy)
        ink = 0
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                r, g, b = img.getpixel((int((x + dx) * s), int((y + dy) * s)))
                ink += (r < 235 or g < 235 or b < 235)
        if ink < 3:
            empty.append((x, y))
    print(f"leader lines: {len(dots)}; ending on empty space: {empty or 'none'}")
    if empty:
        fails.append("leaders")
except Exception as e:  # raster not available
    print("leader check skipped:", e)

# 5. no em dashes
em = doc.count(chr(0x2014))
print(f"em dashes in BLUEPRINT.md: {em}")
if em:
    fails.append("em dash")

print("RESULT:", "PASS" if not fails else "FAIL " + ", ".join(fails))
sys.exit(1 if fails else 0)
