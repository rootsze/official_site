import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Language switch capsule and buttons prevent wrapping and shrinkage across all viewports', () => {
  const rootzeCss = fs.readFileSync(path.join(process.cwd(), 'css/rootze.css'), 'utf8');

  // 1. .lang-switch must have flex-shrink: 0
  assert.match(
    rootzeCss,
    /\.lang-switch\s*\{[\s\S]*?flex-shrink:\s*0;/,
    '.lang-switch must have flex-shrink: 0 to prevent collapsing in tight navbars'
  );

  // 2. .lang-btn must have white-space: nowrap
  assert.match(
    rootzeCss,
    /\.lang-btn\s*\{[\s\S]*?white-space:\s*nowrap(\s*!important)?;/i,
    '.lang-btn must enforce white-space: nowrap to prevent CJK characters from stacking vertically'
  );

  // 3. .lang-btn must have flex-shrink: 0
  assert.match(
    rootzeCss,
    /\.lang-btn\s*\{[\s\S]*?flex-shrink:\s*0;/,
    '.lang-btn must have flex-shrink: 0'
  );

  // 4. Laptop responsive rules (992px to 1199.98px)
  assert.match(
    rootzeCss,
    /@media\s*\(min-width:\s*992px\)\s*and\s*\(max-width:\s*1199\.98px\)/,
    'css/rootze.css must include tailored responsive adjustments for laptop screens (992px-1199.98px)'
  );
});
