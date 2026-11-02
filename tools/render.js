// Render the reference SVGs to PNG (300 dpi) and US Letter landscape PDF with headless Chromium.
// Usage: node tools/render.js <dir> [dpi]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = path.resolve(process.argv[2] || 'reference');
  const dpi = Number(process.argv[3] || 300);
  const scale = dpi / 100;               // SVG units are 1/100 inch; page is 1100 x 850 units
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.svg'));
  const browser = await chromium.launch();
  for (const f of files) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const base = f.replace(/\.svg$/, '');
    // PNG: render the SVG at 1100x850 CSS px scaled by deviceScaleFactor
    const pngPage = await browser.newPage({ viewport: { width: 1100, height: 850 }, deviceScaleFactor: scale });
    const pngSvg = svg.replace('width="11in" height="8.5in"', 'width="1100" height="850"');
    await pngPage.setContent(`<!doctype html><html><head><style>html,body{margin:0;padding:0;background:#fff}svg{display:block}</style></head><body>${pngSvg}</body></html>`);
    await pngPage.evaluate(() => document.fonts.ready);
    await pngPage.screenshot({ path: path.join(dir, base + '.png'), clip: { x: 0, y: 0, width: 1100, height: 850 } });
    await pngPage.close();
    // PDF: exact Letter landscape page, vector output
    const pdfPage = await browser.newPage();
    await pdfPage.setContent(`<!doctype html><html><head><style>@page{size:11in 8.5in;margin:0}html,body{margin:0;padding:0;width:11in;height:8.5in;overflow:hidden}svg{display:block;width:11in;height:8.5in}</style></head><body>${svg}</body></html>`);
    await pdfPage.evaluate(() => document.fonts.ready);
    await pdfPage.pdf({ path: path.join(dir, base + '.pdf'), width: '11in', height: '8.5in', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1' });
    await pdfPage.close();
    console.log('rendered', base);
  }
  await browser.close();
})();
