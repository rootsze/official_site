import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

test('E2E GitHub Pages deployment readiness and full asset audit across index.html, news.html, and products/*.html', () => {
  const root = process.cwd();

  // 1. .nojekyll present
  assert.ok(fs.existsSync(path.join(root, '.nojekyll')), '.nojekyll must exist in root');

  // 2. Core pages at root and products/
  const pages = [
    'index.html',
    'news.html',
    'products/electrical-systems.html',
    'products/railway-equipment.html',
    'products/brake-pad-lines.html',
    'products/special-vehicles.html'
  ];
  for (const page of pages) {
    assert.ok(fs.existsSync(path.join(root, page)), `${page} must exist`);
  }

  // 3. Official brand logos exist
  assert.ok(fs.existsSync(path.join(root, 'images/logo-horizontal.png')), 'images/logo-horizontal.png must exist');
  assert.ok(fs.existsSync(path.join(root, 'images/logo-white.png')), 'images/logo-white.png must exist');

  // 4. .gitignore does not ignore css, js, images, index.html, news.html, products
  if (fs.existsSync(path.join(root, '.gitignore'))) {
    const gitignore = fs.readFileSync(path.join(root, '.gitignore'), 'utf8');
    assert.ok(!/^(?:index\.html|news\.html|products|css|js|images)$/m.test(gitignore), 'Core site assets must not be gitignored');
  }

  // 5. Verify no broken local files referenced anywhere in all pages
  for (const page of pages) {
    const pageDir = path.dirname(path.join(root, page));
    const html = fs.readFileSync(path.join(root, page), 'utf8');
    const links = [...html.matchAll(/(?:src|href)="([^"#?]+)(?:[#?][^"]*)?"/g)].map(m => m[1]);
    for (const l of links) {
      if (l.startsWith('http') || l.startsWith('mailto:') || l.startsWith('https://wa.me')) continue;
      const targetPath = path.resolve(pageDir, l);
      assert.ok(fs.existsSync(targetPath), `Resource missing in ${page}: ${l} (resolved: ${targetPath})`);
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
