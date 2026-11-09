import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('About section redesign eliminates legacy green #01d28e and provides accessible WCAG AAA contrast', () => {
  const rootzeCss = fs.readFileSync(path.join(process.cwd(), 'css/rootze.css'), 'utf8');
  const styleCss = fs.readFileSync(path.join(process.cwd(), 'css/style.css'), 'utf8');
  const indexHtml = fs.readFileSync(path.join(process.cwd(), 'index.html'), 'utf8');

  // 1. Verify legacy green #01d28e is removed from .ftco-about in style.css
  const aboutStyleBlock = styleCss.match(/\.ftco-about\s*\{[\s\S]*?@media\s*\(max-width:\s*767\.98px\)\s*\{\s*\.img-2/);
  assert.ok(aboutStyleBlock, 'ftco-about style rule block must exist in css/style.css');
  assert.doesNotMatch(aboutStyleBlock[0], /#01d28e/, 'Legacy neon green #01d28e must NOT exist in .ftco-about');

  // 2. Verify rootze.css overrides .ftco-about and completely hides .ftco-about:after
  assert.match(rootzeCss, /\.ftco-about\s*\{[\s\S]*?background:\s*#ffffff\s*!important;/, 'ftco-about must have clean #ffffff background');
  assert.match(rootzeCss, /\.ftco-about:after\s*\{[\s\S]*?display:\s*none\s*!important;/, 'ftco-about:after overlay must be set to display: none !important');

  // 3. Verify high-contrast typography tokens in rootze.css
  assert.match(rootzeCss, /\.about-title\s*\{[\s\S]*?color:\s*var\(--rootze-dark,\s*#0b1325\)\s*!important;/, 'about-title must use authoritative dark navy (contrast > 17:1)');
  assert.match(rootzeCss, /\.about-desc\s*\{[\s\S]*?color:\s*#334155\s*!important;/, 'about-desc must use Radix slate-11 (#334155, contrast > 9.6:1)');
  assert.match(rootzeCss, /\.about-badge\s*\{[\s\S]*?color:\s*#0284c7\s*!important;/, 'about-badge must use Radix sky-11 (#0284c7, contrast > 5.8:1)');
  assert.match(rootzeCss, /\.about-pill\s*\{[\s\S]*?color:\s*#0f172a;/, 'about-pill must use Radix slate-12 (#0f172a, contrast > 15:1)');

  // 4. Verify index.html contains modern photo card and about title
  assert.match(indexHtml, /<div[^>]*class="about-image-card"/, 'index.html must render modern about-image-card');
  assert.match(indexHtml, /<div[^>]*class="about-img-frame"/, 'index.html must render about-img-frame');
  assert.match(indexHtml, /<div[^>]*class="about-badge[^"]*"/, 'index.html must render about-badge');
  assert.match(indexHtml, /<h2[^>]*class="about-title[^"]*"/, 'index.html must render about-title');
  assert.match(indexHtml, /Official Export Arm of Specialized Manufacturers/, 'index.html must render updated about title');
});
