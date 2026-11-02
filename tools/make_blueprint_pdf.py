#!/usr/bin/env python3
"""Turn BLUEPRINT.md into a printable Letter PDF (Blueprint.pdf) with color swatches and the reference image."""
import os
import re
import subprocess
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
md = open(os.path.join(ROOT, "BLUEPRINT.md"), encoding="utf-8").read()
md = md.replace("- [ ]", "- ☐").replace("- [x]", "- ☑")


def fix_lists(text):
    """Python-Markdown needs a blank line before a list and 4-space nesting (GitHub does not)."""
    item = re.compile(r"^\s*([-*]|\d+\.) ")
    out = []
    for line in text.split("\n"):
        if re.match(r"^  (?! )", line):
            line = "  " + line                       # 2-space nesting -> 4 spaces
        prev = out[-1] if out else ""
        if item.match(line) and prev.strip() and not item.match(prev) and not prev.startswith("    "):
            out.append("")
        out.append(line)
    return "\n".join(out)


md = fix_lists(md)
body = markdown.markdown(md, extensions=["tables", "sane_lists"])
body = re.sub(r"(?<![\w&])#([0-9A-Fa-f]{6})\b",
              lambda m: f'<span class="sw" style="background:#{m.group(1)}"></span>#{m.group(1).upper()}', body)
fig = ('<figure><img src="reference/membrane_color.png"><figcaption>(a) Full-color reference. '
       'Open reference/membrane_color_grid.pdf for the 1-inch grid and reference/membrane_guide.pdf for the tracing guide.'
       '</figcaption></figure>')
body = body.replace("<hr />", fig, 1)
css = """
@page { size: 8.5in 11in; margin: 0.5in 0.5in 0.55in 0.5in; }
body { font-family: Inter, Helvetica, Arial, sans-serif; font-size: 9.6pt; line-height: 1.38; color: #263238; }
h1 { font-size: 19pt; margin: 0 0 6pt; color: #AD1457; }
h2 { font-size: 14pt; margin: 16pt 0 6pt; padding-bottom: 3pt; border-bottom: 2px solid #F48FB1; color: #263238;
     break-after: avoid; }
h3 { font-size: 11pt; margin: 11pt 0 4pt; color: #6A1B9A; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0 8pt; font-size: 8.4pt; }
th, td { border: 1px solid #CFD8DC; padding: 3pt 4pt; vertical-align: top; text-align: left; }
th { background: #ECEFF1; }
tr { break-inside: avoid; }
code { font-family: 'JetBrains Mono', monospace; font-size: 8pt; background: #F5F5F5; padding: 0 2pt; }
.sw { display: inline-block; width: 9pt; height: 9pt; border: 1px solid #546E7A; border-radius: 2px;
      vertical-align: -1.5pt; margin-right: 3pt; }
figure { margin: 6pt 0 10pt; break-inside: avoid; }
figure img { width: 100%; border: 1px solid #CFD8DC; }
figcaption { font-size: 8pt; color: #546E7A; }
ul, ol { margin: 3pt 0 6pt; padding-left: 16pt; }
li { margin: 1pt 0; }
"""
html = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'
out_html = os.path.join(ROOT, ".blueprint_print.html")
open(out_html, "w", encoding="utf-8").write(html)
js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://{out_html}'); await p.evaluate(() => document.fonts.ready);
  await p.pdf({{ path: '{os.path.join(ROOT, "Blueprint.pdf")}', width: '8.5in', height: '11in', printBackground: true,
                displayHeaderFooter: true, headerTemplate: '<span></span>',
                footerTemplate: '<div style="font-size:7pt;color:#78909C;width:100%;text-align:center">Membrane blueprint, page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
                margin: {{ top: '0.5in', bottom: '0.6in', left: '0.5in', right: '0.5in' }} }});
  await b.close();
}})();
"""
subprocess.run(["node", "-e", js], check=True, cwd=ROOT)
os.remove(out_html)
print("wrote Blueprint.pdf")
