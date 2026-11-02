#!/usr/bin/env python3
"""
Checkpoint 3: science + geometry checks on the coordinates the generator actually drew.
Usage: python3 tools/check_geometry.py reference/geometry.json
Every check prints PASS or FAIL with the numbers it used.
"""
import json
import math
import re
import sys

g = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "reference/geometry.json"))
C = g["constants"]
OUT, IN, MID = C["OUT_SURF"], C["IN_SURF"], C["MID"]
YB = C["YB"]
results = []


def check(name, ok, detail):
    results.append((ok, name, detail))


# ---------------- phospholipids ----------------
pl = g["phospholipids"]
bad = [p for p in pl if not ((p["leaflet"] == "outer" and p["head_y"] == C["YO"] and p["tail_to"] > p["tail_from"] > p["head_y"])
                            or (p["leaflet"] == "inner" and p["head_y"] == C["YI"] and p["tail_to"] < p["tail_from"] < p["head_y"]))]
check("Phospholipids: heads face water, tails point to the middle", not bad,
      f"{len(pl)} phospholipids; outer heads y={C['YO']} tails go down, inner heads y={C['YI']} tails go up; wrong={len(bad)}")
outer_x = sorted(p["x"] for p in pl if p["leaflet"] == "outer")
inner_x = sorted(p["x"] for p in pl if p["leaflet"] == "inner")
check("Phospholipids: every outer one has an inner partner (no floating lipids)", outer_x == inner_x,
      f"{len(outer_x)} outer, {len(inner_x)} inner")

# no holes in the full bilayer: walk along x and look for gaps
items = [(x - C["R_HEAD"], x + C["R_HEAD"], "head") for x in outer_x]
items += [(p["x0"], p["x1"], n) for n, p in g["proteins"].items() if n not in ("peripheral",)]
items += [(c["x"] - 3, c["x"] + 3, "chol") for c in g["cholesterol"] if c["leaflet"] == "outer"]
items.sort()
gaps = []
reach = C["X_BIL"][0]
for a, b, n in items:
    if a - reach > 6:
        gaps.append((round(reach, 1), round(a, 1)))
    reach = max(reach, b)
if C["X_BIL"][1] - reach > 6:
    gaps.append((round(reach, 1), C["X_BIL"][1]))
check("Full bilayer has no holes from x=130 to x=970", not gaps, f"gaps wider than 6 units (1.5 mm): {gaps}")

# ---------------- integral proteins span the bilayer ----------------
for n, p in g["proteins"].items():
    if n == "peripheral":
        continue
    ok = p["top"] < OUT and p["bottom"] > IN
    check(f"Integral protein '{n}' spans the bilayer", ok,
          f"top={p['top']:.1f} < outer surface {OUT} and bottom={p['bottom']:.1f} > inner surface {IN}")
    hits = [x for x in outer_x if x + C["R_HEAD"] > p["x0"] + 0.5 and x - C["R_HEAD"] < p["x1"] - 0.5]
    check(f"No phospholipid drawn inside '{n}'", not hits, f"overlapping heads: {hits}")

# ---------------- peripheral protein ----------------
pp = g["proteins"]["peripheral"]
t = g["touch"]["peripheral"]
check("Peripheral protein touches the inner surface (not floating, not buried)",
      IN - 3 <= pp["top"] <= IN and pp["bottom"] > IN and t["heads_above"],
      f"top={pp['top']:.1f}, inner surface={IN}, heads directly above at x={t['heads_above']}")

# ---------------- cholesterol ----------------
bad = []
for c in g["cholesterol"]:
    lo, hi = (C["TAIL_OUT"][0] - 3, C["TAIL_OUT"][1]) if c["leaflet"] == "outer" else (C["TAIL_IN"][0], C["TAIL_IN"][1] + 3)
    if not (lo <= c["body"][0] and c["body"][1] <= hi):
        bad.append(c)
    left = max([x for x in outer_x if x < c["x"]], default=None)
    right = min([x for x in outer_x if x > c["x"]], default=None)
    if left is None or right is None or not (left < c["x"] < right):
        bad.append(c)
check("Cholesterol sits between phospholipid tails inside the bilayer", not bad,
      f"{len(g['cholesterol'])} cholesterol (pairs in both leaflets); misplaced={len(bad)}")

# ---------------- sugar chains ----------------
gp = g["touch"]["glycoprotein_chain"]
check("Glycoprotein chain is attached and on the outside face",
      gp["side"] == "outside" and gp["chain_top"] < OUT and abs(gp["bead0_bottom"] - gp["protein_top"]) <= 1.0,
      f"first sugar bottom={gp['bead0_bottom']} vs protein top={gp['protein_top']} (joined by a stem line); top of chain y={gp['chain_top']}")
gl = g["touch"]["glycolipid_chain"]
check("Glycolipid chain is attached to an outer-leaflet lipid head, outside only",
      gl["leaflet"] == "outer" and abs(gl["bead0_bottom"] - gl["head_top"]) <= 1.0 and gl["x"] in outer_x,
      f"first sugar bottom={gl['bead0_bottom']} vs head top={gl['head_top']} at x={gl['x']}")

# ---------------- integrin + ECM + microfilaments ----------------
f = g["touch"]["integrin_fibronectin_collagen"]
check("Integrin touches fibronectin, which touches a collagen fiber (outside)",
      f["fibronectin_bottom"] > f["head_top"] and f["fibronectin_top"] <= f["collagen_strand_y_at_end"] + 1.2,
      f"head top={f['head_top']}, fibronectin runs y={f['fibronectin_bottom']:.1f} to {f['fibronectin_top']:.1f}, "
      f"collagen strand at y={f['collagen_strand_y_at_end']:.1f}")
a = g["touch"]["integrin_actin"]
check("Integrin touches the actin microfilament (inside)", a["leg_bottom"] >= a["actin_top"] and a["actin_top"] > IN,
      f"integrin legs end y={a['leg_bottom']}, actin beads start y={a['actin_top']}, inner surface={IN}")

# ---------------- enzyme ----------------
e = g["enzyme"]
check("Enzyme shows substrate in and products out on one (cytoplasm) side",
      "enzyme_in" in g["arrows"] and "enzyme_out1" in g["arrows"] and "enzyme_out2" in g["arrows"]
      and e["active_site_bottom"] > IN,
      f"active site at y={e['active_site_bottom']} (below inner surface {IN}); substrate={e['substrate']}, products={e['products']}")


# ---------------- transport arrows ----------------
def ends(dpath):
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", dpath)]
    return (nums[0], nums[1]), (nums[-2], nums[-1])


def direction(name):
    (x0, y0), (x1, y1) = ends(g["arrows"][name])
    return ("in" if y1 > y0 else "out"), x0, y0, y1


expect = {"o2": "in", "k_channel": "out", "nak_na": "out", "nak_k": "in", "co_na": "in", "co_glucose": "in",
          "proton_pump": "out"}
for n, want in expect.items():
    got, x, y0, y1 = direction(n)
    crosses = min(y0, y1) < OUT and max(y0, y1) > IN
    check(f"Arrow '{n}' points {want} and crosses the whole bilayer", got == want and crosses,
          f"x={x}, y {y0:.0f} -> {y1:.0f}")
_, ox, _, _ = direction("o2")
inside_protein = [n for n, p in g["proteins"].items() if p["x0"] <= ox <= p["x1"]]
check("Simple diffusion arrow goes through lipids, not a protein", not inside_protein, f"x={ox}, proteins there: {inside_protein}")
_, kx, _, _ = direction("k_channel")
pore = g["proteins"]["k_channel"]["pore"]
check("Channel arrow goes through the channel pore", pore[0] < kx < pore[1], f"arrow x={kx}, pore x={pore}")


# ---------------- concentration gradients (count the dots that were drawn) ----------------
def count(kind, x0, x1):
    pts = [p for p in g["particles"] if p[0] == kind and x0 <= p[1] <= x1]
    return sum(1 for p in pts if p[2] < OUT), sum(1 for p in pts if p[2] > IN)


zones = {"simple": (425, 520), "channel": (515, 612), "nak": (612, 722), "co": (722, 836), "proton": (836, 935)}
rows = [("O2 high outside (simple diffusion)", "o2", "simple", "out"),
        ("K+ high inside (channel)", "k", "channel", "in"),
        ("K+ high inside (Na+/K+ pump)", "k", "nak", "in"),
        ("Na+ high outside (Na+/K+ pump)", "na", "nak", "out"),
        ("Na+ high outside (cotransporter)", "na", "co", "out"),
        ("Glucose high inside (cotransporter)", "glucose", "co", "in"),
        ("H+ high outside (proton pump)", "h", "proton", "out")]
for label, kind, z, high in rows:
    o, i = count(kind, *zones[z])
    ok = (o > i) if high == "out" else (i > o)
    check(f"Gradient: {label}", ok and min(o, i) >= 1, f"outside={o}, inside={i}")
check("Same ion, same gradient everywhere: Na+ high outside at pump AND cotransporter; K+ high inside at channel AND pump",
      all(r[0] for r in results if r[1].startswith("Gradient: Na+") or r[1].startswith("Gradient: K+")), "see the 4 lines above")

# pumps move substances against the gradient, passive ones move with it
check("Pumps move ions low -> high (Na+ out, K+ in, H+ out); channel and simple diffusion move high -> low",
      direction("nak_na")[0] == "out" and direction("nak_k")[0] == "in" and direction("proton_pump")[0] == "out"
      and direction("k_channel")[0] == "out" and direction("o2")[0] == "in",
      "Na+ high outside & pumped out; K+ high inside & pumped in; H+ high outside & pumped out; "
      "K+ high inside & leaks out; O2 high outside & diffuses in")
check("Cotransport: Na+ moves down its gradient while glucose moves against its gradient",
      direction("co_na")[0] == "in" and direction("co_glucose")[0] == "in", "both enter; Na+ high->low, glucose low->high")

# ---------------- ATP ----------------
atp = g.get("atp", [])
check("ATP -> ADP is drawn on the cytoplasm side of both pumps (and not at the cotransporter)",
      len(atp) == 2 and all(a["side"] == "inside" for a in atp) and not any(722 <= a["x"] <= 836 for a in atp),
      f"{atp}")
ph = g.get("phosphates", [])
pumps = [g["proteins"]["na_k_pump"], g["proteins"]["proton_pump"]]
ok = len(ph) == 2 and all(any(p["x0"] - 2 <= q["x"] <= p["x1"] + 2 and p["bottom"] - 8 <= q["y"] <= p["bottom"] + 2 and q["y"] > IN
                                  for p in pumps) for q in ph)
check("Phosphate from ATP is attached to each pump on the cytoplasm side", ok, f"{ph}")

# ---------------- clathrin + receptors ----------------
rme = g["touch"]["rme"]
bad_c, bad_r = 0, 0
for px, py, nx, ny in g["clathrin"]:
    for cen in (rme["deep_pit"], rme["vesicle"]):
        if abs(math.dist((px, py), cen) - 27) < 0.6:
            radial = ((px - cen[0]) * nx + (py - cen[1]) * ny) > 0
            bad_c += 0 if radial else 1
            break
    else:
        bad_c += 0 if ny < 0 else 1          # shallow pit: cytoplasm is above
for px, py, nx, ny in g["receptors"]:
    for cen in (rme["deep_pit"], rme["vesicle"]):
        if abs(math.dist((px, py), cen) - 27) < 0.6:
            inward = ((px - cen[0]) * nx + (py - cen[1]) * ny) < 0
            bad_r += 0 if inward else 1
            break
    else:
        bad_r += 0 if ny > 0 else 1          # shallow pit: outside is below
check("Clathrin is on the cytoplasm side of the pit, deep pit and coated vesicle", bad_c == 0,
      f"{len(g['clathrin'])} clathrin bristles, wrong side={bad_c}")
check("LDL receptors (with LDL bound) face the outside / vesicle interior", bad_r == 0,
      f"{len(g['receptors'])} receptors, wrong side={bad_r}")

# ---------------- bulk transport ----------------
lf = g["touch"]["lysosome_fusion"]
check("Lysosome is fused with the food vacuole inside the cell", lf["overlap"] > 0 and IN < lf["vacuole"][1] < YB,
      f"circles overlap by {lf['overlap']} units; vacuole center y={lf['vacuole'][1]}")
st = g["steps"]
check("Pinocytosis steps move outside -> inside (y decreases)", st["pino"][0] > st["pino"][1] - 21 > st["pino"][2],
      f"dip top {st['pino'][0]}, pocket top {st['pino'][1] - 21:.0f}, vesicle center {st['pino'][2]}")
check("Receptor-mediated steps move outside -> inside", st["rme"][0] > st["rme"][1] - 27 > st["rme"][2],
      f"pit top {st['rme'][0]}, deep pit top {st['rme'][1] - 27:.0f}, vesicle center {st['rme'][2]}")
check("Phagocytosis starts outside and the food vacuole moves inside", st["phago"][0] > YB > st["phago"][1],
      f"bacterium y={st['phago'][0]} (outside, below membrane y={YB}), food vacuole y={st['phago'][1]}")
check("Exocytosis #1 steps move inside -> outside (y increases)",
      st["exo1"][0] < st["exo1"][1] < st["exo1"][2] < st["exo1"][3], f"{[round(v) for v in st['exo1']]}")
hor_out = [p for p in g["particles"] if p[0] == "hormone" and p[2] > YB + 5]
waste_out = [p for p in g["particles"] if p[0] == "waste" and p[2] > YB + 5]
check("Exocytosis releases hormones and waste OUTSIDE the cell", len(hor_out) >= 3 and len(waste_out) >= 2,
      f"hormone pieces outside={len(hor_out)}, waste pieces outside={len(waste_out)}")
cup = g["touch"]["phago_bacterium"]
check("Pseudopods wrap around the bacterium (arms reach below it)",
      cup["cup"]["outer_bottom"] > cup["y"][1] and cup["cup"]["inner_x"][0] < cup["x"][0] and cup["cup"]["inner_x"][1] > cup["x"][1],
      f"bacterium x={cup['x']}, y={cup['y']}; pseudopod arms x={cup['cup']['inner_x']}, reach y={cup['cup']['outer_bottom']}")

# ---------------- membrane continuity ----------------
tl, tr = g["touch"]["taper_left"], g["touch"]["taper_right"]
ok = (abs(tl["end_outer"][0] - (C["XL"] - 4.2)) < 0.05 and abs(tl["end_outer"][1] - C["Y_TAPER"]) < 0.05
      and abs(tr["end_outer"][0] - (C["XR"] + 4.2)) < 0.05 and abs(tl["start_outer"][0] - C["X_BIL"][0]) < 0.05)
check("Plasma membrane is one continuous loop (bilayer -> corner -> sides -> bottom -> corner -> bilayer)", ok,
      f"left corner ends at {tl['end_outer']}, right corner ends at {tr['end_outer']}, side walls start at y={C['Y_TAPER']}")

# ---------------- outside / inside labels ----------------
labs = g["labels"]
outs = [l for l in labs if l["text"].startswith("OUTSIDE")]
ins = [l for l in labs if l["text"].startswith("INSIDE")]
ok = all(l["y"] < OUT - 20 or l["y"] > YB + 10 for l in outs) and all(IN < l["y"] < YB and C["XL"] < l["x"] < C["XR"] for l in ins)
check("OUTSIDE labels are outside the cell and the INSIDE label is in the cytoplasm", ok and outs and ins,
      f"outside labels at y={[l['y'] for l in outs]}, inside label at y={[l['y'] for l in ins]}")

# ---------------- report ----------------
fails = [r for r in results if not r[0]]
for ok, name, detail in results:
    print(("PASS " if ok else "FAIL ") + name + "\n     " + detail)
print(f"\n{len(results) - len(fails)}/{len(results)} checks passed")
sys.exit(1 if fails else 0)
