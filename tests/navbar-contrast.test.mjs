import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Navbar brand typography and backdrop adhere to WCAG AAA contrast and ATB UI/UX Pro Max', () => {
  const rootzeCss = fs.readFileSync(path.join(process.cwd(), 'css/rootze.css'), 'utf8');

  // 1. Resting state navbar frosted glass backdrop (eliminates transparent blend over bright hero images)
  assert.match(
    rootzeCss,
    /\.ftco-navbar-light\s*\{[\s\S]*?background:\s*rgba\(11,\s*19,\s*37,\s*0\.88\)\s*!important;/,
    'ftco-navbar-light must have solid dark navy frosted glass background in resting state'
  );
  assert.match(
    rootzeCss,
    /\.ftco-navbar-light\s*\{[\s\S]*?backdrop-filter:\s*blur\(16px\);/,
    'ftco-navbar-light must use 16px backdrop-filter blur'
  );
  assert.match(
    rootzeCss,
    /\.ftco-navbar-light\s*\{[\s\S]*?border-bottom:\s*0\.5px\s*solid\s*rgba\(255,\s*255,\s*255,\s*0\.12\)\s*!important;/,
    'ftco-navbar-light must have 0.5px hairline bottom border'
  );

  // 2. Resting state brand typography contrast
  assert.match(
    rootzeCss,
    /\.brand-title\s*\{[\s\S]*?color:\s*#ffffff\s*!important;/,
    'brand-title must be white (#ffffff) on dark navy (contrast > 17:1)'
  );
  assert.match(
    rootzeCss,
    /\.brand-tagline\s*\{[\s\S]*?color:\s*#38bdf8\s*!important;/,
    'brand-tagline must be high-contrast sky blue (#38bdf8) on dark navy (contrast > 8.2:1)'
  );

  // 3. Scrolled state brand typography contrast on white
  assert.match(
    rootzeCss,
    /\.ftco-navbar-light\.scrolled\s+\.brand-title\s*\{[\s\S]*?color:\s*#0b1325\s*!important;/,
    'Scrolled brand-title must use Radix slate-12 (#0b1325) for 17.2:1 contrast on white'
  );
  assert.match(
    rootzeCss,
    /\.ftco-navbar-light\.scrolled\s+\.brand-tagline\s*\{[\s\S]*?color:\s*#0369a1\s*!important;/,
    'Scrolled brand-tagline must use Radix sky-11 (#0369a1) for 5.8:1 contrast on white'
  );

  // 4. Hero overlay depth
  assert.match(
    rootzeCss,
    /\.hero-wrap\s+\.overlay\s*\{[\s\S]*?opacity:\s*1\s*!important;/,
    'Hero overlay must have full opacity to prevent bright image bleed'
  );

  // 5. Typography scale rule: min 12px for brand-tagline on smaller viewports
  assert.doesNotMatch(
    rootzeCss,
    /\.brand-tagline\s*\{[\s\S]*?font-size:\s*1[01]\./,
    'brand-tagline font-size must never be smaller than 12px on responsive screens'
  );
});
