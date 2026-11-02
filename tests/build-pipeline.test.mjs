import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

test('Build script compiles all root and sub-directory product pages', () => {
  const output = execSync('python3 scripts/build.py', { encoding: 'utf-8' });
  assert.match(output, /electrical-systems\.html/);
  assert.match(output, /railway-equipment\.html/);
  assert.match(output, /brake-pad-lines\.html/);
  assert.match(output, /special-vehicles\.html/);

  const pages = [
    'products/electrical-systems.html',
    'products/railway-equipment.html',
    'products/brake-pad-lines.html',
    'products/special-vehicles.html'
  ];

  for (const page of pages) {
    const p = path.resolve(process.cwd(), page);
    assert.ok(fs.existsSync(p), `Page ${page} must exist`);
    const content = fs.readFileSync(p, 'utf-8');
    assert.ok(content.includes('../css/style.css'), `${page} must use relative parent css`);
    assert.ok(content.includes('../js/i18n.js'), `${page} must use relative parent js`);
  }
});
