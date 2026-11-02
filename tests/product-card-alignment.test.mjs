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
