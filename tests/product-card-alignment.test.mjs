import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('CSS rules in css/rootze.css enforce strict Flexbox equal-height card and table alignment', () => {
  const cssPath = path.resolve(process.cwd(), 'css/rootze.css');
  assert.ok(fs.existsSync(cssPath), 'Missing css/rootze.css');
  const css = fs.readFileSync(cssPath, 'utf-8');

  // 1. .car-wrap flex column & 100% height
  assert.match(css, /\.car-wrap\s*\{[^}]*display:\s*flex;/s, 'car-wrap must have display: flex');
  assert.match(css, /\.car-wrap\s*\{[^}]*flex-direction:\s*column;/s, 'car-wrap must have flex-direction: column');
  assert.match(css, /\.car-wrap\s*\{[^}]*height:\s*100%;/s, 'car-wrap must have height: 100%');

  // 2. .car-wrap .text flex-grow & column
  assert.match(css, /\.car-wrap\s+\.text\s*\{[^}]*display:\s*flex;/s, 'car-wrap .text must have display: flex');
  assert.match(css, /\.car-wrap\s+\.text\s*\{[^}]*flex-direction:\s*column;/s, 'car-wrap .text must have flex-direction: column');
  assert.match(css, /\.car-wrap\s+\.text\s*\{[^}]*flex-grow:\s*1;/s, 'car-wrap .text must have flex-grow: 1');

  // 3. Card titles min-height
  assert.match(css, /min-height:\s*48px;/, 'Card title must have min-height: 48px');

  // 4. Spec badge container uniform height
  assert.match(css, /\.spec-badge-wrap|spec-badges-container/, 'Must define .spec-badge-wrap class');
  assert.match(css, /min-height:\s*52px;/, 'Spec badge container must have min-height: 52px');

  // 5. Button margin-top auto for bottom alignment
  assert.match(css, /margin-top:\s*auto\s*!important;/, 'Buttons in car-wrap must align to bottom via margin-top: auto');

  // 6. Process step cards in brakelines.html
  assert.match(css, /\.process-step-card\s*\{[^}]*display:\s*flex;/s, 'process-step-card must have display: flex');
  assert.match(css, /\.process-step-card\s*\{[^}]*height:\s*100%;/s, 'process-step-card must have height: 100%');
  assert.match(css, /\.step-header|\.step-title/, 'process-step-card must style header/title');

  // 7. Responsive table styling
  assert.match(css, /\.table-responsive\s+table\s*\{[^}]*min-width:\s*680px;/s, 'table-responsive table must have min-width: 680px');
  assert.match(css, /padding:\s*12px\s+14px\s*!important;/, 'table cells must have padding: 12px 14px');
});

test('Product pages and partials implement standard layout contracts', () => {
  const pages = [
    'products/electrical-systems.html',
    'products/railway-equipment.html',
    'products/special-vehicles.html'
  ];

  for (const page of pages) {
    const fullPath = path.resolve(process.cwd(), page);
    assert.ok(fs.existsSync(fullPath), `Missing ${page}`);
    const html = fs.readFileSync(fullPath, 'utf-8');

    // Each page must wrap badges in spec-badge-wrap
    assert.ok(html.includes('spec-badge-wrap'), `${page} must contain spec-badge-wrap`);
    assert.ok(html.includes('spec-badge'), `${page} must use spec-badge classes`);

    // Buttons must have mt-auto or card-action
    assert.ok(html.includes('mt-auto') || html.includes('btn-block'), `${page} must have bottom-aligned buttons`);
  }

  // Check brakelines process cards
  const brakePath = path.resolve(process.cwd(), 'products/brake-pad-lines.html');
  assert.ok(fs.existsSync(brakePath), 'Missing products/brake-pad-lines.html');
  const brakeHtml = fs.readFileSync(brakePath, 'utf-8');
  assert.ok(brakeHtml.includes('process-step-card'), 'brake-pad-lines.html must contain process-step-card');
  assert.ok(brakeHtml.includes('step-badge'), 'brake-pad-lines.html must contain step-badge');
  assert.ok(brakeHtml.includes('step-title'), 'brake-pad-lines.html must contain step-title');
  assert.ok(brakeHtml.includes('table-responsive'), 'brake-pad-lines.html must have table-responsive');
});

test('Product pages hero header layout prevents text collision and overflow', async () => {
  const cssPath = path.resolve(process.cwd(), 'css/rootze.css');
  const css = fs.readFileSync(cssPath, 'utf-8');

  // Must override .hero-wrap.hero-wrap-2 with height: auto !important and slider-text auto
  assert.match(css, /\.hero-wrap\.hero-wrap-2\s*\{[^}]*height:\s*auto\s*!important;/s, 'hero-wrap-2 must have height: auto !important');
  assert.match(css, /\.hero-wrap\.hero-wrap-2\s*\{[^}]*min-height:\s*360px\s*!important;/s, 'hero-wrap-2 must have min-height: 360px !important');
  assert.match(css, /\.hero-wrap\.hero-wrap-2\s+\.slider-text\s*\{[^}]*height:\s*auto\s*!important;/s, 'slider-text must have height: auto !important');

  const { spawn } = await import('node:child_process');
  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if (!fs.existsSync(chromePath)) return;

  const port = 9660 + Math.floor(Math.random() * 50);
  const chrome = spawn(chromePath, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--disable-gpu',
    '--window-size=1200,900'
  ]);

  try {
    for (let i = 0; i < 20; i++) {
      await new Promise(r => setTimeout(r, 200));
      try {
        const res = await fetch(`http://127.0.0.1:${port}/json/version`);
        if (res.ok) break;
      } catch {}
    }

    const pages = ['electrical-systems.html', 'railway-equipment.html', 'special-vehicles.html', 'brake-pad-lines.html'];
    for (const page of pages) {
      const targetUrl = `file://${path.resolve(process.cwd(), 'products', page)}`;
      const newTabRes = await fetch(`http://127.0.0.1:${port}/json/new?${targetUrl}`, { method: 'PUT' });
      const target = await newTabRes.json();
      const ws = new WebSocket(target.webSocketDebuggerUrl);
      await new Promise(r => ws.onopen = r);

      let id = 1;
      function send(method, params = {}) {
        return new Promise(resolve => {
          const curId = id++;
          const handler = (event) => {
            const data = JSON.parse(event.data);
            if (data.id === curId) {
              ws.removeEventListener('message', handler);
              resolve(data.result);
            }
          };
          ws.addEventListener('message', handler);
          ws.send(JSON.stringify({ id: curId, method, params }));
        });
      }

      await send('Page.enable');
      await send('Emulation.setDeviceMetricsOverride', { width: 1200, height: 900, deviceScaleFactor: 1, mobile: false });
      await new Promise(r => setTimeout(r, 200));

      // Switch to Chinese
      await send('Runtime.evaluate', {
        expression: `(() => {
          const zhBtn = document.querySelector('.lang-btn[data-lang="zh"]');
          if (zhBtn) zhBtn.click();
        })()`
      });
      await new Promise(r => setTimeout(r, 200));

      const evalRes = await send('Runtime.evaluate', {
        expression: `(() => {
          const hero = document.querySelector('.hero-wrap');
          const col = hero.querySelector('.col-md-10');
          const nextSection = document.querySelector('.hero-wrap + section');
          return {
            overflow: Math.round(col.getBoundingClientRect().bottom - hero.getBoundingClientRect().bottom),
            gapToNextSection: Math.round(nextSection.getBoundingClientRect().top - col.getBoundingClientRect().bottom)
          };
        })()`,
        returnByValue: true
      });

      const metrics = evalRes.result.value;
      assert.ok(metrics.overflow <= 0, `${page} hero content must not overflow hero-wrap (got overflow: ${metrics.overflow}px)`);
      assert.ok(metrics.gapToNextSection >= 40, `${page} gap to next section must be at least 40px (got: ${metrics.gapToNextSection}px)`);
    }
  } finally {
    chrome.kill();
  }
});

