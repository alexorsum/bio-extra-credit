# AP Bio Membrane Bonus

A blueprint and to-scale reference images for a hand-drawn (GoodNotes) plasma membrane diagram that covers every item on the 40-point rubric, using only content from the Unit 3 class notes (plus the three rubric items the notes do not cover, which are flagged).

- **Start here:** [`BLUEPRINT.md`](BLUEPRINT.md) (same content as `Blueprint.pdf`, which you can import into GoodNotes)
- **Reference images** (landscape US Letter, 300 dpi PNG + vector PDF):
  - `reference/membrane_color.*`: (a) full-color finished reference
  - `reference/membrane_color_grid.*`: (b) with a 1-inch grid and the 0.4" margin
  - `reference/membrane_guide.*`: (c) light gray outline guide to draw on top of
- **Tools** (rebuild and re-check everything):

```bash
python3 tools/make_membrane.py reference
```

```bash
node tools/render.js reference 300
```

```bash
python3 tools/check_geometry.py reference/geometry.json
```

```bash
node tools/audit_layout.js reference/membrane_color.svg /tmp && python3 tools/audit_layout.py /tmp
```

```bash
python3 tools/check_blueprint.py
```

```bash
python3 tools/make_blueprint_pdf.py
```
