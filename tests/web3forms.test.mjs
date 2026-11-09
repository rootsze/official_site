import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const EXPECTED_ACCESS_KEY = '2229a751-f7e9-4769-a151-b9fbb3ef5749';

test('Web3Forms form fields and script integration on index.html', () => {
  const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');

  // Verify form has Web3Forms active access_key, honeypot, and named inputs
  assert.match(html, /name="access_key"/, 'Form must contain access_key input');
  assert.match(html, new RegExp(`value="${EXPECTED_ACCESS_KEY}"`), `index.html must contain active access_key ${EXPECTED_ACCESS_KEY}`);
  assert.match(html, /name="botcheck"/, 'Form must contain botcheck spam prevention');
  assert.match(html, /name="name"/, 'Form must contain named input "name"');
  assert.match(html, /name="company"/, 'Form must contain named input "company"');
  assert.match(html, /name="contact"/, 'Form must contain named input "contact"');
  assert.match(html, /name="category"/, 'Form must contain named input "category"');
  assert.match(html, /name="message"/, 'Form must contain named input "message"');
});

test('Web3Forms active access_key and form contract across all 4 product pages', () => {
  const productPages = [
    'products/electrical-systems.html',
    'products/railway-equipment.html',
    'products/special-vehicles.html',
    'products/brake-pad-lines.html'
  ];

  for (const pagePath of productPages) {
    const fullPath = path.join(root, pagePath);
    assert.ok(fs.existsSync(fullPath), `${pagePath} must exist`);
    const html = fs.readFileSync(fullPath, 'utf8');

    assert.match(html, /id="inquiryForm"/, `${pagePath} must have form id="inquiryForm"`);
    assert.match(html, /name="access_key"/, `${pagePath} must have name="access_key"`);
    assert.match(html, new RegExp(`value="${EXPECTED_ACCESS_KEY}"`), `${pagePath} must contain active access_key ${EXPECTED_ACCESS_KEY}`);
    assert.match(html, /name="botcheck"/, `${pagePath} must contain botcheck spam prevention`);
    assert.match(html, /name="name"/, `${pagePath} must contain named input "name"`);
    assert.match(html, /name="company"/, `${pagePath} must contain named input "company"`);
    assert.match(html, /name="contact"/, `${pagePath} must contain named input "contact"`);
    assert.match(html, /name="category"/, `${pagePath} must contain named input "category"`);
    assert.match(html, /name="quantity"/, `${pagePath} must contain named input "quantity"`);
    assert.match(html, /name="message"/, `${pagePath} must contain named input "message"`);
  }
});

test('Web3Forms JavaScript submission engine in main.js', () => {
  const mainJs = fs.readFileSync(path.join(root, 'js/main.js'), 'utf8');

  // Verify main.js integrates web3forms submit endpoint and FormData
  assert.match(mainJs, /api\.web3forms\.com\/submit/, 'main.js must submit to api.web3forms.com/submit');
  assert.match(mainJs, /new\s+FormData\(/, 'main.js must use FormData for multipart submit');

  // Verify i18n keys for sending state and direct delivery success
  const i18nJs = fs.readFileSync(path.join(root, 'js/i18n.js'), 'utf8');
  assert.match(i18nJs, /contact\.btn_sending/, 'i18n must contain contact.btn_sending');
  assert.match(i18nJs, /contact\.sent_direct_title/, 'i18n must contain contact.sent_direct_title');
  assert.match(i18nJs, /contact\.sent_direct_desc/, 'i18n must contain contact.sent_direct_desc');
});
