import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Homepage product section cards have Explore Product Range button and no Inquire Price link', () => {
  const targets = ['src/partials/04-products.html', 'index.html'];

  for (const file of targets) {
    const fullPath = path.resolve(process.cwd(), file);
    assert.ok(fs.existsSync(fullPath), `Missing ${file}`);
    const html = fs.readFileSync(fullPath, 'utf-8');

    // Extract products section
    const productsSectionMatch = html.match(/<section id="products"[\s\S]*?<\/section>/);
    assert.ok(productsSectionMatch, `${file} missing #products section`);
    const productsSection = productsSectionMatch[0];

    // Assert no Inquire Price in homepage products section
    assert.ok(!productsSection.includes('Inquire Price'), `${file} #products should not contain 'Inquire Price'`);
    assert.ok(!productsSection.includes('products.btn_inquire'), `${file} #products should not reference products.btn_inquire`);

    // Assert all 4 cards have Explore Product Range button
    const catalogBtnMatches = productsSection.match(/data-i18n="products\.btn_catalog">Explore Product Range<\/a>/g);
    assert.equal(catalogBtnMatches?.length, 4, `${file} should have exactly 4 Explore Product Range buttons`);
  }

  // Ensure subpages still retain Inquire / RFQ buttons
  const subpages = [
    'products/special-vehicles.html',
    'products/railway-equipment.html',
    'products/electrical-systems.html'
  ];
  for (const page of subpages) {
    const content = fs.readFileSync(path.resolve(process.cwd(), page), 'utf-8');
    assert.ok(
      content.includes('data-i18n="products.btn_inquire"') || content.includes('data-i18n="catalog.spv.btn_rfq"'),
      `${page} must retain inquiry action button (products.btn_inquire or catalog.spv.btn_rfq)`
    );
  }
});
