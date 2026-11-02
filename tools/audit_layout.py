#!/usr/bin/env python3
"""
Layout audit (Checkpoint 2/3): reads audit_boxes.json + audit_nolabels.png from tools/audit_layout.js.

Reports
  1. labels (text, HIGH/LOW tags, step badges, key box) that sit on top of drawn structures
  2. labels that overlap other labels
  3. leader lines that cross a label other than their own
  4. anything outside the 0.4-inch safe margin (40 units from each page edge)
"""
import json
import sys

from PIL import Image

d = sys.argv[1] if len(sys.argv) > 1 else "."
boxes = json.load(open(f"{d}/audit_boxes.json"))
img = Image.open(f"{d}/audit_nolabels.png").convert("RGB")
px = img.load()
S = img.width / 1100.0
MARGIN = 40
problems = []


def text_box(b):
    """Tighten the font box to the visible glyphs (font boxes include empty ascent/descent)."""
    s = b["size"] or 10
    return (b["x"] + 0.5, b["y"] + 0.22 * s, b["x"] + b["w"] - 0.5, b["y"] + b["h"] - 0.2 * s)


def ink(x0, y0, x1, y1):
    n = 0
    for yy in range(int(y0 * S), int(y1 * S)):
        for xx in range(int(x0 * S), int(x1 * S)):
            if 0 <= xx < img.width and 0 <= yy < img.height:
                r, g, b = px[xx, yy]
                if r < 235 or g < 235 or b < 235:
                    n += 1
    return n


items = []
for b in boxes["labels"]:
    c = b["cls"]
    if c in ("lbl", "tagtxt", "keytxt", "badgetxt"):
        items.append((c, b["text"], text_box(b)))
    elif c in ("tag", "badge", "keybox", "keyitem"):
        items.append((c, b["text"] or c, (b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"])))

# 1. labels on top of drawing
for c, t, (x0, y0, x1, y1) in items:
    if c in ("tagtxt", "keytxt", "badgetxt"):
        continue  # inside their own box, which is tested instead
    n = ink(x0, y0, x1, y1)
    if n > 6:
        problems.append(f"ON-DRAWING  {c:7s} '{t}' covers {n} drawn pixels at ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")


def inter(a, b, gap=1.5):
    """True when two boxes overlap or come closer than `gap` units."""
    return min(a[2], b[2]) - max(a[0], b[0]) > -gap and min(a[3], b[3]) - max(a[1], b[1]) > -gap


def inside(a, b, pad=1.5):
    return a[0] >= b[0] - pad and a[1] >= b[1] - pad and a[2] <= b[2] + pad and a[3] <= b[3] + pad


# 2. label vs label
for i in range(len(items)):
    for j in range(i + 1, len(items)):
        (ci, ti, bi), (cj, tj, bj) = items[i], items[j]
        if not inter(bi, bj):
            continue
        if inside(bi, bj) or inside(bj, bi):
            continue  # text inside its own tag / badge / key box
        if "keybox" in (ci, cj) or ("keyitem" in (ci, cj) and "keytxt" in (ci, cj)):
            continue  # key contents are tested by TAG-FIT
        problems.append(f"LABEL-LABEL '{ti}' ({ci}) overlaps '{tj}' ({cj})")


# 2b. text must fit inside its own tag / key box
for c, t, bt in items:
    if c not in ("tagtxt", "keytxt"):
        continue
    owners = [bb for cc, tt, bb in items if cc in ("tag", "keybox", "keyitem") and
              bb[0] - 2 <= (bt[0] + bt[2]) / 2 <= bb[2] + 2 and bb[1] - 2 <= (bt[1] + bt[3]) / 2 <= bb[3] + 2]
    for bb in owners:
        if bt[0] < bb[0] + 0.5 or bt[2] > bb[2] - 0.5:
            problems.append(f"TAG-FIT     '{t}' is wider than its box ({bt[0]:.0f}-{bt[2]:.0f} vs {bb[0]:.0f}-{bb[2]:.0f})")

# 3. leader lines crossing other labels
def seg_hits_box(x1, y1, x2, y2, b):
    for k in range(0, 41):
        t = k / 40
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        if b[0] < x < b[2] and b[1] < y < b[3]:
            return True
    return False


for b in boxes["labels"]:
    if b["cls"] != "leader":
        continue
    for c, t, bb in items:
        if c in ("tagtxt", "keytxt", "badgetxt"):
            continue
        near_start = bb[0] - 8 <= b["x1"] <= bb[2] + 8 and bb[1] - 8 <= b["y1"] <= bb[3] + 8
        if near_start:
            continue
        if seg_hits_box(b["x1"], b["y1"], b["x2"], b["y2"], bb):
            problems.append(f"LEADER      line from ({b['x1']:.0f},{b['y1']:.0f}) crosses label '{t}'")

# 4. margins
for e in boxes["elements"]:
    if e["x0"] < MARGIN - 0.5 or e["y0"] < MARGIN - 0.5 or e["x1"] > 1100 - MARGIN + 0.5 or e["y1"] > 850 - MARGIN + 0.5:
        problems.append(f"MARGIN      {e['layer']}/{e['tag']} '{e['text']}' box ({e['x0']:.0f},{e['y0']:.0f})-({e['x1']:.0f},{e['y1']:.0f})")

# smallest text size used
sizes = sorted({b["size"] for b in boxes["labels"] if b["cls"] in ("lbl", "tagtxt", "keytxt", "badgetxt")})
print(f"text sizes used (units; 1 unit = 0.72 pt): {sizes}")
print(f"smallest = {sizes[0]} units = {sizes[0] * 0.72:.1f} pt when printed at actual size")
print(f"{len(problems)} problem(s)")
for p in problems:
    print("  " + p)
sys.exit(1 if problems else 0)
