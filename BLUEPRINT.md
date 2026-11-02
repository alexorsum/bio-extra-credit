# Plasma Membrane Bonus: Drawing Blueprint (target 40/40)

This is the full plan for drawing the plasma membrane in GoodNotes on one US Letter page.
Every example comes from your class notes (Unit 3: 3.3 Plasma Membrane, 3.5 Endomembrane System,
3.6 ECM/Cytoskeleton, 3.7 Membrane Transport). The only exceptions are three things the rubric
demands but your notes do not cover. They are flagged in section 1.

**Files (all in this repo)**

| File | What it is | Use it for |
|---|---|---|
| `reference/membrane_color.png` / `.pdf` | (a) Full-color finished reference | Look at this while you draw |
| `reference/membrane_color_grid.png` / `.pdf` | (b) Same, with a 1-inch grid, inch numbers on the edges, and the 0.4" safe margin (red dashes) | Measuring where things go |
| `reference/membrane_guide.pdf` / `.png` | (c) Very light gray outline-only guide | Import into GoodNotes and draw on top |
| `reference/*.svg` | Source drawings (viewBox 0 0 1100 850, 100 units = 1 inch) | Only if you want to edit |
| `tools/` | The scripts that drew the page and ran every self-check | Proof of the checks below |

All PDFs are exactly one landscape US Letter page (11" x 8.5", 792 x 612 pt). All PNGs are 3300 x 2550 px (300 dpi).

---

## 1. Science plan

### 1a. Every rubric item, the example used, and the gradient

"Outside" = extracellular fluid. "Inside" = cytoplasm.

**Part 1: membrane components** (no concentration gradient involved)

| Rubric item | Example on the drawing | In your notes? |
|---|---|---|
| Phospholipids | Phospholipid bilayer: pink hydrophilic heads face the water on both sides, hydrophobic tails point to the middle (one tail straight = saturated, one kinked = unsaturated) | Yes (3.3) |
| Cholesterol | Yellow cholesterol wedged between the tails, in both layers (keeps the membrane from getting too rigid or too loose; animal cells only) | Yes (3.3) |
| Glycoprotein | Integral protein with a green sugar chain on the outside face ("cell ID card", cell-to-cell recognition) | Yes (3.3) |
| Glycolipid | One outer-layer phospholipid with a green sugar chain on the outside face | Yes (3.3 matching) |
| Peripheral protein | Protein resting on the cytoplasm side of the inner heads, not embedded | Yes (3.3) |
| Integral protein (a): enzyme with substrates and products | Transmembrane enzyme with its active site on the cytoplasm side. Substrate (yellow triangle) goes in, products (orange circle + green square) come out. It speeds up the reaction | Yes ("enzymatic activity" figure) |
| Integral protein (b): attachment protein | Integrin. Outside: fibronectin links it to collagen fibers. Inside: microfilaments attach to it | Yes (3.6) |
| Fibers of the extracellular matrix | Collagen fibers + fibronectin | Yes (3.6) |
| Cytoskeleton microfilaments | Microfilaments (actin) running along the inside of the membrane, attached to the integrin | Yes (3.6) |

**Part 2: transport**

| Rubric item | Example on the drawing | High side | Low side | Direction moved | Energy source | In your notes? |
|---|---|---|---|---|---|---|
| Simple diffusion | **O₂** through the lipids | Outside | Inside | In (high → low) | None (passive) | Yes (notes list O₂, CO₂, steroids) |
| Facilitated diffusion through a channel | **K⁺** through a K⁺ channel protein | Inside | Outside | Out (high → low), through the channel | None (passive) | Yes (channels carry ions) |
| Active transport pump #1 | **Na⁺/K⁺ pump** | Na⁺: outside. K⁺: inside | Na⁺: inside. K⁺: outside | Na⁺ out, K⁺ in (both low → high) | **ATP**: the pump takes a phosphate from ATP (ATP → ADP) on the cytoplasm side | Yes ("salty banana") |
| Active transport pump #2 | **Proton (H⁺) pump** | Outside (acidic, lower pH) | Inside | H⁺ out (low → high) | **ATP** (phosphorylation, cytoplasm side) | Yes |
| Cotransport | **Na⁺/glucose cotransporter** | Na⁺: outside. Glucose: inside | Na⁺: inside. Glucose: outside | Both go in. Na⁺ moves down its gradient (high → low) and that powers glucose against its gradient (low → high) | **The Na⁺ gradient made by the Na⁺/K⁺ pump** (secondary active transport, so ATP is used indirectly). No ATP at the cotransporter itself | Yes (exact notes example) |
| Phagocytosis | **A bacterium** engulfed by pseudopods → food vacuole → lysosome fuses and releases hydrolytic enzymes → nutrients diffuse out | (bulk) | (bulk) | In | Energy to make and move vesicles | Yes |
| Pinocytosis | **Extracellular fluid** (water + dissolved solutes) | (bulk) | (bulk) | In | Energy | Yes ("ingesting liquid") |
| Receptor-mediated endocytosis | **LDL** (carries cholesterol) bound to LDL receptors in a clathrin-coated pit | (bulk) | (bulk) | In | Energy | **No** (see 1c) |
| Exocytosis #1 | **Hormones** (proteins) in a secretory vesicle from the Golgi | (bulk) | (bulk) | Out | Energy | Yes (notes list hormones, digestive enzymes, antibodies, growth factors) |
| Exocytosis #2 | **Undigested waste** from the food vacuole after the lysosome digested the bacterium | (bulk) | (bulk) | Out | Energy | Yes (rubric hint) |

Bulk transport moves big batches in vesicles, so it is not drawn with a concentration gradient (your notes: "Energy is required to create and move vesicles").

### 1b. One gradient per substance, used the same way everywhere

| Substance | Outside | Inside | Where it shows up |
|---|---|---|---|
| Na⁺ | HIGH | LOW | Na⁺/K⁺ pump zone **and** cotransporter zone |
| K⁺ | LOW | HIGH | K⁺ channel zone **and** Na⁺/K⁺ pump zone |
| H⁺ | HIGH (acidic) | LOW | Proton pump zone |
| O₂ | HIGH | LOW | Simple diffusion zone |
| Glucose | LOW | HIGH | Cotransporter zone |

The story the drawing tells: the Na⁺/K⁺ pump (center) builds the Na⁺ and K⁺ gradients. The K⁺ channel on its left lets K⁺ leak back out. The cotransporter on its right uses the Na⁺ gradient to pull glucose in. That is why those three sit side by side.

### 1c. Checked against your class notes

Changed from my first draft so nothing is outside your notes:

| First draft | Now | Why |
|---|---|---|
| Ca²⁺ pump | Proton (H⁺) pump | Your notes teach exactly two pumps: Na⁺/K⁺ and proton. Note: your notes say proton pumps are "common in plants, fungi, bacteria". It is still the second pump your teacher taught, so it is the safe choice. If your teacher wants animal-only pumps, ask before you draw it |
| Lactase (lactose → glucose + galactose) | Unnamed enzyme: substrate (triangle) → products (circle + square), active site on the cytoplasm side | Matches the "enzymatic activity" figure in your notes. The rubric only asks for "enzyme with substrates and products" |
| Insulin | Hormones (proteins) | Your notes' list of secreted proteins: hormones, digestive enzymes, antibodies, growth factors. Optional: if you learned insulin somewhere, you may write "Hormones (ex. insulin)" |
| "Symport" | "Secondary active transport" | Your notes' wording |
| "3 Na⁺ out, 2 K⁺ in" | "Na⁺ out, K⁺ in" | The 3:2 ratio is not in your notes |
| Integrin touching collagen directly | Integrin → fibronectin → collagen | Your notes: "Fibronectin molecules act as bridges between integrins and ... collagen" |
| "Actin microfilaments", "Pseudopodia" | "Microfilaments (actin)", "Pseudopods" | Your notes' wording |

**In the rubric but NOT in your notes** (kept, because the rubric gives points for them):
- Receptor-mediated endocytosis (3 pts) and its "clathrin coating inside". Your notes only show phagocytosis and pinocytosis.
- A "specific example of target molecule" for it. I used **LDL**, the standard textbook example. LDL particles carry cholesterol, which you did learn.

### Checkpoint 1 (science), result: PASS

- [x] Every rubric bullet has a specific named example (table 1a). The enzyme is unnamed on purpose, to match your notes, and the rubric does not ask for a name.
- [x] Same ion, same gradient everywhere: Na⁺ is HIGH outside at both the pump and the cotransporter. K⁺ is HIGH inside at both the channel and the pump.
- [x] Pumps move substances low → high and use ATP (Na⁺ out, K⁺ in, H⁺ out). Simple diffusion (O₂ in) and the channel (K⁺ out) move high → low with no ATP.
- [x] Cotransport: Na⁺ moves down its gradient and powers glucose up its gradient. Energy is named as the Na⁺ gradient from the pump (ATP indirectly).
- [x] The two pumps are truly different: Na⁺/K⁺ pump (two ions, opposite directions) and proton pump (one ion, one direction).
- [x] Exocytosis has two different examples: hormones in a vesicle from the Golgi, and waste from the digested food vacuole.
- Mistakes caught here: the Ca²⁺ pump, lactase, insulin, "symport", and the 3:2 ratio were not in your notes. All were replaced (table 1c). In draft 1, the cotransporter showed only glucose tags. It now shows HIGH/LOW for both Na⁺ and glucose, as the rubric needs ("concentration gradients of both molecules").

---

## 2. Layout plan

### 2a. Orientation and shape

**Landscape, one big rounded-rectangle cell that fills the page.**

- **Why landscape:** the full phospholipid bilayer needs one long straight run, 8.4" here. It holds 7 proteins, cholesterol, the sugar chains, and the 5 protein-transport zones with their HIGH/LOW dots. Straight rows also make copy-pasting phospholipids fast and exact. Portrait would give only about 6".
- **Why a whole cell:** the teacher asked for "one continuous plasma membrane **of a cell**". A closed outline makes outside vs inside obvious everywhere. The outside is the band above the cell, the band below it, and thin strips on the sides. The inside is the big middle.
- **Top edge = full bilayer:** all membrane parts and all protein transport.
- **Sides + bottom = simplified double line:** all bulk transport. Endocytosis pockets push **up** into the cell, and exocytosis vesicles open **down** to the outside.

### 2b. Key measurements (inches from the top-left corner of the landscape page)

| Thing | Where |
|---|---|
| Safe margin | Nothing closer than 0.4" to any edge (checked: everything is inside x 0.40 to 10.60, y 0.40 to 8.10) |
| Full bilayer, straight part | x 1.30 to 9.70 |
| Outer surface (top of outer heads) | y 2.605 |
| Middle of bilayer | y 2.915 |
| Inner surface (bottom of inner heads) | y 3.225 |
| Phospholipid size | head 0.13" (3.3 mm) wide, tails 0.17" (4.3 mm), heads 0.14" apart |
| Top corners | The yellow tail band bends down (radius 0.60") and narrows into the double line, reaching the side walls at y 3.515 |
| Side walls (double line center) | x 0.70 (left) and x 10.30 (right), from y 3.515 to 6.20 |
| Bottom corners | radius 0.70" |
| Bottom membrane (double line center) | y 6.90, from x 1.40 to 9.60 |
| Double line | two thin lines, whole band 0.10" (2.5 mm) wide |

### 2c. Zones

Label positions give the text baseline (y) and where the text starts (x), unless it says "centered". The grid version (b) shows everything exactly.


| # | Zone | x (in) | y (in) | Contents |
|---|---|---|---|---|
| T | Title + name | 2.79 to 8.21; name line ends at 10.58 | 0.43 to 0.72 | Title centered at x 5.50 |
| 1 | Outside label | 0.80 to 1.98 | 0.87 to 1.14 | OUTSIDE THE CELL (extracellular fluid) |
| 2 | ECM + integrin + microfilaments | 0.50 to 2.00 | 1.30 to 4.65 | Collagen fibers y 1.80 to 2.05 (x 0.50 to 1.76). Fibronectin at x 1.63 from y 2.02 down to 2.27. Integrin legs x 1.51 to 1.75, head x 1.46 to 1.80, spanning y 2.27 to 3.44. Microfilament beads along y 3.47 from x 1.03 to 2.42, then down the left wall at x 0.86 to y 4.64 |
| 3 | Glycoprotein | 1.94 to 2.22 | 2.11 to 3.36 | Sugar chain on top. Label centered at (2.26, 1.82) |
| 4 | Cholesterol pair #1 | 2.45 | in the tails | Labeled from below at (2.05, 3.86) |
| 5 | Glycolipid | 2.70 | chain 2.39 to 2.60 | Label at (2.40, 2.14) |
| 6 | Peripheral protein | 2.85 to 3.25 | 3.21 to 3.39 | Label centered at (3.09, 4.20) |
| 7 | Enzyme | 3.49 to 3.95 | 2.47 to 3.42 | Active site on the bottom. Substrate at (3.43, 3.74), products at (4.04, 3.80) and (4.15, 3.61). Label "Enzyme" centered at (3.74, 2.14) |
| 8 | Simple diffusion (O₂) | 4.25 to 5.15 | 0.82 to 4.55 | Arrow down at x 4.72 |
| 9 | Facilitated diffusion (K⁺ channel) | 5.15 to 6.12 | 0.82 to 4.55 | Channel x 5.39 to 5.87, pore 5.56 to 5.70, arrow up at x 5.63 |
| 10 | Active transport #1 (Na⁺/K⁺ pump) | 6.12 to 7.22 | 0.82 to 4.55 | Pump x 6.35 to 6.97. Na⁺ arrow up at x 6.52, K⁺ arrow down at x 6.80. ATP at x 6.28, y 3.56 to 3.80 |
| 11 | Cotransport (Na⁺/glucose) | 7.22 to 8.36 | 0.82 to 4.65 | Protein x 7.53 to 8.03. Na⁺ arrow down at x 7.67, glucose arrow down at x 7.89 |
| 12 | Active transport #2 (proton pump) | 8.36 to 9.35 | 0.82 to 4.55 | Pump x 8.61 to 9.07. H⁺ arrow up at x 8.84. ATP at x 9.20, y 3.56 to 3.80 |
| 13 | KEY | 9.44 to 10.58 | 0.82 to 2.42 | Symbol key |
| 14 | Phospholipid label | 9.40 to 10.21 | 3.93 to 4.30 | Points to an inner head at x 9.49 |
| 15 | Energy notes row | 4.25 to 9.35 | 4.31 to 4.63 | One note under each transport zone |
| 16 | INSIDE label | 4.66 to 6.54 | 4.64 to 4.80 | INSIDE THE CELL (cytoplasm) |
| 17 | Phagocytosis + exocytosis #2 | 0.80 to 4.45 | 4.68 to 7.98 | Header at (1.00, 4.80). Step 1: pseudopods hang below the membrane around the bacterium at (2.15, 7.30), arms to y 7.73. Step 2: food vacuole center (1.78, 6.00), radius 0.32. Step 3: vacuole (2.85, 5.25), radius 0.32, fused with lysosome (3.15, 4.98), radius 0.16. Step 4: digesting vacuole (3.52, 6.12), radius 0.28. Step 5: waste pocket open to the outside at x 3.95 |
| 18 | Pinocytosis | 4.40 to 5.90 | 5.38 to 7.75 | Step 1 dip at x 4.70. Step 2 deep pocket at x 5.45. Step 3 vesicle (5.45, 5.98), radius 0.19 |
| 19 | Receptor-mediated endocytosis | 5.90 to 7.95 | 4.90 to 7.55 | Step 1 coated pit at x 6.40. Step 2 deep coated pit at x 7.28. Step 3 coated vesicle (7.28, 5.76), radius 0.27 |
| 20 | Exocytosis #1 | 8.00 to 10.20 | 4.68 to 7.75 | Header right-aligned to x 10.18 at y 4.78. Golgi (4 sacs) centered x 9.00, y 5.04 to 5.57. Step 1 bud (9.18, 5.66). Step 2 secretory vesicle (8.72, 6.20). Step 3 fusing pocket at x 8.42. Step 4 opened at x 9.15, hormones below |
| 21 | Bottom outside label | 5.80 to 8.20 | 7.90 to 8.05 | OUTSIDE THE CELL (extracellular fluid) |

### 2d. Full bilayer vs double line

- **Full phospholipid bilayer** (top edge, x 1.30 to 9.70): phospholipids, cholesterol, glycoprotein, glycolipid, peripheral protein, enzyme, integrin, simple diffusion, K⁺ channel, Na⁺/K⁺ pump, cotransporter, proton pump.
- **Double line** (corners, side walls, bottom, and every vesicle, vacuole and lysosome): phagocytosis, pinocytosis, receptor-mediated endocytosis, exocytosis #1 and #2. The Golgi is drawn as 4 filled sacs.

### Checkpoint 2 (layout), result: PASS

- [x] The plasma membrane is one unbroken loop: bilayer → left corner → left wall → bottom (with every pocket) → right wall → right corner → bilayer. Pinched-off vesicles are separate circles. Checked by script (corner ends meet the walls exactly at x 0.658 / 10.342, y 3.515).
- [x] Outside is always above the top bilayer, below the bottom membrane and beside the walls. Inside is always the middle. Labels: OUTSIDE at the top-left and bottom, INSIDE in the middle (checked by script).
- [x] Everything is at least 0.4" from the edges, and no label touches another label or a drawn structure (layout audit: 0 problems).
- [x] Endocytosis steps move up into the cell (pinocytosis: dip top y 6.68 → pocket top 6.44 → vesicle 5.98; receptor-mediated: 6.60 → 6.32 → 5.76). Exocytosis steps move down and out (Golgi bud 5.66 → vesicle 6.20 → fusing 6.71 → open at 6.90). Every step is numbered.
- [x] There is room inside for the food vacuole loop, lysosome fusion, Golgi, vesicles, and microfilaments (zones 2 and 17 to 20 do not overlap).
- Mistakes caught here: in draft 1, the bottom "OUTSIDE" label sat at y 8.32", inside the bottom margin. It moved to 8.01". Draft 1 also had a big empty middle and a crowded top. The bilayer moved down 0.45" and the bottom membrane moved up 0.22".

---

## 3. Reference images

Built as SVG with viewBox `0 0 1100 850` (landscape, 100 units = 1 inch), then converted with headless Chromium to:
- PNG at **300 dpi** (3300 x 2550 px)
- PDF at exactly **11" x 8.5"** (792 x 612 pt), one page, vector

The three versions:
- (a) `membrane_color` = finished color reference
- (b) `membrane_color_grid` = the same with a 1-inch grid (dashed half-inch lines, inch numbers on all four edges) and the 0.4" margin in red dashes
- (c) `membrane_guide` = light gray (#C4C4C4) outlines only, no fills, labels in gray where they go

### Checkpoint 3 (drawing), result: PASS

Checked with the actual coordinates (`tools/check_geometry.py`, 56/56 pass) and with an image-based label audit (`tools/audit_layout.py`, 0 problems). I also looked at the rendered images.

- [x] Phospholipids: all 68 have heads facing water and tails toward the middle. Outer heads at y 2.67, tails going down. Inner heads at y 3.16, tails going up. Every outer one has an inner partner, and no gap in the bilayer is wider than 1.5 mm.
- [x] Every integral protein spans the bilayer:
  - integrin: 2.27 to 3.44
  - glycoprotein: 2.47 to 3.36
  - enzyme: 2.47 to 3.42
  - K⁺ channel: 2.47 to 3.36
  - Na⁺/K⁺ pump: 2.43 to 3.41
  - cotransporter: 2.47 to 3.36
  - proton pump: 2.45 to 3.39

  All tops are above 2.605 (outer surface) and all bottoms are below 3.225 (inner surface).
- [x] Peripheral protein: top at y 3.21, touching the inner heads (inner surface 3.225). It is not floating and not in the tails.
- [x] Cholesterol: 3 pairs (x 2.45, 5.15, 9.385). Each sits between two phospholipids, with its body inside the tail zone.
- [x] Sugar chains are attached (first sugar touches the protein top / lipid head) and are on the outside face only.
- [x] Integrin → fibronectin → collagen touch on the outside. Integrin legs (end y 3.435) overlap the microfilament beads (start y 3.425) on the inside.
- [x] Enzyme: the substrate arrow goes into the active site and the product arrows come out. Both are on the cytoplasm side.
- [x] Clathrin is on the cytoplasm side of the pit, deep pit and coated vesicle (41 bristles, 0 wrong). All 9 receptors with LDL face the outside or the vesicle interior.
- [x] ATP → ADP is on the cytoplasm side of both pumps, with the phosphate (P) attached to each pump. There is no ATP at the cotransporter.
- [x] The simple diffusion arrow (x 4.72) passes through lipids, not a protein. The channel arrow (x 5.63) passes through the pore (5.56 to 5.70).
- [x] Gradients, counted from the drawn dots:
  - O₂: 9 outside / 2 inside
  - K⁺ at the channel: 2 / 7
  - K⁺ at the pump: 1 / 6
  - Na⁺ at the pump: 10 / 1
  - Na⁺ at the cotransporter: 5 / 2
  - glucose: 1 / 6
  - H⁺: 9 / 1

  Every gradient also has HIGH/LOW tags.
- [x] The lysosome is fused with the food vacuole inside the cell (the circles overlap by 0.076"), and enzymes are moving into the vacuole.
- [x] In both exocytosis examples, the vesicle is part of the plasma membrane path (one continuous line that opens to the outside). Hormones and waste are drawn outside.
- [x] Nothing passes the page edge or overlaps a label.
- [x] PNG and PDF match the SVG:
  - Both are rendered from the same file.
  - The PDF rasterized at 300 dpi lines up with the PNG at offset (0, 0), with mean pixel difference 2.5/255. The only differences are edge smoothing.
  - The PDF is 792 x 612 pt, 1 page.
- Mistakes caught here (all fixed):
  1. 7 step-number circles overlapped vesicles or pits.
  2. "ADP" text touched the Na⁺ arrow.
  3. The two "No energy" notes ran together.
  4. "LOW glucose" was wider than its tag box.
  5. Two arrows ran through tags.
  6. LDLs in the first pit were crowded together.
  7. Holes in the bilayer: no phospholipid fit between the left corner and the integrin, and some gaps beside proteins were up to 0.13" wide. Phospholipids are now spread evenly.
  8. In draft 1, the integrin did not touch the collagen (a 0.08" to 0.11" gap).
  9. In draft 1, cholesterol was too small to see.
  10. In draft 1, the pseudopods looked like a dangling tube.
  11. In draft 1, the corner joint was a lumpy blob.
  12. The title showed "&amp;".
  13. The cytoplasm color showed the outside color between the inner heads.

---

## 4. Step-by-step GoodNotes plan

### 4.1 Set up (about 10 minutes)

Use **Option A** below (easiest at the end). Option B also works.

- **Option A (guide as an image, recommended):**
  1. Make a new notebook: paper **Blank**, size **Letter**, **landscape**.
  2. Use the image tool to insert `membrane_guide.png`.
  3. Drag its corners to the page corners so it covers the whole page.
  4. Open the lasso tool settings and turn **Images off**, so you can never grab or move the guide by accident.
- **Option B (guide as a PDF):** import `membrane_guide.pdf`. It opens as a document whose background is the guide.

Then:
- Open `membrane_color.png` in Split View, or as a second tab, so the color reference is next to you.
- **Save your colors:** add each hex code from section 5 as a custom color (color picker → custom → type the hex). Make favorites for the ones you use most: Charcoal, Rose pink, Gray, Membrane yellow, Na⁺ blue, K⁺ purple, H⁺ teal, O₂ red, Glucose orange.
- Pick the **ballpoint** pen (even width, unlike the fountain pen) and turn on **draw-and-hold to snap shapes** (shape tool) for circles and straight lines.
- Always zoom in to 300 to 400% for small parts.
- **Test layering once on a scrap page:** draw a pen line, then highlight over it. If the highlighter hides the line, always color *first* and outline *after* (the plan below already does this).

### 4.2 Pens, widths and colors

| Part | Tool | Width | Color |
|---|---|---|---|
| Membrane double line (walls, bottom, vesicles, vacuoles, lysosome) | Ballpoint: first one wide yellow stroke down the middle, then the two edges | Yellow 2.0 mm, then edges 0.4 mm | Membrane yellow #FFE08A, edges Charcoal #263238 |
| Phospholipid heads | Fill: pen scribble. Outline: shape-tool circle 3.3 mm wide | Fill 1.5 mm, outline 0.2 mm | Rose pink #F48FB1, outline Charcoal |
| Phospholipid tails | Ballpoint, one straight + one kinked | 0.3 mm | Gray #6D6D6D |
| Bilayer core (behind tails) | Highlighter, one pass along the tail band (optional) | widest | Cream #FFF3C4 |
| Protein shapes | Fill with pen scribble / highlighter, then outline | outline 0.3 mm | See section 5 |
| Cholesterol | Small rounded bar + tiny circle on top | 0.2 mm outline | Amber #FFC107 |
| Sugar chains | Dots (beads) + connecting lines | beads 1.5 mm dots, lines 0.25 mm | Green #43A047 |
| Collagen fibers | Four stacked wavy lines | 0.6 mm | Brown #8D6E63 |
| Fibronectin | One wavy line | 0.55 mm | Blue #1E88E5 |
| Microfilaments | Two offset rows of beads (bead 1.7 mm) | dots | Red #E53935 |
| Ions (Na⁺, K⁺, H⁺) | One dot, about 2.1 mm wide | 2.0 mm pen tap or tiny filled circle | Na⁺ #1E63D6, K⁺ #8E24AA, H⁺ #00897B |
| O₂ | Two touching 1.7 mm dots | | Red #E53935 |
| Glucose | Hexagon 2.8 mm wide | 0.2 mm outline | Orange #FB8C00 |
| Transport arrows (through the membrane) | Shape tool straight line + arrowhead | 0.55 mm | Same color as the molecule |
| Step arrows (bulk transport) | Line or curve + arrowhead | 0.35 mm | Charcoal |
| Label pointer lines | Shape-tool straight line + small dot at the end | 0.2 mm | Charcoal |

### 4.3 Drawing order (so everything fits)

Trace the guide's gray lines. Do not freehand positions. For each part, **color first, then outline**.

1. **Membrane outline (double line).**
   - With the 2.0 mm yellow pen, trace the *middle* of the side walls and bottom, including every pocket, the pseudopod cup, and the two top corners.
   - Then trace both edges in 0.4 mm charcoal.
   - Keep the line unbroken everywhere except where the guide shows an opening to the outside (the exocytosis pockets).
2. **Vesicles, vacuoles, lysosome:** the same yellow-then-edges method, using shape-tool circles. Fill the inside of every vesicle with pale blue #E3F2FD (optional). Fill the lysosome with light purple #E1BEE7.
3. **Golgi:** 4 curved sacs, light pink #F8BBD0, charcoal outline.
4. **Proteins on the top bilayer.** Do these before the phospholipids so the lipids fit around them. Order: integrin, glycoprotein, enzyme, K⁺ channel (2 halves), Na⁺/K⁺ pump, cotransporter, proton pump. Then the peripheral protein under the inner heads. Make each one reach above the top heads and below the bottom heads (the guide shows exactly where).
5. **Phospholipids** (see 4.4): 34 pairs, copy-pasted.
6. **Cholesterol** (3 pairs), **glycolipid chain**, **glycoprotein chain**.
7. **ECM and cytoskeleton:** collagen (4 wavy lines), fibronectin (from the integrin head up into the collagen), microfilament beads (from the integrin legs to the left, then down the wall).
8. **Molecules + arrows for protein transport:**
   - Draw the dots first.
   - Then the arrows: O₂ down, K⁺ up through the pore, Na⁺ up and K⁺ down through the pump, Na⁺ and glucose down through the cotransporter, H⁺ up through the proton pump.
   - Then ATP / ↓ / ADP below each pump, with the yellow "P" circle stuck to the pump.
9. **Bulk transport details:**
   - Phagocytosis: the bacterium (3 times) and enzymes ("pac-man" shapes), plus nutrient dots with arrows and waste bits.
   - Pinocytosis: fluid dots.
   - Receptor-mediated endocytosis: receptors + LDL, then clathrin.
   - Exocytosis: hormone diamonds.
   - Then the step arrows and the numbered circles.
10. **Optional background tints** (section 4.5).
11. **Labels, tags, key, title, name** (section 4.6).
12. **Self-check** with section 6, then **move off the guide** (section 4.7).

### 4.4 Copy-paste plan (draw once, lasso, copy, paste)

How to paste:
- Lasso the part, tap it, **Copy**.
- Long-press where you want it, **Paste**.
- Drag it onto the gray guide shape.
- To make many fast: paste 1, then select both and copy (2), paste (4), select all and copy (8), and so on.

| Repeated part | Draw once | How many | Orientation tips |
|---|---|---|---|
| **Phospholipid PAIR** | Draw the *pair* as one unit: the top lipid head-up with tails down, and right under it the bottom lipid head-down with tails up. Tails nearly touch in the middle. Then you never need to flip anything | **34 pairs**, left to right: 1, integrin, 1, glycoprotein, 1, cholesterol, **7**, enzyme, **8**, cholesterol, 1, K⁺ channel, 3, Na⁺/K⁺ pump, 4, cotransporter, 4, proton pump, 2, cholesterol, 2 | Every pasted pair must sit with heads exactly on the gray head circles. Check that the bottom head of each pair is *below* its tails |
| Cholesterol pair | One up in the top layer, one upside-down in the bottom layer | 3 | Small round end (OH) faces the heads in each layer |
| Na⁺ dot | 1 | 15 outside, 3 inside, plus 4 small ones inside proteins | More outside! |
| K⁺ dot | 1 | 3 outside, 13 inside, plus 3 small ones in the channel/pump | More inside! |
| H⁺ dot | 1 | 9 outside, 1 inside, 1 in the pump | More outside! |
| O₂ (two dots) | 1 | 9 outside, 2 inside, 1 crossing the tails | Rotate copies a little so they look natural |
| Glucose hexagon | 1 | 1 outside, 6 inside, 1 in the cotransporter | More inside! |
| Microfilament segment | 6 beads in two offset rows | about 8 segments (44 beads) | Rotate the copies to follow the corner turn |
| Collagen strand | 1 wavy line | 4 stacked | |
| LDL receptor + LDL ("Y" with a yellow ball in its arms) | 1 | 9 (3 pit, 3 deep pit, 3 vesicle) | Use the lasso rotate handle. The stem always sits on the membrane, and the LDL always points **away from the cytoplasm**: down in the shallow pit, toward the center in the deep pit and vesicle |
| Clathrin bristle (short line with a "Y" tip) | 3 together | about 41 | Bristles always point **into the cytoplasm**: up on the shallow pit, outward (away from the center) on the deep pit and vesicle. Rotate each copy so it sticks straight out |
| Fluid dot, hormone diamond, waste bit, enzyme pac-man, nutrient dot | 1 each | as on the reference | |
| Step-number circle | 1 dark circle | 15 (phagocytosis 5, pinocytosis 3, receptor-mediated 3, exocytosis #1 4) | Then type the white number on top |
| HIGH tag / LOW tag | 1 of each (typed text + shape-tool rectangle) | 14 total (7 outside, 7 inside) | Copy, then edit the text |

### 4.5 Coloring neatly

- Zoom in. Color **inside** the gray guide lines first, then outline on top in charcoal. The outline hides small wobbles.
- For bigger fills (proteins, Golgi, vesicle insides), use the highlighter in **one continuous back-and-forth stroke**. Lifting the pencil and overlapping strokes can make darker streaks.
- For tiny fills (heads, ions), use a scribble with a 1.5 to 2.0 mm pen.
- Wrong color? Lasso it and use the lasso **color** option. Don't redraw.
- **Optional background tints**, done last with the widest highlighter in long smooth strokes: pale blue #E3F2FD outside the cell, pale peach #FFF6E5 inside. If they look streaky, skip them. The labels already mark outside vs inside, so tints earn no extra points.

### 4.6 Labels

- Use **typed text boxes** for every label. They stay sharp and readable when printed. The only handwriting is the drawing itself.
- One font everywhere (for example Helvetica Neue, or Avenir Next). Bold for names, regular for the gray-guide second lines.
- **Sizes for a printed Letter page:**
  - Title 18 pt bold
  - Section headers (SIMPLE DIFFUSION, PHAGOCYTOSIS...) 9 pt bold
  - Structure names 8 pt bold
  - Second lines and notes 7 pt
  - HIGH/LOW tags 7 pt bold
  - **Never go below 7 pt.**
- **Size test:** type "Glycoprotein" at 8 pt bold and set it on top of the gray "Glycoprotein" in the guide. It should be about the same width (0.73"). If not, change the size until it matches, and use that scale for everything.
- **Superscripts:** copy them straight from the label strip in section 5. Copy on the iPad, then paste into the GoodNotes text box.
- Place each label exactly over its gray guide text. Draw pointer lines (0.2 mm) from the label to the part, with a tiny dot on the part.
- Add labels last, after all coloring, so no fill covers them.

### 4.7 Moving the finished drawing onto a clean page

- **If you used Option A (guide as an image):**
  1. Open the lasso settings and select **Images only**.
  2. Lasso the guide image and **Delete** it.
  3. Your drawing stays exactly where it is on the blank Letter page. Done.
- **If you used Option B (guide PDF background), or you prefer copy-paste:**
  1. Lasso settings: handwriting, text and images **all on**.
  2. Draw one big loop around the entire page and **Copy**.
  3. Add a new page: **Blank, Letter, landscape**.
  4. Long-press the middle of the page and **Paste**.
  5. Drag the pasted drawing until the left and right margins are equal and the top and bottom margins are equal (about 0.4" or more each). Don't resize it.
  6. Check that the text boxes came along too.
  7. Delete the guide page, or keep it in a separate notebook.
- Export: Share → **PDF** (with page background) to print or submit. Print at **100% / Actual size**, not "fit to page", so the 7 pt text stays 7 pt.

---

## 5. Color key and label list

### 5a. Color key (same names and colors as the reference)

| Part | Color name | Hex |
|---|---|---|
| Outlines, membrane edge lines, label text | Charcoal | #263238 |
| Simplified membrane band, vesicle and vacuole walls | Membrane yellow | #FFE08A |
| Phospholipid heads | Rose pink | #F48FB1 |
| Phospholipid tails | Gray | #6D6D6D |
| Bilayer core behind the tails (optional) | Cream | #FFF3C4 |
| Cholesterol | Amber | #FFC107 |
| Sugar chains (glycoprotein, glycolipid) | Green | #43A047 |
| Glycoprotein | Light orange | #FFCC80 |
| Peripheral protein | Salmon | #FFAB91 |
| Enzyme | Orchid | #CE93D8 |
| Substrate (triangle) | Yellow | #FFCA28 |
| Products (circle / square) | Orange / Light green | #FB8C00 / #66BB6A |
| Integrin | Sky blue | #90CAF9 |
| Collagen fibers | Brown | #8D6E63 |
| Fibronectin | Blue | #1E88E5 |
| Microfilaments (actin) | Red | #E53935 |
| K⁺ channel | Aqua | #80DEEA |
| Na⁺/K⁺ pump | Lavender | #B39DDB |
| Na⁺/glucose cotransporter | Mint | #A5D6A7 |
| Proton (H⁺) pump | Periwinkle | #9FA8DA |
| Na⁺ ions | Blue | #1E63D6 |
| K⁺ ions | Purple | #8E24AA |
| H⁺ ions (protons) | Teal | #00897B |
| O₂ | Red | #E53935 |
| Glucose | Orange | #FB8C00 |
| ATP / ADP text and arrow | Rust | #BF360C |
| Phosphate "P" on pumps | Yellow | #FFEB3B |
| Bacterium (fill / squiggle inside) | Lime / Dark olive | #7CB342 / #33691E |
| Lysosome contents | Light purple | #E1BEE7 |
| Hydrolytic (digestive) enzymes | Magenta | #C2185B |
| Nutrients leaving the food vacuole | Dark green | #2E7D32 |
| Undigested waste | Dark brown | #6D4C41 |
| Extracellular fluid droplets | Light blue | #29B6F6 |
| LDL particles | Light yellow | #FFD54F |
| LDL receptors | Indigo | #3949AB |
| Clathrin | Dark orange | #EF6C00 |
| Golgi | Light pink | #F8BBD0 |
| Hormones | Raspberry | #D81B60 |
| Step-number circles | Slate | #37474F |
| HIGH tags / LOW tags | Red / Blue | #C62828 / #1565C0 |
| Headers: passive / active / cotransport / bulk | Teal / Purple / Green / Magenta | #00796B / #6A1B9A / #2E7D32 / #AD1457 |
| OUTSIDE labels / INSIDE label | Blue / Orange | #0277BD / #E65100 |
| Outside tint / inside tint (optional) | Pale blue / Pale peach | #E3F2FD / #FFF6E5 |

Label text colors: structure names on the reference use a darker shade of their part (collagen #5D4037, integrin and fibronectin #1565C0, glycoprotein #E65100, glycolipid #2E7D32, microfilaments #C62828, cholesterol #B8860B, peripheral #D84315, enzyme #7B1FA2, phospholipid #AD1457, LDL receptor #3949AB, clathrin #E65100, hormones #D81B60). Typing every label in Charcoal is also fine and still looks neat.

### 5b. Label list (copy-paste strip, exact text)

Everything below goes **on the drawing**, over its gray guide text. The **KEY box** (top right) only defines the symbols.

**Title and regions**
- The Plasma Membrane: Structure & Transport
- Name: ______________
- OUTSIDE THE CELL / (extracellular fluid)  (top left)
- INSIDE THE CELL (cytoplasm)  (middle)
- OUTSIDE THE CELL (extracellular fluid)  (bottom)

**Membrane parts**
- Collagen fibers / (extracellular matrix, ECM)
- Fibronectin
- Glycoprotein / (cell ID card)
- Glycolipid
- Enzyme / (integral protein)
- Substrate
- Products
- Integrin / (attachment protein)
- Microfilaments (actin) / (cytoskeleton)
- Cholesterol
- Peripheral protein
- Phospholipid / (hydrophilic head, / hydrophobic tails)

**Protein transport (headers, then the example line)**
- SIMPLE / DIFFUSION / O₂ through bilayer
- FACILITATED / DIFFUSION / K⁺ channel
- ACTIVE / TRANSPORT #1 / Na⁺/K⁺ pump / Na⁺ out, K⁺ in
- COTRANSPORT / (secondary active / transport) / Na⁺/glucose
- ACTIVE / TRANSPORT #2 / Proton (H⁺) pump
- Tags (outside row): HIGH O₂ · LOW K⁺ · HIGH Na⁺ + LOW K⁺ · HIGH Na⁺ + LOW glucose · HIGH H⁺ (acidic)
- Tags (inside row): LOW O₂ · HIGH K⁺ · HIGH K⁺ + LOW Na⁺ · LOW Na⁺ + HIGH glucose · LOW H⁺
- Under each pump: ATP / ↓ / ADP (and a yellow circle with P on the pump)
- Notes row: No energy used / (passive) · No energy used / (passive) · Energy: ATP / (against gradients) · Energy: Na⁺ gradient / made by the Na⁺/K⁺ pump / (ATP used indirectly) · Energy: ATP / (against gradient)

**Bulk transport**
- PHAGOCYTOSIS / (“cell eating”: a bacterium)
- Pseudopods / wrap around / the bacterium (step 1) · Bacterium · Food / vacuole (step 2)
- Lysosome fuses with / food vacuole; hydrolytic / enzymes are released (step 3)
- Digestion: / nutrients diffuse / into cytoplasm (step 4)
- EXOCYTOSIS #2: / undigested waste / released outside (step 5)
- PINOCYTOSIS / (“cell drinking”) · Extracellular fluid / (water + dissolved solutes) (steps 1 to 3)
- RECEPTOR-MEDIATED / ENDOCYTOSIS (LDL) · Clathrin coat / (cytoplasm side) · LDL (carries / cholesterol) · LDL receptor · Clathrin-coated / vesicle (steps 1 to 3)
- EXOCYTOSIS #1 / (hormones from Golgi) · Golgi / apparatus · Secretory / vesicle · Hormones (proteins) / released outside (steps 1 to 4)

**KEY box** (symbol + text)
- KEY
- Na⁺ sodium ion · K⁺ potassium ion · H⁺ proton · O₂ oxygen · Glucose · Phosphate (ATP) · Direction it moves
- HIGH = More dots · LOW = Fewer dots

### Checkpoint 4 (plan and key), result: PASS

Checked by `tools/check_blueprint.py`:
- Every one of the 97 labels drawn on the reference appears word for word in the label list above.
- Every color used for a part in the reference appears in the color key with the same hex.
- Every label points to something actually drawn. All 15 pointer lines end on a drawn part, and the layout audit found no stray pointers.
- Mistakes caught here: 2 pointer lines ended in empty space. The collagen pointer stopped 0.06" above the fibers after the fibers were moved up for fibronectin, and the glycoprotein pointer ended between two branches of the sugar chain. Both now end on the structure.

---

## 6. Self-grading checklist (use it on your finished page)

**Membrane components (10)**
- [ ] Phospholipids: both layers, heads out, tails in, labeled "Phospholipid"
- [ ] Cholesterol between the tails, labeled
- [ ] Glycoprotein with its sugar chain *outside*, labeled
- [ ] Glycolipid (a lipid with a sugar chain) *outside*, labeled
- [ ] Peripheral protein *touching* the inner surface, labeled
- [ ] Enzyme spans the membrane. Substrate arrow in, product arrows out. All three labeled
- [ ] Integrin spans the membrane, touches fibronectin/collagen outside and microfilaments inside, labeled "attachment protein"
- [ ] Collagen fibers (ECM) labeled
- [ ] Microfilaments (cytoskeleton) labeled

**Membrane transport (12)**
- [ ] Simple diffusion: O₂, more dots outside, arrow down *through lipids*, HIGH/LOW tags
- [ ] Facilitated diffusion: K⁺ through the *channel*, more K⁺ inside, arrow up, tags
- [ ] Two different pumps (Na⁺/K⁺ and proton), arrows low → high, ATP → ADP + P on the cytoplasm side, tags
- [ ] Cotransport: Na⁺ and glucose both going in, tags for *both*, energy = Na⁺ gradient from the pump

**Bulk transport (14)**
- [ ] Phagocytosis: bacterium, pseudopods wrapping, food vacuole, lysosome *fused* with enzymes spilling in, numbered steps
- [ ] Pinocytosis: fluid, dip → pocket → vesicle, numbered
- [ ] Receptor-mediated: LDL on receptors, clathrin on the *inside* (cytoplasm side), pit → deep pit → coated vesicle, numbered
- [ ] Exocytosis: (1) Golgi → secretory vesicle → fuses → hormones outside; (2) waste vacuole opens to the outside. Membranes merge with the plasma membrane

**Visual appeal (4)**
- [ ] Neat lines, all colored, text 7 pt or bigger, nothing crowded

**Digital mistakes to look for (zoom to 400% and scan left to right)**
- [ ] A pasted phospholipid pair is upside down (bottom head above its tails) or floats off the gray circles
- [ ] Two pasted pairs overlap, or there is a hole where a pair is missing (count 34)
- [ ] A protein does not reach past the heads on *both* sides
- [ ] The peripheral protein floats below the heads with a gap
- [ ] A pasted clathrin bristle points into the pit/vesicle instead of into the cytoplasm
- [ ] A pasted receptor points into the cytoplasm instead of toward the outside/vesicle interior
- [ ] A dot cluster was pasted on the wrong side. Check every HIGH tag sits on the side with more dots
- [ ] An arrowhead points the wrong way (O₂ down, K⁺ channel up, Na⁺ pump up, K⁺ pump down, cotransport down, H⁺ up)
- [ ] A label box covers a structure, a dot, or an arrow
- [ ] The double line has a break anywhere except the two exocytosis openings
- [ ] Highlighter fills covered your outlines (redo the outline on top)
- [ ] Gray guide lines or gray guide text are still showing (remove the guide, section 4.7)
- [ ] Anything within 0.4" of the page edge
- [ ] Text boxes left at the default size (too big) or below 7 pt

---

## 7. Final audit

### Pass 1: rubric line by line

| Rubric bullet | Pts | Where on the page (in) | Drawn | Labeled |
|---|---|---|---|---|
| Phospholipids | 10 total for membrane parts (all 9 present) | Bilayer x 1.30 to 9.70, y 2.605 to 3.225. Label starts at (9.40, 4.04) | Yes | "Phospholipid (hydrophilic head, hydrophobic tails)" |
| Cholesterol | | Pairs at x 2.45, 5.15, 9.385. Label (2.05, 3.86) | Yes | "Cholesterol" |
| Glycoprotein | | x 2.08. Label (2.26, 1.82) | Yes | "Glycoprotein (cell ID card)" |
| Glycolipid | | x 2.70. Label (2.40, 2.14) | Yes | "Glycolipid" |
| Peripheral protein | | (3.05, 3.30). Label (3.09, 4.20) | Yes | "Peripheral protein" |
| Integral: enzyme with substrates and products | | x 3.72. Substrate (3.43, 3.74), products (4.04 to 4.15, 3.6 to 3.8) | Yes | "Enzyme (integral protein)", "Substrate", "Products" |
| Integral: attachment protein | | Integrin x 1.63 | Yes | "Integrin (attachment protein)" |
| Fibers of the ECM | | Collagen y 1.80 to 2.05, fibronectin x 1.63 | Yes | "Collagen fibers (extracellular matrix, ECM)", "Fibronectin" |
| Cytoskeleton microfilaments | | y 3.47, x 1.03 to 2.42 + left wall | Yes | "Microfilaments (actin) (cytoskeleton)" |
| Simple diffusion: gradient + example | 2 | Zone x 4.25 to 5.15 | Yes (9 vs 2 dots, arrow through lipids) | Header + "O₂ through bilayer", HIGH/LOW O₂ |
| Facilitated diffusion: gradient + example | 2 | Zone x 5.15 to 6.12 | Yes (7 vs 2 dots, arrow through pore) | Header + "K⁺ channel", HIGH/LOW K⁺ |
| Active transport: gradients, two pumps, molecules + energy | 5 | Zones x 6.12 to 7.22 and 8.36 to 9.35 | Yes | "Na⁺/K⁺ pump", "Proton (H⁺) pump", tags, "Energy: ATP", ATP → ADP + P |
| Cotransport: both gradients, molecules, energy | 3 | Zone x 7.22 to 8.36 | Yes (Na⁺ 5 vs 2; glucose 1 vs 6) | "Na⁺/glucose", 4 tags, "Energy: Na⁺ gradient made by the Na⁺/K⁺ pump (ATP used indirectly)" |
| Phagocytosis: example, steps, engulfing, lysosome fusion/enzymes | 4 | Zone x 0.80 to 4.45, steps 1 to 4 | Yes | Header, "Bacterium", "Pseudopods...", "Food vacuole", "Lysosome fuses... enzymes are released", "Digestion..." |
| Pinocytosis: type of substance, steps, engulfing | 3 | Zone x 4.40 to 5.90, steps 1 to 3 | Yes | Header, "Extracellular fluid (water + dissolved solutes)" |
| Receptor-mediated: target molecule, steps, clathrin inside | 3 | Zone x 5.90 to 7.95, steps 1 to 3 | Yes | Header "(LDL)", "LDL (carries cholesterol)", "LDL receptor", "Clathrin coat (cytoplasm side)", "Clathrin-coated vesicle" |
| Exocytosis: 2 substances, steps, bilayer releasing | 4 | #1 x 8.00 to 10.20 (steps 1 to 4); #2 at x 3.95 (step 5) | Yes | "EXOCYTOSIS #1 (hormones from Golgi)", "Secretory vesicle", "Hormones (proteins) released outside", "EXOCYTOSIS #2: undigested waste released outside" |
| Visual appeal | 4 | Whole page | Neat, colorful, 0 overlaps, smallest text 6.5 to 7 pt | |
| **Total** | **40 / 40** | | | |

### Pass 2: a strict teacher trying to take points off

| Possible deduction | Verdict | What changed |
|---|---|---|
| "Proton pumps are for plants and bacteria" | Your notes present it as the second pump example, and the rubric only needs two different pumps. Small risk, flagged in 1c | Label says "Proton (H⁺) pump" and the tag says "(acidic)", matching your notes' figure |
| "3 Na⁺ / 2 K⁺ wasn't taught" | Fair: not in your notes | **Changed** to "Na⁺ out, K⁺ in" |
| "Exocytosis example isn't specific" | The rubric's own bullets are "vesicle coming from golgi" and "waste from food vacuole". Both are drawn and named | Kept "Hormones (proteins)" (from your notes). Optional "(ex. insulin)" |
| "Cotransport shows only one gradient" | Draft 1 had only glucose tags | **Fixed** earlier: HIGH/LOW for both Na⁺ and glucose |
| "Integrin isn't attached to the ECM" | Draft 1 had a gap | **Fixed**: integrin → fibronectin → collagen, touching |
| "Bilayer has holes / proteins don't span" | Checked by coordinates | **Fixed** earlier (even spacing). Now no gap over 1.5 mm, and all 7 integral proteins span |
| "Clathrin on the wrong side" | Checked: 41/41 bristles on the cytoplasm side | None needed |
| "Bulk transport isn't a bilayer" | The assignment allows a double line for some transport. It is drawn as two lines with the yellow core, continuous with the full bilayer at the corners | None needed |
| "Hard to read" | Smallest text 6.5 pt in the reference. In GoodNotes use 7 pt or larger (section 4.6) | Tag and key text were raised from 6.1 pt |
| "Step order unclear" | Every bulk process has numbered circles and step arrows | None needed |

Result after both passes: 40/40, with one judgment call for you or your teacher (proton pump in an animal cell, section 1c).

---

## 8. Every mistake caught and how it was fixed

1. **Ca²⁺ pump** (not in notes) → proton (H⁺) pump.
2. **Lactase / lactose / glucose + galactose** (not in notes) → unnamed enzyme with substrate → products, active site on the cytoplasm side, like your notes' figure.
3. **Insulin** (not in notes) → hormones (proteins).
4. **"Symport"** (not in notes) → "secondary active transport".
5. **"3 Na⁺ out, 2 K⁺ in"** (ratio not in notes, found in Pass 2) → "Na⁺ out, K⁺ in".
6. **Integrin touching collagen directly** → added fibronectin as the bridge (your notes). In draft 1, the integrin did not even touch the collagen (0.08" to 0.11" gap).
7. **Wording** → "Microfilaments (actin)", "Pseudopods" (your notes' words).
8. **Cotransport gradient tags only for glucose** → added Na⁺ HIGH/LOW tags at the cotransporter.
9. **Title showed "&amp;"** → fixed text escaping.
10. **Bottom OUTSIDE label inside the 0.4" margin** (y 8.32") → moved to y 8.01".
11. **Crowded top band, empty middle** → moved the bilayer down 0.45" and the bottom up 0.22".
12. **Pseudopods looked like a dangling tube** → redrawn to curl under the bacterium with a small gap between the tips.
13. **Lumpy corner joint** → a smooth curve that narrows the yellow tail band into the double line.
14. **Outside color showing between the inner heads** → fixed the cytoplasm fill.
15. **Label collisions in draft 1** (Glycolipid/Lactose, Peripheral/Enzyme, the energy notes, Bacterium/Exocytosis #2, the Exocytosis #1 header on the coated vesicle, the key text past its box) → moved or reworded.
16. **7 step circles on top of vesicles or pits** (found by the audit) → each moved clear.
17. **"ADP + Pᵢ" touching the Na⁺ arrow** → moved, and it now reads ATP ↓ ADP with the P drawn on the pump (matches "phosphorylated" in your notes).
18. **Two "No energy needed (passive: high → low)" notes running together** → "No energy used (passive)".
19. **"LOW glucose" wider than its tag box** → tag widths now measured from the font, with two rows of tags.
20. **Na⁺/K⁺ and cotransport arrows running through the tags** → shortened.
21. **Phosphate symbol in the key counted as part of the drawing** → fixed the layer.
22. **5 crowded LDLs in the shallow pit** → 3, spaced out.
23. **Holes in the bilayer** (none fit between the left corner and the integrin, and gaps up to 0.13" beside proteins) → phospholipids spread evenly between proteins, integrin moved 0.11" right, last cholesterol moved. Now no gap over 1.5 mm.
24. **Cholesterol too small to see** → enlarged, with its own space between phospholipids.
25. **Smallest text 6.1 pt** → raised to 6.5 pt in the reference (use 7 pt in GoodNotes).
26. **Two pointer lines ending in empty space** (found in Checkpoint 4: collagen and glycoprotein) → each now ends on its structure.

---

*How the checks were run (for the curious):*
- `python3 tools/make_membrane.py reference` draws the SVGs.
- `node tools/render.js reference 300` makes the PNGs and PDFs.
- `python3 tools/check_geometry.py reference/geometry.json` runs the 56 science/geometry checks.
- `node tools/audit_layout.js reference/membrane_color.svg <dir>` followed by `python3 tools/audit_layout.py <dir>` runs the label/margin audit.
- `python3 tools/check_blueprint.py` cross-checks this document against the drawing.
