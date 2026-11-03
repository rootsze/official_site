import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const rootDir = process.cwd();

test('Product Spec Modal contracts in HTML and CSS eliminate horizontal scrolling', () => {
  const indexHtml = fs.readFileSync(path.join(rootDir, 'index.html'), 'utf-8');
  const css = fs.readFileSync(path.join(rootDir, 'css', 'rootze.css'), 'utf-8');

  // Modal must use spec-modal-table class
  assert.match(indexHtml, /class="[^"]*spec-modal-table[^"]*"/, 'specModal must have spec-modal-table class');

  // CSS must override min-width for specModal and enforce fluid width
  assert.match(css, /#specModal\s+\.table-responsive\s+table|\.spec-modal-table/, 'rootze.css must define rules for spec-modal-table');
  assert.match(css, /min-width:\s*0\s*!important/, 'spec-modal-table must override min-width to 0 !important');

  // Mobile rules for spec-modal-table
  assert.match(css, /@media[^{]*max-width:\s*767\.98px[^{]*\{[\s\S]*?\.spec-modal-table\s+tr\s*\{[\s\S]*?display:\s*block/, 'Mobile CSS must convert spec-modal-table tr to block');
});

test('Product catalog pages comparison tables implement mobile responsive cards and remove scroll hints', () => {
  const catalogPages = [
    'products/electrical-systems.html',
    'products/railway-equipment.html',
    'products/special-vehicles.html',
    'products/brake-pad-lines.html'
  ];

  const css = fs.readFileSync(path.join(rootDir, 'css', 'rootze.css'), 'utf-8');

  for (const page of catalogPages) {
    const html = fs.readFileSync(path.join(rootDir, page), 'utf-8');
    assert.match(html, /class="[^"]*catalog-specs-table[^"]*"/, `${page} must include catalog-specs-table class`);
    assert.match(html, /data-label=/, `${page} table cells must include data-label attributes for mobile card rendering`);
  }

  // CSS must define responsive transformation for .catalog-specs-table
  assert.match(css, /\.catalog-specs-table/, 'rootze.css must define .catalog-specs-table rules');
  assert.match(css, /content:\s*attr\(data-label\)/, 'Mobile CSS must use attr(data-label) for catalog spec cards');
  assert.match(css, /\.table-scroll-hint\s*\{[\s\S]*?display:\s*none\s*!important/, 'Scroll hint must be hidden via display: none !important');
});
