import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

function loadI18n() {
  const code = fs.readFileSync(path.join(process.cwd(), 'js/i18n.js'), 'utf8');
  let storedLang = 'en';
  const mockStorage = {
    getItem: (k) => (k === 'rootze_lang' ? storedLang : null),
    setItem: (k, v) => {
      if (k === 'rootze_lang') storedLang = v;
    }
  };

  const sandbox = {
    window: {},
    localStorage: mockStorage,
    document: {
      documentElement: {
        lang: 'en',
        setAttribute: function(k, v) { this[k] = v; }
      },
      querySelectorAll: () => []
    }
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox);
  return { i18n: sandbox.RootZeI18n, mockStorage };
}

test('i18n engine has complete product catalog keys and symmetric translations', () => {
  const { i18n } = loadI18n();
  assert.ok(i18n, 'RootZeI18n must exist');
  
  const enKeys = Object.keys(i18n.translations.en).sort();
  const zhKeys = Object.keys(i18n.translations.zh).sort();
  assert.deepEqual(enKeys, zhKeys, 'EN and ZH translation keys must be completely symmetric');

  // Verify critical catalog namespaces
  const sampleKeys = [
    // Electrical
    'catalog.elec.badge_hv_ss', 'catalog.elec.badge_hv_vfd', 'catalog.elec.badge_cap_comp', 'catalog.elec.badge_switchgear',
    'catalog.elec.p1_title', 'catalog.elec.p1_desc', 'catalog.elec.p2_title', 'catalog.elec.p2_desc',
    'catalog.elec.p3_title', 'catalog.elec.p3_desc', 'catalog.elec.p4_title', 'catalog.elec.p4_desc',
    'catalog.elec.tbl_r1_features', 'catalog.elec.tbl_r1_apps',
    // Railway
    'catalog.rail.badge_testing', 'catalog.rail.badge_maintenance', 'catalog.rail.badge_cutting', 'catalog.rail.badge_adjuster',
    'catalog.rail.p1_title', 'catalog.rail.p1_desc', 'catalog.rail.p2_title', 'catalog.rail.p2_desc',
    'catalog.rail.p3_title', 'catalog.rail.p3_desc', 'catalog.rail.p4_title', 'catalog.rail.p4_desc',
    'catalog.rail.tbl_r1_specs', 'catalog.rail.tbl_r1_standards',
    // Brake lines
    'catalog.brake.step1_title', 'catalog.brake.step1_desc',
    'catalog.brake.step2_title', 'catalog.brake.step2_desc',
    'catalog.brake.step3_title', 'catalog.brake.step3_desc',
    'catalog.brake.step4_title', 'catalog.brake.step4_desc',
    'catalog.brake.step5_title', 'catalog.brake.step5_desc',
    'catalog.brake.video_title', 'catalog.brake.video_desc',
    'catalog.brake.video_f1', 'catalog.brake.video_f2', 'catalog.brake.video_f3',
    'catalog.brake.video_fallback', 'catalog.brake.video_caption',
    'catalog.brake.tbl_r1_stage', 'catalog.brake.tbl_r1_features',
    // Special Vehicles
    'catalog.spv.badge_cold', 'catalog.spv.badge_tanker', 'catalog.spv.badge_sweeper', 'catalog.spv.badge_dump',
    'catalog.spv.p1_title', 'catalog.spv.p1_desc', 'catalog.spv.p2_title', 'catalog.spv.p2_desc',
    'catalog.spv.p3_title', 'catalog.spv.p3_desc', 'catalog.spv.p4_title', 'catalog.spv.p4_desc',
    'catalog.spv.tbl_r1_model', 'catalog.spv.tbl_r1_drive', 'catalog.spv.tbl_r1_superstructure'
  ];

  for (const k of sampleKeys) {
    assert.ok(i18n.translations.en[k], `Missing EN key: ${k}`);
    assert.ok(i18n.translations.zh[k], `Missing ZH key: ${k}`);
  }
});

test('compiled product pages contain valid data-i18n attributes with zero missing keys', () => {
  const { i18n } = loadI18n();
  const productHtmlFiles = [
    'electrical-systems.html',
    'railway-equipment.html',
    'brake-pad-lines.html',
    'special-vehicles.html'
  ];

  for (const file of productHtmlFiles) {
    const filePath = path.join(process.cwd(), 'products', file);
    assert.ok(fs.existsSync(filePath), `Compiled file must exist: ${filePath}`);
    const html = fs.readFileSync(filePath, 'utf8');

    // Extract all data-i18n="key" instances
    const matches = [...html.matchAll(/data-i18n=["']([^"']+)["']/g)].map(m => m[1]);
    assert.ok(matches.length > 20, `${file} must contain at least 20 data-i18n elements (found ${matches.length})`);

    // Ensure every single key exists in i18n dictionary
    for (const key of matches) {
      assert.ok(i18n.translations.en[key], `Unknown or unmapped data-i18n key in ${file}: "${key}"`);
      assert.ok(i18n.translations.zh[key], `Missing ZH translation for key: "${key}"`);
    }

    // Ensure breadcrumbs have data-i18n
    assert.match(html, /data-i18n=["']nav\.home["']/, `${file} must have localized Home breadcrumb`);
    assert.match(html, /data-i18n=["']nav\.products["']/, `${file} must have localized Products breadcrumb`);
  }
});

test('i18n language switching persists in localStorage and toggles html lang attribute', () => {
  const { i18n, mockStorage } = loadI18n();
  
  i18n.setLanguage('zh');
  assert.equal(i18n.getLanguage(), 'zh');
  assert.equal(mockStorage.getItem('rootze_lang'), 'zh');

  i18n.setLanguage('en');
  assert.equal(i18n.getLanguage(), 'en');
  assert.equal(mockStorage.getItem('rootze_lang'), 'en');
});
