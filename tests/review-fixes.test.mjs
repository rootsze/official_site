import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.cwd();

test('Finding 1 & 2: Element visibility guaranteed and no duplicate ID on track section', () => {
  const rootzeCss = fs.readFileSync(path.join(root, 'css/rootze.css'), 'utf8');
  assert.match(rootzeCss, /\.ftco-animate\s*\{[^}]*opacity:\s*1/s, '.ftco-animate must have opacity: 1 override in rootze.css to prevent invisible content');
  assert.match(rootzeCss, /#track\.ftco-counter\s*\{[^}]*background-color:\s*var\(--rootze-dark\)/s, '#track must have dark background override');
  assert.match(rootzeCss, /\.nav-link\s*\{[^}]*white-space:\s*nowrap/s, 'Navbar links must enforce white-space: nowrap to avoid vertical word wrapping');

  const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
  // Check no element has duplicate id attribute
  const doubleIdMatches = html.match(/id="[^"]+"\s+[^>]*id="[^"]+"/g);
  assert.equal(doubleIdMatches, null, 'HTML elements must not contain multiple id attributes');
  assert.ok(!html.includes('id="section-counter"'), 'id="section-counter" duplicate must be removed');
  assert.ok(!html.includes('id="track" class="ftco-counter ftco-section img bg-light"'), '#track must not have bg-light class');
  assert.match(html, /<nav[^>]*id="ftco-navbar"[^>]*>[\s\S]*?<div class="container-fluid/, 'Navbar should use container-fluid to give desktop items full horizontal space');
});

test('Finding 3 & 4: Inquiry success modal exists and placeholders/subheadings are translated', () => {
  const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
  assert.match(html, /id="inquirySuccessModal"/, '#inquirySuccessModal must exist in index.html');
  assert.match(html, /id="modalMailtoLink"/, 'Modal mailto action button must exist');
  assert.match(html, /id="modalWhatsappLink"/, 'Modal WhatsApp action button must exist');

  // Verify subheadings have data-i18n
  assert.match(html, /<span class="subheading"[^>]*data-i18n="[^"]+"/, 'Section subheadings must have data-i18n attributes');

  // Verify form placeholders have data-i18n-placeholder
  const placeholders = [...html.matchAll(/data-i18n-placeholder="([^"]+)"/g)].map(m => m[1]);
  assert.ok(placeholders.length >= 5, 'Form fields must have data-i18n-placeholder attributes');

  // Verify i18n updates document.documentElement.lang
  const i18nCode = fs.readFileSync(path.join(root, 'js/i18n.js'), 'utf8');
  assert.match(i18nCode, /documentElement\.setAttribute\(['"]lang['"]/, 'i18n engine must update documentElement lang attribute');
});

test('Finding 5 & 6: Localized email payload and spec modal smooth integration', () => {
  const mainJsCode = fs.readFileSync(path.join(root, 'js/main.js'), 'utf8');
  assert.match(mainJsCode, /buildInquiryPayload/, 'main.js must define buildInquiryPayload for localized inquiry drafts');

  const sandbox = { module: { exports: {} }, window: {}, document: {}, jQuery: () => ({ on: () => {}, ready: () => {} }) };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(mainJsCode, sandbox);

  const { buildInquiryPayload, productSpecs } = sandbox.module.exports;
  assert.ok(buildInquiryPayload, 'buildInquiryPayload must be exported');
  assert.ok(productSpecs, 'productSpecs must be exported');

  // Test EN payload
  const enPayload = buildInquiryPayload('Alice', 'TestCo', 'alice@test.com', 'LFP Cells', '1000', 'Fast delivery', 'en');
  assert.match(enPayload.subject, /RootZe (?:Distribution|Industrial Equipment) Inquiry/, 'EN subject formatted');
  assert.match(enPayload.body, /Dear RootZe Distribution Team/, 'EN body formatted');
  assert.match(enPayload.waUrl, /https:\/\/wa\.me\//, 'waUrl formatted');

  // Test ZH payload
  const zhPayload = buildInquiryPayload('张总', '测试企业', 'zhang@test.com', '动力电芯', '1000', '加急交付', 'zh');
  assert.match(zhPayload.subject, /RootZe 工业装备与特种车辆出口询盘/, 'ZH subject formatted');
  assert.match(zhPayload.body, /尊敬的 RootZe 业务团队/, 'ZH body formatted in Chinese');
});
