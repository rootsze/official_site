import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

test('E2E GitHub Pages deployment readiness and full asset audit across index.html and news.html', () => {
  const root = process.cwd();

  // 1. .nojekyll present
  assert.ok(fs.existsSync(path.join(root, '.nojekyll')), '.nojekyll must exist in root');

  // 2. index.html and news.html at root
  assert.ok(fs.existsSync(path.join(root, 'index.html')), 'index.html must exist at root');
  assert.ok(fs.existsSync(path.join(root, 'news.html')), 'news.html must exist at root');

  // 3. Official brand logos exist
  assert.ok(fs.existsSync(path.join(root, 'images/logo-horizontal.png')), 'images/logo-horizontal.png must exist');
  assert.ok(fs.existsSync(path.join(root, 'images/logo-white.png')), 'images/logo-white.png must exist');

  // 4. .gitignore does not ignore css, js, images, index.html, news.html
  if (fs.existsSync(path.join(root, '.gitignore'))) {
    const gitignore = fs.readFileSync(path.join(root, '.gitignore'), 'utf8');
    assert.ok(!/^(?:index\.html|news\.html|css|js|images)$/m.test(gitignore), 'Core site assets must not be gitignored');
  }

  // 5. Verify no broken local files referenced anywhere in index.html or news.html
  const pages = ['index.html', 'news.html'];
  for (const page of pages) {
    const html = fs.readFileSync(path.join(root, page), 'utf8');
    const links = [...html.matchAll(/(?:src|href)="([^"#?]+)(?:[#?][^"]*)?"/g)].map(m => m[1]);
    for (const l of links) {
      if (l.startsWith('http') || l.startsWith('mailto:') || l.startsWith('https://wa.me')) continue;
      assert.ok(fs.existsSync(path.join(root, l)), `Resource missing in ${page}: ${l}`);
    }

    // Verify official company email and WhatsApp in each page
    assert.match(html, /sales@rootzeglobal\.com/, `${page} must contain sales@rootzeglobal.com`);
    assert.match(html, /8615168203740/, `${page} must contain WhatsApp phone 8615168203740`);
  }

  // 6. Verify bilingual completeness across all pages
  const i18nCode = fs.readFileSync(path.join(root, 'js/i18n.js'), 'utf8');
  const sandbox = { window: {}, localStorage: { getItem: () => null, setItem: () => {} }, document: {} };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(i18nCode, sandbox);
  const { en, zh } = sandbox.RootZeI18n.translations;

  for (const page of pages) {
    const html = fs.readFileSync(path.join(root, page), 'utf8');
    const keys = [...html.matchAll(/data-i18n="([^"]+)"/g)].map(m => m[1]);
    for (const k of keys) {
      assert.ok(en[k], `Missing EN translation for key "${k}" used in ${page}`);
      assert.ok(zh[k], `Missing ZH translation for key "${k}" used in ${page}`);
    }
  }
});
