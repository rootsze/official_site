import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('CSS rules in css/rootze.css enforce equal height & flex structure for contact section', () => {
  const cssPath = path.resolve(process.cwd(), 'css/rootze.css');
  assert.ok(fs.existsSync(cssPath), 'Missing css/rootze.css');
  const css = fs.readFileSync(cssPath, 'utf-8');

  // Must define .contact-form-card with flex column & height: 100%
  assert.match(css, /\.contact-form-card\s*\{[^}]*display:\s*flex;/s, 'contact-form-card must have display: flex');
  assert.match(css, /\.contact-form-card\s*\{[^}]*flex-direction:\s*column;/s, 'contact-form-card must have flex-direction: column');
  assert.match(css, /\.contact-form-card\s*\{[^}]*height:\s*100%;/s, 'contact-form-card must have height: 100%');

  // Must define .contact-info-card with flex column & height: 100%
  assert.match(css, /\.contact-info-card\s*\{[^}]*display:\s*flex;/s, 'contact-info-card must have display: flex');
  assert.match(css, /\.contact-info-card\s*\{[^}]*flex-direction:\s*column;/s, 'contact-info-card must have flex-direction: column');
  assert.match(css, /\.contact-info-card\s*\{[^}]*height:\s*100%;/s, 'contact-info-card must have height: 100%');
});

test('Contact section in partial and index.html implements strict equal-height layout contracts', () => {
  const files = [
    path.resolve(process.cwd(), 'src/partials/08-contact.html'),
    path.resolve(process.cwd(), 'index.html')
  ];

  for (const filePath of files) {
    assert.ok(fs.existsSync(filePath), `Missing ${filePath}`);
    const html = fs.readFileSync(filePath, 'utf-8');

    // 1. Row has align-items-stretch
    assert.match(html, /class="[^"]*row\s+block-9[^"]*align-items-stretch[^"]*"/, `${filePath} row must include align-items-stretch`);

    // 2. col-md-8 has d-flex and mb-4 mb-md-0 (no mb-md-5)
    assert.match(html, /class="[^"]*col-md-8\s+d-flex\s+mb-4\s+mb-md-0[^"]*"/, `${filePath} left column must have d-flex mb-4 mb-md-0`);
    assert.doesNotMatch(html, /class="[^"]*col-md-8[^"]*mb-md-5[^"]*"/, `${filePath} left column must not have mb-md-5`);

    // 3. Form has contact-form-card & submit wrapper has mt-auto
    assert.match(html, /<form[^>]*class="[^"]*contact-form-card[^"]*"/, `${filePath} form must include contact-form-card`);
    assert.match(html, /<div[^>]*class="[^"]*form-group[^"]*mt-auto[^"]*"[^>]*>\s*<button[^>]*type="submit"/s, `${filePath} submit button wrapper must have mt-auto`);

    // 4. Right column has d-flex and contact-info-card
    assert.match(html, /class="[^"]*col-md-4\s+d-flex\s+mb-4\s+mb-md-0[^"]*"/, `${filePath} right column must have d-flex mb-4 mb-md-0`);
    assert.match(html, /class="[^"]*contact-info-card[^"]*"/, `${filePath} right column inner container must include contact-info-card`);
  }
});
