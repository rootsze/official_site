import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

test('i18n engine has symmetric keys and exports RootZeI18n', () => {
  const code = fs.readFileSync(path.join(process.cwd(), 'js/i18n.js'), 'utf8');
  const sandbox = { window: {}, localStorage: { getItem: () => null, setItem: () => {} }, document: {} };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox);

  const i18n = sandbox.RootZeI18n;
  assert.ok(i18n, 'RootZeI18n must be attached to window');
  assert.ok(i18n.translations.en, 'translations.en must exist');
  assert.ok(i18n.translations.zh, 'translations.zh must exist');

  const enKeys = Object.keys(i18n.translations.en).sort();
  const zhKeys = Object.keys(i18n.translations.zh).sort();
  assert.deepEqual(enKeys, zhKeys, 'EN and ZH translation keys must be completely symmetric');

  // Verify critical corporate, industrial sector, and news keys
  const requiredKeys = [
    'brand.name', 'brand.legal_name', 'brand.tagline',
    'nav.home', 'nav.products', 'nav.about', 'nav.news', 'nav.contact',
    'hero.title', 'hero.subtitle', 'hero.cta_products', 'hero.cta_contact',
    'about.title', 'about.subtitle', 'about.body1', 'about.body2',
    'products.title', 'products.subtitle',
    'products.cat1_title', 'products.cat1_desc',
    'products.cat2_title', 'products.cat2_desc',
    'products.cat3_title', 'products.cat3_desc',
    'products.cat4_title', 'products.cat4_desc',
    'why.title', 'why.subtitle',
    'why.card1_title', 'why.card1_desc',
    'why.card2_title', 'why.card2_desc',
    'why.card3_title', 'why.card3_desc',
    'why.card4_title', 'why.card4_desc',
    'workflow.title', 'workflow.subtitle',
    'workflow.step1_title', 'workflow.step2_title', 'workflow.step3_title', 'workflow.step4_title',
    'news.hero_title', 'news.hero_subtitle', 'news.filter_all',
    'news.art1_title', 'news.art2_title', 'news.art3_title',
    // New catalog keys
    'products.elec_hero_title', 'products.elec_hero_subtitle',
    'products.rail_hero_title', 'products.rail_hero_subtitle',
    'products.brake_hero_title', 'products.brake_hero_subtitle',
    'products.spv_hero_title', 'products.spv_hero_subtitle',
    'products.btn_catalog', 'products.quick_specs', 'products.tech_specs_title'
  ];
  for (const k of requiredKeys) {
    assert.ok(i18n.translations.en[k], `Missing EN key: ${k}`);
    assert.ok(i18n.translations.zh[k], `Missing ZH key: ${k}`);
  }
});
