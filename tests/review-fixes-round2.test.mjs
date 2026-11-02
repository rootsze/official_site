import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.cwd();

test('Review Fix 1: Sticky navbar contrast rules in css/rootze.css', () => {
  const rootzeCss = fs.readFileSync(path.join(root, 'css/rootze.css'), 'utf8');
  assert.match(
    rootzeCss,
    /\.ftco-navbar-light\.scrolled\s+\.navbar-brand/,
    'css/rootze.css must define dark contrast styling for navbar-brand when scrolled'
  );
});

test('Review Fix 2: Sticky navbar scroll listener and AOS in js/news.js', () => {
  const newsJs = fs.readFileSync(path.join(root, 'js/news.js'), 'utf8');
  assert.match(newsJs, /scrolled/, 'js/news.js must handle scrolled navbar state');
  assert.match(newsJs, /AOS\.init/, 'js/news.js must initialize AOS animations');
});

test('Review Fix 3: i18n fallback protection against raw key overwrite in js/i18n.js', () => {
  const i18nCode = fs.readFileSync(path.join(root, 'js/i18n.js'), 'utf8');
  assert.match(
    i18nCode,
    /val\s*&&\s*val\s*!==\s*key/,
    'setLanguage must check val && val !== key before overwriting innerHTML'
  );
});

test('Review Fix 4: OpenGraph and Twitter Card meta tags in index.html and news.html', () => {
  const indexHtml = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
  const newsHtml = fs.readFileSync(path.join(root, 'news.html'), 'utf8');

  for (const [page, html] of [['index.html', indexHtml], ['news.html', newsHtml]]) {
    assert.match(html, /<meta property="og:title"/, `${page} must contain og:title`);
    assert.match(html, /<meta property="og:description"/, `${page} must contain og:description`);
    assert.match(html, /<meta property="og:image"/, `${page} must contain og:image`);
    assert.match(html, /<meta name="twitter:card"/, `${page} must contain twitter:card`);
  }
});

test('Review Fix 5: Modernized Chinese inquiry subject line without legacy new-energy residue', () => {
  const mainJsCode = fs.readFileSync(path.join(root, 'js/main.js'), 'utf8');
  const sandbox = { module: { exports: {} }, window: {}, document: {}, jQuery: () => ({ on: () => {}, ready: () => {} }) };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(mainJsCode, sandbox);

  const { buildInquiryPayload } = sandbox.module.exports;
  const zhPayload = buildInquiryPayload('张总', '测试企业', 'zhang@test.com', '软起动柜', '5台', '加急', 'zh');
  assert.match(zhPayload.subject, /\[RootZe 工业装备与特种车辆出口询盘\]/, 'ZH inquiry subject must reflect industrial equipment rebrand');
});
