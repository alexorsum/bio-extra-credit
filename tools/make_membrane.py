#!/usr/bin/env python3
"""
Plasma membrane reference diagram generator (AP Biology membrane bonus).

Page: landscape US Letter, viewBox 0 0 1100 850, so 100 units = 1 inch.
Outputs (in the folder given as argv[1], default "reference"):
  membrane_color.svg       full-color finished reference
  membrane_color_grid.svg  same, with a light 1-inch grid and 0.4" margin box
  membrane_guide.svg       very light gray outline-only tracing guide
  geometry.json            coordinates used by the self-checks (tools/check_geometry.py)
"""
import json
import math
import os
import random
import sys

W, H = 1100, 850
OUT = sys.argv[1] if len(sys.argv) > 1 else "reference"

# --------------------------------------------------------------------------
# Palette: single source of truth for the color key in the blueprint.
# --------------------------------------------------------------------------
PAL = {
    "ink": "#263238",        # outlines, text, membrane lines
    "outside": "#E3F2FD",    # extracellular fluid tint (optional)
    "cyto": "#FFF6E5",       # cytoplasm tint (optional)
    "band": "#FFE08A",       # simplified bilayer (between the double lines)
    "tails": "#FFF3C4",      # hydrophobic core tint behind the tails
    "head": "#F48FB1",       # phospholipid heads
    "tail": "#6D6D6D",       # phospholipid tails
    "chol": "#FFC107",       # cholesterol
    "carb": "#43A047",       # sugar chains (glycoprotein, glycolipid)
    "glycoprot": "#FFCC80",  # glycoprotein
    "periph": "#FFAB91",     # peripheral protein
    "enzyme": "#CE93D8",     # membrane enzyme
    "integrin": "#90CAF9",   # integrin
    "collagen": "#8D6E63",   # ECM collagen fibers
    "actin": "#E53935",      # actin microfilament beads
    "channel": "#80DEEA",    # K+ channel
    "nakpump": "#B39DDB",    # Na+/K+ pump
    "hpump": "#9FA8DA",      # proton (H+) pump
    "cotrans": "#A5D6A7",    # Na+/glucose cotransporter
    "na": "#1E63D6",         # Na+ ion
    "k": "#8E24AA",          # K+ ion
    "h": "#00897B",          # H+ ion (proton)
    "o2": "#E53935",         # O2
    "glucose": "#FB8C00",    # glucose hexagon
    "substrate": "#FFCA28",  # enzyme substrate (triangle)
    "product1": "#FB8C00",   # enzyme product (circle)
    "product2": "#66BB6A",   # enzyme product (square)
    "fibronectin": "#1E88E5",  # fibronectin strand (ECM)
    "phosphate": "#FFEB3B",  # phosphate group added to a pump
    "atp": "#BF360C",        # ATP text
    "bacteria": "#7CB342",   # bacterium
    "lyso": "#E1BEE7",       # lysosome contents
    "enz_dot": "#C2185B",    # digestive enzymes
    "nutrient": "#2E7D32",   # nutrients leaving food vacuole
    "waste": "#6D4C41",      # undigested waste
    "fluid": "#29B6F6",      # pinocytosis fluid droplets
    "ldl": "#FFD54F",        # LDL particle
    "receptor": "#3949AB",   # LDL receptor
    "clathrin": "#EF6C00",   # clathrin coat
    "golgi": "#F8BBD0",      # Golgi cisternae
    "hormone": "#D81B60",    # secreted hormone (protein)
    "badge": "#37474F",      # step-number badges
    "hdr_passive": "#00796B",
    "hdr_active": "#6A1B9A",
    "hdr_co": "#2E7D32",
    "hdr_bulk": "#AD1457",
    "out_lbl": "#0277BD",
    "in_lbl": "#E65100",
}

GUIDE_LINE = "#C4C4C4"
GUIDE_TEXT = "#ABABAB"
GUIDE_SW = 0.7
FONT = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"

# --------------------------------------------------------------------------
# Membrane geometry
# --------------------------------------------------------------------------
R_HEAD = 6.5
SP = 14
TAIL = 17
YO = 267                         # outer-leaflet head centers
YI = YO + 2 * R_HEAD + 2 * TAIL + 2 + 0  # 316: inner-leaflet head centers
OUT_SURF = YO - R_HEAD           # 260.5 outer surface
IN_SURF = YI + R_HEAD            # 322.5 inner surface
TAIL_OUT0 = YO + R_HEAD          # 273.5
TAIL_OUT1 = TAIL_OUT0 + TAIL     # 290.5
TAIL_IN0 = YI - R_HEAD           # 309.5
TAIL_IN1 = TAIL_IN0 - TAIL       # 292.5
MID = (YO + YI) / 2              # 291.5
X_BIL0, X_BIL1 = 130, 970        # full-bilayer section
XL, XR = 70, 1030                # cell side walls (centerline)
RT = X_BIL0 - XL                 # 60: corner radius of the taper
Y_TAPER = MID + RT               # 351.5
YB = 690                         # bottom membrane centerline
RB = 70                          # bottom corner radius
DL_W = 10                        # simplified double-line band width
DL_LINE = 1.6                    # each of the two lines
DL_EDGE = DL_W / 2 - DL_LINE / 2  # 4.2

# x positions on the top bilayer
IX = 163      # integrin (attachment protein)
GPX = 208     # glycoprotein
GLX = 268     # glycolipid target slot
PPX = 305     # peripheral protein
EX = 372      # enzyme (integral protein)
O2X = 472     # simple diffusion lane
KX = 563      # K+ channel
NKX = 666     # Na+/K+ pump
CTX = 778     # Na+/glucose cotransporter
HX = 884      # proton (H+) pump
CHOL_TARGETS = [245, 515, 938.5]

# bottom-membrane features
PH_X = 215                    # bacterium being engulfed (phagocytosis step 1)
WASTE_X = 395                 # exocytosis #2 (waste)
PINO1_X, PINO2_X = 470, 545
RME1_X, RME2_X = 640, 728
EXO3_X, EXO4_X = 842, 915

GEOM = {}

try:
    from PIL import ImageFont
    _TAGFONT = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", 95)
except Exception:  # pragma: no cover - fallback when the font is missing
    _TAGFONT = None


def text_w(s, size):
    """Approximate rendered width of an extra-bold Inter string, in page units."""
    if _TAGFONT is None:
        return len(s) * size * 0.66
    return _TAGFONT.getlength(s) * size / 95.0


def reset_geom():
    GEOM.clear()
    GEOM.update({"proteins": {}, "phospholipids": [], "cholesterol": [], "touch": {}, "gradients": {},
                 "arrows": {}, "labels": [], "particles": [], "clathrin": [], "receptors": []})


# --------------------------------------------------------------------------
class Doc:
    LAYERS = ("bg", "ecm", "band", "lipid", "protein", "deco", "mol", "arrow", "label")

    def __init__(self, mode):
        self.mode = mode
        self.layers = {k: [] for k in self.LAYERS}
        self.markers = {}

    def _st(self, fill=None, stroke=None, sw=1.0, role=None):
        if self.mode == "guide":
            if role == "tint":
                return None
            if role == "dl_inner":
                return f'fill="none" stroke="#FFFFFF" stroke-width="{sw:.2f}"'
            if role == "dl_outer":
                return f'fill="none" stroke="{GUIDE_LINE}" stroke-width="{sw:.2f}"'
            if role == "white":
                return f'fill="#FFFFFF" stroke="{GUIDE_LINE}" stroke-width="{GUIDE_SW}"'
            if fill is None and stroke is None:
                return None
            return f'fill="none" stroke="{GUIDE_LINE}" stroke-width="{GUIDE_SW}"'
        return f'fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{sw:.2f}"'

    def add(self, layer, s):
        self.layers[layer].append(s)

    @staticmethod
    def _cls(cls):
        return f' class="{cls}"' if cls else ""

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=1.0, layer="mol", role=None, cls=None):
        st = self._st(fill, stroke, sw, role)
        if st:
            self.add(layer, f'<circle{self._cls(cls)} cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" {st}/>')

    def ellipse(self, cx, cy, rx, ry, fill=None, stroke=None, sw=1.0, layer="protein", role=None):
        st = self._st(fill, stroke, sw, role)
        if st:
            self.add(layer, f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" {st}/>')

    def path(self, d, fill=None, stroke=None, sw=1.0, layer="protein", role=None, extra="", cls=None):
        st = self._st(fill, stroke, sw, role)
        if st:
            self.add(layer, f'<path{self._cls(cls)} d="{d}" {st} stroke-linejoin="round" stroke-linecap="round"{extra}/>')

    def line(self, x1, y1, x2, y2, stroke, sw=1.0, layer="lipid", role=None, cls=None):
        st = self._st(None, stroke, sw, role)
        if st:
            self.add(layer, f'<line{self._cls(cls)} x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" {st} '
                            f'stroke-linecap="round"/>')

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=1.0, rx=0, layer="protein", role=None, cls=None):
        st = self._st(fill, stroke, sw, role)
        if st:
            self.add(layer, f'<rect{self._cls(cls)} x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
                            f'rx="{rx:.2f}" {st}/>')

    def polygon(self, pts, fill=None, stroke=None, sw=1.0, layer="mol", role=None, cls=None):
        st = self._st(fill, stroke, sw, role)
        if st:
            p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
            self.add(layer, f'<polygon{self._cls(cls)} points="{p}" {st} stroke-linejoin="round"/>')

    def text(self, x, y, s, size=11, weight=400, anchor="start", color=None, layer="label",
             halo=True, italic=False, cls="lbl"):
        c = GUIDE_TEXT if self.mode == "guide" else (color or PAL["ink"])
        h = ' stroke="#FFFFFF" stroke-width="3" paint-order="stroke" stroke-linejoin="round"' if halo else ""
        it = ' font-style="italic"' if italic else ""
        s = s.replace("&", "&amp;")
        self.add(layer, f'<text class="{cls}" x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" '
                        f'font-weight="{weight}" text-anchor="{anchor}" fill="{c}"{h}{it}>{s}</text>')
        if cls == "lbl" and self.mode == "color":
            GEOM["labels"].append({"text": s, "x": x, "y": y, "size": size, "color": color or PAL["ink"],
                                   "weight": weight})

    def marker(self, color):
        col = GUIDE_LINE if self.mode == "guide" else color
        mid = "ah" + col.replace("#", "")
        if mid not in self.markers:
            if self.mode == "guide":
                body = f'<path d="M1,1 L10,5 L1,9 z" fill="none" stroke="{col}" stroke-width="1.0"/>'
            else:
                body = f'<path d="M0,0 L10,5 L0,10 z" fill="{col}"/>'
            self.markers[mid] = (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8.5" refY="5" '
                                 f'markerWidth="7.5" markerHeight="7.5" markerUnits="userSpaceOnUse" '
                                 f'orient="auto-start-reverse">{body}</marker>')
        return mid

    def arrow(self, d, color, sw=1.6, layer="arrow", halo=True, name=None, cls="arrow"):
        mid = self.marker(color)
        if self.mode == "guide":
            self.add(layer, f'<path class="{cls}" d="{d}" fill="none" stroke="{GUIDE_LINE}" stroke-width="{GUIDE_SW}" '
                            f'marker-end="url(#{mid})"/>')
        else:
            if halo:
                self.add(layer, f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{sw + 2.6:.2f}" '
                                f'stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>')
            self.add(layer, f'<path class="{cls}" d="{d}" fill="none" stroke="{color}" stroke-width="{sw:.2f}" '
                            f'stroke-linecap="round" stroke-linejoin="round" marker-end="url(#{mid})"/>')
        if name:
            GEOM["arrows"][name] = d

    def leader(self, x1, y1, x2, y2):
        """Thin pointer line from a label to the structure, ending in a small dot."""
        self.line(x1, y1, x2, y2, PAL["ink"], 0.75, layer="label", cls="leader")
        self.circle(x2, y2, 1.6, fill=PAL["ink"], layer="label", cls="leaderdot")

    def svg(self, grid=False):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="11in" height="8.5in" viewBox="0 0 {W} {H}">',
               "<defs>" + "".join(self.markers.values()) + "</defs>",
               f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>']
        for k in self.LAYERS:
            out.append(f'<g id="{k}">' + "\n".join(self.layers[k]) + "</g>")
        if grid:
            out.append(grid_svg())
        out.append("</svg>")
        return "\n".join(out)


def grid_svg():
    g = ['<g id="grid">']
    for i in range(1, 22):
        x, major = i * 50, i % 2 == 0
        g.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{"#29B6F6" if major else "#81D4FA"}" '
                 f'stroke-width="{0.9 if major else 0.5}" stroke-dasharray="{"none" if major else "3 4"}" opacity="0.75"/>')
    for i in range(1, 17):
        y, major = i * 50, i % 2 == 0
        g.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{"#29B6F6" if major else "#81D4FA"}" '
                 f'stroke-width="{0.9 if major else 0.5}" stroke-dasharray="{"none" if major else "3 4"}" opacity="0.75"/>')
    lab = f'font-family="{FONT}" font-size="10" font-weight="700" fill="#0277BD"'
    for i in range(1, 11):
        g.append(f'<text x="{i * 100 + 3}" y="12" {lab}>{i}"</text>')
        g.append(f'<text x="{i * 100 + 3}" y="{H - 4}" {lab}>{i}"</text>')
    for i in range(1, 9):
        g.append(f'<text x="3" y="{i * 100 - 3}" {lab}>{i}"</text>')
        g.append(f'<text x="{W - 3}" y="{i * 100 - 3}" text-anchor="end" {lab}>{i}"</text>')
    g.append(f'<rect x="40" y="40" width="{W - 80}" height="{H - 80}" fill="none" stroke="#EF5350" '
             f'stroke-width="0.8" stroke-dasharray="6 4"/>')
    g.append(f'<text x="{W - 44}" y="{H - 44}" text-anchor="end" font-family="{FONT}" font-size="9" '
             f'fill="#EF5350">0.4" safe margin</text>')
    g.append("</g>")
    return "\n".join(g)


# --------------------------------------------------------------------------
# Generic helpers
# --------------------------------------------------------------------------
def rrect_path(x0, y0, x1, y1, r):
    return (f"M {x0 + r},{y0} L {x1 - r},{y0} Q {x1},{y0} {x1},{y0 + r} L {x1},{y1 - r} "
            f"Q {x1},{y1} {x1 - r},{y1} L {x0 + r},{y1} Q {x0},{y1} {x0},{y1 - r} "
            f"L {x0},{y0 + r} Q {x0},{y0} {x0 + r},{y0} Z")


def hexagon(d, cx, cy, r, fill, layer="mol", cls=None):
    pts = [(cx + r * math.cos(math.radians(60 * i + 30)), cy + r * math.sin(math.radians(60 * i + 30)))
           for i in range(6)]
    d.polygon(pts, fill=fill, stroke=PAL["ink"], sw=0.8, layer=layer, cls=cls)
    if layer == "mol" and fill == PAL["glucose"]:
        GEOM["particles"].append(["glucose", round(cx, 1), round(cy, 1)])


def ion(d, cx, cy, kind, r=4.2, layer="mol"):
    d.circle(cx, cy, r, fill=PAL[kind], stroke=PAL["ink"], sw=0.5, layer=layer)
    if layer == "mol":
        GEOM["particles"].append([kind, round(cx, 1), round(cy, 1)])


def o2(d, cx, cy, rot=0, layer="mol"):
    a = math.radians(rot)
    dx, dy = 3.2 * math.cos(a), 3.2 * math.sin(a)
    for s in (-1, 1):
        d.circle(cx + s * dx, cy + s * dy, 3.4, fill=PAL["o2"], stroke=PAL["ink"], sw=0.5, layer=layer)
    if layer == "mol":
        GEOM["particles"].append(["o2", round(cx, 1), round(cy, 1)])


def badge(d, cx, cy, n):
    if d.mode == "guide":
        d.circle(cx, cy, 7.5, stroke=GUIDE_LINE, layer="label", role="x", cls="badge")
    else:
        d.circle(cx, cy, 7.5, fill=PAL["badge"], stroke="#FFFFFF", sw=1.2, layer="label", cls="badge")
    c = GUIDE_TEXT if d.mode == "guide" else "#FFFFFF"
    d.add("label", f'<text class="badgetxt" x="{cx:.2f}" y="{cy + 3.6:.2f}" font-family="{FONT}" font-size="10" '
                   f'font-weight="700" text-anchor="middle" fill="{c}">{n}</text>')


def tag(d, x, y, s, kind, w=None):
    """HIGH / LOW concentration tag. (x, y) = left end of the tag, text baseline."""
    col = "#C62828" if kind == "high" else "#1565C0"
    w = max(w or 0, text_w(s, 9.5) + 9)
    if d.mode == "guide":
        d.rect(x, y - 9, w, 12, stroke=GUIDE_LINE, rx=3, layer="label", role="x", cls="tag")
    else:
        d.rect(x, y - 9, w, 12, fill="#FFFFFF", stroke=col, sw=0.9, rx=3, layer="label", cls="tag")
    d.text(x + w / 2, y + 0.3, s, size=9.5, weight=800, anchor="middle", color=col, halo=False, cls="tagtxt")
    return w


def scatter(seed, n, box, mind, avoid=()):
    """Deterministic loose scatter of n points in box (x0, y0, x1, y1) with a minimum spacing."""
    x0, y0, x1, y1 = box
    rnd = random.Random(seed)
    pts, tries = [], 0
    while len(pts) < n and tries < 40000:
        tries += 1
        p = (rnd.uniform(x0, x1), rnd.uniform(y0, y1))
        if any(math.dist(p, q) < mind for q in pts):
            continue
        if any(a0 <= p[0] <= a1 and b0 <= p[1] <= b1 for a0, b0, a1, b1 in avoid):
            continue
        pts.append(p)
    if len(pts) < n:
        raise RuntimeError(f"scatter seed {seed}: only placed {len(pts)}/{n}")
    return pts


def dl_path(d, dpath, layer="band"):
    """Simplified bilayer as a double line (dark wide stroke + lighter narrower stroke on top)."""
    d.path(dpath, stroke=PAL["ink"], sw=DL_W, layer=layer, role="dl_outer", extra=' stroke-linecap="butt"')
    d.path(dpath, stroke=PAL["band"], sw=DL_W - 2 * DL_LINE, layer=layer, role="dl_inner",
           extra=' stroke-linecap="butt"')


def dl_circle(d, cx, cy, r, lumen=None, layer="band"):
    if lumen:
        d.circle(cx, cy, r, fill=lumen, layer=layer, role="tint")
    d.circle(cx, cy, r, stroke=PAL["ink"], sw=DL_W, layer=layer, role="dl_outer")
    d.circle(cx, cy, r, stroke=PAL["band"], sw=DL_W - 2 * DL_LINE, layer=layer, role="dl_inner")


def omega(cx, base, neck, R):
    """Flask-shaped pocket on the bottom membrane; the bulb bulges up into the cell."""
    hx, hn = neck / 2, 5
    dy = math.sqrt(R * R - hx * hx)
    cy = base - (hn + dy)
    seg = (f" L {cx - hx - 9:.2f},{base:.2f} Q {cx - hx:.2f},{base:.2f} {cx - hx:.2f},{base - hn:.2f}"
           f" A {R},{R} 0 1 1 {cx + hx:.2f},{base - hn:.2f}"
           f" Q {cx + hx:.2f},{base:.2f} {cx + hx + 9:.2f},{base:.2f}")
    return seg, (cx, cy)


def circle_union_path(c1, r1, c2, r2):
    (x1, y1), (x2, y2) = c1, c2
    dd = math.dist(c1, c2)
    a = (r1 * r1 - r2 * r2 + dd * dd) / (2 * dd)
    h = math.sqrt(r1 * r1 - a * a)
    xm, ym = x1 + a * (x2 - x1) / dd, y1 + a * (y2 - y1) / dd
    px, py = -(y2 - y1) / dd, (x2 - x1) / dd
    p1 = (xm + h * px, ym + h * py)
    p2 = (xm - h * px, ym - h * py)
    return (f"M {p1[0]:.2f},{p1[1]:.2f} A {r1},{r1} 0 1 1 {p2[0]:.2f},{p2[1]:.2f} "
            f"A {r2},{r2} 0 1 1 {p1[0]:.2f},{p1[1]:.2f} Z")


def protein(d, name, x0, y0, x1, y1, fill, r=10, dpath=None):
    d.path(dpath or rrect_path(x0, y0, x1, y1, r), fill=fill, stroke=PAL["ink"], sw=1.1, layer="protein")
    GEOM["proteins"][name] = {"x0": x0, "x1": x1, "top": y0, "bottom": y1}


# --------------------------------------------------------------------------
# Membrane pieces
# --------------------------------------------------------------------------
def phospholipid(d, x, leaflet):
    if leaflet == "outer":
        hy, t0, t1 = YO, TAIL_OUT0, TAIL_OUT1
    else:
        hy, t0, t1 = YI, TAIL_IN0, TAIL_IN1
    sgn = 1 if t1 > t0 else -1
    d.line(x - 2.8, t0, x - 2.8, t1, PAL["tail"], 1.3, layer="lipid")             # saturated (straight)
    d.path(f"M {x + 2.8:.2f},{t0} L {x + 2.8:.2f},{t0 + sgn * 8:.2f} L {x + 4.8:.2f},{t1}",  # unsaturated (kink)
           stroke=PAL["tail"], sw=1.3, layer="lipid")
    d.circle(x, hy, R_HEAD, fill=PAL["head"], stroke=PAL["ink"], sw=0.8, layer="lipid")
    GEOM["phospholipids"].append({"x": round(x, 2), "leaflet": leaflet, "head_y": hy,
                                  "tail_from": t0, "tail_to": t1})


def cholesterol(d, xm, leaflet):
    if leaflet == "outer":
        oh, b0, b1, tl = TAIL_OUT0 - 0.5, TAIL_OUT0 + 2.5, TAIL_OUT0 + 13.5, (TAIL_OUT0 + 13.5, TAIL_OUT1)
    else:
        oh, b0, b1, tl = TAIL_IN0 + 0.5, TAIL_IN0 - 13.5, TAIL_IN0 - 2.5, (TAIL_IN1, TAIL_IN0 - 13.5)
    d.line(xm, tl[0], xm, tl[1], PAL["ink"], 1.1, layer="lipid")
    d.path(rrect_path(xm - 3, b0, xm + 3, b1, 2), fill=PAL["chol"], stroke=PAL["ink"], sw=0.8, layer="lipid")
    d.circle(xm, oh, 2.4, fill=PAL["chol"], stroke=PAL["ink"], sw=0.7, layer="lipid")
    GEOM["cholesterol"].append({"x": round(xm, 2), "leaflet": leaflet, "body": [b0, b1], "oh_y": oh})


def sugar_chain(d, beads, links, attach_y):
    for a, b in links:
        d.line(*beads[a], *beads[b], PAL["ink"], 1.0, layer="deco")
    d.line(beads[0][0], attach_y, *beads[0], PAL["ink"], 1.0, layer="deco")
    for bx, by in beads:
        d.circle(bx, by, 3.5, fill=PAL["carb"], stroke=PAL["ink"], sw=0.6, layer="deco")


def taper(d, left=True):
    """Rounded top corner: the hydrophobic band of the full bilayer narrows into the double line."""
    cx = X_BIL0 if left else X_BIL1
    cy = Y_TAPER
    outer, inner = [], []
    n = 40
    for i in range(n + 1):
        t = i / n
        s = t * t * (3 - 2 * t)
        hw = 18 + (DL_W / 2 - 18) * s                 # half width: tail band (18) -> double line (5)
        phi = math.radians(270 - 90 * t) if left else math.radians(270 + 90 * t)
        ux, uy = math.cos(phi), math.sin(phi)
        o = hw - DL_LINE / 2
        outer.append((cx + (RT + o) * ux, cy + (RT + o) * uy))
        inner.append((cx + (RT - o) * ux, cy + (RT - o) * uy))
    fillp = ("M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in outer) + " L " +
             " L ".join(f"{x:.2f},{y:.2f}" for x, y in reversed(inner)) + " Z")
    d.path(fillp, fill=PAL["band"], layer="band", role="tint")
    d.path("M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in outer), stroke=PAL["ink"], sw=DL_LINE, layer="band",
           extra=' stroke-linecap="butt"')
    d.path("M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in inner), stroke=PAL["ink"], sw=DL_LINE, layer="band",
           extra=' stroke-linecap="butt"')
    GEOM["touch"]["taper_" + ("left" if left else "right")] = {
        "start_outer": outer[0], "start_inner": inner[0], "end_outer": outer[-1], "end_inner": inner[-1]}


def bottom_path():
    """Centerline of the side walls + bottom membrane, left to right, with every pocket."""
    s, F = [], {}
    s.append(f"M {XL},{Y_TAPER} L {XL},{YB - RB} A {RB},{RB} 0 0 0 {XL + RB},{YB}")
    cx = PH_X
    s.append(f" L {cx - 75},{YB} C {cx - 58},{YB} {cx - 51},{YB + 8} {cx - 51},{YB + 28}"
             f" L {cx - 51},{YB + 50} C {cx - 51},{YB + 70} {cx - 38},{YB + 78} {cx - 18},{YB + 78}"
             f" A 9,9 0 0 0 {cx - 18},{YB + 60}"
             f" C {cx - 28},{YB + 60} {cx - 33},{YB + 52} {cx - 33},{YB + 42}"
             f" L {cx - 33},{YB + 32} C {cx - 33},{YB + 24} {cx - 28},{YB + 20} {cx - 20},{YB + 20}"
             f" L {cx + 20},{YB + 20} C {cx + 28},{YB + 20} {cx + 33},{YB + 24} {cx + 33},{YB + 32}"
             f" L {cx + 33},{YB + 42} C {cx + 33},{YB + 52} {cx + 28},{YB + 60} {cx + 18},{YB + 60}"
             f" A 9,9 0 0 0 {cx + 18},{YB + 78}"
             f" C {cx + 38},{YB + 78} {cx + 51},{YB + 70} {cx + 51},{YB + 50}"
             f" L {cx + 51},{YB + 28} C {cx + 51},{YB + 8} {cx + 58},{YB} {cx + 75},{YB}")
    F["phago_cup"] = {"inner_x": [cx - 33, cx + 33], "inner_bottom": YB + 60, "cup_top": YB + 20,
                      "tips_x": [cx - 9, cx + 9], "outer_bottom": YB + 78}
    seg, c = omega(WASTE_X, YB, 22, 20)
    s.append(seg)
    F["waste"] = c
    x = PINO1_X
    s.append(f" L {x - 30},{YB} C {x - 16},{YB} {x - 16},{YB - 22} {x},{YB - 22}"
             f" C {x + 16},{YB - 22} {x + 16},{YB} {x + 30},{YB}")
    seg, c = omega(PINO2_X, YB, 14, 21)
    s.append(seg)
    F["pino2"] = c
    x = RME1_X
    s.append(f" L {x - 38},{YB} C {x - 20},{YB} {x - 22},{YB - 30} {x},{YB - 30}"
             f" C {x + 22},{YB - 30} {x + 20},{YB} {x + 38},{YB}")
    seg, c = omega(RME2_X, YB, 14, 27)
    s.append(seg)
    F["rme2"] = c
    seg, c = omega(EXO3_X, YB, 20, 17)
    s.append(seg)
    F["exo3"] = c
    x = EXO4_X
    s.append(f" L {x - 30},{YB} C {x - 14},{YB} {x - 14},{YB - 13} {x},{YB - 13}"
             f" C {x + 14},{YB - 13} {x + 14},{YB} {x + 30},{YB}")
    s.append(f" L {XR - RB},{YB} A {RB},{RB} 0 0 0 {XR},{YB - RB} L {XR},{Y_TAPER}")
    return "".join(s), F


def cyto_outline():
    p, _ = bottom_path()
    return p + f" A {RT},{RT} 0 0 0 {X_BIL1},{MID} L {X_BIL0},{MID} A {RT},{RT} 0 0 0 {XL},{Y_TAPER} Z"


# --------------------------------------------------------------------------
def draw(mode):
    reset_geom()
    d = Doc(mode)
    P = PAL

    # ---------- optional background tints ----------
    d.rect(0, 0, W, H, fill=P["outside"], layer="bg", role="tint")
    d.path(cyto_outline(), fill=P["cyto"], layer="bg", role="tint")

    # ---------- title ----------
    d.text(550, 66, "The Plasma Membrane: Structure & Transport", size=24, weight=800, anchor="middle",
           halo=False)
    d.text(1058, 64, "Name: ______________", size=11, anchor="end", halo=False)

    # ---------- outside / inside region labels ----------
    d.text(80, 98, "OUTSIDE THE CELL", size=12.5, weight=800, color=P["out_lbl"])
    d.text(80, 111, "(extracellular fluid)", size=10.5, weight=600, color=P["out_lbl"])
    d.text(560, 476, "INSIDE THE CELL (cytoplasm)", size=13, weight=800, anchor="middle", color=P["in_lbl"])
    d.text(700, 801, "OUTSIDE THE CELL (extracellular fluid)", size=12.5, weight=800, anchor="middle",
           color=P["out_lbl"])

    # ---------- bilayer core tint + corner tapers + double-line membrane ----------
    d.rect(X_BIL0, TAIL_OUT0, X_BIL1 - X_BIL0, TAIL_IN0 - TAIL_OUT0, fill=P["tails"], layer="band", role="tint")
    taper(d, True)
    taper(d, False)
    path, F = bottom_path()
    dl_path(d, path)
    GEOM["bottom_features"] = F

    # ---------- ECM collagen fibers ----------
    strands = []
    for k, (base, ph) in enumerate(((182, 0.0), (188, 1.4), (194, 2.8), (200, 4.2))):
        pts = [(x, base + 2.4 * math.sin((x - 50) / 6.5 + ph)) for x in [50 + i * 2 for i in range(0, 64)]]
        strands.append(pts)
        d.path("M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts), stroke=P["collagen"], sw=2.3, layer="ecm")
    low = strands[-1]
    y_low_at_ix = [y for x, y in low if abs(x - (IX + 3)) < 1.01][0]  # bottom strand right above the fibronectin end

    # ---------- proteins ----------
    excl = []
    # integrin: two legs + head; head holds fibronectin (which holds collagen), legs touch actin
    head_ry = 9
    head_cy = 236
    leg_bot = IN_SURF + 21                         # 343.5: reaches the actin filament
    for dx in (-7, 7):
        d.path(rrect_path(IX + dx - 5, head_cy, IX + dx + 5, leg_bot, 4.5), fill=P["integrin"], stroke=P["ink"],
               sw=1.0, layer="protein")
    d.ellipse(IX, head_cy, 17, head_ry, fill=P["integrin"], stroke=P["ink"], sw=1.0)
    GEOM["proteins"]["integrin"] = {"x0": IX - 12, "x1": IX + 12, "top": head_cy - head_ry, "bottom": leg_bot}
    fn = [(IX - 3 + 3 * math.sin(i / 3.0) + 6 * i / 24, head_cy - head_ry + 0.8 - i * (head_cy - head_ry + 0.8 - y_low_at_ix + 0.8) / 24)
          for i in range(25)]
    d.path("M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in fn), stroke=P["fibronectin"], sw=2.2, layer="ecm")
    GEOM["touch"]["integrin_fibronectin_collagen"] = {
        "head_top": head_cy - head_ry, "fibronectin_bottom": fn[0][1], "fibronectin_top": fn[-1][1],
        "collagen_strand_y_at_end": y_low_at_ix}
    excl.append((IX - 12, IX + 12))

    # glycoprotein + sugar chain (outside face only)
    gp_top = 247
    protein(d, "glycoprotein", GPX - 14, gp_top, GPX + 14, 336, P["glycoprot"], r=11)
    excl.append((GPX - 14, GPX + 14))
    beads = [(GPX, gp_top - 4), (GPX, gp_top - 11.5), (GPX, gp_top - 19), (GPX - 6.5, gp_top - 25.5),
             (GPX + 6.5, gp_top - 25.5), (GPX - 11, gp_top - 32.5), (GPX + 11, gp_top - 32.5)]
    sugar_chain(d, beads, [(0, 1), (1, 2), (2, 3), (2, 4), (3, 5), (4, 6)], gp_top)
    GEOM["touch"]["glycoprotein_chain"] = {"bead0_bottom": gp_top - 4 + 3.5, "protein_top": gp_top,
                                           "chain_top": gp_top - 32.5 - 3.5, "side": "outside"}

    # enzyme: active-site cup faces the cytoplasm (like the "enzymatic activity" figure in the notes)
    ex0, ex1, ey0, ey1 = EX - 23, EX + 23, 247, 342
    cup = (f"M {ex0 + 10},{ey0} L {ex1 - 10},{ey0} Q {ex1},{ey0} {ex1},{ey0 + 10} L {ex1},{ey1 - 10} "
           f"Q {ex1},{ey1} {ex1 - 10},{ey1} L {EX + 9},{ey1} C {EX + 9},{ey1 - 14} {EX - 9},{ey1 - 14} {EX - 9},{ey1} "
           f"L {ex0 + 10},{ey1} Q {ex0},{ey1} {ex0},{ey1 - 10} L {ex0},{ey0 + 10} Q {ex0},{ey0} {ex0 + 10},{ey0} Z")
    protein(d, "enzyme", ex0, ey0, ex1, ey1, P["enzyme"], dpath=cup)
    excl.append((ex0, ex1))

    # K+ channel: two subunits around a water-filled pore
    for sx0, sx1 in ((KX - 24, KX - 7), (KX + 7, KX + 24)):
        d.path(rrect_path(sx0, 247, sx1, 336, 7), fill=P["channel"], stroke=P["ink"], sw=1.1, layer="protein")
    GEOM["proteins"]["k_channel"] = {"x0": KX - 24, "x1": KX + 24, "top": 247, "bottom": 336,
                                     "pore": [KX - 7, KX + 7]}
    excl.append((KX - 24, KX + 24))

    # Na+/K+ pump
    nk = (f"M {NKX - 30},259 Q {NKX - 32},243 {NKX - 14},243 L {NKX + 14},243 Q {NKX + 32},243 {NKX + 30},259 "
          f"L {NKX + 30},325 Q {NKX + 32},341 {NKX + 14},341 L {NKX - 14},341 Q {NKX - 32},341 {NKX - 30},325 Z")
    protein(d, "na_k_pump", NKX - 31, 243, NKX + 31, 341, P["nakpump"], dpath=nk)
    excl.append((NKX - 31, NKX + 31))

    # Na+/glucose cotransporter
    protein(d, "cotransporter", CTX - 25, 247, CTX + 25, 336, P["cotrans"], r=12)
    excl.append((CTX - 25, CTX + 25))

    # proton (H+) pump
    hp = (f"M {HX - 22},257 Q {HX - 24},245 {HX - 10},245 L {HX + 10},245 Q {HX + 24},245 {HX + 22},257 "
          f"L {HX + 22},327 Q {HX + 24},339 {HX + 10},339 L {HX - 10},339 Q {HX - 24},339 {HX - 22},327 Z")
    protein(d, "proton_pump", HX - 23, 245, HX + 23, 339, P["hpump"], dpath=hp)
    excl.append((HX - 23, HX + 23))

    # ---------- phospholipid slots: spread evenly between proteins and cholesterol ----------
    chol_x = list(CHOL_TARGETS)
    blocks = sorted(excl + [(c - 3.5, c + 3.5) for c in chol_x])
    edges = [X_BIL0] + [v for a, b in blocks for v in (a, b)] + [X_BIL1]
    slots = []
    for a, b in zip(edges[0::2], edges[1::2]):        # free stretches of membrane
        L = b - a
        n = int((L - 1 - 2 * R_HEAD) // SP) + 1 if L >= 2 * R_HEAD + 1 else 0
        if n <= 0:
            continue
        slack = L - (2 * R_HEAD + (n - 1) * SP)
        gap = slack / (n + 1)
        for k in range(n):
            slots.append(round(a + gap + R_HEAD + k * (SP + gap), 2))
    for x in slots:
        phospholipid(d, x, "outer")
        phospholipid(d, x, "inner")
    for xc in chol_x:
        cholesterol(d, xc, "outer")
        cholesterol(d, xc, "inner")
    GEOM["slots"] = slots

    # glycolipid: sugar chain on one outer-leaflet phospholipid
    glx = min(slots, key=lambda s: abs(s - GLX))
    gb = [(glx, OUT_SURF - 4), (glx, OUT_SURF - 11.5), (glx - 5.5, OUT_SURF - 18), (glx + 5.5, OUT_SURF - 18)]
    sugar_chain(d, gb, [(0, 1), (1, 2), (1, 3)], OUT_SURF)
    GEOM["touch"]["glycolipid_chain"] = {"x": glx, "bead0_bottom": OUT_SURF - 4 + 3.5, "head_top": OUT_SURF,
                                         "side": "outside", "leaflet": "outer"}

    # peripheral protein on the cytoplasmic face, touching the inner heads
    pp_ry = 9
    pp_cy = IN_SURF + pp_ry - 1.5
    d.ellipse(PPX, pp_cy, 20, pp_ry, fill=P["periph"], stroke=P["ink"], sw=1.1)
    GEOM["proteins"]["peripheral"] = {"x0": PPX - 20, "x1": PPX + 20, "top": pp_cy - pp_ry, "bottom": pp_cy + pp_ry}
    GEOM["touch"]["peripheral"] = {"top": pp_cy - pp_ry, "inner_surface": IN_SURF,
                                   "heads_above": [s for s in slots if abs(s - PPX) < 20]}

    # ---------- actin microfilament: runs under the bilayer, attached to integrin, then down the wall ----------
    ya = IN_SURF + 25
    pts = [(242 - i, ya) for i in range(0, 140)]                       # 242 -> 103
    for i in range(1, 31):                                            # quarter turn down to the wall
        a = math.radians(90 + 90 * i / 30)
        pts.append((103 + 17 * math.cos(a), ya + 17 - 17 * math.sin(a) + 0))
    pts += [(86, ya + 17 + i) for i in range(1, 100)]                  # down the left wall
    acc, beads = 0, []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.dist((x0, y0), (x1, y1))
        acc += seg
        if acc >= 5.2:
            acc = 0
            beads.append((x1, y1, x1 - x0, y1 - y0))
    for i, (bx, by, tx, ty) in enumerate(beads):
        n = math.hypot(tx, ty)
        nx, ny = -ty / n, tx / n
        off = 1.7 if i % 2 else -1.7
        d.circle(bx + nx * off, by + ny * off, 3.3, fill=P["actin"], stroke=P["ink"], sw=0.5, layer="deco")
    GEOM["touch"]["integrin_actin"] = {"leg_bottom": leg_bot, "actin_top": ya - 1.7 - 3.3}

    # ---------- labels: membrane structures ----------
    d.text(80, 140, "Collagen fibers", size=11, weight=700, color="#5D4037")
    d.text(80, 152, "(extracellular matrix, ECM)", size=10, color="#5D4037")
    top_strand_y = [y for x, y in strands[0] if abs(x - 104) < 1.01][0]
    d.leader(104, 156, 104, top_strand_y)
    d.text(78, 222, "Fibronectin", size=11, weight=700, color="#1565C0")
    d.leader(141, 219, fn[9][0] - 1, fn[9][1])
    d.text(226, 182, "Glycoprotein", size=11, weight=700, anchor="middle", color="#E65100")
    d.text(226, 193, "(cell ID card)", size=9.5, anchor="middle", color="#E65100")
    d.leader(212, 197, GPX, gp_top - 21)
    d.text(240, 214, "Glycolipid", size=11, weight=700, color="#2E7D32")
    d.leader(glx - 2, 218, glx - 1, OUT_SURF - 22)
    d.text(100, 386, "Integrin", size=11, weight=700, color="#1565C0")
    d.text(100, 398, "(attachment protein)", size=10, color="#1565C0")
    d.leader(122, 376, IX - 8, 334)
    d.text(100, 432, "Microfilaments (actin)", size=11, weight=700, color="#C62828")
    d.text(100, 444, "(cytoskeleton)", size=10, color="#C62828")
    d.leader(98, 428, 90.5, 428)
    cx_l = chol_x[0]
    d.text(205, 386, "Cholesterol", size=11, weight=700, color="#B8860B")
    d.leader(cx_l, 375, cx_l, TAIL_IN0 - 8)
    d.text(PPX + 4, 420, "Peripheral protein", size=11, weight=700, anchor="middle", color="#D84315")
    d.leader(PPX + 4, 409, PPX + 4, pp_cy + 4)
    d.text(EX + 2, 214, "Enzyme", size=11, weight=700, anchor="middle", color="#7B1FA2")
    d.text(EX + 2, 226, "(integral protein)", size=10, anchor="middle", color="#7B1FA2")
    d.leader(EX + 2, 230, EX + 2, ey0 + 6)
    pl = min(slots, key=lambda s: abs(s - 952))
    d.text(940, 404, "Phospholipid", size=11, weight=700, color="#AD1457")
    d.text(940, 416, "(hydrophilic head,", size=9.5, color="#AD1457")
    d.text(940, 427, "hydrophobic tails)", size=9.5, color="#AD1457")
    d.leader(pl, 393, pl, YI + 3)

    # enzyme: substrate goes into the active site, products come out (cytoplasm side)
    sub = (343, 374)
    d.polygon([(sub[0], sub[1] - 6.5), (sub[0] + 6.5, sub[1] + 5), (sub[0] - 6.5, sub[1] + 5)],
              fill=P["substrate"], stroke=P["ink"], sw=0.8)
    d.arrow(f"M {sub[0] + 4},{sub[1] - 9} Q {EX - 14},{352} {EX - 5},{ey1 - 9}", P["ink"], sw=1.3, name="enzyme_in")
    d.circle(404, 380, 5, fill=P["product1"], stroke=P["ink"], sw=0.8)
    d.rect(410, 356, 10, 10, fill=P["product2"], stroke=P["ink"], sw=0.8, layer="mol")
    d.arrow(f"M {EX + 4},{ey1 - 6} Q {EX + 10},{362} {398},{373}", P["ink"], sw=1.3, name="enzyme_out1")
    d.arrow(f"M {EX + 7},{ey1 - 8} Q {EX + 22},{350} {407},{356}", P["ink"], sw=1.3, name="enzyme_out2")
    d.text(sub[0], 396, "Substrate", size=10, weight=700, anchor="middle")
    d.text(410, 396, "Products", size=10, weight=700, anchor="middle")
    GEOM["enzyme"] = {"substrate": "triangle", "products": ["circle", "square"], "side": "inside (cytoplasm)",
                      "active_site_bottom": ey1}

    # ---------- transport: headers ----------
    def header(x, l1, l2, l3, color):
        d.text(x, 92, l1, size=11.5, weight=800, anchor="middle", color=color)
        d.text(x, 104, l2, size=11.5, weight=800, anchor="middle", color=color)
        d.text(x, 117, l3, size=10.5, weight=700, anchor="middle")

    header(O2X, "SIMPLE", "DIFFUSION", "O₂ through bilayer", P["hdr_passive"])
    header(KX, "FACILITATED", "DIFFUSION", "K⁺ channel", P["hdr_passive"])
    header(NKX, "ACTIVE", "TRANSPORT #1", "Na⁺/K⁺ pump", P["hdr_active"])
    d.text(CTX, 92, "COTRANSPORT", size=11.5, weight=800, anchor="middle", color=P["hdr_co"])
    d.text(CTX, 103.5, "(secondary active", size=9.5, weight=700, anchor="middle", color=P["hdr_co"])
    d.text(CTX, 114, "transport)", size=9.5, weight=700, anchor="middle", color=P["hdr_co"])
    d.text(CTX, 127, "Na⁺/glucose", size=10.5, weight=700, anchor="middle")
    header(HX, "ACTIVE", "TRANSPORT #2", "Proton (H⁺) pump", P["hdr_active"])
    d.text(NKX, 129, "Na⁺ out, K⁺ in", size=9.5, weight=600, anchor="middle")

    def note(x, l1, l2, color, l3=None):
        d.text(x, 441, l1, size=10, weight=700, anchor="middle", color=color)
        d.text(x, 452, l2, size=9.5, anchor="middle", italic=True)
        if l3:
            d.text(x, 463, l3, size=9.5, anchor="middle", italic=True)

    OUT_Y = (156, 238)      # outside dot band
    IN_Y = (348, 392)       # inside dot band
    TOP_TAG, BOT_TAG = 143, 408

    # ---- simple diffusion: O2 high outside -> low inside, straight through the lipids ----
    lane = (O2X - 9, 0, O2X + 9, 999)
    for p in scatter(11, 9, (432, OUT_Y[0], 514, OUT_Y[1]), 15, avoid=[lane, (420, 150, 446, 196)]):
        o2(d, *p, rot=random.Random(int(p[0] * 7 + p[1])).randint(0, 180))
    for p in ((448, 372), (500, 386)):
        o2(d, *p, rot=30)
    o2(d, O2X, MID, rot=90)
    d.arrow(f"M {O2X},{OUT_Y[0] + 4} L {O2X},{IN_Y[1] - 2}", P["o2"], sw=2.2, name="o2")
    tag(d, O2X - 24, TOP_TAG, "HIGH O₂", "high", w=48)
    tag(d, O2X - 24, BOT_TAG, "LOW O₂", "low", w=48)
    note(O2X, "No energy used", "(passive)", P["hdr_passive"])
    GEOM["gradients"]["O2"] = {"outside": 9, "inside": 2, "high": "outside", "moves": "in"}

    # ---- facilitated diffusion: K+ high inside -> low outside, through the channel pore ----
    lane = (KX - 9, 0, KX + 9, 999)
    for p in ((530, 222), (598, 184)):
        ion(d, *p, "k")
    for p in scatter(21, 7, (521, IN_Y[0], 598, IN_Y[1]), 13, avoid=[lane]):
        ion(d, *p, "k")
    ion(d, KX, MID, "k")
    d.arrow(f"M {KX},{IN_Y[1] - 2} L {KX},{OUT_Y[0] + 6}", P["k"], sw=2.2, name="k_channel")
    tag(d, KX - 23, TOP_TAG, "LOW K⁺", "low", w=46)
    tag(d, KX - 25, BOT_TAG, "HIGH K⁺", "high", w=50)
    note(KX, "No energy used", "(passive)", P["hdr_passive"])
    GEOM["gradients"]["K_channel"] = {"outside": 2, "inside": 7, "high": "inside", "moves": "out"}

    # ---- Na+/K+ pump: Na+ out (low in -> high out), K+ in (low out -> high in), ATP inside ----
    na_lanes = [(NKX - 22, 0, NKX - 6, 999), (NKX + 6, 0, NKX + 22, 999),
                (CTX - 19, 0, CTX - 3, 999), (CTX + 3, 0, CTX + 19, 999)]
    na_out = scatter(31, 15, (614, OUT_Y[0] + 12, 834, OUT_Y[1]), 13,
                     avoid=na_lanes + [(700, 150, 720, 205), (796, 190, 834, 238)])
    for p in na_out:
        ion(d, *p, "na")
    ion(d, 712, 188, "k")                                   # K+ low outside
    for p in scatter(41, 6, (NKX + 4, IN_Y[0], 720, IN_Y[1]), 13,
                     avoid=[(NKX + 6, 0, NKX + 22, 999), (692, 352, 708, 368)]):
        ion(d, *p, "k")                                     # K+ high inside
    ion(d, 700, 360, "na")                                  # Na+ low inside
    for yy in (272, 287, 302):
        ion(d, NKX - 14, yy, "na", r=3.6)
    for yy in (279, 297):
        ion(d, NKX + 14, yy, "k", r=3.6)
    d.arrow(f"M {NKX - 14},{IN_Y[1] - 4} L {NKX - 14},{OUT_Y[0] + 12}", P["na"], sw=2.2, name="nak_na")
    d.arrow(f"M {NKX + 14},{OUT_Y[0] + 12} L {NKX + 14},{IN_Y[1] - 4}", P["k"], sw=2.2, name="nak_k")
    atp(d, 628, 356, NKX - 26, 336)
    tag(d, NKX - 28, TOP_TAG, "HIGH Na⁺", "high", w=56)
    tag(d, NKX - 28, TOP_TAG + 14, "LOW K⁺", "low", w=56)
    tag(d, NKX - 28, BOT_TAG, "HIGH K⁺", "high", w=56)
    tag(d, NKX - 28, BOT_TAG + 14, "LOW Na⁺", "low", w=56)
    note(NKX, "Energy: ATP", "(against gradients)", P["hdr_active"])
    GEOM["gradients"]["Na_pump"] = {"outside_na": "high", "inside_na": "low", "na_moves": "out",
                                    "outside_k": "low", "inside_k": "high", "k_moves": "in", "atp_side": "inside"}

    # ---- cotransport: Na+ in (down its gradient) powers glucose in (against its gradient) ----
    for p in ((738, 384), (812, 360)):
        ion(d, *p, "na")                                    # Na+ low inside
    for p in ((812, 214), ):
        hexagon(d, *p, 5.5, P["glucose"])                   # glucose low outside
    for p in scatter(51, 6, (CTX - 4, IN_Y[0], 834, IN_Y[1]), 15, avoid=[(CTX + 3, 0, CTX + 19, 999), (800, 350, 822, 370)]):
        hexagon(d, *p, 5.5, P["glucose"])                   # glucose high inside
    ion(d, CTX - 11, 282, "na", r=3.6)
    hexagon(d, CTX + 11, 298, 5, P["glucose"])
    d.arrow(f"M {CTX - 11},{OUT_Y[0] + 12} L {CTX - 11},{IN_Y[1] - 4}", P["na"], sw=2.2, name="co_na")
    d.arrow(f"M {CTX + 11},{224} L {CTX + 11},{IN_Y[1] - 4}", P["glucose"], sw=2.2, name="co_glucose")
    tag(d, CTX - 36, TOP_TAG, "HIGH Na⁺", "high", w=72)
    tag(d, CTX - 36, TOP_TAG + 14, "LOW glucose", "low", w=72)
    tag(d, CTX - 36, BOT_TAG, "LOW Na⁺", "low", w=72)
    tag(d, CTX - 36, BOT_TAG + 14, "HIGH glucose", "high", w=72)
    note(CTX, "Energy: Na⁺ gradient", "made by the Na⁺/K⁺ pump", P["hdr_co"], "(ATP used indirectly)")
    GEOM["gradients"]["cotransport"] = {"outside_na": "high", "inside_na": "low", "na_moves": "in",
                                        "outside_glucose": "low", "inside_glucose": "high", "glucose_moves": "in"}

    # ---- proton pump: H+ low inside -> high outside (acidic outside), ATP inside ----
    lane = (HX - 9, 0, HX + 9, 999)
    for p in scatter(61, 9, (840, OUT_Y[0], 930, OUT_Y[1]), 13, avoid=[lane]):
        ion(d, *p, "h")
    ion(d, 852, 384, "h")
    ion(d, HX, MID, "h", r=3.6)
    d.arrow(f"M {HX},{IN_Y[1] - 4} L {HX},{OUT_Y[0] + 6}", P["h"], sw=2.2, name="proton_pump")
    atp(d, 920, 356, HX + 18, 336)
    tag(d, HX - 43, TOP_TAG, "HIGH H⁺ (acidic)", "high")
    tag(d, HX - 24, BOT_TAG, "LOW H⁺", "low", w=48)
    note(HX, "Energy: ATP", "(against gradient)", P["hdr_active"])
    GEOM["gradients"]["proton_pump"] = {"outside": 9, "inside": 1, "high": "outside", "moves": "out",
                                        "atp_side": "inside"}

    key(d, 944, 82)
    bulk(d, F)
    return d


def atp(d, tx, ty, px, py):
    """'ATP -> ADP + Pi' on the cytoplasm side, with an arrow pointing to the pump."""
    c = PAL["atp"]
    d.text(tx, ty + 4, "ATP", size=10, weight=800, anchor="middle", color=c)
    d.text(tx, ty + 14, "↓", size=9, weight=700, anchor="middle", color=c)
    d.text(tx, ty + 24, "ADP", size=9.5, weight=700, anchor="middle", color=c)
    sx = tx + (12 if px > tx else -12)
    ux, uy = px - sx, py - (ty - 1)
    n = math.hypot(ux, uy)
    d.arrow(f"M {sx},{ty - 1} L {px - ux / n * 6.5:.2f},{py - uy / n * 6.5:.2f}", c, sw=1.2)
    phosphate(d, px, py)
    GEOM.setdefault("atp", []).append({"x": tx, "y": ty, "side": "inside" if ty > IN_SURF else "outside"})


def phosphate(d, x, y, layer="arrow"):
    """Phosphate group (P) stuck to the pump: the pump is phosphorylated by ATP."""
    d.circle(x, y, 5.2, fill=PAL["phosphate"], stroke=PAL["ink"], sw=0.8, layer=layer)
    d.text(x, y + 3.2, "P", size=8.5, weight=800, anchor="middle", halo=False, cls="ptxt")
    if layer == "arrow":
        GEOM.setdefault("phosphates", []).append({"x": x, "y": y})


def key(d, x, y):
    P = PAL
    w, h = 114, 160
    if d.mode == "guide":
        d.rect(x, y, w, h, stroke=GUIDE_LINE, rx=6, layer="label", role="x", cls="keybox")
    else:
        d.rect(x, y, w, h, fill="#FFFFFF", stroke=P["ink"], sw=1.0, rx=6, layer="label", cls="keybox")
    d.text(x + w / 2, y + 15, "KEY", size=11.5, weight=800, anchor="middle", halo=False, cls="keytxt")
    rows = [("na", "Na⁺ sodium ion"), ("k", "K⁺ potassium ion"), ("h", "H⁺ proton"),
            ("o2", "O₂ oxygen"), ("glucose", "Glucose"), ("phos", "Phosphate (ATP)"),
            ("arrow", "Direction it moves"), ("high", "More dots"), ("low", "Fewer dots")]
    yy = y + 31
    for kind, label in rows:
        sx = x + 13
        if kind in ("na", "k", "h"):
            ion(d, sx, yy - 3.5, kind, layer="label")
        elif kind == "phos":
            phosphate(d, sx, yy - 3.5, layer="label")
        elif kind == "o2":
            o2(d, sx, yy - 3.5, layer="label")
        elif kind == "glucose":
            hexagon(d, sx, yy - 3.5, 5.5, P[kind], layer="label")
        elif kind == "arrow":
            d.arrow(f"M {sx - 8},{yy - 3.5} L {sx + 8},{yy - 3.5}", P["ink"], sw=1.4, halo=False, layer="label",
                    cls="keyarrow")
        if kind in ("high", "low"):
            col = "#C62828" if kind == "high" else "#1565C0"
            word = "HIGH" if kind == "high" else "LOW"
            if d.mode == "guide":
                d.rect(x + 5, yy - 10, 32, 12, stroke=GUIDE_LINE, rx=3, layer="label", role="x", cls="keyitem")
            else:
                d.rect(x + 5, yy - 10, 32, 12, fill="#FFFFFF", stroke=col, sw=0.9, rx=3, layer="label", cls="keyitem")
            d.text(x + 21, yy - 0.8, word, size=9, weight=800, anchor="middle", color=col, halo=False, cls="keytxt")
            d.text(x + 41, yy, "= " + label, size=9.5, weight=600, halo=False, cls="keytxt")
        else:
            d.text(sx + 13, yy, label, size=9.5, weight=600, halo=False, cls="keytxt")
        yy += 14


# --------------------------------------------------------------------------
# Bulk transport
# --------------------------------------------------------------------------
def bulk(d, F):
    P = PAL

    # ===== PHAGOCYTOSIS (steps 1-4) + EXOCYTOSIS #2 (step 5: waste) =====
    d.text(100, 480, "PHAGOCYTOSIS", size=12.5, weight=800, color=P["hdr_bulk"])
    d.text(100, 492, "(“cell eating”: a bacterium)", size=10, color=P["hdr_bulk"])
    bacterium(d, PH_X, YB + 40, 48, 24)
    GEOM["touch"]["phago_bacterium"] = {"x": [PH_X - 24, PH_X + 24], "y": [YB + 28, YB + 52]}
    badge(d, 150, 711, 1)
    d.text(156, 732, "Pseudopods", size=10, weight=700, anchor="end")
    d.text(156, 743, "wrap around", size=9.5, anchor="end")
    d.text(156, 754, "the bacterium", size=9.5, anchor="end")
    GEOM["touch"]["phago_bacterium"]["cup"] = F["phago_cup"]
    d.text(PH_X, 796, "Bacterium", size=10, weight=700, anchor="middle")
    d.leader(PH_X, 786, PH_X, YB + 46)

    v2, r2 = (178, 600), 32
    dl_circle(d, *v2, r2, lumen=P["outside"])
    bacterium(d, v2[0], v2[1], 40, 19)
    badge(d, 138, 572, 2)
    d.text(135, 598, "Food", size=10, weight=700, anchor="end")
    d.text(135, 609, "vacuole", size=10, weight=700, anchor="end")
    d.arrow(f"M {PH_X - 4},{YB - 7} L {v2[0] + 14},{v2[1] + r2 + 7}", P["ink"], sw=1.4, name="phago_1_2")

    v3, r3 = (285, 525), 32
    ly, rl = (v3[0] + 30, v3[1] - 27), 16
    up = circle_union_path(v3, r3, ly, rl)
    d.path(up, fill=P["outside"], layer="band", role="tint")
    d.circle(*ly, rl - 5, fill=P["lyso"], layer="band", role="tint")
    d.path(up, stroke=P["ink"], sw=DL_W, layer="band", role="dl_outer")
    d.path(up, stroke=P["band"], sw=DL_W - 2 * DL_LINE, layer="band", role="dl_inner")
    bacterium(d, v3[0] - 5, v3[1] + 5, 38, 18)
    for ex, ey in ((ly[0] - 3, ly[1] - 4), (ly[0] + 5, ly[1] + 2), (ly[0] - 5, ly[1] + 5),
                   (v3[0] + 13, v3[1] - 11), (v3[0] + 19, v3[1] + 1), (v3[0] + 4, v3[1] - 17)):
        enzyme_dot(d, ex, ey)
    badge(d, 246, 487, 3)
    d.text(342, 489, "Lysosome fuses with", size=10, weight=700)
    d.text(342, 500, "food vacuole; hydrolytic", size=9.5)
    d.text(342, 511, "enzymes are released", size=9.5)
    d.leader(340, 494, ly[0] + rl + 2, ly[1] - 2)
    d.arrow(f"M {v2[0] + 22},{v2[1] - 30} L {v3[0] - 26},{v3[1] + 26}", P["ink"], sw=1.4, name="phago_2_3")
    GEOM["touch"]["lysosome_fusion"] = {"vacuole": v3, "r": r3, "lysosome": ly, "rl": rl,
                                        "overlap": round(r3 + rl - math.dist(v3, ly), 2), "inside_cell": True}

    v4, r4 = (352, 612), 28
    dl_circle(d, *v4, r4, lumen=P["outside"])
    for wx, wy in ((v4[0] - 8, v4[1] - 4), (v4[0] + 6, v4[1] + 7), (v4[0] - 1, v4[1] + 11)):
        waste_bit(d, wx, wy)
    enzyme_dot(d, v4[0] + 9, v4[1] - 9)
    enzyme_dot(d, v4[0] - 12, v4[1] + 8)
    for ang in (170, 215, 255, 295):
        a = math.radians(ang)
        x0, y0 = v4[0] + (r4 - 10) * math.cos(a), v4[1] + (r4 - 10) * math.sin(a)
        x1, y1 = v4[0] + (r4 + 17) * math.cos(a), v4[1] + (r4 + 17) * math.sin(a)
        d.circle(x0, y0, 2.6, fill=P["nutrient"], stroke=P["ink"], sw=0.4)
        d.arrow(f"M {x0 + 4 * math.cos(a):.1f},{y0 + 4 * math.sin(a):.1f} L {x1:.1f},{y1:.1f}", P["nutrient"], sw=1.2)
        d.circle(x1 + 4.5 * math.cos(a), y1 + 4.5 * math.sin(a), 2.6, fill=P["nutrient"], stroke=P["ink"], sw=0.4)
    badge(d, 399, 598, 4)
    d.text(296, 640, "Digestion:", size=10, weight=700, anchor="end")
    d.text(296, 651, "nutrients diffuse", size=9.5, anchor="end")
    d.text(296, 662, "into cytoplasm", size=9.5, anchor="end")
    d.arrow(f"M {v3[0] + 18},{v3[1] + 32} L {v4[0] - 14},{v4[1] - 33}", P["ink"], sw=1.4, name="phago_3_4")

    wc = F["waste"]
    d.circle(*wc, 15, fill=P["outside"], layer="band", role="tint")
    for wx, wy in ((wc[0] - 5, wc[1] - 4), (wc[0] + 5, wc[1] + 3), (WASTE_X + 4, YB + 16), (WASTE_X - 6, YB + 24)):
        waste_bit(d, wx, wy)
    d.arrow(f"M {WASTE_X + 14},{YB + 4} L {WASTE_X + 14},{YB + 28}", P["waste"], sw=1.4, name="waste_out")
    d.arrow(f"M {v4[0] + 16},{v4[1] + 30} L {wc[0] - 9},{wc[1] - 23}", P["ink"], sw=1.4, name="phago_4_5")
    badge(d, 428, 652, 5)
    d.text(WASTE_X, 735, "EXOCYTOSIS #2:", size=10.5, weight=800, anchor="middle", color=P["hdr_bulk"])
    d.text(WASTE_X, 747, "undigested waste", size=9.5, anchor="middle")
    d.text(WASTE_X, 758, "released outside", size=9.5, anchor="middle")
    GEOM["touch"]["waste_exocytosis"] = {"bulb": wc, "open_to": "outside"}
    GEOM.setdefault("steps", {})["phago"] = [YB + 40, v2[1], v3[1], v4[1], wc[1]]

    # ===== PINOCYTOSIS =====
    d.text(450, 548, "PINOCYTOSIS", size=12.5, weight=800, color=P["hdr_bulk"])
    d.text(450, 560, "(“cell drinking”)", size=10, color=P["hdr_bulk"])
    for p in scatter(71, 13, (446, YB + 10, 572, YB + 42), 9):
        fluid(d, *p)
    for p in ((PINO1_X - 5, YB - 11), (PINO1_X + 6, YB - 8), (PINO1_X, YB - 3)):
        fluid(d, *p)
    c2 = F["pino2"]
    d.circle(*c2, 16, fill=P["outside"], layer="band", role="tint")
    for p in ((c2[0] - 6, c2[1] - 4), (c2[0] + 6, c2[1] + 3), (c2[0] - 1, c2[1] + 9), (c2[0] + 3, c2[1] - 9)):
        fluid(d, *p)
    pv = (PINO2_X, 598)
    dl_circle(d, *pv, 19, lumen=P["outside"])
    for p in ((pv[0] - 6, pv[1] - 3), (pv[0] + 6, pv[1] + 4), (pv[0] + 1, pv[1] - 8), (pv[0] - 3, pv[1] + 8)):
        fluid(d, *p)
    badge(d, PINO1_X, 650, 1)
    badge(d, 582, c2[1] - 2, 2)
    badge(d, 582, pv[1] - 4, 3)
    d.arrow(f"M {PINO1_X + 14},{YB - 30} Q {PINO1_X + 28},{YB - 52} {PINO2_X - 28},{c2[1] - 4}", P["ink"], sw=1.3,
            name="pino_1_2")
    d.arrow(f"M {PINO2_X},{c2[1] - 28} L {PINO2_X},{pv[1] + 26}", P["ink"], sw=1.3, name="pino_2_3")
    GEOM.setdefault("steps", {})["pino"] = [YB - 22, c2[1], pv[1]]
    d.text(509, 760, "Extracellular fluid", size=10, weight=700, anchor="middle")
    d.text(509, 771, "(water + dissolved solutes)", size=9.5, anchor="middle")

    # ===== RECEPTOR-MEDIATED ENDOCYTOSIS =====
    d.text(612, 500, "RECEPTOR-MEDIATED", size=12.5, weight=800, color=P["hdr_bulk"])
    d.text(612, 513, "ENDOCYTOSIS (LDL)", size=12.5, weight=800, color=P["hdr_bulk"])
    pit = pit_points(RME1_X)
    for i, (px, py, nx, ny) in enumerate(pit):
        if i % 2 == 0:
            clathrin(d, px, py, -nx, -ny)
    for i in (3, 8, 13):
        receptor_ldl(d, *pit[i])
    c = F["rme2"]
    R2 = 27
    for ang in range(-56, 237, 21):
        a = math.radians(ang)
        clathrin(d, c[0] + R2 * math.cos(a), c[1] - R2 * math.sin(a), math.cos(a), -math.sin(a))
    for ang in (20, 90, 160):
        a = math.radians(ang)
        receptor_ldl(d, c[0] + R2 * math.cos(a), c[1] - R2 * math.sin(a), -math.cos(a), math.sin(a))
    rv = (RME2_X, 576)
    dl_circle(d, *rv, R2, lumen=P["outside"])
    for ang in range(0, 360, 20):
        a = math.radians(ang)
        clathrin(d, rv[0] + R2 * math.cos(a), rv[1] - R2 * math.sin(a), math.cos(a), -math.sin(a))
    for ang in (30, 150, 270):
        a = math.radians(ang)
        receptor_ldl(d, rv[0] + R2 * math.cos(a), rv[1] - R2 * math.sin(a), -math.cos(a), math.sin(a))
    badge(d, 598, 645, 1)
    badge(d, 778, 672, 2)
    badge(d, 678, 556, 3)
    d.arrow(f"M {RME1_X + 18},{YB - 44} Q {RME1_X + 32},{YB - 64} {RME2_X - 38},{c[1] - 16}", P["ink"], sw=1.3,
            name="rme_1_2")
    d.arrow(f"M {RME2_X + 40},{c[1] - 14} Q {RME2_X + 52},{c[1] - 38} {RME2_X + 40},{rv[1] + 20}", P["ink"], sw=1.3,
            name="rme_2_3")
    d.text(772, 561, "Clathrin-coated", size=10, weight=700)
    d.text(772, 572, "vesicle", size=10, weight=700)
    d.text(602, 611, "Clathrin coat", size=10, weight=700, anchor="middle", color="#E65100")
    d.text(602, 622, "(cytoplasm side)", size=9.5, anchor="middle", color="#E65100")
    d.leader(614, 627, 626, 652)
    d.text(636, 742, "LDL (carries", size=10, weight=700, anchor="middle")
    d.text(636, 753, "cholesterol)", size=10, weight=700, anchor="middle")
    d.leader(636, 732, pit[8][0] + pit[8][2] * 17.6, pit[8][1] + pit[8][3] * 17.6)
    d.text(690, 722, "LDL receptor", size=10, weight=700, color=P["receptor"])
    rp = pit[13]
    d.leader(692, 714, rp[0] + rp[2] * 9, rp[1] + rp[3] * 9)
    GEOM["steps"] = GEOM.get("steps", {})
    GEOM["steps"]["rme"] = [YB - 30, c[1], rv[1]]
    GEOM["touch"]["rme"] = {"pit_center_x": RME1_X, "deep_pit": c, "vesicle": rv,
                            "clathrin_side": "cytoplasm", "receptor_side": "outside/lumen"}

    # ===== EXOCYTOSIS #1 (hormones from the Golgi) =====
    gx, gy = 900, 512
    golgi(d, gx, gy)
    d.text(1018, 478, "EXOCYTOSIS #1", size=12.5, weight=800, anchor="end", color=P["hdr_bulk"])
    d.text(1018, 490, "(hormones from Golgi)", size=10, anchor="end", color=P["hdr_bulk"])
    d.text(944, 520, "Golgi", size=10, weight=700)
    d.text(944, 531, "apparatus", size=10, weight=700)
    b1 = (918, 566)
    dl_circle(d, *b1, 11, lumen=P["outside"])
    hormone_pack(d, *b1, 3)
    v2e = (872, 620)
    dl_circle(d, *v2e, 14, lumen=P["outside"])
    hormone_pack(d, *v2e, 4)
    c3 = F["exo3"]
    d.circle(*c3, 12, fill=P["outside"], layer="band", role="tint")
    hormone_pack(d, c3[0], c3[1] - 1, 3)
    for p in ((EXO3_X - 3, YB + 12), (EXO3_X + 5, YB + 21)):
        hormone(d, *p)
    for p in ((EXO4_X - 14, YB + 15), (EXO4_X - 2, YB + 27), (EXO4_X + 11, YB + 13), (EXO4_X + 19, YB + 29),
              (EXO4_X + 3, YB + 40), (EXO4_X - 13, YB + 35)):
        hormone(d, *p)
    d.arrow(f"M {EXO4_X},{YB - 6} L {EXO4_X},{YB + 23}", P["hormone"], sw=1.3, name="hormone_out")
    badge(d, 946, 576, 1)
    badge(d, 842, 603, 2)
    badge(d, 808, 664, 3)
    badge(d, 950, 668, 4)
    d.arrow(f"M {b1[0] - 9},{b1[1] + 11} L {v2e[0] + 10},{v2e[1] - 17}", P["ink"], sw=1.3, name="exo_1_2")
    d.arrow(f"M {v2e[0] - 9},{v2e[1] + 14} L {c3[0] + 6},{c3[1] - 19}", P["ink"], sw=1.3, name="exo_2_3")
    d.text(892, 620, "Secretory", size=9.5, weight=700)
    d.text(892, 631, "vesicle", size=9.5, weight=700)
    d.text(EXO4_X + 2, 760, "Hormones (proteins)", size=10, weight=700, anchor="middle", color=P["hormone"])
    d.text(EXO4_X + 2, 771, "released outside", size=10, weight=700, anchor="middle", color=P["hormone"])
    GEOM["touch"]["exocytosis1"] = {"golgi": (gx, gy), "fusing": c3, "open_to": "outside"}
    GEOM.setdefault("steps", {})["exo1"] = [b1[1], v2e[1], c3[1], YB]


def pit_points(cx):
    """Points along the coated pit centerline with unit normals pointing OUT of the cell (down)."""
    def cub(p0, p1, p2, p3, t):
        return tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * e
                     for a, b, c, e in zip(p0, p1, p2, p3))
    segs = [((cx - 38, YB), (cx - 20, YB), (cx - 22, YB - 30), (cx, YB - 30)),
            ((cx, YB - 30), (cx + 22, YB - 30), (cx + 20, YB), (cx + 38, YB))]
    pts = []
    for seg in segs:
        for k in range(9):
            t = 0.12 + k * 0.095
            p, q = cub(*seg, t), cub(*seg, min(1, t + 0.01))
            tx, ty = q[0] - p[0], q[1] - p[1]
            n = math.hypot(tx, ty)
            nx, ny = -ty / n, tx / n
            if ny < 0:
                nx, ny = -nx, -ny
            pts.append((p[0], p[1], nx, ny))
    return pts


def clathrin(d, px, py, nx, ny):
    """Clathrin bristle on the cytoplasmic face; (nx, ny) points into the cytoplasm."""
    x0, y0 = px + nx * (DL_W / 2 + 0.3), py + ny * (DL_W / 2 + 0.3)
    x1, y1 = px + nx * (DL_W / 2 + 6.5), py + ny * (DL_W / 2 + 6.5)
    tx, ty = -ny, nx
    GEOM["clathrin"].append([round(px, 2), round(py, 2), round(nx, 3), round(ny, 3)])
    d.line(x0, y0, x1, y1, PAL["clathrin"], 2.0, layer="deco")
    d.line(x1, y1, x1 + 2.2 * (nx + tx), y1 + 2.2 * (ny + ty), PAL["clathrin"], 1.4, layer="deco")
    d.line(x1, y1, x1 + 2.2 * (nx - tx), y1 + 2.2 * (ny - ty), PAL["clathrin"], 1.4, layer="deco")


def receptor_ldl(d, px, py, nx, ny):
    """LDL receptor on the extracellular face with LDL bound; (nx, ny) points away from the cytoplasm."""
    x0, y0 = px + nx * (DL_W / 2), py + ny * (DL_W / 2)
    x1, y1 = px + nx * (DL_W / 2 + 6), py + ny * (DL_W / 2 + 6)
    tx, ty = -ny, nx
    GEOM["receptors"].append([round(px, 2), round(py, 2), round(nx, 3), round(ny, 3)])
    d.line(x0, y0, x1, y1, PAL["receptor"], 1.8, layer="mol")
    d.line(x1, y1, x1 + 3.2 * (nx + tx), y1 + 3.2 * (ny + ty), PAL["receptor"], 1.6, layer="mol")
    d.line(x1, y1, x1 + 3.2 * (nx - tx), y1 + 3.2 * (ny - ty), PAL["receptor"], 1.6, layer="mol")
    lx, ly = x1 + nx * 6.6, y1 + ny * 6.6
    d.circle(lx, ly, 4.6, fill=PAL["ldl"], stroke=PAL["ink"], sw=0.7)
    d.circle(lx, ly, 1.3, fill=PAL["ink"])


def bacterium(d, cx, cy, w, h):
    d.path(rrect_path(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2), fill=PAL["bacteria"],
           stroke=PAL["ink"], sw=1.0, layer="mol")
    d.path(f"M {cx - w / 4},{cy} q {w / 16},{-h / 4} {w / 8},0 t {w / 8},0 t {w / 8},0 t {w / 8},0",
           stroke="#33691E", sw=1.0, layer="mol")


def enzyme_dot(d, x, y):
    r = 3.6
    c, s = math.cos(math.radians(30)), math.sin(math.radians(30))
    d.path(f"M {x},{y} L {x + r * c:.2f},{y - r * s:.2f} A {r},{r} 0 1 0 {x + r * c:.2f},{y + r * s:.2f} Z",
           fill=PAL["enz_dot"], stroke=PAL["ink"], sw=0.4, layer="mol")


def waste_bit(d, x, y):
    GEOM["particles"].append(["waste", round(x, 1), round(y, 1)])
    d.polygon([(x - 3.5, y - 1), (x - 1, y - 3.8), (x + 3.2, y - 2.2), (x + 3.6, y + 2), (x - 0.5, y + 3.4)],
              fill=PAL["waste"], stroke=PAL["ink"], sw=0.4)


def fluid(d, x, y):
    d.circle(x, y, 2.3, fill=PAL["fluid"], stroke=PAL["ink"], sw=0.35)


def hormone(d, x, y):
    GEOM["particles"].append(["hormone", round(x, 1), round(y, 1)])
    d.polygon([(x, y - 3.4), (x + 3.4, y), (x, y + 3.4), (x - 3.4, y)], fill=PAL["hormone"],
              stroke=PAL["ink"], sw=0.4)


def hormone_pack(d, cx, cy, n):
    for dx, dy in [(-4, -3), (4, 2), (-1, 5), (5, -5)][:n]:
        hormone(d, cx + dx, cy + dy)


def golgi(d, gx, gy):
    for w, dy in ((70, 0), (64, 13), (58, 26), (50, 39)):
        x0, x1, y = gx - w / 2, gx + w / 2, gy + dy
        dd = (f"M {x0},{y} Q {gx},{y - 16} {x1},{y} Q {x1 + 3},{y + 5} {x1 - 2},{y + 6} "
              f"Q {gx},{y - 9} {x0 + 2},{y + 6} Q {x0 - 3},{y + 5} {x0},{y} Z")
        d.path(dd, fill=PAL["golgi"], stroke=PAL["ink"], sw=1.0, layer="protein")


# --------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    for mode, fname, grid in (("guide", "membrane_guide.svg", False),
                              ("color", "membrane_color_grid.svg", True),
                              ("color", "membrane_color.svg", False)):
        d = draw(mode)
        with open(os.path.join(OUT, fname), "w") as f:
            f.write(d.svg(grid=grid))
    GEOM["constants"] = {"OUT_SURF": OUT_SURF, "IN_SURF": IN_SURF, "MID": MID, "YO": YO, "YI": YI,
                         "R_HEAD": R_HEAD, "TAIL_OUT": [TAIL_OUT0, TAIL_OUT1], "TAIL_IN": [TAIL_IN1, TAIL_IN0],
                         "YB": YB, "XL": XL, "XR": XR, "X_BIL": [X_BIL0, X_BIL1], "Y_TAPER": Y_TAPER,
                         "DL_W": DL_W}
    GEOM["palette"] = PAL
    with open(os.path.join(OUT, "geometry.json"), "w") as f:
        json.dump(GEOM, f, indent=1, default=list)
    print("ok")


if __name__ == "__main__":
    main()
