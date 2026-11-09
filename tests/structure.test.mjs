import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

test('index.html structure contains official brand, 4 product sectors, about, why rootze, news link, and valid i18n keys', () => {
  const htmlPath = path.join(process.cwd(), 'index.html');
  assert.ok(fs.existsSync(htmlPath), 'index.html must exist');
  const html = fs.readFileSync(htmlPath, 'utf8');

  // Verify navbar & brand
  assert.match(html, /id="ftco-navbar"/, 'Navbar must exist');
  assert.match(html, /src="\.\/images\/logo-horizontal\.png"/, 'Navbar brand must include official horizontal logo');
  assert.match(html, /data-i18n="brand\.legal_name"/, 'Navbar brand must include company legal name i18n tag');

  // Verify navigation links
  assert.match(html, /href="#home"[^>]*data-i18n="nav\.home"/, 'Nav must link to #home');
  assert.match(html, /data-i18n="nav\.products"/, 'Nav must link to products');
  assert.match(html, /href="#about"[^>]*data-i18n="nav\.about"/, 'Nav must link to #about');
  assert.match(html, /href="news\.html"[^>]*data-i18n="nav\.news"/, 'Nav must link to news.html');
  assert.match(html, /href="#contact"[^>]*data-i18n="nav\.contact"/, 'Nav must link to #contact');

  // Verify Advantages and Track Record are REMOVED from top navigation
  assert.doesNotMatch(html, /<li[^>]*class="nav-item"[^>]*>\s*<a[^>]*href="#advantages"/, 'Nav must NOT have #advantages link');
  assert.doesNotMatch(html, /<li[^>]*class="nav-item"[^>]*>\s*<a[^>]*href="#track"/, 'Nav must NOT have #track link');

  // Verify section anchors
  assert.match(html, /id="home"/, 'Home section must exist');
  assert.match(html, /id="about"/, 'About section must exist');
  assert.match(html, /id="products"/, 'Products section must exist');
  assert.match(html, /id="advantages"/, 'Why Rootze (advantages) section must exist in body');
  assert.match(html, /<h2 class="mb-3" data-i18n="why\.title">Why Rootze<\/h2>/, 'Why Rootze section must have simplified title');
  assert.doesNotMatch(html, /data-i18n="subheading\.why"/, 'Why Rootze section must not have duplicate subheading');
  assert.doesNotMatch(html, /data-i18n="why\.subtitle"/, 'Why Rootze section must not have subtitle description');
  assert.match(html, /id="workflow"/, 'How We Work section must exist');
  assert.match(html, /id="contact"/, 'Contact section must exist');
  assert.match(html, /id="specModal"/, 'Product spec modal must exist');

  // Verify track record section is hidden/commented out
  assert.ok(
    html.includes('<!-- Track record section hidden') || !html.includes('<section id="track" class="ftco-counter'),
    'Track record counter section must not be active on page'
  );

  // Verify 4 core product cards in #products
  assert.match(html, /data-inquire-cat="Special Purpose Vehicles \(SPV & Trucks\)"/, 'Card 1 (Special Purpose Vehicles) must exist with inquire link');
  assert.match(html, /data-inquire-cat="Railway Equipment & Maintenance Tools"/, 'Card 2 (Railway track equipment) must exist with inquire link');
  assert.match(html, /data-inquire-cat="Automotive Manufacturing Lines \(Brake Pads\)"/, 'Card 3 (Brake pad equipment) must exist with inquire link');
  assert.match(html, /data-inquire-cat="Industrial Electrical Systems \(Soft Starters\)"/, 'Card 4 (Electrical systems) must exist with inquire link');

  // Verify deep links to product catalog pages
  assert.ok(html.includes('./products/electrical-systems.html'), 'Card 1 must link to electrical catalog');
  assert.ok(html.includes('./products/railway-equipment.html'), 'Card 2 must link to railway catalog');
  assert.ok(html.includes('./products/special-vehicles.html'), 'Card 3 must link to vehicle catalog');
  assert.ok(html.includes('./products/brake-pad-lines.html'), 'Card 4 must link to brake lines catalog');

  // Verify authentic brochure images are used
  assert.ok(html.includes('images/products/electrical/'), 'Card 1 must use extracted electrical image');
  assert.ok(html.includes('images/products/railway/'), 'Card 2 must use extracted railway image');
  assert.ok(html.includes('images/products/vehicles/'), 'Card 3 must use vehicle image');
  assert.ok(html.includes('images/products/brakelines/'), 'Card 4 must use extracted brake lines image');

  // Verify contact info and channels
  assert.match(html, /sales@rootzeglobal\.com/, 'Official email must be sales@rootzeglobal.com');
  assert.match(html, /\+8615168203740/, 'Official phone/whatsapp must be +8615168203740');
  assert.match(html, /https:\/\/wa\.me\/8615168203740/, 'WhatsApp direct link must use 8615168203740');

  // Verify footer white logo and legal name
  assert.match(html, /src="\.\/images\/logo-white\.png"/, 'Footer must use white logo variant');

  // Verify relative links (no absolute /css or http:// localhost)
  const hrefsAndSrcs = [...html.matchAll(/(?:href|src)="([^"]+)"/g)].map(m => m[1]);
  for (const link of hrefsAndSrcs) {
    if (link.startsWith('http') || link.startsWith('#') || link.startsWith('mailto:') || link.startsWith('https://wa.me')) {
      continue;
    }
    assert.ok(!link.startsWith('/'), `Link must be relative, found: ${link}`);
    const resolved = path.join(process.cwd(), link);
    assert.ok(fs.existsSync(resolved), `Linked asset does not exist: ${link}`);
  }

  // Verify all data-i18n keys in index.html exist in i18n dictionary
  const i18nCode = fs.readFileSync(path.join(process.cwd(), 'js/i18n.js'), 'utf8');
  const sandbox = { window: {}, localStorage: { getItem: () => null, setItem: () => {} } };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(i18nCode, sandbox);
  const translations = sandbox.RootZeI18n.translations.en;

  const i18nKeys = [...html.matchAll(/data-i18n="([^"]+)"/g)].map(m => m[1]);
  assert.ok(i18nKeys.length > 25, 'index.html should have comprehensive data-i18n tags');
  for (const key of i18nKeys) {
    assert.ok(translations[key], `i18n key "${key}" found in index.html is missing in i18n.js`);
  }
});
