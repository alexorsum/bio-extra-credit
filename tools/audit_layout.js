// Layout audit: measures every label box and writes a label-free raster of the drawing.
// Usage: node tools/audit_layout.js <svg> <outdir>
// Writes <outdir>/audit_boxes.json and <outdir>/audit_nolabels.png (2 px per unit).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const svgPath = path.resolve(process.argv[2]);
  const outDir = path.resolve(process.argv[3]);
  const svg = fs.readFileSync(svgPath, 'utf8').replace('width="11in" height="8.5in"', 'width="1100" height="850"');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1100, height: 850 }, deviceScaleFactor: 2 });
  await page.setContent(`<!doctype html><html><head><style>html,body{margin:0}svg{display:block}</style></head><body>${svg}</body></html>`);
  await page.evaluate(() => document.fonts.ready);
  const data = await page.evaluate(() => {
    const out = { labels: [], elements: [] };
    const sw = el => parseFloat(el.getAttribute('stroke-width') || '0');
    for (const el of document.querySelectorAll('#label > *')) {
      const b = el.getBBox();
      const rec = { tag: el.tagName, cls: el.getAttribute('class') || '', x: b.x, y: b.y, w: b.width, h: b.height,
                    text: el.textContent, size: parseFloat(el.getAttribute('font-size') || '0') };
      if (el.tagName === 'line') {
        rec.x1 = +el.getAttribute('x1'); rec.y1 = +el.getAttribute('y1');
        rec.x2 = +el.getAttribute('x2'); rec.y2 = +el.getAttribute('y2');
      }
      out.labels.push(rec);
    }
    for (const g of ['ecm', 'band', 'lipid', 'protein', 'deco', 'mol', 'arrow', 'label']) {
      for (const el of document.querySelectorAll('#' + g + ' > *')) {
        const b = el.getBBox();
        const s = sw(el) / 2 + (el.getAttribute('marker-end') ? 4 : 0);
        out.elements.push({ layer: g, tag: el.tagName, x0: b.x - s, y0: b.y - s, x1: b.x + b.width + s, y1: b.y + b.height + s,
                            text: el.tagName === 'text' ? el.textContent : '' });
      }
    }
    // hide labels and background tints for the raster used in the overlap test
    document.querySelector('#label').style.display = 'none';
    document.querySelector('#bg').style.display = 'none';
    return out;
  });
  await page.screenshot({ path: path.join(outDir, 'audit_nolabels.png') });
  fs.writeFileSync(path.join(outDir, 'audit_boxes.json'), JSON.stringify(data));
  await browser.close();
  console.log('boxes', data.labels.length, 'elements', data.elements.length);
})();
